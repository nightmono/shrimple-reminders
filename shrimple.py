#!/usr/bin/env python3

import argparse
from datetime import datetime
import shlex

def get_reminders_from_file(file=None):
    if file is None:
        file = "shrimple-reminders.txt"
    
    reminders = []
    
    try:
        with open(file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                reminders.append(line)
    except FileNotFoundError:
        # Create shrimple-reminders text file if it file not found.
        with open(file, "w") as f:
            pass
            
    return reminders

def save_reminders_to_file(file=None, reminders_dict=None):
    if file is None:
        file = "shrimple-reminders.txt"
    if reminders_dict is None:
        reminders_dict = []
        
    with open(file, "w", encoding="utf-8") as f:
        for reminder in format_reminders_from_dict(reminders_dict):
            f.write(reminder)
            f.write("\n")

def format_reminders_into_dict(reminders):
    reminders_dict = []
    
    for reminder in reminders:
        formatted_reminder = {}
        # Split via quotation marks. 
        # The reminder should ideally be in this format (date is optional):
        # [-] "Reminder content" DD-MM-YYYY
        # [X] "Reminder content" DD-MM-YYYY
        # Resulting in these args: [complete_or_not, content, optional_date]
        reminder_args = shlex.split(reminder)
        
        formatted_reminder["complete"] = reminder_args[0] == "[X]"
        formatted_reminder["reminder"] = reminder_args[1]
        
        # Only add the date if it is present.
        if len(reminder_args) == 3:
            formatted_reminder["date"] = reminder_args[2]
        
        reminders_dict.append(formatted_reminder)
    
    return reminders_dict

def format_reminders_from_dict(reminders_dict):
    reminders = []
    
    for formatted_reminder in reminders_dict:
        reminder = "[X] " if reminder["complete"] else "[-] "
        reminder += reminder["reminder"]
        # := Assigns date to date within the if statement.
        if (date := reminder.get("date", False)):
            reminder += " " + date
            
    return reminders

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

def add_reminder(args):
    if not args.reminder:
        add_parser.print_help()
        exit()
        
def list_reminder(args):
    reminders = get_reminders_from_file()
    reminders_dict = format_reminders_into_dict(reminders)
    
    print("\n".join(reminders))

parser = argparse.ArgumentParser(description='A Shrimple reminders app.')
subparsers = parser.add_subparsers()

add_parser = subparsers.add_parser("add", help="Add a new reminder")
add_parser.add_argument('reminder', nargs='*',
                    help='reminder description')
add_parser.add_argument("--date", type=date,
                        help="date of the reminder")
add_parser.set_defaults(func=add_reminder)

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
list_parser.set_defaults(func=list_reminder)

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
print(args)

# Print help if ran without arguments.
if not vars(args):
    parser.print_help()
    exit()
    
args.func(args)