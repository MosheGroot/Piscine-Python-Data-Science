#!/usr/local/bin/python3

######################
#      CLASSES       #
######################

class Research:
    """Class with research utils above the provided file
    """
    def file_reader(self) -> str:
        """Read the `data.csv` file
        """
        with open('data.csv', 'r', encoding='utf-8') as file:
            return file.read()



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    researcher = Research()
    print(researcher.file_reader())


if __name__ == '__main__':
    main()
