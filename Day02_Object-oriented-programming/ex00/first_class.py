#!/usr/local/bin/python3

######################
#      CLASSES       #
######################

class Must_read:
    with open('data.csv', 'r', encoding='utf-8') as file:
        print(file.read())



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    pass

if __name__ == '__main__':
    main()