"""Module with classes for research above the provided file
"""

import os
from random import randint

import logging
import json
import requests

import config

class Research:
    """Class with research utils above the provided file
    """
    # csv file format parametrs
    separator = ','
    header_fields_number = 2
    correct_values = [['0', '1'],
                      ['1', '0']]
    
    
    # logging
    logging.basicConfig(filename = 'analytics.log',
                    filemode = 'w',
                    format = '%(asctime)s %(message)s',
                    level = logging.DEBUG)
    logger = logging.getLogger()


    # methods
    def __init__(self, filename: str) -> None:
        # filename
        self.filename = filename

    def __is_correct_csv_header(self, csv_header: str) -> bool:
        header_fields = csv_header.replace('\n', '').split(self.separator)
        if len(header_fields) != self.header_fields_number: # correct number of fields
            return False

        return all(header_fields)   # all not empty
        
    def __is_correct_csv_line(self, csv_line: str) -> bool:
        csv_line = csv_line.replace('\n', '')
        if not csv_line:
            return False
        
        values = csv_line.split(self.separator)
        if len(values) != self.header_fields_number:    # incorect number of fields
            return False
        
        return values in self.correct_values            # only allowed values

    def __convert_to_list(self, csv_data: list, has_header: bool) -> list:
        result = []

        for index in range(int(has_header), len(csv_data)):
            values = csv_data[index].split(self.separator)
            result.append([int(val) for val in values])

        return result

    def file_reader(self, has_header=True) -> str:
        """Read the file with format checking

        Raises:
            OSError: Can't read the file
            SyntaxError: File is incorrect formated

        Returns:
            str: data of file
        """
        self.logger.debug('Reading input file')
        
        # check access
        if not os.access(self.filename, os.R_OK):
            raise OSError("Can't read the file")

        # read
        data = []
        with open(self.filename, 'r', encoding='utf-8') as file:
            # header
            if has_header:
                header = file.readline()
                if not self.__is_correct_csv_header(header):
                    raise ValueError('Incorect format of header')
                data.append(header)

            # other lines
            for csv_line in file:
                if not self.__is_correct_csv_line(csv_line):
                    raise ValueError('Incorect format of line')
                data.append(csv_line)

        return self.__convert_to_list(data, has_header)

    def sent_report_notification(self, success: bool) -> None:
        """Send log about report creation with a slack bot
        Args:
            success (bool): is report creation was success
        """
        self.logger.debug('Sending report notification')
        
        # create request
        message = json.loads('{"channel": "", "text": ""}')
        message['channel'] = config.SLACKBOT_CHANNEL_ID
        if success:
            message['text'] = 'The report has been successfully created'
        else:
            message['text'] = "The report hasn't been created due to an error"

        # send request
        requests.post('https://slack.com/api/chat.postMessage', data=message,
                      headers={'Authorization': f'Bearer {config.SLACKBOT_TOKEN}'})


    class Calculations:
        """Nested class for calculations
        """
        def __init__(self, data: list) -> None:
            self.data = data

        def counts(self) -> tuple:
            """Count heads and tails of list of [0, 1] or [1, 0] lists
            Args:
                data (list): list for count
            Returns:
                tuple[int, int]: number of heads and tails
            """
            Research.logger.debug('Counting the counts of heads and tails')
            heads = 0
            tails = 0

            for values in self.data:
                if values[0]:
                    tails += 1
                else:
                    heads += 1

            return (heads, tails)

        def fractions(self, heads_and_tails: tuple) -> tuple:
            """Calculate fractions in precents
            Args:
                heads_and_tails (tuple[int, int]): number of head and tails
            Returns:
                tuple[int, int]: heads and tails fractions in precents
            """
            Research.logger.debug('Counting fractions of heads and tails')
            total = sum(heads_and_tails)
            return tuple(value / total * 100 for value in heads_and_tails)


    class Analytics(Calculations):
        """Class for analytics utils
        """
        def predict_random(self, number_of_predictions: int) -> list:
            """Predict randomly next `number_of_predictions` tails or heads
            Args:
                number_of_predictions (int): nubmer of predictions
            Returns:
                list: list of predicted values
            """
            Research.logger.debug('Predicting randomly')
            result = []

            while number_of_predictions:
                rand = randint(0, 1)
                result.append([rand, int(not rand)])
                number_of_predictions -= 1

            return result

        def predict_last(self) -> list:
            """Get last value from original data
            Returns:
                list: last value
            """
            Research.logger.debug('Predicting last')
            return self.data[-1]

        def save_file(self, data: str, filename: str, extention: str) -> None:
            """Save data to file

            Args:
                data (str): data to write
                filename (str): name of file
                extention (str): extention of file
            """
            Research.logger.debug('Saving data to file')
            path = os.path.relpath(f'{filename}.{extention}')

            with open(path, 'w', encoding='utf-8') as file:
                file.write(data)
