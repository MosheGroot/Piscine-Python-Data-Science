from collections import Counter, defaultdict
from functools import reduce, lru_cache
from datetime import datetime
from typing_extensions import runtime

from bs4 import BeautifulSoup
import requests
import re

import pytest

#-------------------------------#
#         Movies class          #
#-------------------------------#

class Movies:
    """
    Analyzing data from movies.csv
    """
    __csv_headers = ('movieId','title','genres')
    __csv_types = (int, str, str)

    def __init__(self, path_to_the_file: str):
        self.filename = path_to_the_file

    @classmethod
    def __parse_line(cls, data_line: str):
        data_line = data_line.replace('\n', '')

        if data_line.find('"') != -1:
            splitted = re.split(r',\"|\",', data_line)
        else:
            splitted = data_line.split(',')

        return [cls.__csv_types[index](splitted[index])
                for index in range(len(cls.__csv_headers))]

    def get_next_data_line(self):
        """Read next data from file
        Yields:
            list with parsed values
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            line = file.readline()              # header line, ignore
            line = file.readline()              # first data line
            while line:
                yield self.__parse_line(line)
                line = file.readline()          # data line

    def __init__(self, path_to_the_file):
        self.filename = path_to_the_file
        self.__init_titles()
        
    def __init_titles(self):
        self.titles = {}
        for data in self.get_next_data_line():
            self.titles[data[0]] = data[1]

    def dist_by_release(self):
        """
        The method returns a dict or an OrderedDict where the keys are years and the values are counts.
        You need to extract years from the titles. Sort it by counts descendingly.
        """
        years_distribution = Counter()
        
        for data in self.get_next_data_line():
            year = re.search(r'\((\d{4})\)', data[1])
            if year:
                year = year.group(1)
            else:
                year = 'Null'
            years_distribution[year] += 1

        return dict(years_distribution.most_common())

    def dist_by_genres(self):
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """
        genres_distribution = Counter()

        for data in self.get_next_data_line():
            genres = data[2].split('|')
            for genre in genres:
                genre = genre.strip()
                if genre:
                    genres_distribution[genre] += 1

        return dict(genres_distribution.most_common())

    def most_genres(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        dict_movies = {}
        for data in self.get_next_data_line():
            dict_movies[data[1]] = len(data[2].split('|'))

        return dict(sorted(dict_movies.items(), key=lambda x: x[1], reverse=True)[:n])

    @lru_cache(maxsize=1024*1024*64) # 64 MB
    def get_movie_title(self, movie_id):
        """
        The method receives a list of IDs (as int) as input and returns a list of movie titles
        """
        return self.titles.get(movie_id)

#-------------------------------#
#          Links class          #
#-------------------------------#

class Links:
    """
    Analyzing data from links.csv
    """
    __csv_headers = ('movieId','imdbId','tmdbId')
    __csv_separator = ','
    __csv_types = (int, str, lambda x: int(x) if x else 0)

    __film_page_base_urls = {
        'movielens': 'https://movielens.org/movies/',
        'imdb': 'https://www.imdb.com/title/tt',
        'tmdb': 'https://www.themoviedb.org/movie/'
    }

    def __init__(self, path_to_the_file: str, movies_cls: Movies):
        self.filename = path_to_the_file
        if not isinstance(movies_cls, Movies):
            raise ValueError('invalid Movies class object')
        self.movies_cls = movies_cls

    @classmethod
    def __parse_line(cls, data_line: str):
        splitted = data_line.replace('\n', '').split(cls.__csv_separator)
        return [cls.__csv_types[index](splitted[index]) 
                for index in range(len(cls.__csv_headers))]

    def get_next_data_line(self):
        """Read next data from file
        Yields:
            list with parsed values
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            line = file.readline()              # header line, ignore
            line = file.readline()              # first data line
            while line:
                yield self.__parse_line(line)
                line = file.readline()          # data line

    @lru_cache(maxsize=1024*1024*128) # 128 MB
    def __get_imdb_all_fields(self, movie_imdb_id: str):
        # request page
        page = requests.get(self.__film_page_base_urls['imdb'] + movie_imdb_id)
        if page.status_code != 200:
            raise RuntimeError("imdb request failed")

        # get info block
        soup = BeautifulSoup(page.text, features='html.parser')
        soup = soup.find_all('div', attrs={'class': 'ipc-page-content-container'})[5]
        soup = soup.find_all('li', attrs={'role': 'presentation', 'class': 'ipc-metadata-list__item'})

        # parse all avaliable info
        result = {}
        for data_line in soup:
            # get label and value
            row_name = data_line.find(attrs={'class': 'ipc-metadata-list-item__label'})
            if row_name is None:
                continue
            row_name = row_name.text.strip()
            row_value = data_line.find(attrs={'class': 'ipc-metadata-list-item__content-container'})
            result[row_name] = row_value.text if row_value is not None else None

        return result
    
    def __get_imdb_movie_info(self, movie_links, list_of_fields):
        all_fields = self.__get_imdb_all_fields(str(movie_links[1]))
        result = [all_fields.get(field) for field in list_of_fields]
        return [str(movie_links[0]), *result]

    def get_imdb(self, list_of_movies, list_of_fields):
        """
        The method returns a list of lists [movieId, field1, field2, field3, ...] for the list of movies given as the argument (movieId).
        For example, [movieId, Director, Budget, Cumulative Worldwide Gross, Runtime].
        The values should be parsed from the IMDB webpages of the movies.
        Sort it by movieId descendingly.
        """
        imdb_info = [self.__get_imdb_movie_info(data, list_of_fields) 
                     for data in self.get_next_data_line()
                     if data[0] in list_of_movies]
        return list(sorted(imdb_info, key=lambda fields: fields[0]))

    def top_directors(self, n):
        """
        The method returns a dict with top-n directors where the keys are directors and 
        the values are numbers of movies created by them. Sort it by numbers descendingly.
        """
        directors_list = [self.__get_imdb_movie_info(data, ['Director'])
                          for data in self.get_next_data_line()]
        directors_list = map(lambda pair: pair[1], directors_list)
        directors_counter = Counter(directors_list)
        return dict(directors_counter.most_common(n))

    def most_expensive(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their budgets. Sort it by budgets descendingly.
        """
        budgets = [self.__get_imdb_movie_info(data, ['Budget'])
                   for data in self.get_next_data_line()]
        budgets = map(lambda item: (
                        self.movies_cls.get_movie_title(self.__csv_types[0](item[0])),
                        item[1] if item[1] is not None else ''
                    ), budgets)
        return dict(sorted(budgets, key=lambda item: item[1], reverse=True)[:n])

    def most_profitable(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the difference between worldwide gross and budget.
        Sort it by the difference descendingly.
        """
        profits = []
        for data in self.get_next_data_line():
            info = self.__get_imdb_movie_info(data, ['Gross worldwide', 'Budget'])
            
            if info[1] is None or info[2] is None:
                profits.append([self.movies_cls.get_movie_title(data[0]), float('NaN')])
                continue
            
            values = (float(re.sub(r'[^\d.]', '', info[1])), float(re.sub(r'[^\d.]', '', info[2])))
            profits.append([
                self.movies_cls.get_movie_title(data[0]),
                round(values[0] - values[1], 2)])

        return dict(sorted(profits, key=lambda item: item[1] if item[1] is not None else '', reverse=True)[:n])

    def longest(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are their runtime. If there are more than one version – choose any.
        Sort it by runtime descendingly.
        """
        runtimes = [self.__get_imdb_movie_info(data, ['Runtime'])
                    for data in self.get_next_data_line()]
        runtimes = map(lambda item: (
                        self.movies_cls.get_movie_title(self.__csv_types[0](item[0])),
                        item[1]
                    ), runtimes)
        
        def key_func(item):         # text to minutes
            if item[1] is None:
                return float('-inf')
            item = item[1].split()
            return int(item[0]) * 60 + int(item[2])
        
        return dict(sorted(runtimes, key=key_func, reverse=True)[:n])

    def top_cost_per_minute(self, n):
        """
        The method returns a dict with top-n movies where the keys are movie titles and
        the values are the budgets divided by their runtime. The budgets can be in different currencies – do not pay attention to it.
        The values should be rounded to 2 decimals. Sort it by the division descendingly.
        """
        costs = []
        for data in self.get_next_data_line():
            info = self.__get_imdb_movie_info(data, ['Budget', 'Runtime'])
            
            if info[1] is None or info[2] is None:
                costs.append([self.movies_cls.get_movie_title(data[0]), float('NaN')])
                continue
            
            budget_value = float(re.sub(r'[^\d.]', '', info[1]))
            runtime_value = info[2].split()
            runtime_value = int(runtime_value[0]) * 60 + int(runtime_value[2])
            costs.append([
                self.movies_cls.get_movie_title(data[0]),
                round(budget_value / runtime_value, 2)])

        return dict(sorted(costs, key=lambda item: item[1] if item[1] is not None else '', reverse=True)[:n])



#-------------------------------#
#       Statistics class        #
#-------------------------------#

class Statistics:
    """
    Statistics utils
    """
    @staticmethod
    def average(values: list):
        """Get average value of values list
        """
        return sum(values) / len(values)

    @staticmethod
    def median(values: list):
        """Get median value of values list
        """
        if len(values) == 0:
            raise ValueError('provided list is empty')

        if len(values) == 1:
            return float(values[0])

        values = sorted(values)
        mid = int(len(values) / 2)
        if len(values) % 2:
            return float(values[mid])
        return (values[mid - 1] + values[mid]) / 2.0

    @classmethod
    def variance(cls, values: list):
        """Calculate variance of values list
        """
        mean = cls.average(values)

        def reduce_func(prev, curr):
            diff = curr - mean
            return prev + diff * diff
        squares_sum = reduce(reduce_func, values)

        return squares_sum / len(values)



#-------------------------------#
#        Ratings class          #
#-------------------------------#

class Ratings:
    """
    Analyzing data from ratings.csv
    """

    __csv_headers = ('userId','movieId','rating','timestamp')
    __csv_separator = ','
    __csv_types = (int, int, float, int)

    def __init__(self, path_to_the_file: str):
        self.filename = path_to_the_file

    @classmethod
    def __parse_line(cls, data_line: str):
        splitted = data_line.split(cls.__csv_separator)
        return [cls.__csv_types[index](splitted[index]) 
                for index in range(len(cls.__csv_headers))]

    def get_next_data_line(self):
        """Read next data from file
        Yields:
            list with parsed values
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            line = file.readline()              # header line, ignore
            line = file.readline()              # first data line
            while line:
                yield self.__parse_line(line)
                line = file.readline()          # data line

    class Movies:
        """Analyzing movies data from ratings.csv
        """
        def __init__(self, ratings_cls, movies_cls: Movies):
            if not isinstance(ratings_cls, Ratings):
                raise ValueError('invalid Movies class object')
            if not isinstance(movies_cls, Movies):
                raise ValueError('invalid Movies class object')
            self.ratings = ratings_cls
            self.movies_cls = movies_cls

        def dist_by_year(self):
            """
            The method returns the years distribution by ratings count,
            sorted by years ascendingly.

            Returns:
                dict: a dict where the keys are years and the values are counts of ratings
            """
            years_distribution = Counter()

            for data in self.ratings.get_next_data_line():
                year = datetime.fromtimestamp(data[3]).year
                years_distribution[year] += 1

            return dict(sorted(years_distribution.items()))


        def dist_by_rating(self):
            """
            The method returns the ratings distribution by counts,
            sorted by ratings ascendingly.

            Returns:
                dict: a dict where the keys are ratings and the values are counts
            """
            ratings_distribution = Counter()

            for data in self.ratings.get_next_data_line():
                ratings_distribution[data[2]] += 1

            return dict(sorted(ratings_distribution.items()))

        def top_by_num_of_ratings(self, top_size: int):
            """
            The method returns top-n movies by the number of ratings,
            sorted by numbers descendingly.

            Returns:
                dict: a dict where the keys are movie titles and the values are numbers
            """
            top_movies = Counter()

            for data in self.ratings.get_next_data_line():
                top_movies[self.movies_cls.get_movie_title(data[1])] += 1

            return dict(top_movies.most_common(top_size))

        def top_by_ratings(self, n, metric=Statistics.average):
            """
            The method returns top-n movies by the `average` or `median` of the ratings,
            sorted by metric descendingly.

            Returns:
                dict: a dict where the keys are movie titles and the values are metric values
            """
            all_movies = defaultdict(list)

            for data in self.ratings.get_next_data_line():
                all_movies[self.movies_cls.get_movie_title(data[1])].append(data[2])

            for movie in all_movies:
                all_movies[movie] = round(metric(all_movies[movie]), 2)

            return dict(sorted(all_movies.items(), key=lambda item: item[1], reverse=True)[:n])

        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings,
            sorted by variance descendingly.

            Returns:
                dict: a dict where the keys are movie titles and the values are the variances
            """
            all_movies = defaultdict(list)

            for data in self.ratings.get_next_data_line():
                all_movies[self.movies_cls.get_movie_title(data[1])].append(data[2])

            for movie in all_movies:
                all_movies[movie] = round(Statistics.variance(all_movies[movie]), 2)

            return dict(sorted(all_movies.items(), key=lambda item: item[1], reverse=True)[:n])


    class Users(Movies):
        """Analyzing users data from ratings.csv
        """
        def dist_by_ratings_number(self):
            """
            The method returns the distribution of users by the number of ratings made by them,
            sorted by ratings ascendingly.

            Returns:
                dict: a dict where the keys are users and the values are number of ratings
            """
            ratings_distribution = Counter()

            for data in self.ratings.get_next_data_line():
                ratings_distribution[data[0]] += 1

            return dict(sorted(ratings_distribution.items(), key=lambda item: item[1]))

        def dist_by_ratings_values(self, metric=Statistics.average):
            """
            The method returns the distribution of users by `average` or `median` ratings made by them,
            sorted by ratings ascendingly.

            Returns:
                dict: a dict where the keys are users and the values are metric of ratings
            """
            all_ratings = defaultdict(list)

            for data in self.ratings.get_next_data_line():
                all_ratings[data[0]].append(data[2])

            for user in all_ratings:
                all_ratings[user] = round(metric(all_ratings[user]), 2)

            return dict(sorted(all_ratings.items(), key=lambda item: item[1]))

        def top_by_variance(self, n: int):
            """
            The method returns top-n users with the biggest variance of their ratings,
            sorted by variance descendingly.

            Returns:
                dict: a dict where the keys are users and the values are the variances
            """
            all_ratings = defaultdict(list)

            for data in self.ratings.get_next_data_line():
                all_ratings[data[1]].append(data[2])

            for user in all_ratings:
                all_ratings[user] = round(Statistics.variance(all_ratings[user]), 2)

            return dict(sorted(all_ratings.items(), key=lambda item: item[1], reverse=True)[:n])



#-------------------------------#
#          Tags class           #
#-------------------------------#

class Tags:
    """
    Analyzing data from tags.csv
    """
    __csv_headers = ('userId', 'movieId', 'tag', 'timestamp')
    __csv_separator = ','
    __csv_types = (int, int, str, int)

    def __init__(self, path_to_the_file: str):
        self.filename = path_to_the_file

    def __parse_line(self, data_line: str):
        splitted = data_line.split(self.__csv_separator)
        return [self.__csv_types[index](splitted[index])
                for index in range(len(self.__csv_headers))]

    def get_next_data_line(self):
        """Read next data from file
        Yields:
            list with parsed values
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            line = file.readline()  # header line, ignore
            line = file.readline()  # first data line
            while line:
                yield self.__parse_line(line)
                line = file.readline()  # data line

    def most_words(self, n):
        """
            The method returns top-n tags with most words inside,
            sorted by numbers descendingly.

            Returns:
                dict: a dict where the keys are tags
                and the values are the number of words inside the tag
        """
        all_tags = {}

        for data in self.get_next_data_line():
            if data[2] not in all_tags:
                all_tags[data[2]] = len(re.findall(r'\b', data[2]))

        return dict(sorted(all_tags.items(), key=lambda item: item[1], reverse=True)[:n])

    def longest(self, n):
        """
            The method returns top-n longest tags in terms of the number of characters,
            sorted by numbers descendingly.

            Returns:
                list: list of the longest tags
        """
        all_tags = {}

        for data in self.get_next_data_line():
            if data[2] not in all_tags:
                all_tags[data[2]] = len(data[2])
        all_tags = dict(sorted(all_tags.items(), key=lambda item: item[1], reverse=True)[:n])

        return list(all_tags.keys())[:n]

    def most_words_and_longest(self, n):
        """
        The method returns the intersection between top-n tags with most words inside and
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        big_tags = list(self.most_words(n).keys())
        long_tags = self.longest(n)
        for value in long_tags:
            if value not in big_tags:
                big_tags.append(value)

        return big_tags

    def most_popular(self, n):
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        all_tags = []

        for data in self.get_next_data_line():
            if data[2] not in all_tags:
                all_tags.append(data[2].lower())
        popular_tags = dict(Counter(all_tags).most_common(n))

        return popular_tags

    def tags_with(self, word):
        """
        The method returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sort it by tag names alphabetically.
        """
        tags_with_word = []

        for data in self.get_next_data_line():
            if word.lower() in data[2].lower():
                if data[2] not in tags_with_word:
                    tags_with_word.append(data[2])

        return sorted(tags_with_word)



#-------------------------------#
#          Tests class          #
#-------------------------------#

class Tests:
    """Tests class
    """
    class TestMovies:
        """Tests for Movies class
        """

        @classmethod
        def setup_class(cls):
            cls.mov = Movies('./ml-latest-small/movies.csv')

        def test__dist_by_release_sorted(self):
            result = self.mov.dist_by_release()
            releases = list(result.values())
            sorted = True
            for i in range(1, len(releases)):
                if releases[i - 1] < releases[i]:
                    sorted = False
                    break
            assert sorted

        def test__dist_by_release_type(self):
            result = self.mov.dist_by_release()
            assert isinstance(result, dict)

        def test__dist_by_genres_sorted(self):
            result = self.mov.dist_by_genres()
            genres = list(result.values())
            sorted = True
            for i in range(1, len(genres)):
                if genres[i - 1] < genres[i]:
                    sorted = False
                    break
            assert sorted

        def test__dist_by_genres_type(self):
            result = self.mov.dist_by_genres()
            assert isinstance(result, dict)

        def test__most_genres_sorted(self):
            result = self.mov.most_genres(10)
            genres = list(result.values())
            sorted = True
            for i in range(1, len(genres)):
                if genres[i - 1] < genres[i]:
                    sorted = False
                    break
            assert sorted

        def test__most_genres_type(self):
            result = self.mov.most_genres(10)
            assert isinstance(result, dict)

        def test_get_movie_title_type(self):
            result = self.mov.get_movie_title(8)
            assert isinstance(result, str)

        def test_get_movie_title_check_result(self):
            assert self.mov.get_movie_title(5) == 'Father of the Bride Part II (1995)'

        def test_get_movie_title_incorrect_id(self):
            assert self.mov.get_movie_title(98222222222222222222222222523) is None

    class TestLinks:
        @classmethod
        def setup_class(cls):
            INPUT_FILE = './ml-latest-small/links.csv'
            OUTPUT_FILE = './ml-latest-small/micro_links.csv'
            
            # create micro dataset
            with open(INPUT_FILE, 'r', encoding='utf-8') as input_file:
                with open(OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
                    for i in range(11):
                        output_file.write(input_file.readline())
   
            cls.mov = Movies('./ml-latest-small/movies.csv')
            cls.links = Links(OUTPUT_FILE, cls.mov)

        def test__get_imdb__types(self):
            result = self.links.get_imdb([1, 2], ['Director', 'Budget'])

            # return type
            assert isinstance(result, list)

            # inner types
            is_correct_types = True
            for movie_fields in result:
                if not isinstance(movie_fields, list):
                    is_correct_types = False
                    break
                for value in movie_fields:
                    if not isinstance(value, str):
                        is_correct_types = False
                        break
                if not is_correct_types:
                    break

            assert is_correct_types
            
        def test__top_directors__types(self):
            result = self.links.top_directors(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for director, count in result.items():
                if not isinstance(director, str) or not isinstance(count, int):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__top_directors__is_sorted(self):
            result = self.links.top_directors(10)

            # is sorted correctly (by descending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] < values[i]:
                    is_sorted = False
                    break
            assert is_sorted

        def test__most_expensive__types(self):
            result = self.links.most_expensive(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for director, count in result.items():
                if not isinstance(director, str) or not isinstance(count, str):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__most_expensive__is_sorted(self):
            result = self.links.most_expensive(10)

            # is sorted correctly (by descending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] < values[i]:
                    is_sorted = False
                    break
            assert is_sorted
            
        def test__most_profitable__types(self):
            result = self.links.most_profitable(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for director, count in result.items():
                if not isinstance(director, str) or not isinstance(count, float):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__most_profitable__is_sorted(self):
            result = self.links.most_profitable(10)

            # is sorted correctly (by descending order)
            keys = list(result.values())
            is_sorted = True
            for i in range(1, len(keys)):
                if keys[i - 1] < keys[i]:
                    is_sorted = False
                    break
            assert is_sorted

        def test__longest__types(self):
            result = self.links.longest(10)
            print(result)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for director, count in result.items():
                if not isinstance(director, str) or not isinstance(count, str):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__longest__is_sorted(self):
            result = self.links.longest(10)

            # is sorted correctly (by descending order)
            def key_func(item):         # text to minutes
                item = item.split()
                return int(item[0]) * 60 + int(item[2])
        
            keys = list(result.values())
            is_sorted = True
            for i in range(1, len(keys)):
                if key_func(keys[i - 1]) < key_func(keys[i]):
                    is_sorted = False
                    break
            assert is_sorted
            
        def test__top_cost_per_minute__types(self):
            result = self.links.top_cost_per_minute(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for director, count in result.items():
                if not isinstance(director, str) or not isinstance(count, float):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__top_cost_per_minute__is_sorted(self):
            result = self.links.top_cost_per_minute(10)
            
            # is sorted correctly (by descending order)
            keys = list(result.values())
            is_sorted = True
            for i in range(1, len(keys)):
                if keys[i - 1] < keys[i]:
                    is_sorted = False
                    break
            assert is_sorted
            
    class TestStatistics:
        def test__average__type(self):
            result = Statistics.average([1, 2, 500])
            assert isinstance(result, float)
        
        def test__average__values(self):
            result = Statistics.average([1, 2, 3])
            assert result == 2.0
        
        def test__median__type(self):
            result = Statistics.median([1, 2, 500])
            assert isinstance(result, float)
        
        def test__median__values(self):
            result = Statistics.median([1, 2, 3])
            assert result == 2.0

            result = Statistics.median([1, 2, 3, 4])
            assert result == 2.5
            
        def test__variance__type(self):
            result = Statistics.variance([1, 2, 3])
            assert isinstance(result, float)

        def test__variance__values(self):
            result = Statistics.variance([1, 2, 3])
            assert round(result, 5) == 0.66667

    class TestRatings:
        """Tests for Ratings class
        """
        @classmethod
        def setup_class(cls):
            cls.ratings = Ratings('ml-latest-small/ratings.csv')
            cls.mov = Movies('./ml-latest-small/movies.csv')
            cls.ratings_movies = Ratings.Movies(cls.ratings, cls.mov)
            cls.ratings_users = Ratings.Users(cls.ratings, cls.mov)

        def test__movies__dist_by_years__types(self):
            """Test are dist_by_years method result types correct
            """
            # call the method   
            result = self.ratings_movies.dist_by_year()

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for year, count in result.items():
                if not isinstance(year, int) or not isinstance(count, int):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__movies__dist_by_years__is_sorted(self):
            """Test is dist_by_years method result sorted
            """
            # call the method
            result = self.ratings_movies.dist_by_year()

            # is sorted correctly (by ascending order)
            keys = list(result.keys())
            is_sorted = True
            for i in range(1, len(keys)):
                if keys[i - 1] > keys[i]:
                    is_sorted = False
                    break
            assert is_sorted

        def test__movies__dist_by_rating__types(self):
            """Test are dist_by_rating method result types correct
            """
            # call the method
            result = self.ratings_movies.dist_by_rating()

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, float) or not isinstance(count, int):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__movies__dist_by_rating__is_sorted(self):
            """Test is dist_by_rating method result sorted
            """
            # call the method
            result = self.ratings_movies.dist_by_rating()

            # is sorted correctly (by ascending order)
            keys = list(result.keys())
            is_sorted = True
            for i in range(1, len(keys)):
                if keys[i - 1] > keys[i]:
                    is_sorted = False
                    break
            assert is_sorted

        def test__movies__top_by_num_of_ratings__types(self):
            """Test are top_by_num_of_ratings method result types correct
            """
            # call the method
            result = self.ratings_movies.top_by_num_of_ratings(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, str) or not isinstance(count, int):
                    is_correct_types = False
                    break
            assert is_correct_types
            
            # check len
            assert len(result) == 10

        def test__movies__top_by_num_of_ratings__is_sorted(self):
            """Test is top_by_num_of_ratings method result sorted
            """
            # call the method
            result = self.ratings_movies.top_by_num_of_ratings(10)

            # is sorted correctly (by ascending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] < values[i]:
                    is_sorted = False
                    break
            assert is_sorted
            
            # check len
            assert len(result) == 10

        def test__movies__top_by_ratings__types(self):
            """Test are top_by_ratings method result types correct
            """
            # call the method
            result = self.ratings_movies.top_by_ratings(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, str) or not isinstance(count, float):
                    is_correct_types = False
                    break
            assert is_correct_types
            
            # check len
            assert len(result) == 10

        def test__movies__top_by_ratings__is_sorted(self):
            """Test is top_by_ratings method result sorted
            """
            # call the method
            result = self.ratings_movies.top_by_ratings(10)

            # is sorted correctly (by ascending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] < values[i]:
                    is_sorted = False
                    break
            assert is_sorted
            
            # check len
            assert len(result) == 10
            
        def test__movies__top_controversial__types(self):
            """Test are top_controversial method result types correct
            """
            # call the method
            result = self.ratings_movies.top_controversial(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, str) or not isinstance(count, float):
                    is_correct_types = False
                    break
            assert is_correct_types
            
            # check len
            assert len(result) == 10

        def test__movies__top_controversial__is_sorted(self):
            """Test is top_controversial method result sorted
            """
            # call the method
            result = self.ratings_movies.top_controversial(10)

            # is sorted correctly (by ascending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] < values[i]:
                    is_sorted = False
                    break
            assert is_sorted
            
            # check len
            assert len(result) == 10

            
        def test__users__dist_by_ratings_number__types(self):
            """Test are dist_by_ratings_number method result types correct
            """
            # call the method
            result = self.ratings_users.dist_by_ratings_number()

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, int) or not isinstance(count, int):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__users__dist_by_ratings_number__is_sorted(self):
            """Test is dist_by_ratings_number method result sorted
            """
            # call the method
            result = self.ratings_users.dist_by_ratings_number()

            # is sorted correctly (by ascending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] > values[i]:
                    is_sorted = False
                    break
            assert is_sorted

        def test__users__dist_by_ratings_values__types(self):
            """Test are dist_by_ratings_values method result types correct
            """
            # call the method
            result = self.ratings_users.dist_by_ratings_values()

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, int) or not isinstance(count, float):
                    is_correct_types = False
                    break
            assert is_correct_types

        def test__users__dist_by_ratings_values__is_sorted(self):
            """Test is dist_by_ratings_values method result sorted
            """
            # call the method
            result = self.ratings_users.dist_by_ratings_values()

            # is sorted correctly (by ascending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] > values[i]:
                    is_sorted = False
                    break
            assert is_sorted
        
        def test__users__top_by_variance__types(self):
            """Test are top_by_variance method result types correct
            """
            # call the method
            result = self.ratings_users.top_by_variance(10)

            # return type
            assert isinstance(result, dict)

            # inner types
            is_correct_types = True
            for rating, count in result.items():
                if not isinstance(rating, int) or not isinstance(count, float):
                    is_correct_types = False
                    break
            assert is_correct_types
            
            # check len
            assert len(result) == 10

        def test__users__top_by_variance__is_sorted(self):
            """Test is top_by_variance method result sorted
            """
            # call the method
            result = self.ratings_users.top_by_variance(10)

            # is sorted correctly (by ascending order)
            values = list(result.values())
            is_sorted = True
            for i in range(1, len(values)):
                if values[i - 1] < values[i]:
                    is_sorted = False
                    break
            assert is_sorted
            
            # check len
            assert len(result) == 10


    class TestTags:
        """Tests for Tags class
        """

        @classmethod
        def setup_class(cls):
            cls.tags = Tags('./ml-latest-small/tags.csv')

        def test__most_words__types(self):
            result = self.tags.most_words(10)
            assert isinstance(result, dict)

        def test__most_words__is_sorted(self):
            result = self.tags.most_words(10)

            sorted_list = True
            words = list(result.values())
            for i in range(1, len(words)):
                if words[i - 1] < words[i]:
                    sorted_list = False
                    break
            assert sorted_list
            
            # check len
            assert len(result) == 10

        def test__longest__types(self):
            result = self.tags.longest(10)
            assert isinstance(result, list)

        def test__longest__is_sorted(self):
            result = self.tags.longest(10)
            sorted_list = True
            for i in range(1, len(result)):
                if len(result[i - 1]) < len(result[i]):
                    sorted_list = False
                    break
            assert sorted_list
    
            # check len
            assert len(result) == 10

        def test_most_words_and_longest_types(self):
            result = self.tags.most_words_and_longest(10)
            assert isinstance(result, list)

        def test_most_words_and_longest_duplicates(self):
            my_list = self.tags.most_words_and_longest(10)
            test_set = set(my_list)
            assert len(my_list) == len(test_set)

        def test_most_popular_type(self):
            result = self.tags.most_popular(10)
            assert isinstance(result, dict)

        def test_most_popular_duplicates(self):
            my_list = list(self.tags.most_popular(10).keys())
            test_set = set(my_list)
            assert len(my_list) == len(test_set)

        def test_most_popular_sorted(self):
            result = self.tags.most_popular(10)
            
            tag = list(result.values())
            sorted_list = True
            for i in range(1, len(tag)):
                if tag[i - 1] < tag[i]:
                    sorted = False
                    break
            assert sorted_list
            
            # check len
            assert len(result) == 10

        def test_tags_with_out(self):
            word = 'comedy'
            result = self.tags.tags_with(word)
            check_word = True
            for i in range(len(result)):
                if word not in result[i].lower():
                    check_word = False
                    break
            assert check_word

        def test_tags_with_type(self):
            result = self.tags.tags_with('comedy')
            assert isinstance(result, list)

        def test_tags_with_dupl(self):
            my_list = list(self.tags.tags_with('comedy'))
            test_set = set(my_list)
            assert len(my_list) == len(test_set)

        def test_tags_with_sorted(self):
            result = self.tags.tags_with('comedy')
            sort_list = True
            for i in range(1, len(result)):
                if result[i - 1][0] > result[i][0]:
                    sort_list = False
            assert sort_list
