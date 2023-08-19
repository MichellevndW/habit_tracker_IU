import questionary
import os
import sys
import re
from datetime import date
from tracker import Tracker
from habit import Habit
from db import get_db, create_tables, retrieve_all, retrieve_one, edit_habit_db
from sample_data import add_sample_data

db = get_db("habit_tracker.db")
create_tables(db)

def print_cust(text, style="bold"):
    return questionary.print(text, style = style)


def new_con():
    os.system('clear')

def exit_cli():
    sys.exit()


def main_menu():
    print_cust("\n****MAIN MENU****\n", "bold fg:cyan")
    menu_option = questionary.select("What would you like to do today?\n", 
                                     choices=["1. Log a Habit",
                                              "2. Add a New Habit", 
                                              "3. Edit Habit", 
                                              "4. Remove Habit", 
                                              "5. View Current Habits",
                                              "6. Analysis",
                                              "7. Exit"]).ask()
    return menu_option


def create_new_habit(username):
    print_cust("\n***Create New Habit***", "bold fg:cyan")
    print_cust(f"\nOk {username}, let's create a new habit!")
    name = questionary.text("Name of new habit: ").ask()
    description = questionary.text("Description of habit: ").ask()
    interval = questionary.select("What is the interval for this habit?\n",
                                  choices = ["Daily", "Weekly", "Monthly"]).ask()
    category = questionary.select("Habit category:\n",
                                  choices = ["Health", "Productivity", "Career", 
                                             "Relationships", "Emotional", "Financial",
                                             "Spiritual", "Religious", "Social"]).ask()
    habit = Habit(None, name, description, interval, category, (date.today().strftime("%Y%m%d")))
    habit.store_habit(db)
    print_cust(f"\nNew {interval} {name} habit created.","bold fg:green")

def demo_data_check(username):
    demo_loaded = False
    all_data, headers = retrieve_all(db, "habit")
    if all_data:
        for data in all_data:
            if data[1] == "DEMO_DATA":
                demo_loaded = True
    if demo_loaded:
        #TODO SCREEN BREAK
        print_cust("\n--Demo data has already been loaded--")
    else:
        demo_data = questionary.select("Would you like to load the available demo data?", choices=["Yes","No thanks"]).ask()
        if demo_data == "Yes":
            add_sample_data(db)
        else:
            create_new_habit(username)

def get_date_input():
    date_correct = False

    while date_correct == False:
        date_input = questionary.text("When would you like to log this habit for? (yyyy mm dd)").ask()
        date_check=re.sub("[^0-9]","",date_input)
        current_year = int(date.today().year)
        current_date = int(date.today().strftime("%Y%m%d"))
        print(current_date)
        if int(date_check) > current_date:
            print("Habits cannot be marked complete in the future, please try again")
        elif int(date_check[0:4]) > current_year or int(date_check[0:4]) < 2020:
            print("Only years between 2020 and the current year can be entered, please try again")
        elif int(date_check[4:6]) > 12 or int(date_check[4:6]) < 1:
            print_cust("There seems to be an error with the month entered, please try again")
        elif int(date_check[6:8]) >31 or int(date_check[6:8]) < 1:
            print_cust("There seems to be an error with the day entered, please try again")  
        elif int(date_check[4:6]) in [4, 6, 9, 11]:
            if int(date_check[6:8]) > 30:
                print_cust("There seems to be an error with your date, please try again")
        elif int(date_check[4:6]) == 2:
            if int(date_check[6:8]) > 28:
                print_cust("There seems to be an error with your date, please try again")
        else:
            date_correct = True
    return date_input


