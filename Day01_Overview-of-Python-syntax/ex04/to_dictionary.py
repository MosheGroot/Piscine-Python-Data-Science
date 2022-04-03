#!/usr/local/bin/python3

######################
#   Subject's data   #
######################

def get_subjects_data() -> list:
    """Get prepared by subject list_of_tuples

    Returns:
        list[tuple[str, str]]: list of tuples
    """
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    return list_of_tuples



#####################
# PROCESS FUNCTIONS #
#####################

def convert_list_of_tuples(list_of_tuples: list) -> dict:
    """Convert list of tuples (in `(country, code)` format)
    to dict (in `code : list[country]` format)

    Args:
        list_of_tuples (list[tuple[str, str]]): list of tuples (in `(country, code)` format)

    Returns:
        dict[str, list[str]]: converter dict (in `code : list[country]` format)
    """
    list_of_tuples = get_subjects_data()

    converted_dict = {}
    for tuple_elem in list_of_tuples:
        if tuple_elem[1] not in converted_dict:
            converted_dict[tuple_elem[1]] = [tuple_elem[0]]
        else:
            converted_dict[tuple_elem[1]].append(tuple_elem[0])

    return converted_dict


def pretty_print(converted_dict: dict) -> None:
    """Print dictionary in `'code' : 'country'` format
    Args:
        converted_dict (dict[str, list[str]]): dict to print
    """
    for code, countries in converted_dict.items():
        for country in countries:
            print(f"'{code}' : '{country}'")



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    dict_data = convert_list_of_tuples(get_subjects_data())
    pretty_print(dict_data)

if __name__ == '__main__':
    main()
