class Habit:
    def __init__(self, habit_id:str, name:str, description:str, interval:str, category:str, date_added:str ):
        self.habit_id = habit_id
        self.name = name
        self.description = description
        self.interval = interval
        self.category = category
        self.date_added = date_added
    