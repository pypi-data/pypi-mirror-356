import datetime
from rich import print
from src.food_helper import  get_json_file, print_all_food, print_date_file, open_file, write_file, add_new_line


file_name = "" # file to open
new_data_list = ""
all_food = "json/all_food.json"
# Get all food data
all_food_list = get_json_file(all_food)


def init():
    # Ask user for a filname to store new data
    global file_name 
    file_name = input("Choose your filename or hit Enter for todays date: ")
    if file_name == "":
        date =  datetime.date.today()
        file_name = "json/" + str(date) + ".json"

    # Show filname
    print(f"Open : {file_name}")

    # Open new file {filename} returns data_list
    global new_data_list 
    new_data_list = open_file(file_name)


def ask_new_food():
    ''' ask user to type in Food and Amount '''
    food_choice = 0
    # Ask for food-index to add
    while True:
        food_choice = input("Choose food (index nr) from the list: ")
        try :
            food_choice = int(food_choice)
            if food_choice >= len(all_food_list):
                print(f"{food_choice} is not a valid number! Choose a number between 0 and {len(all_food_list) -1}")
                continue
            break
        except:
            print(f"{food_choice} is not a valid number!")

    # ask for amount of 100g food
    food_amount = 0
    while True:
        food_amount = input(f"How many 100g of {all_food_list[food_choice]['Mat']}: ")
        try :
            food_amount = float(food_amount)
            break
        except:
            print(f"{food_amount} is not a valid number!")

    print(f"You added {food_amount * 100}g of {all_food_list[food_choice]['Mat']}")

    # Add new line to list and calculate Totals
    add_new_line(new_data_list, food_choice, food_amount)


### add data to new_data_list ###
def add_food():
    init()
    while True:
        answer = input("Hit Enter to continue or ( 'q' to quit): ")
        if answer == 'q':
            break
        # print all food with index
        print_all_food(all_food)
        # ask to add more food or "q" to quit
        ask_new_food()
    
    # Write the file with the new data
    _ = write_file(file_name, new_data_list)
    # Print out the new file
    print_date_file(file_name)


if __name__ == "__main__":
    # print all food with index
    print_all_food(all_food)
    add_food()
