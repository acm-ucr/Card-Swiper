#!/usr/bin/env python

from colorama import Fore, Back, Style
from getpass import getpass as getswipe
import psycopg2
import os
import re

# Will be set in main
conn = None # Connection to db
db = None   # Actual interface to db

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
    
    # Sanity checks
    if not os.getenv('MEMBER_DB_NAME') or \
       not os.getenv('MEMBER_DB_USER') or \
       not os.getenv('MEMBER_DB_PASS') or \
       not os.getenv('MEMBER_DB_HOST') or \
       not os.getenv('MEMBER_DB_PORT'):
        print_error('Please set your MEMBER_DB environment variables. See github README for more info')
        exit(1)
    
    print_status ('Connecting to DB... Kill me if I take waaaay to long...')
    
    # Establish a connection to our DB
    global conn, db
    conn = psycopg2.connect(database=os.getenv('MEMBER_DB_NAME'), \
                            user=os.getenv('MEMBER_DB_USER'), \
                            password=os.getenv('MEMBER_DB_PASS'), \
                            host=os.getenv('MEMBER_DB_HOST'), \
                            port=os.getenv('MEMBER_DB_PORT'))

    db = conn.cursor()
        
    print_success ('Ready for action!')

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

