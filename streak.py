from habit import Habit

class Streak:
    def __init__(self, habit_id:int, current_streak:int , streak_broken: str, longest_streak:int):
        self.habit_id = habit_id
        self.current_streak = current_streak
        self.streak_broken = streak_broken
        self.longest_streak = longest_streak
