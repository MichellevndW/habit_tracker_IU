import questionary
import os
import sys
import re
from datetime import date
from analyse import view_habits, view_longest_streak, view_streaks_all, view_streak_single
from analyse import streak_broken, view_daily, view_weekly, view_monthly
from tracker import Tracker
from habit import Habit
from streak import Streak
from db import get_db,create_tables,retrieve_all,retrieve_one,edit_habit_db,remove_habit, edit_streak
from sample_data import add_sample_data
from datetime import date

db = get_db("habit_tracker.db")
create_tables(db)

def print_cust(text, style="bold"):
    """
    To print in custom styles for better user experience
    :param text: Text that has to be printed
    :param style: Any custom style
    :return questionary print statement
    """
    return questionary.print(text, style = style)

def new_con():
    """
    To clear terminal for better user experience
    (Replace with pass to disable this functionality)
    """
    os.system('clear')

def check_streaks():
    """
    Function to check if user hasn't logged a habit in time and resets current streak to 0.
    Called in main_menu()
    Disabled for the purpose of this project - uncomment in main_menu() to activate
    """
    streaks, headers = retrieve_all(db, "streak")
    todays_date = date.today()
    for streak in streaks:
        habit, headers = retrieve_one(db, "habit", streak[0])
        interval = habit[0][3]
        print(interval)
        trackers, headers = retrieve_all(db, "tracker", streak[0])
        latest_tracker = trackers[-1]
        date_latest_tracker = date(int(latest_tracker[3][0:4]), int(latest_tracker[3][4:6]), int(latest_tracker[3][6:8]))
        if interval.lower() == "daily":
            if (todays_date - date_latest_tracker).days > 1:
                edit_streak(db, "current_streak", "'0'", streak[0])
        elif interval.lower() == "weekly":
            if (todays_date - date_latest_tracker).days > 7:
                edit_streak(db, "current_streak", "'0'", streak[0])
        elif interval.lower() == "monthly":
            if date_latest_tracker.month in [4,6,9,11]:
                if (todays_date - date_latest_tracker).days > 30:
                    edit_streak(db, "current_streak", "'0'", streak[0])
            elif date_latest_tracker.month == 2:
                if (todays_date - date_latest_tracker).days > 28:
                    edit_streak(db, "current_streak", "'0'", streak[0])
            else:
                if (todays_date - date_latest_tracker).days > 31:
                    edit_streak(db, "current_streak", "'0'", streak[0])

def exit_cli():
    """Calls to exit terminal"""
    sys.exit()

def main_menu():
    """
    Prints main menu for user selection
    :return: User selected menu option 
    """
    # For purposes of this project, check_streaks() is disabled, to enable, please uncomment
    # check_streaks()
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
    """
    Function to get user input, create and save a new habit to the database
    :param username: User's name from cli input
    """
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
    
def demo_data_check(username):
    """
    Function to: -check if demo data is loaded
                 -ask the user whether they want demo data loaded
                 -call function add_sample_data() to load data if necessary
                 -redirect to create_new_habit if needed
    :param username: User's name from cli input

    """
    demo_loaded = False
    all_data, headers = retrieve_all(db, "habit")
    if all_data:
        for data in all_data:
            if data[1] == "DEMO_DATA":
                demo_loaded = True
    if demo_loaded:
        print_cust("\n--Demo data has already been loaded--")
    else:
        demo_data = questionary.select("Would you like to load the available demo data?", choices=["Yes","No thanks"]).ask()
        if demo_data == "Yes":
            add_sample_data(db)
            print_cust("\nDemo Data Loaded", "bold fg:green")
        else:
            create_new_habit(username)

