#!/usr/bin/env python3

import sys
import resource

#-------------------------------#
#       Generator Reader        #
#-------------------------------#

def read_lines(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as file:
        tmp_line = 'dummy'
        while tmp_line:
            tmp_line = file.readline()
            yield tmp_line


#-------------------------------#
#             Main              #
#-------------------------------#

def main(filename: str):
    for line in read_lines(filename):
        pass
    
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(f'Peak Memory Usage = {(usage.ru_maxrss / (1024**3)):.3f} GB')
    print(f'User Mode Time + System Mode Time = {(usage.ru_utime + usage.ru_stime):.2f}s')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
