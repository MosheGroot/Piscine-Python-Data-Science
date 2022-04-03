#!/usr/local/bin/python3

######################
#   Subject's data   #
######################

def get_subjects_data() -> list:
    """Get prepared by subject dictionary of counters and codes

    Returns:
        dict[str, str]: dictionary with `contry: code` pairs
    """
    country_codes_dict = {
        'Russia': '25',
        'France': '132',
        'Germany': '132',
        'Spain': '178',
        'Italy': '162',
        'Portugal': '17',
        'Finland': '3',
        'Hungary': '2',
        'The Netherlands': '28',
        'The USA': '610',
        'The United Kingdom': '95',
        'China': '83',
        'Iran': '76',
        'Turkey': '65',
        'Belgium': '34',
        'Canada': '28',
        'Switzerland': '26',
        'Brazil': '25',
        'Austria': '14',
        'Israel': '12'
    }

    return country_codes_dict



######################
#  PROCESS FUNCTION  #
######################

def sort_dictionary(dictionary: dict) -> dict:
    """Sort dictionary by value in descending order,
    and key if values are the same.
    Warning: value must be int-convertable!

    Args:
        dictionary (dict): dictionary to sort

    Returns:
        dict: sorted dictionary
    """

    return dict(sorted(dictionary.items(),
                        key=lambda item: (-int(item[1]), item[0])))


def pretty_print(dictionary: dict) -> None:
    """Pretty print dictionary: only keys print.
    Args:
        dictionary (dict): dictionary to print
    """

    for country in dictionary.keys():
        print(country)



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    sorted_dict = sort_dictionary(get_subjects_data())
    pretty_print(sorted_dict)


if __name__ == '__main__':
    main()
