#!/usr/bin/env python

from colorama import Fore, Back, Style
from getpass import getpass as getswipe
import psycopg2
import os
import re
import time
from db_config import *

# Will be set in main
conn = None  # Connection to db
db = None    # Actual interface to db

'''
Extracts name from r'card swipe
string
@param carddump {String}
@return {String, None}
'''

def parse_name(carddump):
    # Last Name is after a ^ symbol
    # First name is after a /
    # Characters are in carddump
    name = ""

    regex = '\^(.*?)/'

    # There should only be one match
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        name += matches[0]
    else:
        return None

    regex = '/([^\s]+)'
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        name = matches[0] + " " + name
    else:
        return None

    return name.title()


'''
Parse id from r'card swipe
int
@param carddump {String}
@return {int, None}
'''

def parse_id(carddump):
    #ID follows a string of 6 zeros, and is 9 numbers long

    regex = '000000([0-9]{9}).*'

    # There should only be one match
    matches = re.findall(regex, carddump)
    if len(matches) == 1:
        return matches[0]
    else:
        return None


'''
Extracts r'card number from card swipe
string
@param carddump {String}
@return {String,None}
'''


def parse_number(carddump):
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
Fetches a student with the given r'card
number
@param cardnum {String}
@return {Dict, None}

{
    name : {String, None}
    email : {String, None}
    checked_in : {Boolean, None}
    points : {Int, None}
}
'''


def fetch_info(cardnum):
    # Bail if connection with DB is lost
    if conn.closed:
        print_error('Connection with DB was lost! Please restart application')
        exit(1)

    # Query the database, we should only have
    # one hit
    db.execute(
        """SELECT name, email, checked_in, points, card_number
           FROM students
           WHERE card_number = (%s);""", (cardnum,))

    # If we didn't get a hit, return None
    # otherwise, return student data
    hit = db.fetchone()
    if hit is None:
        return None
    else:
        # We don't need to return the card number
        return {'name': hit[0], 'email': hit[1], 'checked_in': hit[2], 'points': hit[3]}

'''
Create a new student in the DB
@param cardnumber {String}
'''


def insert_student(cardnum):
    # Bail if connection with DB is lost
    if conn.closed:
        print_error('Connection with DB was lost! Please restart application')
        exit(1)

    # Create new row for student using their cardnumber
    db.execute(
        """INSERT INTO students (card_number)
           VALUES (%s);""", (cardnum,))

    # Commit changes
    conn.commit()

'''
Update a student's name and email
@param cardnum {String}
@param name {String}
@param email {String}
'''


def update_student_contact(cardnum, name, email, s_id):
    # Bail if connection with DB is lost
    if conn.closed:
        print_error('Connection with DB was lost! Please restart application')
        exit(1)

    # Update DB with name and email
    db.execute(
        """UPDATE students
           SET name = %s, email = %s, s_id=%s
           WHERE card_number = %s;""", (name, email, s_id, cardnum))

    # Commit changes
    conn.commit()

'''
Update a student's checked_in status
@param cardnum {String}
@param checkedin {Boolean}
'''


def update_student_checkin(cardnum, checkedin):
    # Bail if connection with DB is lost
    if conn.closed:
        print_error('Connection with DB was lost! Please restart application')
        exit(1)

    # Update DB with checkin
    db.execute(
        """UPDATE students
           SET checked_in = %s
           WHERE card_number = %s;""", (checkedin, cardnum))

    # Update DB with points
    db.execute(
        """UPDATE students
           SET points = points + 1
           WHERE card_number = %s;""", (cardnum,))

    # Commit changes
    conn.commit()

'''
Print strings in different colors
@param string {String}
@return none
'''


def print_error(string):
    print '{}{}{}{}'.format(Fore.RED, Style.BRIGHT, string, Style.RESET_ALL)


def print_success(string):
    print '{}{}{}{}'.format(Fore.GREEN, Style.BRIGHT, string, Style.RESET_ALL)


def print_status(string):
    print '{}{}{}{}'.format(Fore.CYAN, Style.BRIGHT, string, Style.RESET_ALL)

'''
Ask for string input
@param request {String}
@return {String}
'''

#poop
def get_info(request):
    response = raw_input('{}{}{}{} => '.format(Fore.YELLOW, Style.BRIGHT, request, Style.RESET_ALL))
    return response

if __name__ == '__main__':

    print_status('Connecting to DB... Kill me if I take waaaay to long...')

    # Establish a connection to our DB
    global conn, db
    try:
        conn = psycopg2.connect(database=DATABASE,
                                user=USER,
                                password=PASSWORD,
                                host=HOST,
                                port=PORT)
    except NameError:
        print("Your config file is not set properly. Or you need to contact Kyle for the info.")

    db = conn.cursor()

    print_success('Ready for action!')

    # Some sleep to see success message
    time.sleep(1)
    # Clear screen
    os.system('clear')

    # Main event loop
    while 1:
        card_dump = getswipe("Swipe your R'card ID\n")
        card_number = parse_number(card_dump)

        # If we were NOT able to get a valid number
        # from the swipe, let the user know and skip everything
        # else
        if card_number is None:
            print_error("Invalid swipe. Try again")
            continue

        student_info = fetch_info(card_number)

        # If we are missing info from the student
        # IE name or email (don't let them modify anything else!), or
        # if we are missing them entirely, ask for missing required info
        if student_info is None or student_info['name'] is None \
                or student_info['email'] is None:
            # If student is missing entirely, make a model for them
            # and create a row in the DB
            if student_info is None:
                student_info = {'name': None, 'email': None, 'checked_in': None}
                insert_student(card_number)

            name = None
            email = None
            s_id = None
            checked = False

            # Keep asking for name and email till student is content
            # TODO: Some sort of verification to check for valid email
            # and name
            while 1:
                # Get name and email
                #name = get_info("Enter your full name")
                if not checked:
                    name = parse_name(card_dump)
                else:
                    name = get_info("Enter your full name")
                email = get_info("Enter your email")
                s_id = parse_id(card_dump)
                print ''
                print_status("Is the following correct?\nName: {}\nEmail: {}\nID: {}".format(name, email, s_id))

                # Break out if student is content
                response = get_info("[y/n]")
                if response.lower() == 'y':
                    # Save responses and break
                    student_info['name'] = name
                    student_info['email'] = email
                    student_info['s_id'] = s_id
                    break
                checked = True

            # Update DB with student contact info
            update_student_contact(card_number, name, email, s_id)

        # Figure out if the student has already logged in today
        # if so, let them know they have already!
        if student_info['checked_in']:
            print_success("You have already checked in, {}!".format(student_info['name']))
        else:
            update_student_checkin(card_number, True)
            print_success("Thanks for checking in, {}!".format(student_info['name']))

        # Some sleep so person can see results
        time.sleep(2)

        # Clear screen
        os.system('clear')
