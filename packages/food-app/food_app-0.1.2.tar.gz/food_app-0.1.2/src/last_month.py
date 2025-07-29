import os
from datetime import datetime, timedelta
from rich import print
from src.food_helper import get_kcal_values
from src.food_helper import print_kcal_values


def get_this_month():
    # Get today's date
    today = datetime.today().date()
    #print("Today:", today)
    this_month = str(today)[:-2]

    # Subtract 7 days
    #seven_days_ago = today - timedelta(days=7)
    #print("7 days ago:", seven_days_ago)
    
    path = 'json'
    json_files = [j for j in os.listdir(path) if j.endswith('.json') and j.startswith(this_month)]
    json_files.sort()
    if len(json_files) < 1:
        print("No files this month.")
    
    for file in json_files:
        f = "json/" + file
        print_kcal_values(f)
        print('[bold yellow]*******************************************************************')


