import json , os
from datetime import datetime

def get_input(prompt="", answers = [], specific = True, as_int = False, non_empty = False, error="Invalid", no_repeat_characters = False, acknowledge_negative = False):
    """Repeatedly prompts user until input meets requirements"""
    while True:
        user = input(prompt)
        user = (user.replace(" ","") if as_int else user)
        if not (non_empty and user.strip() == "") and ("".join([str(user.count(char)) for char in user]).replace("1","") == "" or not no_repeat_characters):
            if (user in answers or (not specific and user.strip().lower() in [ans.strip().lower() for ans in answers if ans == str(ans)]) or answers == []) and not as_int:
                break
            elif as_int and user.isdigit() and (answers == [] or int(user) in answers):
                user = int(user)
                break
            elif acknowledge_negative and as_int and user.find("-") == 0 and user.count("-") == 1 and user.replace("-","").isdigit() and (answers == [] or int(user.replace("-","")) *-1 in answers):
                user = int(user.replace("-","")) * -1
                break
        if error != "":
            print(error)
    return user

def menu_choice():
    """Displays menu and prompts user for a choice"""
    print("Zombie Shelter Manager \n1. View shelter info \n2. Change shelter value \n3. View change log \n4. Quit")
    user = get_input(prompt = "Enter choice: ", answers = [1,2,3,4], as_int= True)
    return user

def view_shelter(shelter: dict):
    """Displays shelter information"""
    for key, val in shelter.items():
        print(f"{key.title().replace("_"," ")}: {val}")

def change_val(shelter: dict):
    """Allows the user to change a value of their shelter"""
    for index, key in enumerate(shelter.keys()):
        print(f"{index+1}. {key.title().replace("_"," ")}")
    user = get_input(prompt= "Which value would you like to change: ", answers=[1,2,3,4,5,6,7], as_int=True)
    val = ["shelter_name", "leader", "survivors", "food", "water", "barricade_health", "radio_working"][user-1]
    old_val = shelter[val]
    print("", end=(f"Current {val.title().replace("_"," ")} is {shelter[val]}\n" if user != 7 else ""))
    new_val = ((get_input(prompt="Enter a new value: ", non_empty=True) if user < 3 else get_input(prompt="Enter a new value: ", as_int=True)) if user != 6 else get_input(prompt = "Enter a new value from 0-100: ", as_int=True, answers=range(0,101))) if user < 7 else (True if get_input(prompt = "Is the radio working(y-n): ", answers=["y","n"], specific= False)=="y" else False)
    shelter.update({val:new_val})
    with open("shelter.json", "w") as file:
        json.dump(shelter, file, indent= 4)
    with open("shelter.log", "a") as file:
        file.write(f"{str(datetime.now())[:19]} | {val.title().replace("_"," ")} changed from {old_val} to {new_val}\n")
    print(f"{val.title().replace("_"," ")} changed from {old_val} to {new_val}\nShelter data saved. Change recorded in shelter.log.")
    return shelter


def view_log():
    """Displays the shelter log"""
    lines = 0
    with open("shelter.log", "r") as file:
        for line in file:
            lines += 1
            print(line)
    if lines == 0:
        print("No changes have been recorded yet.")

def main():
    """The main code for 'Zombie Shelter Manager'"""
    os.system('cls' if os.name == 'nt' else 'clear')
    with open("shelter.json", "r") as file:
        shelter = json.load(file)
    while True:
        choice = menu_choice()
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == 1:
            view_shelter(shelter)
        elif choice == 2:
            shelter = change_val(shelter)
        elif choice == 3:
            view_log()
        else:
            print("Goodbye")
            break
        input(":")
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()