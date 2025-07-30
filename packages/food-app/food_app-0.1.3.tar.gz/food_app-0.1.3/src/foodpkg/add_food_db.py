import json

def new_food():
    all_food = "json/all_food.json"
    print(f"Add new food to the database: {all_food}")

    # Load existing data
    try:
        with open(all_food, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
    except FileNotFoundError:
        data_list = []

    while True:
        food = input("Enter food (or 'q' to quit): ")
        if food == 'q':
            break
        kcal = float(input("Enter calories: "))
        fat = float(input("Enter fat: "))
        carbs = float(input("Enter carbohydrates: "))
        protein = float(input("Enter protein: "))

        data_list.append({'Mat': food, 'Kcal': kcal, 'Fett': fat, 'Kolhydrater': carbs, 'Protein': protein})
        #data_list.append({food, kcal, fat, carbs, protein})

    # Write updated data
    with open(all_food, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    new_food()