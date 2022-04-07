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

    @staticmethod
    def get_with_map() -> list:
        def appliable_function(_: str):
            if _.find(GmailTester.email_domain) != -1:
                return _
        return list(map(appliable_function, GmailTester.emails))



#-------------------------------#
#             Main              #
#-------------------------------#

def main():
    ## settings
    PRINT_RESULTS = True
    ITERATIONS_NUMBER = 900000
    
    ## measure
    time_results = {'loop': timeit.timeit(GmailTester.get_with_for_loop, number=ITERATIONS_NUMBER),
                    'list comprehension': timeit.timeit(GmailTester.get_with_list_comprehension, number=ITERATIONS_NUMBER),
                    'map': timeit.timeit(GmailTester.get_with_map, number=ITERATIONS_NUMBER)
                    }

    ## prints
    # get fastest
    fastest = min(time_results.items(), key=lambda t: t[1])
    print(f'it is better to use a {fastest[0]}')

    # print time results
    output = ''
    for val in sorted(time_results.values()):
        output += f'{val} vs '
    print(output[:-4])

    # print value results
    if PRINT_RESULTS:
        results =  {'loop': GmailTester.get_with_for_loop(),
                    'list comprehension': GmailTester.get_with_list_comprehension(),
                    'map': GmailTester.get_with_map()
                    }
        for res in results.items():
            print(f'\n{res[0]} : {res[1]}')


if __name__ == '__main__':
    main()
