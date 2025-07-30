import json
import sys
import os
import subprocess
from rich.table import Table
from rich import print


def get_json_file(file):
    ''' open file data, return json_list '''
    data_file = file
    # load data from json file
    with open(data_file, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    return data_list


def print_food_file(file):
    ''' open file data, print rich.table from json_list '''
    data_file = file
    # load data from json file
    data_list = get_json_file(data_file)
   
    # create a table
    table = Table(title=data_file, style="orange1", show_lines=True)
    
    # add columns to the table
    table.add_column("food / 100g", style="green")
    table.add_column("kcal", style="cyan")
    table.add_column("fat", style="cyan")
    table.add_column("carbs", style="cyan")
    table.add_column("protein", style="cyan")
    
    # add rows to the table
    for food_data in data_list:
        table.add_row(food_data['Mat'], str(food_data['Kcal']), str(food_data['Fett']), str(food_data['Kolhydrater']), str(food_data['Protein']))
    
    # print the table using rich console
    print(table)


def print_all_food(file):
    ''' print all food with index '''
    all_food = "data/json/all_food.json"
    data_list = get_json_file(file)

    # Create a table
    table = Table(title="Food Data", show_lines=True)
    
    # Add columns to the table
    table.add_column("index", style="red")
    table.add_column("Food", style="green")
    table.add_column("Kcal", style="cyan")
    table.add_column("Fat", style="cyan")
    table.add_column("Carbs", style="cyan")
    table.add_column("Protein", style="cyan")
    
    # Add index to rows
    index = 0
    for food_data in data_list:
        table.add_row(str(index), food_data['Mat'], str(food_data['Kcal']), str(food_data['Fett']), str(food_data['Kolhydrater']), str(food_data['Protein']))
        index += 1

    # Print the table useing rich console
    print(table)


def smal_print_all_food(file='data/json/all_food.json'):
    ''' print all food with index '''
    data_list = get_json_file(file)

    # Create a table
    table = Table(title="Food Data", show_lines=True)
    
    # Add columns to the table
    table.add_column("Index", style="red")
    table.add_column("Food", style="green")
    table.add_column("Index", style="red")
    table.add_column("Food", style="green")
    table.add_column("Index", style="red")
    table.add_column("Food", style="green")
    
    index = 0
    food = {}
    for food_data in data_list:
        food.update({index: food_data['Mat']})
        index += 1
        #table.add_row(str(index), food_data['Mat'], str(index), food_data['Mat'], str(index), food_data['Mat'])

    print(food)
    #print(table)


def show_command():
    print('All commands:')
    print(' "q" for quit')
    print(' "l" list all_food in db with index.')
    print(' "ll" list all food you added.')
    print(' "c" show commands')


def print_date_file(file):
    ''' print food table from date-json-file '''
    data_file = file
    # load data from json file
    data_list = get_json_file(data_file)
    
    # create a table
    table = Table(title=data_file, style="orange1", show_lines=True, expand=True)
    
    # add columns to the table
    table.add_column("Food/100g", style="cyan")
    table.add_column("Kcal", style="magenta")
    table.add_column("Fat", style="yellow")
    table.add_column("Carbs", style="green")
    table.add_column("Prot", style="cyan")
    table.add_column("Amount", style="plum2")
    table.add_column("SumKcal", style="gray37")
    table.add_column("SumCarbs", style="gray37")
    
    # calculate total carbs, kcal, fat and protein
    totalCarbs = 0
    totalKcal = 0
    totalFat = 0
    totalProt = 0

    # add rows to the table
    for food_data in data_list:
        table.add_row(food_data['Mat'], str(food_data['Kcal']), str(food_data['Fett']), str(food_data['Kolhydrater']), str(food_data['Protein']), str(food_data['Amount'] * 100) + "g", str("{:.2f}".format(food_data['TotKcal'])), str("{:.2f}".format(food_data['TotCarbs'])))
        totalCarbs += float(food_data['TotCarbs'])
        totalKcal += float(food_data['TotKcal'])
        totalFat += float(food_data['Fett']) * float(food_data['Amount'])
        totalProt += float(food_data['Protein']) * float(food_data['Amount'])

    # print the table using rich console
    print(table)
    print(f"Total Kcal: [magenta]{totalKcal:.2f}[/],   Fat: [yellow]{totalFat:.2f}[/],   Carbs: [green]{totalCarbs:.2f}[/],   Prot: [cyan]{totalProt:.2f}[/],")


def get_kcal_values(file) -> list:
    ''' print food table from date-json-file '''
    data_file = file
    data_list = get_json_file(data_file)
    
    # calculate total carbs, kcal, fat and protein
    totalCarbs = 0
    totalKcal = 0
    totalFat = 0
    totalProt = 0

    # add rows to the table
    for food_data in data_list:
        totalCarbs += float(food_data['TotCarbs'])
        totalKcal += float(food_data['TotKcal'])
        totalFat += float(food_data['Fett']) * float(food_data['Amount'])
        totalProt += float(food_data['Protein']) * float(food_data['Amount'])

    return [totalKcal, totalFat, totalCarbs, totalProt]


def print_kcal_values(file):
    v = get_kcal_values(file)
    # Calculate % of Kcal
    fat = v[1]*9/v[0]
    carbs =  v[2]*4/v[0]
    prot =  v[3]*4/v[0]

    print("values from file: ", file)
    print(f"Total g Kcal: [magenta]{v[0]:.2f}[/],   Fat: [yellow]{v[1]:.2f}[/]g,   Carbs: [green]{v[2]:.2f}[/]g,   Prot: [cyan]{v[3]:.2f}[/]g,")
    print(f"Total % Kcal: [magenta]{v[0]:.2f}[/],   Fat: [yellow]{fat*100:.2f}[/]%,   Carbs: [green]{carbs*100:.2f}[/]%,   Prot: [cyan]{prot*100:.2f}[/]%,")


def open_file(file_name):
    ''' open file and returns data list as empty if not exist '''
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
    except FileNotFoundError:
        data_list = []
    return data_list
    

def write_file(file_name, data_list):
    ''' Write updated data '''
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)
    return data_list


