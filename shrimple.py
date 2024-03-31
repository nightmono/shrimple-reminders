#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('reminder', metavar='reminder', type=str, nargs='*',
                    help='The reminder to add')

reminder = parser.parse_args().reminder
reminder = " ".join(reminder)
print(f"Reminder: {reminder}")