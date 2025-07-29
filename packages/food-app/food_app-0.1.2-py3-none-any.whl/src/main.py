from rich import print
from rich.console import Console
from rich.markdown import Markdown

from src.food_helper import smal_print_all_food, print_date_file, print_all_food, print_img
from src.run import add_food
from src.add_food_db import new_food
from src.pie_chart import make_pie
from src.last_month import get_this_month


# Start the app with background image
print_img("images/meat.jpg")

''' main menu '''
console = Console()
def menu():
    with open("src/menu.md") as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)


run = True
while run:
    answer = input(" m - menu: ")
    if answer == "q":
        print("Bye")
        run = False
    elif answer == "m":
        menu()
    elif answer == "r":
        # run food app
        add_food()
    elif answer == "k":
        make_pie()
    elif answer == "s":
        smal_print_all_food()
    elif answer == "a":
        # TODO print 10 line and stop
        print_all_food("json/all_food.json")
    elif answer == "d":
        # open file to print to console
        file = input("file to open: ")
        if file == "":
            print_date_file("json/2025-06-09.json")
        else:
            try: 
                print_date_file(file)
            except:
                print(file, "do not exist")
    elif answer == "l":
        get_this_month()
    elif answer == "n":
        # add new item/food to DB
        new_food()
    elif answer == "j":
        print_img("images/meat.jpg")
    else:
        print("wrong value: q - quit; m - menu")
