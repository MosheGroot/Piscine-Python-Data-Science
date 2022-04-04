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
    def __init__(self, filename: str) -> None:
        # filename
        self.filename = filename

        # csv file format
        self.separator = ','
        self.header_fields_number = 2
        self.correct_values = [('0', '1'),
                               ('1', '0')]

        self.logger = logging.getLogger()

    def __is_correct_format(self, csv_data: list, has_header: bool) -> bool:
        # empty or header-only
        if len(csv_data) <= 1:
            return True

        # check header
        if has_header:
            header_fields = csv_data[0].split(self.separator)
            if len(header_fields) != self.header_fields_number: # correct number of fields
                return False

            for value in header_fields:                         # all non-empty
                if len(value) == 0:
                    return False

        # check other lines
        for index in range(1, len(csv_data)):
            if len(csv_data[index]) <= 1:   # empty lines
                continue

            values = csv_data[index].split(self.separator)
            if len(values) != self.header_fields_number:    # incorect number of fields
                return False

            value_tuple = (*values[:-1], values[-1].replace('\n', ''))
            if value_tuple not in self.correct_values:      # not allowed values
                return False

        return True

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
        # log
        self.logger.debug('Reading the file')

        # check access
        if not os.access(self.filename, os.R_OK):
            self.logger.error("Can't read the file")
            raise OSError("Can't read the file")

        # read
        with open(self.filename, 'r', encoding='utf-8') as file:
            raw_data = file.read()

        # check syntax
        splitted_data = raw_data.split('\n')
        if not self.__is_correct_format(splitted_data, has_header):
            self.logger.error('Incorect format of file')
            raise SyntaxError('Incorect format of file')

        # convert to list of lists
        try:
            data = self.__convert_to_list(splitted_data, has_header)
            return data
        except ValueError:
            self.logger.error('File contains non-int data')
            raise ValueError('File contains non-int data')

    def sent_report_notification(self, success: bool) -> None:
        """Send log about report creation with a slack bot
        Args:
            success (bool): is report creation was success
        """
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
            self.logger = logging.getLogger()

        def counts(self) -> tuple:
            """Count heads and tails of list of [0, 1] or [1, 0] lists
            Args:
                data (list): list for count
            Returns:
                tuple[int, int]: number of heads and tails
            """
            self.logger.debug('Counting the counts of heads and tails')
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
            self.logger.debug('Counting fractions of heads and tails')
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
            return self.data[-1]

        def save_file(self, data: str, filename: str, extention: str) -> None:
            """Save data to file

            Args:
                data (str): data to write
                filename (str): name of file
                extention (str): extention of file
            """
            path = f'{filename}.{extention}'

            with open(path, 'w', encoding='utf-8') as file:
                file.write(data)
