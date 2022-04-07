#!/usr/local/bin/python3

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
# LINES PROCESSINGS  #
######################

def get_csv_string_value(csv_line: str, begin_index: int, sep=',') -> str:
    """Extract next string csv value that begins at `begin_index` pos from `csv_line`.
    Escape quotes are supported.
    Warning: `csv_line[begin_index]` must be a quote, otherwise exception is rising.

    Args:
        csv_line (str): line to parse
        begin_index (int): begin index of value
        sep (str, optional): separator of csv filke

    Raises:
        ValueError: raises if value is not beginning with quote
        RuntimeError: raises if there is a syntax error

    Returns:
        str: extracted string value (with quotes included)
    """

    # check opening quote
    if csv_line[begin_index] != '"':
        raise ValueError("Can't get csv string value: the value is not a string")

    # get closing quote
    end_index = csv_line.find('"', begin_index + 1)
    while end_index != -1:
        if (end_index - begin_index > 1) and (csv_line[end_index - 1] == '\\'):     # escape quote
            end_index = csv_line.find('"', end_index + 1)                           # find next
        else:
            break

    if end_index == -1:
        raise RuntimeError("Syntax error: unclosed quote")

    end_index += 1

    # check separator
    if (end_index + 1 != len(csv_line)) and (csv_line[end_index] != sep):
        raise RuntimeError("Syntax error: separator after quote is missing")

    # return
    return csv_line[begin_index:end_index]


def get_csv_any_value(csv_line: str, begin_index: int, sep=',') -> str:
    """Extract any next csv value that begins at `begin_index` pos from `csv_line`.

    Args:
        csv_line (str): line to parse
        begin_index (int): begin index of value
        sep (str, optional): separator of csv filke

    Returns:
        str: extracted value as string
    """

    end_index = csv_line.find(sep, begin_index + 1)

    if end_index == -1:
        return csv_line[begin_index:]

    return csv_line[begin_index:end_index]


def split_csv_line(csv_line: str, sep=',') -> list:
    """Split line of `.csv` file to list[str] of fields
    Args:
        line (str): line to split
        sep (str, optional): separator of `.csv` file. Defaults to '","'.
    Returns:
        list: list[str] of fields
    """
    splitted_line = []

    # parse csv_line
    begin_index = 0
    while begin_index < len(csv_line):
        if csv_line[begin_index] == sep:
            begin_index += 1

        # get end index of current field
        if csv_line[begin_index] == '"':                    # field is "string"
            value = get_csv_string_value(csv_line, begin_index)
        else:                                             # field is bool/number/whatever
            value = get_csv_any_value(csv_line, begin_index)

        # get current field
        splitted_line.append(value)

        # go next
        begin_index += len(value)

    # return the result
    return splitted_line


def join_scv_fields(fields: list, sep=',') -> str:
    """Join all `fields` to one string with specified separator
    Args:
        fields (list): list[str] of fields to join
        sep (str, optional): output separator between fields. Defaults to ','.
    Returns:
        str: joined string
    """
    return sep.join(fields)



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    input_lines = read_file('ds.csv')
    output_lines = []

    for line in input_lines:
        output_lines.append(join_scv_fields(split_csv_line(line), '\t'))

    write_file("ds.tsv", output_lines)


if __name__ == '__main__':
    main()
