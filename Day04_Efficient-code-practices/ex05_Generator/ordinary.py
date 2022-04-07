#!/usr/bin/env python3

import sys
import resource

#-------------------------------#
#       Ordinary Reader         #
#-------------------------------#

def read_lines(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as file:
        return file.readlines()



#-------------------------------#
#             Main              #
#-------------------------------#

def main(filename: str):
    lines = read_lines(filename)
    
    for line in lines:
        pass

    usage = resource.getrusage(resource.RUSAGE_SELF)
    print(f'Peak Memory Usage = {(usage.ru_maxrss / (1024**3)):.3f} GB')
    print(f'User Mode Time + System Mode Time = {(usage.ru_utime + usage.ru_stime):.2f}s')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
