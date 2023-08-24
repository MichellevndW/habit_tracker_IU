from db import get_db, add_habit, retrieve_all
from streak import Streak

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
        """
        Function to store habit to the Database
        :param db: Database where habit should be stored
        """
        add_habit(db, name=self.name, description=self.description, 
                  interval=self.interval, category=self.category, date_added=self.date_added)
        habits, headers = retrieve_all(db, "habit")
        self.habit_id = habits[-1][0]
        streak = Streak(self.habit_id, 0, "", 0)
        streak.store_streak(db)
    
