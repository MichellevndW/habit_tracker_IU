from db import get_db, add_streak, remove_streak

db = get_db("habit_tracker.db")

class Streak:
    def __init__(self, habit_id:int, current_streak:int , streak_broken: str, longest_streak:int):
        self.habit_id = habit_id
        self.current_streak = current_streak
        self.streak_broken = streak_broken
        self.longest_streak = longest_streak

    def store_streak(db, self):
        add_streak(db, self.habit_id, self.current_streak, self.streak_broken, self.longest_streak)

    def delete_streak(db, self):
        remove_streak(db, self.habit_id)