import questionary
import os
from db import get_db, create_tables
from sample_data import add_sample_data



def print_cust(text, style="bold"):
    return questionary.print(text, style = style)
def new_con():
    os.system('clear')



def startup_cli():
    db = get_db("habit_tracker.db")
    create_tables(db)

    print_cust("\nWELCOME TO YOUR HABIT TRACKER! \n", "bold fg:cyan")
    name = questionary.text("What should we call you?").ask() 
    print_cust(f"\nWelcome {name}! You are one step closer to healthy habits!")
    demo_data = questionary.select("Would you like to load the available demo data?", choices=["Yes","No thanks"]).ask()
    if demo_data == "Yes":
        add_sample_data(db)
    print_cust("\n****MAIN MENU****\n", "bold fg:cyan")
    menu_option = questionary.select("What would you like to do today?\n", 
                                     choices=["1. Log a Habit",
                                              "2. Add a New Habit", 
                                              "3. Edit Habit", 
                                              "4. Remove Habit", 
                                              "5. View Current Habits",
                                              "6. Exit"]).ask()
    print(menu_option)




if __name__ == "__main__":
    startup_cli()