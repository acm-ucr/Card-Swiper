#!/usr/bin/env python

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
Get a list of all students who checked into the meeting
'''
def get_checked_in ():
    # Bail if connection with the DB is lost
    if conn.closed:
        print_error ('Connection with DB was lost. Please try again')
        exit(1)

    # Get data from DB
    db.execute(
        """SELECT name,email FROM students
           WHERE checked_in = true""")

    return db.fetchall()

'''
Set all checked_in students to false
'''
def update_checked_in ():

    if conn.closed:
        print_error ('Connection with DB was lost. Please try again.')
        exit(1)

    db.execute(
        """UPDATE students
           SET checked_in = 'f'""")

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

    print_success('Connected to DB. Gathering data.')
    names = get_checked_in()

    date = datetime.date.today()

    print_status('Writing names.')

    f = open(str(date), 'w+')
    for name in names:
        f.write(name[0]+" "+name[1]+"\n")
    f.close()

    num_lines = sum(1 for line in open(str(date)))
    f = open(str(date), 'a+')
    f.write(str(num_lines)+"\n")
    f.close()

    print_success('Written to file')

    update_checked_in()

    print_success('Success.')
    time.sleep(1)

