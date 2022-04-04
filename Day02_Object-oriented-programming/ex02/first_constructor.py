#!/usr/local/bin/python3

from dataclasses import replace
import sys
import os

######################
#      CLASSES       #
######################

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


    def __is_correct_format(self, csv_data: str) -> bool:
        # split
        splitted = csv_data.split('\n')

        if len(splitted) <= 1:      # empty or header-only
            return True

        # check header
        header_fields = splitted[0].split(self.separator)
        if len(header_fields) != self.header_fields_number: # correct number of fields
            return False

        for value in header_fields:                         # all non-empty
            if len(value) == 0:
                return False

        # check other lines
        for index in range(1, len(splitted)):
            if len(splitted[index]) <= 1:   # empty lines
                continue

            values = splitted[index].split(self.separator)
            if len(values) != self.header_fields_number:    # incorect number of fields
                return False

            value_tuple = (*values[:-1], values[-1].replace('\n', ''))
            if value_tuple not in self.correct_values:      # not allowed values
                return False

        return True


    def file_reader(self) -> str:
        """Read the file with format checking

        Raises:
            OSError: Can't read the file
            SyntaxError: File is incorrect formated

        Returns:
            str: data of file
        """

        # check access
        if not os.access(self.filename, os.R_OK):
            raise OSError("Can't read the file")

        # read
        with open(self.filename, 'r', encoding='utf-8') as file:
            data = file.read()

        # check syntax
        if not self.__is_correct_format(data):
            raise SyntaxError('Incorect format of file')

        # return
        return data



######################
#   MAIN FUNCTION    #
######################

def main(filename: str):
    """Main function"""
    research = Research(filename)
    try:
        print(research.file_reader())
    except Exception as err:
        print(type(err).__name__, err, sep=': ')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
