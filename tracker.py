from db import get_db, add_tracker, remove_single_tracker, remove_all_trackers
import re

db = get_db("habit_tracker.db")

class Tracker:
    def __init__(self, habit_id:int, tracker_id:int, description:str, date_tracked:str, notes:str):
        date_tracked = str(date_tracked)
        date_tracked = re.sub("[^0-9]","",date_tracked)
        self.habit_id = habit_id
        self.tracker_id = tracker_id
        self.description = description
        self.date_tracked = date_tracked
        self.notes = notes

    
    def store_tracker(self, db):
        add_tracker(db, self.habit_id, self.description, self.date_tracked, self.notes)

    def delete_single_tracker(self, db):
        remove_single_tracker(db, self.tracker_id)
    
    def delete_all_trackers(self, db):
        remove_all_trackers(db, self.habit_id)

