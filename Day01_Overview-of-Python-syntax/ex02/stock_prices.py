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
# PROCESS FUNCTION  #
#####################

def process_stocks_request(company_name: str) -> None:
    """Find stocks for specified `company_name`
    Args:
        company_name (str): company name to find
    """
    companies, stocks = get_subjects_data()

    company_name = company_name.lower()
    for company, ticker_symbol in companies.items():
        if (company_name == company.lower()):
            print(stocks[ticker_symbol])
            return

    print('Unknown company')



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    if len(sys.argv) == 2:
        process_stocks_request(sys.argv[1])


if __name__ == '__main__':
    main()
