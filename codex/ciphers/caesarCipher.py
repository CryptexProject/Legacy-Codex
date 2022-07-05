#!/usr/bin/python

# caesar cipher package for the the codex project
# created by : C0SM0

# TODO: add colors
# TODO: cleanup code
# TODO: fix menu

# imports
import sys
import getopt

# banner for cli
banner = """
_________                                              _________ .__       .__                  
\\_   ___ \\_____    ____   ___________ _______          \\_   ___ \\|__|_____ |  |__   ___________ 
/    \\  \\/\\__  \\ _/ __ \\ /  ___/\\__  \\\\_  __ \\  ______ /    \\  \\/|  \\____ \\|  |  \\_/ __ \\_  __ \\
\\     \\____/ __ \\\\  ___/ \\___ \\  / __ \\|  | \\/ /_____/ \\     \\___|  |  |_> >   Y  \\  ___/|  | \\/
 \\______  (____  /\\___  >____  >(____  /__|             \\______  /__|   __/|___|  /\\___  >__|   
        \\/     \\/     \\/     \\/      \\/                        \\/   |__|        \\/     \\/       
"""

# help menu for displaying argument options
help_menu = """
        Caesar-Cipher Arguments:

        First Argument: Ciphering Process
        -e = encrypt
        -d = decrypt
        -b = bruteforce [bruteforces using all possible keys by default]

        Additional Arguments:
        -k <integer key> = key [not required for bruteforcing '-b']
        -r <start,end>   = choose a range of keys to start and end the bruteforce
        -t <plaintext>   = input text
        -i <input file>  = input file [.txt]
        -o <output file> = output file [output will be printed to screen by default]

        Example:
        main.py -c -e -k 5 -t hello 
        """

# symbols that can't be processed through the cipher
symbols = ['\n', '\t', ' ', '.', '?', '!', ',', '/', '\\', '<', '>', '|',
           '[', ']', '{', '}', '@', '#', '$', '%', '^', '&', '*', '(', ')',
           '-', '_', '=', '+', '`', '~', ':', ';', '"', "'", '0', '1', '2', '3',
           '4', '5', '6', '7', '8', '9']

# generate path
# path = f"{getpass.getuser()}@caesar-cipher $ "

# encrypts content
def encrypt_caesar(plain_content, encryption_key, print_cnt):
    # output variable
    output = ''
 
    # encryption process
    for character in plain_content:
        if character in symbols:
            output += character
        elif character.isupper():
            output += chr((ord(character) + int(encryption_key) - 65) % 26 + 65)
        else:
            output += chr((ord(character) + int(encryption_key) - 97) % 26 + 97)

    # output content to cli
    if print_cnt == True:
        print(f'Encrypted Content:\n{output}\n')

    # output content to file
    else:
        with open(print_cnt, 'w') as f:
            f.write(output)
        print('Output written to file sucessfully')


# decrypts content
def decrypt_caesar(plain_content, encryption_key, print_cnt):
    # output variable
    output = ''
 
    # decryption process
    for character in plain_content:
        if character in symbols:
            output += character
        elif character.isupper():
            output += chr((ord(character) - int(encryption_key) - 65) % 26 + 65)
        else:
            output += chr((ord(character) - int(encryption_key) - 97) % 26 + 97)

    # outputs content to cli
    if print_cnt == True:
        print(f'Decrypted Content:\n{output}\n')

    # outputs content to file
    else:
        with open(print_cnt, 'w') as f:
            f.write(output)
        print('Output written to file sucessfully')

# bruteforces content
def bruteforce_caesar(plain_content, print_cnt, start_range=0, end_range=27):
    # output variable
    output = ''

    shift_key = start_range
    for shift in range(start_range, end_range):
        output += f'Shift Key: {shift_key}\n'
        shift_key += 1

        for character in plain_content:
            if character in symbols:
                output += character
            elif character.isupper():
                output += chr((ord(character) - shift - 65) % 26 + 65)
            else:
                output += chr((ord(character) - shift - 97) % 26 + 97)

        output += '\n\n'

    # outputs content to cli
    if print_cnt == True:
        print(f'Bruteforced Content:\n{output}\n')

    # outputs content to file
    else:
        with open(print_cnt, 'w') as f:
            f.write(output)
        print('Output written to file sucessfully')

# parse all arguments
def caesar_parser():
    opts, args = getopt.getopt(sys.argv[2:], 'k:i:t:o:r:', ['key', 'inputFile', 'inputText', 'outputFile', 'range'])
    arg_dict = {}

    # loop through arguments, assign them to dict [arg_dict]
    for opt, arg in opts:
        # processing options
        if opt == '-k':
            arg_dict['-k'] = int(arg)
        if opt == '-r':
            arg_dict['-r'] = arg.split(',')
        # input options
        if opt == '-i':
            arg_dict['-i'] = arg
        if opt == '-t':
            arg_dict['-t'] = arg
        # output options
        if opt == '-o':
            arg_dict['-o'] = arg

    return arg_dict

# command line interface
def cli(argument_check):
    # display banner
    print(banner)

    # one liners
    if argument_check == True:

        # tries to get all arguments
        try:
            arguments = caesar_parser()

        # catches arguments with no value
        except getopt.GetoptError:
            print(f'[!!] No value was given to your argument\n{help_menu}')

        # continues with recieved arguments
        else:    
            # getting variables for ciphering process
            key = arguments.get('-k')
            inputted_content = arguments.get('-t')
            print_content = True
            
            # checks users output type
            if ('-i' in arguments):
                # tries to read file
                try:
                    inputted_content = open(arguments.get('-i'), 'r').read()

                # file does not exist
                except FileNotFoundError:
                    print('[!!] The attached file does not exist')

            # checks if output was specified
            if ('-o' in arguments):
                print_content = arguments.get('-o')

            # checks if range was specified
            if '-r' in arguments:   
                range = arguments.get('-r', False)

            # check ciphering process
            ciphering_process = sys.argv[1]

            # attempts to run cipher
            try:
                # encrypts caesar
                if ciphering_process == '-e':
                    encrypt_caesar(inputted_content, key, print_content)

                # decrypts caesar
                if ciphering_process == '-d':
                    decrypt_caesar(inputted_content, key, print_content)

                # bruteforce caesar
                if ciphering_process == '-b':
                    range = range if '-r' in arguments else False
                    if range == False:
                        bruteforce_caesar(inputted_content, print_content)
                    else:
                        bruteforce_caesar(inputted_content, print_content, int(range[0]), int(range[1])+1)

            # catches unspecified arguments
            except TypeError:
                print(f'[!!] No Key or Argument was specified\n{help_menu}')

    # help menu 
    else:
        print(help_menu)

# main code
def caesar_main():

    # checks for arguments
    try:
        sys.argv[1]
    except IndexError:
        arguments_exist = False
    else:
        arguments_exist = True

    cli(arguments_exist)

# runs main function if file is not being imported
if __name__ == '__main__':
    caesar_main()
