#!/usr/bin/env python3

import timeit
from random import randint
from collections import Counter

#-------------------------------#
#           Tester              #
#-------------------------------#

class CounterRandomTester:
    min_value = 0
    max_value = 100
    
    def __init__(self, list_size: int) -> None:
        self.random_list = [randint(self.min_value, self.max_value) for _ in range(list_size)]
        self.cached_counts_loop = None
        self.cached_counts_counter = None

    def get_counts_with_loop(self) -> dict:
        counts = {}
        for value in self.random_list:
            if value in counts.keys():
                counts[value] += 1
            else:
                counts[value] = 1
                
        self.cached_counts_loop = counts
        return counts

    def get_top_10_with_loop(self) -> dict:
        if self.cached_counts_loop is None:
            self.get_counts_with_loop()
            
        return dict(sorted(self.cached_counts_loop.items(), 
                      key=lambda item: item[1], reverse=True)[:10])

    def get_counts_with_counter(self) -> dict:
        self.cached_counts_counter = Counter(self.random_list)
        return dict(self.cached_counts_counter)

    def get_top_10_with_counter(self) -> dict:
        if self.cached_counts_counter is None:
            self.get_counts_with_loop()
            
        return self.cached_counts_counter.most_common(10)


#-------------------------------#
#             Main              #
#-------------------------------#

def main():
    # prepare
    PRINT_RESULTS = False
    ITERATIONS_NUMBER = 10000
    RANDOM_LIST_SIZE = 1000

    tester = CounterRandomTester(RANDOM_LIST_SIZE)

    test_functions =  {
        'my function': tester.get_counts_with_loop,
        'Counter': tester.get_counts_with_counter,
        'my top': tester.get_top_10_with_loop,
        "Counter's top": tester.get_top_10_with_counter
    }

    # measure
    time_results = map(lambda func: (func[0], timeit.timeit(func[1], number=ITERATIONS_NUMBER)),
                            test_functions.items())
    
    for func_name, time in time_results:
        print(f'{func_name}: {time}')
        
        
    # values checks
    if PRINT_RESULTS:
        for name, function in test_functions.items():
            print(f'\n{name} : {function()}')

if __name__ == '__main__':
    main()
