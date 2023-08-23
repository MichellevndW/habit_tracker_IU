import questionary
from db import retrieve_all, retrieve_one, get_db
import plotext as ptx
from datetime import date
import re

db = get_db("habit_tracker.db")
def print_cust(text, style="bold"):
    return questionary.print(text, style = style)

def view_habits():
    all_data, headers = retrieve_all(db, 'habit')
    for data in all_data:
        if data[1] != "DEMO_DATA":
            if data[2] and data[2] != "" and data[2] != " ":
                description = data[2].capitalize()
            else:
                description = "No Description"
            date_edited = re.sub("[^0-9]","",data[5])
            date_edited = date(int(date_edited[0:4]), int(date_edited[4:6]), int(date_edited[6:8])).strftime("%d %B %Y")
            print_cust(f"\n**Habit {data[0]}**\nHabit Name: {data[1].capitalize()}\nDescription:{description}\nInterval: {data[3].capitalize()}\nCategory: {data[4].capitalize()}\nDate Added: {date_edited}\n")
    back_to_main = questionary.select("Back to main menu?", choices=["Yes"]).ask()
    return back_to_main

def view_streaks_all():
    all_habit_data, headers = retrieve_all(db, 'habit')
    all_streak_data, headers = retrieve_all(db, "streak")
    habit_names = []
    longest_streaks = []
    current_streaks = []
    for habit in all_habit_data:
        if habit[1] != "DEMO_DATA":
            habit_names.append(habit[1].capitalize())
        for streak in all_streak_data:
            if streak[0] == habit[0]:
                longest_streaks.append(int(streak[3]))
                current_streaks.append(int(streak[1]))
    ptx.clear_data()
    ptx.multiple_bar(habit_names, [current_streaks, longest_streaks])
    ptx.xlabel("Habit. Current Streak, Longest Streak")
    ptx.title("All Habit Streaks")
    ptx.show()
    print("\n\n")
    back_to_main = questionary.select("\nBack to main menu?", choices=["Yes"]).ask()

def view_streak_single(habit_id):
    habit_data, headers = retrieve_one(db, "habit", habit_id)
    streak_data, headers = retrieve_one(db, "streak", habit_id)
    habit_name = [habit_data[0][1], "", "", ""]
    longest_streak = [int(streak_data[0][3]), 0, 0, 0]
    current_streak = [int(streak_data[0][1]), 0, 0, 0]
    title = f"Habit Streaks for {habit_data[0][1].capitalize()}"
    ptx.clear_data()
    ptx.multiple_bar(habit_name, [current_streak, longest_streak])
    ptx.xlabel("Habit - Current Streak, Longest Streak")
    ptx.title(title)
    ptx.show()
    print("\n\n")
    back_to_main = questionary.select("\nBack to main menu?", choices=["Yes"]).ask()

def view_longest_streak():
    streak_data, headers = retrieve_all(db, "streak")
    longest_streak = None
    for streak in streak_data:
        if longest_streak:
            if int(streak[3]) > longest_streak:
                longest_streak = int(streak[3])
        else:
            longest_streak = int(streak[3])
    habit_ids = []
    for streak in streak_data:
        if longest_streak != 0:
            if int(streak[3]) == longest_streak:
                habit_ids.append(streak[0])
    habit_data = []
    for id in habit_ids:
        habit, headers = retrieve_one(db, "habit", id)
        habit_data.append(habit)
    print_cust("\n**View Longest Streak**", "bold fg: cyan")
    for habit in habit_data:
        print_cust(f"\n**Habit ID: {habit[0][0]}**\nHabit name: {habit[0][1].capitalize()}\nInterval: {habit[0][3].capitalize()}\nLongest streak: {longest_streak}\n", 
                    "bold fg:green")
    back_to_main = questionary.select("Back to main menu?", choices=["Yes"]).ask()

