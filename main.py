import os, shutil, sys
from datetime import datetime
from settings import settings
from calendar import month_name as months_list

def get_day_group_folder(day_of_month):
    folders = (
        {'min': 1, 'max': 10, 'name': '01-10'},
        {'min': 11, 'max': 20, 'name': '11-20'},
        {'min': 21, 'max': 31, 'name': '21-31'}
    )

    for folder in folders:
        if day_of_month >= folder['min'] and day_of_month <= folder['max']:
            return os.path.join(settings.tickler_path, 'Days', folder['name'])

def get_day_folder(day_of_month):
    day_group_folder = get_day_group_folder(day_of_month)
    return os.path.join(day_group_folder, str(day_of_month).zfill(2))

def move_files_to_inbox(source_path):
    items = os.listdir(source_path)
    
    # Move each item to the destination directory
    for item in items:
        item_source_path = os.path.join(source_path, item)
        item_destination_path = os.path.join(settings.inbox_path, item)
        
        # Use shutil.move to move the item
        shutil.move(item_source_path, item_destination_path)
        print("Moved item " + item)

def get_current_month():
    now = datetime.now()
    # find current month
    return now.strftime('%B')

def get_month_folder(month):
    months_folder = os.path.join(settings.tickler_path, 'Months')
    month_folders = os.listdir(months_folder)
    
    for folder in month_folders:
        if month in folder:
            return os.path.join(months_folder, folder)

def get_current_day():
    now = datetime.now()
    return now.day

def get_day_month_from_input(dayMonth=None):
    day = None
    month = None
    if dayMonth == None:
        day = get_current_day()
        if day == 1:
            month = get_current_month()
    elif isinstance(dayMonth, int):
        day = dayMonth
    elif isinstance(dayMonth, str):
        # include negative numbers
        if dayMonth.lstrip('-').isdigit():
            day = int(dayMonth)
            if day == 1:
                month = get_current_month()
        else:
            day_month_lower = dayMonth.lower()
            for m in months_list:
                if m.lower().startswith(day_month_lower):
                    month = m
                    break
    if day == 0:
        day = get_current_day()
    elif day < 0:
        # use relative day when negative number
        current_day = get_current_day()
        day = ((current_day + day - 1) % 31) + 1
    elif day > 31:
        day = ((day - 1) % 31) + 1
    
    # print("Day: " + str(day) + ", Month: " + str(month))
    return day, month

def fetch_tickler_notes(day=None, month=None):
    print("Fetching tickler notes...")
    if day != None:
        day_folder = get_day_folder(day)
        
        # move all notes from day folder into inbox
        print(f"Moving notes from day folder ({os.path.basename(day_folder)})\n")
        move_files_to_inbox(day_folder)
    
    if month != None:
        month_folder = get_month_folder(month)
        
        print(f"\nMoving notes from month folder ({os.path.basename(month_folder)})\n")
        move_files_to_inbox(month_folder)

def get_tickler_status(day=None, month=None):
    if day != None:
        day_folder = get_day_folder(day)
        dir_list = os.listdir(day_folder)
        print(f"Day folder ({os.path.basename(day_folder)}) ({len(dir_list)} file{'' if len(dir_list) == 1 else 's'}): {dir_list}")
        
    if month != None:
        month_folder = get_month_folder(month)
        dir_list = os.listdir(month_folder)
        print(f"Month folder ({os.path.basename(month_folder)}) ({len(dir_list)} file{'' if len(dir_list) == 1 else 's'}): {dir_list}")

if __name__ == "__main__":
    args = sys.argv
    # first argument is script name
    # so we want second argument onwards
    if len(args) == 1:
        fetch_tickler_notes()
    elif len(args) == 2:
        if args[1] == 'status':
            get_tickler_status(*get_day_month_from_input())
        else:
            day, month = get_day_month_from_input(args[1])
            fetch_tickler_notes(day, month)
    elif len(args) == 3 and args[1] == 'status':
        day, month = get_day_month_from_input(args[2])
        get_tickler_status(day, month)
