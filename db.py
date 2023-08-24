import sqlite3
import re
import questionary

def get_db(name):
    db = sqlite3.connect(name)
    return db

def print_cust(text, style="bold"):
    """
    To print in custom styles for better user experience
    :param text: Text that has to be printed
    :param style: Any custom style
    :return questionary print statement
    """
    return questionary.print(text, style = style)

def create_tables(db):
    """
    Function to create habit, tracker and streak tables in the database
    :param db: Database where tables should be created
    """
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
    """
    Function to add a habit to the habit table
    :param db: Database where data should be stored
    :param name: Name of habit (str)
    :param interval: Interval of habit (str)
    :param category: Category of habit (str)
    :param date_added: Date habit was created (str)
    :param description: Description of habit (str)
    """
    cur = db.cursor()
    if name and interval and category and date_added:
        cur.execute("INSERT INTO habit VALUES (null,?,?,?,?,?)", 
                    ( name, description, interval, category, date_added))
        db.commit()
        print_cust(f"\nNew {interval} {name} habit created.", "bold fg:green")
    else:
        print_cust("\n***HABIT NOT ADDED, all required fields not entered. Please try again***", "bold fg:red") 

def add_tracker(db,habit_id, description, date_tracked, notes=None):
    """
    Function to add a tracker to the tracker table
    :param db: Database were tracker should be stored
    :param habit_id: ID of habit that is logged (int)
    :param description: Description of tracked event (str)
    :param date_tracked: Date when habit was logged/tracked (str)
    :param notes: Any notes the user may have on the tracked event (str)
    """
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (null,?,?,?,?)", 
                ( habit_id, description, (re.sub("[^0-9]","",date_tracked)), notes))
    db.commit()

def add_streak(db,habit_id, current_streak, streak_broken, longest_streak):
    """
    Function to add a streak to the streak table
    :param db: Database where data should be stored
    :param habit_id: Id of the habit the streak is connected to (int)
    :param current_streak: Current streak of the habit (str)
    :param streak_broken: List of dates where streak was reset (str)
    :param longest_streak: Longest streak of the chosen habit (str)
    """
    cur = db.cursor()
    cur.execute("INSERT INTO streak VALUES (?,?,?,?)", 
                (habit_id, current_streak, streak_broken, longest_streak))
    db.commit()

def edit_habit_db(db, prop, new_value, habit_id):
    """
    Function to edit habit in the habit table
    :param db: Database where data should be edited
    :param prop: Property that should be edited
    :param new_value: New value that should be stored
    :param habit_id: ID of the habit to be edited
    """
    cur = db.cursor()
    to_update = f"UPDATE habit SET {prop} = {new_value} WHERE id = {habit_id};"
    cur.execute(to_update)
    db.commit()

def edit_streak(db, prop, new_value, habit_id):
    """
    Function to edit a streak in the streak table
    :param db: Database where streak should be edited
    :param prop: Property to be edited
    :param new_value: New value to be stored
    :param habit_id: ID of the habit the streak is connected to
    """
    cur = db.cursor()
    to_update = f"UPDATE streak SET {prop} = {new_value} WHERE habit_id = {habit_id};"
    cur.execute(to_update)
    db.commit()

def edit_tracker(db, prop, new_value, tracker_id):
    """
    Function to edit a tracker in the tracker table
    :param db: Database where tracker should be edited
    :param prop: Property that should be edited
    :param new_value: New value that should be stored
    :param tracker_id: ID of the tracker that should be edited
    """
    cur = db.cursor()
    to_update = f"UPDATE tracker SET {prop} = {new_value} WHERE tracker_id = {tracker_id};"
    cur.execute(to_update)
    db.commit()

def remove_habit(db, habit_id):
    """
    Function to remove a habit from the habit table
    :param db: Database where habit should be removed
    :param habit_id: ID of the habit to be removed
    """
    cur = db.cursor()
    to_delete = [f"DELETE FROM habit WHERE id = {habit_id}", 
                 f"DELETE FROM tracker WHERE habit_id = {habit_id}", 
                 f"DELETE FROM streak WHERE habit_id = {habit_id}"]
    for item in to_delete:
        cur.execute(item)
    db.commit()

def remove_streak(db, habit_id):
    """
    Function to remove a streak from the streak table
    :param db: Database where streak should be removed from
    :param habit_id: ID of the habit the streak is connected to
    """
    cur = db.cursor()
    to_delete = f"DELETE FROM streak WHERE habit_id = {habit_id}"
    cur.execute(to_delete)
    db.commit()

def remove_single_tracker(db, tracker_id):
    """
    Function to remove a single tracker
    :param db: Database where tracker should be removed
    :param tracker_id: ID of the tracker to be removed
    """
    cur = db.cursor()
    to_delete = f"DELETE FROM tracker WHERE tracker_id = {tracker_id}"
    cur.execute(to_delete)
    db.commit()

def remove_all_trackers(db, habit_id):
    """
    Function to remove all trackers connected to a specific habit
    :param db: Database where trackers should be removed
    :param habit_id: ID of the habit the trackers are connected to
    """
    cur = db.cursor()
    to_delete = f"DELETE FROM tracker WHERE habit_id = {habit_id}"
    cur.execute(to_delete)
    db.commit()

def retrieve_all(db, table_name, habit_id=None, no_order=False):
    """
    Function to retrieve all data from a table in the database
    :param db: Database where data should be retrieved from
    :param table_name: Name of the table 
    :param habit_id: ID of the habit where applicable
    :param no_order: Set to True for tracker data to be ordered by date
    :return results, headers: Results - dataset retrieved, Headers- Headers of the table

    """
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
    """
    Function to retrieve a single data set from a table in the database
    :param db: Database where data should be retrieved from
    :param table_name: Name of the table data can be found
    :param id: Id of the item to be retrieved
    :param special: Property of any special enquiries
    :param special_value: Value of a special enquiry
    :return results, headers: Results - dataset retrieved, Headers- Headers of the table
    """
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


