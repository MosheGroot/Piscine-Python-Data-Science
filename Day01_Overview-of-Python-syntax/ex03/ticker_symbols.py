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

def process_stocks_request(ticker_symbol: str) -> None:
    """Find company with specified `ticker_symbol`
    Args:
        ticker_symbol (str): ticker symbol of company
    """
    companies, stocks = get_subjects_data()

    ticker_symbol = ticker_symbol.upper()
    if ticker_symbol in stocks:
        company_name = list(companies.keys())[list(companies.values()).index(ticker_symbol)]
        print(company_name, stocks[ticker_symbol])
    else:
        print('Unknown ticker')



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    if len(sys.argv) == 2:
        process_stocks_request(sys.argv[1])

if __name__ == '__main__':
    main()
