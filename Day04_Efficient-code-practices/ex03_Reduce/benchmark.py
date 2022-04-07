#!/usr/bin/env python3

import timeit
import sys
from functools import reduce

#-------------------------------#
#           Tester              #
#-------------------------------#

class SquaresSumTester:
    @staticmethod
    def get_with_for_loop(last_number: int) -> int:
        sum = 0
        for num in range(1, last_number + 1):
            sum += num**2
        return sum

    @staticmethod
    def get_with_reduce(last_number: int) -> int:
        def sum2(prev: int, next: int):
            return prev + next**2
        return reduce(sum2, range(1, last_number + 1))   


#-------------------------------#
#             Main              #
#-------------------------------#

def main(test: str, iterations: str, number: str):
    # prepare
    PRINT_RESULTS = True
    results =  {
        'loop': SquaresSumTester.get_with_for_loop,
        'reduce': SquaresSumTester.get_with_reduce,
    }
    
    # error checks
    try:
        iterations = int(iterations)
        number = int(number)
    except:
        print("Can't parse number of iterations or number")
        return
    
    if test not in results.keys():
        print("Invalid test name")
        return
    
    # print time result
    print(timeit.timeit(lambda: results[test](number), number=iterations))
    
    # print value result
    if PRINT_RESULTS:
        print(f'\n{results[test](number)}')


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
