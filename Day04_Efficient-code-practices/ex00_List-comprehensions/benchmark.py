#!/usr/bin/env python3

import timeit

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



#-------------------------------#
#             Main              #
#-------------------------------#

def main():
    # settings
    PRINT_RESULTS = False
    ITERATIONS_NUMBER = 900000

    ## measure
    time__for_loop = timeit.timeit(GmailTester.get_with_for_loop,
                                   number=ITERATIONS_NUMBER)
    time__list_comprehension = timeit.timeit(GmailTester.get_with_list_comprehension,
                                             number=ITERATIONS_NUMBER)

    ## prints
    # get fastest
    if time__list_comprehension < time__for_loop:
        print('it is better to use a list comprehension')
    else:
        print('it is better to use a loop')

    # print time results
    print(f'{min(time__for_loop, time__list_comprehension)} vs ' + \
          f'{max(time__for_loop, time__list_comprehension)}')
    
    # print value result
    if PRINT_RESULTS:
        print("\nLoop :", GmailTester.get_with_for_loop())
        print("\nList comprehension :", GmailTester.get_with_list_comprehension())


if __name__ == '__main__':
    main()
