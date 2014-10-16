#!/usr/bin/env python

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

if __name__ == '__main__':
    # Main event loop
    while 1    