def add_food(file_name, data_list):
    ''' Add entries to file and write to file'''
    while True:
        food = input("Enter food (or 'q' to quit): ")
        if food == 'q':
            break
        kcal = float(input("Enter calories: "))
        fat = float(input("Enter fat: "))
        carbs = float(input("Enter carbohydrates: "))
        protein = float(input("Enter protein: "))
    
        data_list.append({'Mat': food, 'Kcal': kcal, 'Fett': fat, 'Kolhydrater': carbs, 'Protein': protein})
        write_file(file_name, data_list)


def add_new_line(new_data_list, choice, amount):
    ''' Add new line to list and calculate Totals '''
    # Get all food data
    all_food = "data/json/all_food.json"
    all_food_list = get_json_file(all_food)
    
    # Calculate Total Carbs end Kcal
    totkcal = amount * all_food_list[choice]['Kcal']
    totcarbs = amount * all_food_list[choice]['Kolhydrater']

    food  = all_food_list[choice]['Mat']
    kcal  = all_food_list[choice]['Kcal']
    fat   = all_food_list[choice]['Fett']
    carbs = all_food_list[choice]['Kolhydrater']
    protein  = all_food_list[choice]['Protein']
    
    new_data_list.append({'Mat': food, 'Kcal': kcal, 'Fett': fat, 'Kolhydrater': carbs, 'Protein': protein, 'Amount': amount, 'TotKcal': totkcal, 'TotCarbs': totcarbs})
    

def print_img(img):
    ''' Display the image in the kitty terminal '''
    if 'KITTY_WINDOW_ID' in os.environ:
        kitty_path = "/usr/bin/kitty"
        if sys.platform == 'darwin': # macos
            kitty_path = "/opt/homebrew/bin/kitty"
        subprocess.run([kitty_path, "icat", img])
    else:
        print("Can not display image. Not running inside Kitty terminal")