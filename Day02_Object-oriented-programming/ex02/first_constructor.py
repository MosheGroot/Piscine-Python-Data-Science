#!/usr/local/bin/python3

from dataclasses import replace
from email import header
import sys
import os

######################
#      CLASSES       #
######################

class Research:
    """Class with research utils above the provided file
    """
    # csv file format parametrs
    separator = ','
    header_fields_number = 2
    correct_values = [['0', '1'],
                      ['1', '0']]
    
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
        data = ''
        with open(self.filename, 'r', encoding='utf-8') as file:
            header = file.readline()
            if not self.__is_correct_csv_header(header):
                raise ValueError('Incorect format of header')
            
            data += header
            for csv_line in file:
                if not self.__is_correct_csv_line(csv_line):
                    raise ValueError('Incorect format of line')
                data += csv_line

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
