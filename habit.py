from db import get_db, add_habit, remove_habit
from datetime import date

db = get_db("habit_tracker.db")

class Habit:
    def __init__(self, habit_id:str, name:str, description:str, interval:str, category:str, date_added:str ):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.interval = interval
        self.category = category
        self.date_added = date_added
    
    def store_habit(self, db):
        add_habit(db, name=self.name, description=self.description, 
                  interval=self.interval, category=self.category, date_added=self.date_added)
    
    def delete_habit(self, db):
        remove_habit(db, self.habit_id)
