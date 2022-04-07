#!/usr/local/bin/python3

import sys

######################
#   Subject's data   #
######################

def get_subjects_data() -> tuple:
    """Get prepared by subject data as two dictionaries:
    COMPANIES and STOCKS

    Returns:
        tuple[dict, dict]: COMPANIES and STOCKS dictionaries
    """
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }

    return COMPANIES, STOCKS



#####################
#  PARSE FUNCTIONS  #
#####################

def delete_whitespaces(string: str) -> str:
    """Delete all whitespaces from the string
    Args:
        string (str): input string
    Returns:
        str: cleared string
    """
    
    output_string = ''

    for sym in string:
        if not str.isspace(sym):
            output_string += sym
    
    return output_string


def parse_arguments(arg: str, sep=',') -> list:
    """Parse argumetns from `arg` string.
    Returns empty list if there is some empty value
    between separators
    Args:
        arg (str): string to parse
        sep (str, optional): separator between values. Defaults to ','.
    Returns:
        list[str]: list of values (may be empty)
    """

    # delete all whitespaces
    arg = delete_whitespaces(arg)

    # parse
    parsed_values = []
    begin_index = 0
    while begin_index < len(arg):
        # get end index of current value
        end_index = arg.find(sep, begin_index)
        if end_index + 1 >= len(arg):   # trailing comma
            return []

        if end_index == -1:             # end of line
            end_index = len(arg)

        # empty value -> return empty list
        if end_index - begin_index < 1:
            return []

        # push and go next
        parsed_values.append(arg[begin_index:end_index])
        begin_index = end_index + 1

    # return the result
    return parsed_values



#####################
# PROCESS FUNCTIONS #
#####################

def is_key(value: str, dictionary: dict) -> tuple:
    """Check if `value` is key of `dictionary` dict.
    Important: funciton is not case-sensitive!

    Args:
        value (str): value to search
        dictionary (dict): dictionary to search in

    Returns:
        tuple[bool, str]: pair
        of bool (`True` if `value` is a key, and `False` otherwise)
        and string (value of the key in dictionary)
    """

    lower_value = value.lower()

    for company_name in dictionary:
        if lower_value == company_name.lower():
            return (True, company_name)

    return (False, '')


def process_stocks_request(requests: list) -> None:
    """Process various requests from `requests` list:
    finding stock price for a company
    and find company name by ticker symbol.
    Prints an error if value in request is not valud.

    Args:
        requests (list): list of values to check
    """

    # get prepared data
    companies, stocks = get_subjects_data()

    # check empty (or wrong) request
    if len(requests) == 0:
        print()
        return

    # process all requests
    for value in requests:
        # is company
        result = is_key(value, companies)
        if result[0]:
            print(f'{ result[1] } stock price is { stocks[companies[result[1]]] }')
            continue

        # is ticker symbol
        result = is_key(value, stocks)
        if result[0]:
            print(f'{result[1]} is a ticker symbol' +
                  f'for { list(companies.keys())[list(companies.values()).index(result[1])] }')
            continue

        # neither company or ticker symbol
        print(f'{value} is an unknown company or an unknown ticker symbol')

    # end
    return



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    if len(sys.argv) == 2:
        requests = parse_arguments(sys.argv[1])
        process_stocks_request(requests)

if __name__ == '__main__':
    main()