def log_habit():
    habits, headers = retrieve_all(db, "habit")
    menu_options = []
    chosen_habit = None
    for habit in habits:
        if habit[1].lower() != "demo_data":
            menu_options.append(habit[1].capitalize())
    menu_options.append("Exit")
    menu_option = questionary.select("Which habit would you like to mark as complete?\n", 
                                     choices=menu_options).ask()
    for habit in habits:
        if habit[1].lower() == menu_option.lower():
            chosen_habit = habit
    menu_option = questionary.select("Did you complete this habit today?\n", 
                                     choices=["Yes", "No"]).ask()
    if menu_option == "Yes":
        description = questionary.text("Give a brief description: ").ask()
        notes = questionary.text("Add any notes here: ").ask()
        track = Tracker(chosen_habit[0], None, description, date.today(), notes )
        track.store_tracker(db)
        data_pushed, headers = retrieve_all(db, "tracker")
        data_pushed = data_pushed[-1]
        habit, headers = retrieve_one(db, "habit", data_pushed[1])
        print_cust(f"\n{habit[0][1].capitalize()} habit marked as complete!\nDate: {data_pushed[3]}", "bold fg:green")
    else:
        date_input = get_date_input()
        description = questionary.text("Give a brief description: ").ask()
        notes = questionary.text("Add any notes here: ").ask()
        track = Tracker(chosen_habit[0], None, description, date_input, notes )
        track.store_tracker(db)
        data_pushed, headers = retrieve_all(db, "tracker")
        data_pushed = data_pushed[-1]
        habit, headers = retrieve_one(db, "habit", data_pushed[1])
        print_cust(f"\n{habit[0][1].capitalize()} habit marked as complete!\nDate: {data_pushed[3]}", "bold fg:green")

def edit_habit():
    print_cust("\n***Edit Habit***", "bold fg:cyan")
    all_data, headers = retrieve_all(db, "habit")
    menu_options = []
    for data in all_data:
        if data[1] != "DEMO_DATA":
            menu_options.append(f"ID:{data[0]} Name: {data[1].capitalize()}")
    habit_to_edit = questionary.select("Which habit would you like to edit?\n", 
                                       choices=menu_options).ask()
    habit_id = int(habit_to_edit[3])
    habit_data, headers = retrieve_one(db, "habit", habit_id)
    menu_options = []
    for header in headers:
        if header != "id" and header != "date_added":
            menu_options.append(header.capitalize())
    to_edit = questionary.select("What would you like to edit?\n", 
                                 choices=menu_options).ask()
    if to_edit.lower() == "name" or to_edit.lower() == "description":
        new_data = questionary.text(f"Please enter a new {to_edit.lower()}: ").ask()
    elif to_edit.lower() == "interval":
        new_data = questionary.select("What is the interval for this habit?\n",
                                  choices = ["Daily", "Weekly", "Monthly"]).ask()
    elif to_edit.lower() == "category":
        new_data = questionary.select("Habit category:\n",
                                      choices = ["Health", "Productivity", "Career", 
                                                 "Relationships", "Emotional", "Financial",
                                                 "Spiritual", "Religious", "Social"]).ask()
    edit_habit_db(db, to_edit.lower(), f"'{new_data}'", habit_id)
    print_cust(f"\nHabit -{habit_data[0][1].lower()}-'s {to_edit.lower()} changed to {new_data}", "bold fg:green")
    

def remove_habit():
    pass

def view_current():
    pass

def analysis():
    pass



def startup_cli():
    running = True

    print_cust("\nWELCOME TO YOUR HABIT TRACKER! \n", "bold fg:cyan")
    name = questionary.text("What should we call you?").ask() 
    print_cust(f"\nWelcome {name}! You are one step closer to healthy habits!")
    demo_data_check(name)
    menu_option = main_menu()
    
    while running:
        if "1" in menu_option:
            log_habit()
            menu_option = main_menu()
        elif "2" in menu_option:
            create_new_habit(name)
            menu_option = main_menu()
        elif "3" in menu_option:
            edit_habit()
            menu_option = main_menu()
        elif "4" in menu_option:
            remove_habit()
            menu_option = main_menu()
        elif "5" in menu_option:
            view_current()
            menu_option = main_menu()
        elif "6" in menu_option:
            analysis()
            menu_option = main_menu()
        elif "7" in menu_option:
            print_cust("Goodbye, see you soon!\n")
            exit_cli()




if __name__ == "__main__":
    startup_cli()