def get_date_input():
    """
    Gathers manual date input from user and does basic validity checks
    :return: The date that was input as date_input 
    """
    date_correct = False
    while date_correct == False:
        date_input = questionary.text("When would you like to log this habit for? (yyyy mm dd)").ask()
        date_check = re.sub("[^0-9]","",date_input)
        current_year = int(date.today().year)
        current_date = int(date.today().strftime("%Y%m%d"))
    
        if date_check == "":
            print_cust("The date cannot contain letters. Please try again", "bold fg: red")
        elif len(date_check) != 8:
            print_cust("Your date is not in the correct format, please try again", "bold fg: red")
        elif int(date_check[4:6]) > 12 or int(date_check[4:6]) < 1:
            print_cust("There seems to be an error with the month entered, please try again", "bold fg: red")
        elif int(date_check[6:8]) >31 or int(date_check[6:8]) < 1:
            print_cust("There seems to be an error with the day entered, please try again", "bold fg: red")  
        elif int(date_check[0:4]) > current_year or int(date_check[0:4]) < 2020:
            print_cust("Only years between 2020 and the current year can be entered, please try again", "bold fg: red")
        elif int(date_check) > current_date:
            print_cust("Habits cannot be marked complete in the future, please try again", "bold fg: red")
        elif int(date_check[4:6]) in [4, 6, 9, 11]:
            if int(date_check[6:8]) > 30:
                print_cust("There seems to be an error with your date, please try again", "bold fg: red")
            else:
                date_correct = True
        elif int(date_check[4:6]) == 2:
            if int(date_check[6:8]) > 28:
                print_cust("There seems to be an error with your date, please try again", "bold fg: red")
            else:
                date_correct = True
        else:
            date_correct = True
    return date_input

def check_date_exists(chosen_habit):
    """
    Checks if the date entered already exists for the specific habit in the database
    :param chosen_habit: Habit chosen to mark as complete
    :return date input through cli as date_input
    """
    check = True 
    all_tracker_data, headers = retrieve_all(db, "tracker", chosen_habit[0])
    habit_date = re.sub("[^0-9]","",chosen_habit[5])
    while check:
        date_input = get_date_input()
        date_input = re.sub("[^0-9]","",date_input)
        date_exists = False
        for tracker in all_tracker_data:
            if tracker[3] == date_input:
                date_exists = True
                print_cust("\nYou have already logged this habit on this date, please try again", "bold fg:red")
                break
            elif int(date_input) < int(habit_date):
                date_exists = True
                print_cust("\nDate cannot be before habit was created, please try again", "bold fg:red")
                break
            else:
                pass
        if date_exists == False:
            check = False
    return date_input

def log_habit():
    """
    Function to mark a habit as complete or log a tracker for a specific habit.
        -Creates new tracker and streak data in the respective tables
    """
    print_cust("\n***Log Habit***", "bold fg:cyan")
    habits, headers = retrieve_all(db, "habit")
    menu_options = []
    chosen_habit = None
    for habit in habits:
        if habit[1].lower() != "demo_data":
            menu_options.append(f"ID:{habit[0]} Name:{habit[1].capitalize()}")
    menu_option = questionary.select("Which habit would you like to mark as complete?\n", 
                                     choices=menu_options).ask()
    for habit in habits:
        if habit[0] == int(menu_option[3]):
            chosen_habit = habit
    menu_option = questionary.select("Did you complete this habit today?\n", 
                                     choices=["Yes", "No"]).ask()
    if menu_option == "Yes":
        description = questionary.text("Give a brief description: ").ask()
        notes = questionary.text("Add any notes here: ").ask()
        track = Tracker(chosen_habit[0], None, description, date.today(), notes )
        track.store_tracker(db)
        data_pushed, headers = retrieve_all(db, "tracker", track.habit_id, no_order=True)
        data_pushed = data_pushed[-1]
        track.tracker_id = data_pushed[0]
        trackers_ob_date, headers = retrieve_all(db, "tracker", track.habit_id)
        index = trackers_ob_date.index(data_pushed)
        if index != 0:
            previous_data = trackers_ob_date[(index-1)]
        else:
            previous_data = None    
        streak = Streak(data_pushed[1])
        streak.push_streak_one(db, data_pushed, previous_data)
        habit, headers = retrieve_one(db, "habit", data_pushed[1])
        new_con()
        date_clean = re.sub("[^0-9]","",data_pushed[3])
        date_str = date(int(date_clean[0:4]), int(date_clean[4:6]), int(date_clean[6:8])).strftime("%d %b %Y")
        print_cust(f"\n{habit[0][1].capitalize()} habit marked as complete!\nDate: {date_str}", "bold fg:green")
    else:
        date_input = check_date_exists(chosen_habit)
        description = questionary.text("Give a brief description: ").ask()
        notes = questionary.text("Add any notes here: ").ask()
        track = Tracker(chosen_habit[0], None, description, date_input, notes )
        track.store_tracker(db)
        data_pushed, headers = retrieve_all(db, "tracker", track.habit_id, no_order=True)
        data_pushed = data_pushed[-1]
        track.tracker_id = data_pushed[0]
        trackers_ob_date, headers = retrieve_all(db, "tracker", track.habit_id)
        index = trackers_ob_date.index(data_pushed)
        if index != 0:
            previous_data = trackers_ob_date[(index-1)]
        else:
            previous_data = None    
        habit, headers = retrieve_one(db, "habit", data_pushed[1])
        streak = Streak(data_pushed[1])
        streak.push_streak_one(db, data_pushed, previous_data)
        new_con()
        print_cust(f"\n{habit[0][1].capitalize()} habit marked as complete!\nDate: {data_pushed[3]}", "bold fg:green")

