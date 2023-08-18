import sqlite3

def get_db(name):
    db = sqlite3.connect(name)
    return db

def create_tables(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit(
        id TEXT PRIMARY KEY,
        name TEXT,
        description TEXT,
        interval TEXT,
        category TEXT,
        date_added TEXT 
        )
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS tracker(
        habit_id TEXT, 
        tracker_id TEXT PRIMARY KEY,
        description TEXT,
        date_tracked TEXT,
        notes TEXT,
        FOREIGN KEY(habit_id) REFERENCES habit(id)
        )
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS streak(
        habit_id TEXT,
        current_streak TEXT,
        streak_broken TEXT,
        longest_streak TEXT,
        FOREIGN KEY(habit_id) REFERENCES habit(id)
        )
        """)
    
    db.commit()

def add_habit(db, id, name, interval, category, date_added, description=None):
    cur = db.cursor()
    cur.execute("INSERT INTO habit VALUES (?,?,?,?,?,?)", 
                (id, name, description, interval, category, date_added))
    db.commit()

def add_tracker(db,habit_id,tracker_id, description, date_tracked, notes=None):
    #TODO - ensure habit_id exists in habit table - perhaps do this in app level
    cur = db.cursor()
    cur.execute("INSERT INTO tracker VALUES (?,?,?,?,?)", 
                (habit_id, tracker_id, description, date_tracked, notes))
    db.commit()

def add_streak(db,habit_id, current_streak, streak_broken, longest_streak):
    #TODO - ensure habit_id exists in habit table - perhaps do this in app level
    cur = db.cursor()
    cur.execute("INSERT INTO streak VALUES (?,?,?,?)", 
                (habit_id, current_streak, streak_broken, longest_streak))
    db.commit()

def edit_habit(db, prop, new_value, habit_id):
    cur = db.cursor()
    to_update = f"UPDATE habit SET {prop} = {new_value} WHERE id = {habit_id}"
    cur.execute(to_update)
    db.commit()

def edit_streak(db, prop, new_value, habit_id):
    cur = db.cursor()
    to_update = f"UPDATE streak SET {prop} = {new_value} WHERE habit_id = {habit_id}"
    cur.execute(to_update)
    db.commit()

def edit_tracker(db, prop, new_value, tracker_id):
    cur = db.cursor()
    to_update = f"UPDATE tracker SET {prop} = {new_value} WHERE tracker_id = {tracker_id}"
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

def retrieve_all(db, table_name, habit_id):
    cur = db.cursor()
    if table_name == "habit":
        to_retrieve = f"SELECT * FROM habit WHERE id = {habit_id}"
    else:
        to_retrieve = f"SELECT * FROM {table_name} WHERE habit_id = {habit_id}"
    data = cur.execute(to_retrieve)
    results = cur.fetchall()
    headers = []
    for column in data.description:
        headers.append(column[0])
    return results, headers

def retrieve_one(db, table_name, id):
    cur = db.cursor()
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


