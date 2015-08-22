Card-Swiper
===========

app.py:
    CLI application which is used for signing in using a student's rcard.

checkin.py:
    CLI application that will compile a list of everyone in attendance to the meeting.
    Output file is the current date. eg '2015-08-21'

paid.py:
    CLI application that will update the record of a member if they have paid for club membership.

db_config-TEMPLATE:
    Config file used to store the database information. Only template is on github.
    Message Kyle if you want the credentials for access.

# Database schema

| name          | email          | checked_in   | card_number    | paid       | tshirt_size |
| ------------- |:---------------|:-------------|:---------------|:-----------|:----------- |
| Kyle Minshall |kmins002@ucr.edu|t             |6021123456789100| t          | XL          |
