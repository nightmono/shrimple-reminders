#!/usr/bin/env python3

import argparse
from datetime import datetime

def date(date):
    # Give support for dd/mm/yyyy, yyyy/mm/dd, mm/dd/yyyy.
    # Support for dd/mm and mm/dd dates too, via appending the current year.
    for date_format in ["%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y"]:
        try:
            return datetime.strptime(date, date_format)
        except ValueError:
            try:
                # Assume user forgot the year and append it for them.
                year = datetime.today().year
                return datetime.strptime(f"{date}/{year}", date_format)
            except ValueError:
                pass
        
    raise ValueError(f"{date} is an invalid date")

parser = argparse.ArgumentParser(description='A Shrimple reminders app.')
subparsers = parser.add_subparsers()

add_parser = subparsers.add_parser("add", help="Add a new reminder")
add_parser.add_argument('reminder', nargs='*',
                    help='reminder description')
add_parser.add_argument("--date", type=date,
                        help="date of the reminder")

subparsers.add_parser("today", help="View today's reminders")

list_parser = subparsers.add_parser("list", 
                                    help="Searches for and lists reminders")
list_parser.add_argument("--reminder",
                         help="searches for reminders containing the passed text")
list_parser.add_argument("-complete", 
                         help="searches for reminders marked as complete")
list_parser.add_argument("--on", 
                         help="searches for reminders set to provided date")
list_parser.add_argument("--after", 
                         help="searches for reminders set to after the provided date")
list_parser.add_argument("--before", 
                         help="searches for reminders set to before the provided date")
list_parser.add_argument("--made-on", 
                         help="searches for reminders created on provided date")
list_parser.add_argument("--made-after", 
                         help="searches for reminders created after provided date")
list_parser.add_argument("--made-before",
                         help="searches for reminders created before provided date")

complete_parser = subparsers.add_parser("complete",
                                        help="Marks a reminder as complete")
complete_parser.add_argument("--reminder",
                             help="complete reminder that exactly matches passed text")
complete_parser.add_argument("--index",
                             help="complete reminder at passed index")

delete_parser = subparsers.add_parser("delete",
                                      help="Deletes reminders")
delete_parser.add_argument("--reminder",
                             help="delete reminder that exactly matches passed text")
delete_parser.add_argument("--index",
                             help="delete reminder at passed index")

args = parser.parse_args()