def streak_broken():
    print_cust("\n**Broken Streaks**", "bold fg: cyan")
    all_streak_data, headers = retrieve_all(db, "streak")
    for streak in all_streak_data:
        habit, headers = retrieve_one(db, "habit", streak[0])
        broken_streaks = list(streak[2].split(", "))
        print_cust("\n-----------------------------------", "bold fg:green")
        print_cust(f"*ID: {streak[0]}*\nHabit Name: {habit[0][1].capitalize()}\n")
        if broken_streaks[0] != "" and broken_streaks and broken_streaks[0] != " ":
            broken_times = len(broken_streaks)
        else:
            broken_times = 0
        print_cust(f"Times Streak Was Broken: {broken_times}")
        print_cust("\nDates your streak was reset: ")
        for broken_streak in broken_streaks:
            if broken_streak != "" and broken_streak != None and broken_streak != " ":
                broken_streak = date(int(broken_streak[0:4]), int(broken_streak[4:6]), int(broken_streak[6:8])).strftime("%d %B %Y")
                print_cust(broken_streak)
            else:
                print_cust("**Streak has never been broken**", "bold fg: pink")
        print("\n")
        next = questionary.select("Next habit", choices=["next"]).ask()
    print("\n")
    back_to_main = questionary.select("Back to main menu?", choices=["Yes"]).ask()

def view_daily():
    print_cust("\n**View Daily Habits**", "bold fg:cyan")
    all_habits,headers = retrieve_all(db, "habit")
    all_daily_habits = []
    print(len(all_daily_habits))
    for habit in all_habits:
        if habit[3].lower() == "daily":
            all_daily_habits.append(habit)
    if len(all_daily_habits) > 0:        
        for habit in all_daily_habits:
            date_added = habit[5]
            date_clean = re.sub("[^0-9]","",date_added)
            date_added = date(int(date_clean[0:4]), int(date_clean[4:6]), int(date_clean[6:8])).strftime("%d %B %Y")
            print_cust(f"\n**Habit {habit[0]}**\nHabit Name: {habit[1].capitalize()}\nDescription:{habit[2].capitalize()}\nInterval: {habit[3].capitalize()}\nCategory: {habit[4].capitalize()}\nDate Added: {date_added}\n")
    else:
        print_cust("No active daily habits")
    back_to_main = questionary.select("Back to main menu?", choices=["Yes"]).ask()

def view_weekly():
    print_cust("\n**View Weekly Habits**", "bold fg:cyan")
    all_habits,headers = retrieve_all(db, "habit")
    all_weekly_habits = []
    for habit in all_habits:
        if habit[3].lower() == "weekly":
            all_weekly_habits.append(habit)
    if len(all_weekly_habits) > 0:        
        for habit in all_weekly_habits:
            date_added = habit[5]
            date_clean = re.sub("[^0-9]","",date_added)
            date_added = date(int(date_clean[0:4]), int(date_clean[4:6]), int(date_clean[6:8])).strftime("%d %B %Y")
            print_cust(f"\n**Habit {habit[0]}**\nHabit Name: {habit[1].capitalize()}\nDescription:{habit[2].capitalize()}\nInterval: {habit[3].capitalize()}\nCategory: {habit[4].capitalize()}\nDate Added: {date_added}\n")
    else:
        print_cust("\nNo active weekly habits")
    back_to_main = questionary.select("Back to main menu?", choices=["Yes"]).ask()

def view_monthly():
    print_cust("\n**View Monthly Habits**", "bold fg:cyan")
    all_habits,headers = retrieve_all(db, "habit")
    all_monthly_habits = []
    for habit in all_habits:
        if habit[3].lower() == "monthly":
            all_monthly_habits.append(habit)
    if len(all_monthly_habits) > 0:        
        for habit in all_monthly_habits:
            date_added = habit[5]
            date_clean = re.sub("[^0-9]","",date_added)
            date_added = date(int(date_clean[0:4]), int(date_clean[4:6]), int(date_clean[6:8])).strftime("%d %B %Y")
            print_cust(f"\n**Habit {habit[0]}**\nHabit Name: {habit[1].capitalize()}\nDescription:{habit[2].capitalize()}\nInterval: {habit[3].capitalize()}\nCategory: {habit[4].capitalize()}\nDate Added: {date_added}\n")
    else:
        print_cust("\nNo active monthly habits")
    back_to_main = questionary.select("Back to main menu?", choices=["Yes"]).ask()
