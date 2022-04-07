#!/usr/local/bin/python3

from multiprocessing.sharedctypes import Value
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

    class Calculations:
        """Nested class for calculations
        """
        def counts(self, data: list) -> tuple:
            """Count heads and tails of list of [0, 1] or [1, 0] lists
            Args:
                data (list): list for count
            Returns:
                tuple[int, int]: number of heads and tails
            """
            heads = 0
            tails = 0

            for values in data:
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
            total = sum(heads_and_tails)
            return tuple(value / total * 100 for value in heads_and_tails)



######################
#   MAIN FUNCTION    #
######################

def main(filename: str):
    """Main function"""
    research = Research(filename)

    try:
        data = research.file_reader()
    except Exception as err:
        print(type(err).__name__, err, sep=': ')
        return

    calculations = research.Calculations()
    counts = calculations.counts(data)
    fractions = calculations.fractions(counts)

    print(data, counts, fractions, sep='\n')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
