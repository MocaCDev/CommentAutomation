"""
Usage:
    cauto -[language] [code_file]

Supported Languages:
    Python, C, C++, QML, GoLang

Description:
    Comment Automation enables developers to stores unused code in a file and add 
    comments around that code that describes the "block" of code.
    The comments around each "block" of code consists of the following information:
        `IS_FOR` - This denotes where the code is supposed to be saved to upon this script being ran.
        `USAGE` - This will be the command that gets put above the code.
        `AT_COMMENT` - This tells the script where this code needs to go in the source code file. In the source code file, when removing a piece of code you might need later, simply add a comment with the `HERE` "keyword". The value can be an integer or string, or both.
        `TIMES` - This denotes the amount of times this code should occurr within a source code file. Make sure it matches.
        `END_IS_FOR` - This denotes the end of a "block".
    
    Example in Python:
        # IS_FOR: main.py 
        # USAGE: Prints hello
        # AT_COMMENT: 1
        # TIMES: 1

        def say_hello():
            print("Hello!")

        # END_IS_FOR

    Example of source-code file where the code came from:
        # HE6RE: 1
"""

import sys
from backend import CommentAutomation

# The file passed to this script must be the file where all unused code is stored.
# There needs to be a comment above each "block" of code explaining where the code should go
# if it needs to be re-instated into the script.

CA = CommentAutomation()

def main():
    global CA

    if len(sys.argv) < 2:
        print('Arguments needed:\n\t-[language] [code_file]\n\tThe [code_file] cannot be the source code where the code snippets are to be relocated to.')
        sys.exit(1)

    CA.good_to_set_file()

    try:
        with open(CA.unused_code_file, 'r') as file:
            data = file.read()
            file.close()

        CA.read_format(data)
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()
