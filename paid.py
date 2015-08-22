#!/usr/bin/env python

from getpass import getpass as getid
from colorama import Fore, Back, Style
import psycopg2
import os
import re
import time
import datetime
from db_config import *

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
Set student as a paid member
@param cardnum {String}
'''
def update_paid (cardnum):

    if conn.closed:
        print_error ('Connection with DB was lost. Please try again.')
        exit(1)

    if cardnum.startswith("%B"):
        cardnum = parse_number(cardnum)

    db.execute(
        """UPDATE students
           SET paid = 't'
           WHERE card_number = (%s);""", (cardnum,))

    conn.commit()

'''
Print strings in different colors
@param string {String}
@return none
'''
def print_error (string):
    print '{}{}{}{}'.format(Fore.RED, Style.BRIGHT, string, Style.RESET_ALL)

def print_success (string):
    print '{}{}{}{}'.format(Fore.GREEN, Style.BRIGHT, string, Style.RESET_ALL)

def print_status (string):
    print '{}{}{}{}'.format(Fore.CYAN, Style.BRIGHT, string, Style.RESET_ALL)

if __name__ == '__main__':

    # Establish a connection to our DB
    global conn, db
    try:
        conn = psycopg2.connect(database=DATABASE, \
                                user=USER, \
                                password=PASSWORD, \
                                host=HOST, \
                                port=PORT)
    except NameError:
       print("Your config file is not set properly. Or you need to contact Kyle for the info.")

    db = conn.cursor()
    # Clear the screen
    os.system('clear')

    print_success('Connected to DB.')
    time.sleep(1)
    os.system('clear')

    while 1:
        card_id = getid('Enter the card ID of the student to update\n')

        update_paid(card_id)

        print_success('Update successful')
        time.sleep(1)
        os.system('clear')

