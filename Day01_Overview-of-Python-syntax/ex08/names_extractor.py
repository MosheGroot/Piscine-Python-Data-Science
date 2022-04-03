#!/usr/local/bin/python3

import sys

######################
#   I/O FUNCTIONS    #
######################

def read_file(filename: str) -> list:
    """Read all lines from `filename` file to list[str]
    Args:
        filename (str): path to file
    Returns:
        list: list of readed lines (strings)
    """
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return lines


def write_file(filename: str, lines: list) -> None:
    """Write all lines to `filename` file

    Args:
        filename (str): path to file
        lines (list): list[str] of lines to write
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.writelines(lines)



######################
#  PROCESS FUNCTION  #
######################

def email_extract_names(email: str) -> tuple:
    """Extract name and surname from email in
    `name.surname@corp.com` format.

    Args:
        email (str): email to parse

    Returns:
        tuple: `(name, surname)` pair
    """
    # indexes
    dot_index = email.find('.')
    at_sign_index = email.find('@')

    # name
    name = email[:dot_index]
    name = str.upper(name[0]) + name[1:]

    # surname
    surname = email[dot_index + 1:at_sign_index]
    surname = str.upper(surname[0]) + surname[1:]

    # return
    return (name, surname)


def extract_names_to_csv(emails: list) -> list:
    """Extract name and surname from each of emails
    and prepare tsv data with `"Name" "Surname" "E-mail"` header

    Args:
        emails (list[str]): list of emails

    Returns:
        list: list of tsv lines
    """
    # headers
    tsv_data = ['"Name"\t"Surname"\t"E-mail"\n']

    # parse
    for email in emails:
        email = email.replace('\n', '')
        extracted = email_extract_names(email)
        tsv_data.append(f'"{extracted[0]}"\t"{extracted[1]}"\t"{email}"\n')

    # return
    return tsv_data



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    if len(sys.argv) == 2:
        data = extract_names_to_csv(read_file(sys.argv[1]))
        write_file('employees.tsv', data)


if __name__ == '__main__':
    main()
