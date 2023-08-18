from habit import Habit

class Tracker:
    def __init__(self, habit_id:int, tracker_id:int, date_tracked:str, notes:str):
        self.habit_id = habit_id
        self.tracker_id = tracker_id
        self.date_tracked = date_tracked
        self.notes = notes

