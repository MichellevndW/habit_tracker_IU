import questionary
from db import retrieve_all, retrieve_one, get_db
import plotext as ptx

db = get_db("habit_tracker.db")
def print_cust(text, style="bold"):
    return questionary.print(text, style = style)

def view_habits():
    all_data, headers = retrieve_all(db, 'habit')
    for data in all_data:
        if data[1] != "DEMO_DATA":
            print_cust(f"\n**Habit {data[0]}**\nHabit Name: {data[1].capitalize()}\nDescription:{data[2].capitalize()}\nInterval: {data[3].capitalize()}\nCategory: {data[4].capitalize}\nDate Added: {data[5]}\n")
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
    print(habit_data)
    print_cust("***View Longest Streak***", "bold fg: cyan")
    for habit in habit_data:
        print_cust(f"\n**Habit ID: {habit[0][0]}**\nHabit name: {habit[0][1].capitalize()}\nLongest streak: {longest_streak}", 
                    "bold fg:green")
    back_to_main = questionary.select("\nBack to main menu?", choices=["Yes"]).ask()