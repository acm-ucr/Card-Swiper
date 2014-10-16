#!/usr/bin/env python

from colorama import Fore, Back, Style
from getpass import getpass as getswipe
import re

'''
Extracts r'card number from card swipe
string
@param carddump {String}
@return {String,None}
'''
def parse_number (carddump):
    # R'card number is always 16 numerical digits 
    # long and starts with %B. %B should be the first
    # characters in carddump
    regex = '%B([0-9]{16}).*'

    # There should be only one match
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        return matches[0]
    else:
        return None

'''
Print strings in different colors
@param string {String}
@return none
'''
def print_error (string):
    print '{}{}{}'.format(Fore.RED, Style.BRIGHT, string)
    print Style.RESET_ALL

def print_success (string):
    print '{}{}{}'.format(Fore.GREEN, Style.BRIGHT, string)
    print Style.RESET_ALL

def print_status (string):
    print '{}{}{}'.format(Fore.CYAN, Style.BRIGHT, string)
    print Style.RESET_ALL

if __name__ == '__main__':
    # Main event loop
    while 1:
        card_dump = getswipe("Swipe your R'card ID\n")
        card_number = parse_number(card_dump)
        
        # If we were NOT able to get a valid number
        # from the swipe, let the user know and skip everything
        # else
        if card_number == None:
           print_error ("Invalid swipe. Try again") 
           continue
