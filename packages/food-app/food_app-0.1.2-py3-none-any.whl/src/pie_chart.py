import matplotlib.pyplot as plt
import subprocess
import datetime
from rich import print
from src.food_helper import get_kcal_values, print_img

def make_pie():
    date =  datetime.date.today()
    tile_name = "% of Kcal " + str(date) 
    img_name = "images/pie_chart_" + str(date) + ".png"


    # Values for the pie chart
    values = get_pie_values()

    # Labels for the pie chart
    labels = ['Fat', 'Protein', 'Carbs']

    # Create the pie chart
    fig, ax = plt.subplots()

    # Set the background color to black
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    colors = ['darkorange', 'darkcyan', 'green']

    # Create pie chart
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                  startangle=90, colors=colors)

    # Set the text color and font weight to white and bold
    for text in texts:
        text.set_color('white')
        text.set_weight('bold')

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')

    # Title with white bold text
    plt.title(tile_name, color='white', weight='bold')

    # Save the pie chart to an image file
    plt.savefig(img_name, facecolor=fig.get_facecolor(), edgecolor='none')

    # Display the image in the kitty terminal
    print_img(img_name)


def get_pie_values() -> list:
    ''' open todays json-file, return Kcal % of Fat, Carbs and protein and print it out'''

    # try open file if exist, else return a fix value
    date =  datetime.date.today()
    file = "json/" + str(date) + ".json"
    values = try_open_file(file)
    if values != []:
        print(file, ": Do not exist!")
        return [0.5, 0.3, 0.2]

    # get total Kcal, Fat, Carbs and Protein in gram
    v = get_kcal_values(file)
    # Calculate % of Kcal
    fat = v[1]*9/v[0]
    carbs =  v[2]*4/v[0]
    prot =  v[3]*4/v[0]

    print("values from file: ", file)
    print(f"Total g Kcal: [magenta]{v[0]:.2f}[/],   Fat: [yellow]{v[1]:.2f}[/]g,   Carbs: [green]{v[2]:.2f}[/]g,   Prot: [cyan]{v[3]:.2f}[/]g,")
    print(f"Total % Kcal: [magenta]{v[0]:.2f}[/],   Fat: [yellow]{fat*100:.2f}[/]%,   Carbs: [green]{carbs*100:.2f}[/]%,   Prot: [cyan]{prot*100:.2f}[/]%,")

    return [fat, prot, carbs]


def try_open_file(file) -> list:   
    try:
        with open(file, 'r', encoding='utf-8') as f:
            values = []
    except FileNotFoundError:
        values = [0.7, 0.2, 0.1]
    return values