def edit_habit():
    """
    Function to edit an already existing habit in the habit table
             - User can not edit habit_id or date_added
             - Only one parameter can be edited per edit_habit()
    """
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
    new_con()
    print_cust(f"\nHabit -{habit_data[0][1].lower()}-'s {to_edit.lower()} changed to {new_data}", "bold fg:green")
    
def delete_habit():
    """
    Function to permanently delete habit data and all related tracker and streak data
        -User is prompted whether they are sure they want to delete as to prevent accidental deletion
    """
    print_cust("\n***Delete Habit***", "bold fg:cyan")
    all_habits, headers = retrieve_all(db, 'habit')
    menu_options = []
    for habit in all_habits:
        if habit[1] != "DEMO_DATA":
            menu_options.append(f"ID:{habit[0]} Name: -{habit[1]}-")
    to_delete = questionary.select("\nWhich habit would you like to delete?\n",
                                   choices=menu_options).ask()
    confirm = questionary.select(f"Are you sure you want to permanently delete habit: -{to_delete}- and all its records?",
                                 choices = ["Yes", "No"]).ask()
    if confirm == "Yes":
        remove_habit(db, int(to_delete[3]))
        new_con()
        print_cust(f"\nHabit {to_delete} permanently deleted", "bold fg:green")

def analysis():
    """
    Function to handle terminal printing, user input and redirection of the analysis menu
    """
    print_cust("\n***Analysis***", "bold fg: cyan")
    menu_option = questionary.select("Please choose an option to view",
                                      choices = ["1. View Current Habits", 
                                                 "2. View Current and Longest Streak - All Habits",
                                                 "3. View Current and Longest Streak - One Habit",
                                                 "4. View Longest Streak",
                                                 "5. View Broken Streaks - All Habits",
                                                 "6. View Daily Habits",
                                                 "7. View Weekly Habits",
                                                 "8. View Monthly Habits"]).ask()
    if menu_option[0] == "1":
        print_cust("\n**View Current Habits**", "bold fg:cyan")
        view_habits()
        new_con()
    elif menu_option[0] == "2":
        view_streaks_all()
        new_con()
    elif menu_option[0] == "3":
        habit_data, headers = retrieve_all(db, "habit")
        menu_options = []
        for habit in habit_data:
            if habit[1] != "DEMO_DATA":
                menu_options.append(f"ID: {habit[0]}. Name: {habit[1].capitalize()}")
        menu_option = questionary.select("Which Habit's Streak would you like to view?\n",
                                         choices = menu_options).ask()
        view_streak_single((int(menu_option[4])))
        new_con()
    elif menu_option[0] == "4":
        view_longest_streak()
        new_con()
    elif menu_option[0] == "5":
        streak_broken()
        new_con()
    elif menu_option[0] == "6":
        view_daily()
        new_con()
    elif menu_option[0] == "7":
        view_weekly()
        new_con()
    elif menu_option[0] == "8":
        view_monthly()
        new_con()
        
def startup_cli():
    """
    Function to continually loop to the main menu until user decides to exit. 
    """
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
            delete_habit()
            menu_option = main_menu()
        elif "5" in menu_option:
            view_habits()
            menu_option = main_menu()
        elif "6" in menu_option:
            analysis()
            menu_option = main_menu()
        elif "7" in menu_option:
            print_cust("Goodbye, see you soon!\n")
            exit_cli()

if __name__ == "__main__":
    startup_cli()