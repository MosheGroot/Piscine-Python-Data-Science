#!/usr/bin/env python3

import timeit
import sys

#-------------------------------#
#           Tester              #
#-------------------------------#

class GmailTester:
    emails = ['john@gmail.com', 'james@gmail.com',
              'alice@yahoo.com', 'anna@live.com', 
              'philipp@gmail.com'] * 5
    
    email_domain = '@gmail.com'
    
    @staticmethod
    def get_with_for_loop() -> list:
        result = []
        for email in GmailTester.emails:
            if email.find(GmailTester.email_domain) != -1:
                result.append(email)
        return result

    @staticmethod
    def get_with_list_comprehension() -> list:
        return [email for email in GmailTester.emails if email.find(GmailTester.email_domain) != -1]

    @staticmethod
    def get_with_map() -> list:
        def appliable_function(_: str):
            if _.find(GmailTester.email_domain) != -1:
                return _
        return list(map(appliable_function, GmailTester.emails))

    @staticmethod
    def get_with_filter() -> list:
        def appliable_function(_: str):
            if _.find(GmailTester.email_domain) != -1:
                return _
        return list(filter(appliable_function, GmailTester.emails))



#-------------------------------#
#             Main              #
#-------------------------------#

def main(test: str, iterations: str):
    # prepare
    PRINT_RESULTS = True
    results =  {
        'loop': GmailTester.get_with_for_loop,
        'list_comprehension': GmailTester.get_with_list_comprehension,
        'map': GmailTester.get_with_map,
        'filter': GmailTester.get_with_filter
    }
    
    # error checks
    try:
        iterations = int(iterations)
    except:
        print("Can't parse number of iterations")
        return
    
    if test not in results.keys():
        print("Invalid test name")
        return
    
    # print
    print(timeit.timeit(results[test], number=iterations))
    
    # print value result
    if PRINT_RESULTS:
        print(f'\n{results[test]()}')


if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])