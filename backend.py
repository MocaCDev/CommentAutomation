import sys

class CommentAutomation:

    # `ucf` = Unused Code File.
    def __init__(self):
        # The user has to pass the language of the code so we can decipher
        # what to look for in regards to comments. Each language is different.
        self.comment_type = ''

        self.unused_code_file = ''

        match sys.argv[1]:
            case '-Python':
                self.comment_type = '#'
            case '-C' | '-C++' | '-QML' | '-GoLang':
                self.comment_type = '//'
            case _:
                print(f'{sys.argv[1]} is not a supported langauge, or has a typo.')
                sys.exit(1)

        # Keep track of the line we are at in the file where the unused code is stored.
        # The file passed to this script has to follow the format. It is nice to print 
        # the line if an error occurrs.
        self.line = 1

        # The file where the "block" of code is to be relocated to.
        self.is_for_file = ''

        # The usage of the "block" of code. Will be converted to a comment above the code.
        self.usage = ''

        # The "block" of code. It is an array just in case the piece of code will need 
        # to be inserted into the source code file more than one time.
        self.code = []

        # The index we are at in `self.code` when we are adding the code to the source 
        # code file. This will only increment if `self.times_to_repeat` is greater than 
        # 1. The developer can still have `# TIMES: 1`.
        self.code_index = 0

        # This is the value of `HERE` where the current "block" of code will be inserted.
        # In the source code file, any comment with `HERE`, as far as using this script,
        # is where a snippet of code will be inserted.
        self.at_comment = ''

        # This will be the "new structure" to the source code file with the snippets
        # of code replacing all `HERE` comments.
        self.new_code = []

        # This describes the number of times each "block" of code occurrs in the source
        # code file. Default value is 1.
        # TODO: I am pretty sure this variable is useless. There are a few instances where this can be used however.
        # TODO: Add features where the below variables will have more of a prominent standing in the automation.
        self.times_to_repeat = 1

        # This will be the actual "block" of code.
        self.current_code = ''

    def check_for_colon(self, data):
        if not ':' in data:
            print(f'Error on line {self.line} in {self.unused_code_file}: Missing colon.')
            sys.exit(1)

    def good_to_set_file(self): self.unused_code_file = sys.argv[2]

    # `file_data` will be the source code of the file with all of the code that is unused
    # but is saved just in case. It is in this file where the developer will need to 
    # specify the source code file where the code is to be relocated to as well as where 
    # in the source code the "block" of code is to be.
    def read_format(self, file_data):
        # First, split all the data by newlines.
        file_data = file_data.split('\n')

        # `l` = line
        for l in file_data:
            if self.comment_type in l:
                if 'END' in l:
                    if self.times_to_repeat > 1:
                        for i in range(0, self.times_to_repeat):
                            self.code.append(self.current_code)
                    else:
                        self.code.append(self.current_code)

                    if self.at_comment == '':
                        print('Error: the placement of a (or multiple) blocks of code was not specified.')
                        sys.exit(1)

                    with open(self.is_for_file, 'r') as file:
                        source_code = file.read()
                        file.close()

                    source_code = source_code.split('\n')

                    added = False

                    for l2 in source_code:
                        if not self.comment_type in l2 or not 'HERE' in l2:
                            self.new_code.append(l2)
                            continue

                        self.check_for_colon(l2)
                        l2 = l2.split(':')
                        
                        # The `.replace` methods below are in place to make sure 
                        # both values have no extra spaces.
                        # This can be a common error with errors where there is a 
                        # different number of spaces/tabs in the comment.
                        if l2[1].replace(' ', '') == self.at_comment.replace(' ', ''):
                            code = self.code[self.code_index].split('\n')

                            # Add the comment above the "block" of code being added.
                            # The "block" of code being added gets added 1 line at 
                            # a time.
                            self.new_code.append(f'{self.comment_type} {self.usage}')

                            for c in code:
                                if c == '\n' or c == '': continue
                                self.new_code.append(c) 

                            if self.times_to_repeat > 1:
                                self.code_index += 1

                            added = True

                            continue
                        else:
                            # We will assume `l2` will be a comment.
                            # We want to keep that comment as part of the source 
                            # code.
                            self.new_code.append(': '.join(l2))
                            continue

                    try:
                        if added:
                            with open(self.is_for_file, 'w') as file:
                                file.write('\n'.join(self.new_code))
                                file.flush()
                                file.close()
                    except:
                        print(self.new_code, end='!')
                        sys.exit(1)

                    # Reset all the variables so nothing carries over to the next
                    # "block" of code.
                    self.current_code = ''
                    self.code = []
                    self.new_code = []
                    self.code_index = 0
                    self.times_to_repeat = 1
                    self.usage = ''
                    self.is_for_file = ''

                    continue
                
                self.check_for_colon(l)
                l = l.split(':')

                # Just precautionary steps to make sure we are getting just the 
                # value we need to get.
                # It is important to note that formatters use underscores, not spaces.
                l[0] = l[0].replace('#', '')
                l[0] = l[0].replace(' ', '')

                match l[0]:
                    case 'IS_FOR': self.is_for_file = l[1].replace(' ', '')
                    case 'USAGE':
                        self.usage = l[1]

                        # Getting rid of any unwanted spaces in the beginning/end of the string.
                        self.usage = self.usage.split()
                        self.usage = ' '.join(self.usage)

                    case 'AT_COMMENT': self.at_comment = l[1]
                    case 'TIMES':
                        l[1] = l[1].replace(' ', '')

                        try:
                            self.times_to_repeat = int(l[1])
                        except Exception as e:
                            # This should (hopefully) never occurr, however it is better to play it safe and catch any sort of unwanted errors.
                            # Who knows, developers tend to make silly mistakes so.. better to account for the miscellaneous ones as well.
                            print(f'An error occurred whilst attempting to grab the integer value for `TIMES`.\n\tError: {str(e)}')
                            sys.exit(1)
                    case _:
                        print(f'Unknown formatter: {l}')
                        sys.exit(1)
                
            else:
                if l == '\n' or l == '': continue

                self.current_code += l 
                self.current_code += '\n'

            self.line += 1
