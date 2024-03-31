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
# Default behaviour is to add a reminder.
parser.add_argument('reminder', nargs='*',
                    help='The reminder to add')
parser.add_argument("--date", required=False, type=date,
                    help="The date of the reminder")

reminder = parser.parse_args().reminder
reminder = " ".join(reminder)
print(f"Reminder: {reminder}")
print("args:", parser.parse_args())