import sqlite3
import re
import questionary

def get_db(name):
    db = sqlite3.connect(name)
    return db

def print_cust(text, style="bold"):
    return questionary.print(text, style = style)

def create_tables(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        interval TEXT,
        category TEXT,
        date_added TEXT 
        )
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS tracker(
        tracker_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER, 
        description TEXT,
        date_tracked TEXT,
        notes TEXT,
        FOREIGN KEY(habit_id) REFERENCES habit(id)
        )
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS streak(
        habit_id INTEGER,
        current_streak TEXT,
        streak_broken TEXT,
        longest_streak TEXT,
        FOREIGN KEY(habit_id) REFERENCES habit(id)
        )
        """)
    
    db.commit()

def add_habit(db, name, interval, category, date_added, description=None):
    cur = db.cursor()
    if name and interval and category and date_added:
        cur.execute("INSERT INTO habit VALUES (null,?,?,?,?,?)", 
                    ( name, description, interval, category, date_added))
        db.commit()
        print_cust(f"\nNew {interval} {name} habit created.", "bold fg:green")
    else:
        print_cust("\n***HABIT NOT ADDED, all required fields not entered. Please try again***", "bold fg:red")
    

def add_tracker(db,habit_id, description, date_tracked, notes=None):
    #TODO - ensure habit_id exists in habit table - perhaps do this in app level
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (null,?,?,?,?)", 
                ( habit_id, description, (re.sub("[^0-9]","",date_tracked)), notes))
    db.commit()

def add_streak(db,habit_id, current_streak, streak_broken, longest_streak):
    #TODO - ensure habit_id exists in habit table - perhaps do this in app level
    cur = db.cursor()
    cur.execute("INSERT INTO streak VALUES (?,?,?,?)", 
                (habit_id, current_streak, streak_broken, longest_streak))
    db.commit()

def edit_habit_db(db, prop, new_value, habit_id):
    cur = db.cursor()
    to_update = f"UPDATE habit SET {prop} = {new_value} WHERE id = {habit_id};"
    cur.execute(to_update)
    db.commit()

def edit_streak(db, prop, new_value, habit_id):
    cur = db.cursor()
    to_update = f"UPDATE streak SET {prop} = {new_value} WHERE habit_id = {habit_id};"
    cur.execute(to_update)
    db.commit()

def edit_tracker(db, prop, new_value, tracker_id):
    cur = db.cursor()
    to_update = f"UPDATE tracker SET {prop} = {new_value} WHERE tracker_id = {tracker_id};"
    cur.execute(to_update)
    db.commit()

def remove_habit(db, habit_id):
    cur = db.cursor()
    to_delete = [f"DELETE FROM habit WHERE id = {habit_id}", 
                 f"DELETE FROM tracker WHERE habit_id = {habit_id}", 
                 f"DELETE FROM streak WHERE habit_id = {habit_id}"]
    for item in to_delete:
        cur.execute(item)
    db.commit()

def remove_streak(db, habit_id):
    cur = db.cursor()
    to_delete = f"DELETE FROM streak WHERE habit_id = {habit_id}"
    cur.execute(to_delete)
    db.commit()

def remove_single_tracker(db, tracker_id):
    cur = db.cursor()
    to_delete = f"DELETE FROM tracker WHERE tracker_id = {tracker_id}"
    cur.execute(to_delete)
    db.commit()

def remove_all_trackers(db, habit_id):
    cur = db.cursor()
    to_delete = f"DELETE FROM tracker WHERE habit_id = {habit_id}"
    cur.execute(to_delete)
    db.commit()

def retrieve_all(db, table_name, habit_id=None, no_order=False):
    cur = db.cursor()
    if table_name == "habit":
        to_retrieve = f"SELECT * FROM habit"
    elif table_name == "tracker" and habit_id != None and no_order == False:
        to_retrieve = f"SELECT * FROM {table_name} WHERE habit_id = {habit_id} ORDER BY date_tracked ASC"
    elif table_name == "tracker" and no_order == True:
        to_retrieve = f"SELECT * FROM {table_name}"
    elif table_name == "tracker":
        to_retrieve = f"SELECT * FROM {table_name} ORDER BY date_tracked ASC"
    elif habit_id != None:
        to_retrieve = f"SELECT * FROM {table_name} WHERE habit_id = {habit_id}"
    else:
        to_retrieve = f"SELECT * FROM {table_name}"
    data = cur.execute(to_retrieve)
    results = cur.fetchall()
    headers = []
    for column in data.description:
        headers.append(column[0])
    return results, headers

def retrieve_one(db, table_name, id, special=None, special_value=None):
    cur = db.cursor()
    if special:
        to_retrieve = f"SELECT * FROM {table_name} WHERE {special} = {special_value}"
    else:
        if table_name == "habit":
            to_retrieve = f"SELECT * FROM habit WHERE id = {id}"
        elif table_name == "tracker":
            to_retrieve = f"SELECT * FROM tracker WHERE tracker_id = {id}"
        else:
            to_retrieve = f"SELECT * FROM streak WHERE habit_id = {id}"
    data = cur.execute(to_retrieve)
    headers = []
    for column in data.description:
        headers.append(column[0])
    results = cur.fetchall()
    return results, headers

#Test--------------------------------------->
#TODO test retrieve funct with non manual data entry

db = get_db("habit_tracker.db")
# create_tables(db)
# add_habit(db, "ok", "monthly", "category", "date_added", None)
# add_tracker(db, 1, "balbal", "datehere", "notes")

