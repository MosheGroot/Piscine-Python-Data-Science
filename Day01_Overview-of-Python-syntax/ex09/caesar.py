#!/usr/local/bin/python3

import sys

######################
#  PROCESS FUNCTIONS #
######################

def ascii_shift_char(char: str, shift: int) -> str:
    """Shift symbol with ascii code
    Args:
        char (str): char to shift
        shift (int): shift value
    Raises:
        ValueError: raises if symbol is not an ascii symbol
    Returns:
        str: shifted char
    """
    
    # constants
    ALPHABET_SIZE=26
    CLETTER_CODE_BEGIN = 65 # A
    CLETTER_CODE_END = 90   # Z
    SLETTER_CODE_BEGIN = 97 # a
    SLETTER_CODE_END = 122  # z
    ASCII_CODE_MIN=0
    ASCII_CODE_MAX=127

    # get code
    code = ord(char)
    if (code < ASCII_CODE_MIN) or (code > ASCII_CODE_MAX):
        raise ValueError('The script does not support your language yet')

    # shift
    if CLETTER_CODE_BEGIN <= code <= CLETTER_CODE_END:
        code += shift
        if code < CLETTER_CODE_BEGIN:
            code = CLETTER_CODE_END - (CLETTER_CODE_BEGIN - code - 1) % ALPHABET_SIZE
        elif code > CLETTER_CODE_END:
            code = CLETTER_CODE_BEGIN + (code - CLETTER_CODE_END - 1) % ALPHABET_SIZE
    elif SLETTER_CODE_BEGIN <= code <= SLETTER_CODE_END:
        code += shift 
        if code < SLETTER_CODE_BEGIN:
            code = SLETTER_CODE_END - (SLETTER_CODE_BEGIN - code - 1) % ALPHABET_SIZE
        elif code > SLETTER_CODE_END:
            code = SLETTER_CODE_BEGIN + (code - SLETTER_CODE_END - 1) % ALPHABET_SIZE

    # return char
    return chr(code)


def caesar_encode(data: str, caesar_shift: int) -> str:
    """Encode `data` using caesar cipher with `caesar_shift` shift
    Args:
        data (str): data to encode
        caesar_shift (int): shift
    Returns:
        str: encoded string
    """
    encoded_string = ''

    for char in data:
        encoded_string += ascii_shift_char(char, caesar_shift)

    return encoded_string


def caesar_decode(data: str, caesar_shift: int) -> str:
    """Decode the `data` that was encoded using caesar cipher
    with `caesar_shift` shift
    Args:
        data (str): data to decode
        caesar_shift (int): shift
    Returns:
        str: encoded string
    """
    dencoded_string = ''

    for char in data:
        dencoded_string += ascii_shift_char(char, -caesar_shift)

    return dencoded_string


def caesar_cipher(task: str, data: str, caesar_shift=3) -> str:
    """Caesar cipher with two tasks: `encode` and `decode`.
    Args:
        task (str): `"encode"`/`"decode"`
        data (str): data to process
        caesar_shift (int, optional): shift. Defaults to 3.
    Raises:
        ValueError: raises if task is unknown
    Returns:
        str: processed string
    """
    if task == 'encode':
        return caesar_encode(data, caesar_shift)
    if task == 'decode':
        return caesar_decode(data, caesar_shift)
    raise ValueError("Unknown task for Caesar cipher")



######################
#   MAIN FUNCTION    #
######################

def main():
    """Main function"""
    if len(sys.argv) == 4:
        print(caesar_cipher(sys.argv[1], sys.argv[2], int(sys.argv[3])))
    else:
        raise RuntimeError('''Invalid number of agruments:
        Please provide next parametrs:
        ./caesar.py  <encode/decode>  <string_to_process>  <shift>''')


if __name__ == '__main__':
    main()
