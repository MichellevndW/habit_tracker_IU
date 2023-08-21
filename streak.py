from db import get_db, add_streak, remove_streak, edit_streak, retrieve_one, retrieve_all
import re
from datetime import date

db = get_db("habit_tracker.db")

class Streak:
    def __init__(self, habit_id:int, current_streak:int=None , streak_broken: str=None, longest_streak:int=None):
        self.habit_id = habit_id
        self.current_streak = current_streak
        self.streak_broken = streak_broken
        self.longest_streak = longest_streak

    def store_streak(self, db):
        add_streak(db, self.habit_id, self.current_streak, self.streak_broken, self.longest_streak)

    def push_streak_all(self, db):
        #TODO get habit data, do calculations and edit streak
        current_streak_data, headers = retrieve_one(db, "streak", self.habit_id)
        all_trackers, headers = retrieve_all(db, "tracker", self.habit_id)
        print(all_trackers)
        habit, headers = retrieve_one(db, "habit", self.habit_id)
        interval = habit[0][3]
        streak_count = 0
        longest_streak = 0
        print("HABIT", habit)
        habit_creation_date = habit[0][5]
        print("HABIT CREATION DATE", habit_creation_date)
        latest_date = re.sub("[^0-9]","",habit_creation_date)
        print("LATEST", latest_date)
        latest_date = date(int(latest_date[0:4]), int(latest_date[4:6]), int(latest_date[6:8]))
        if current_streak_data[0][2] != None and current_streak_data[0][2] != "" and current_streak_data[0][2] != " ":
            streak_broken = list(current_streak_data[0][2].split(","))
            print("here")
        else:
            streak_broken = []
            print("over_here")
        print("streak broken", streak_broken)
        if interval.lower() == "daily":
            for tracker in all_trackers:
                clean_date = re.sub("[^0-9]","",tracker[3])
                tracker_date = date(int(clean_date[0:4]), int(clean_date[4:6]), int(clean_date[6:8]))
                print("tracker date", tracker_date)
                print("latest_date", latest_date)
                if (tracker_date - latest_date).days > 1:
                    streak_broken.append(clean_date)
                    streak_count = 0
                else:
                    streak_count += 1
                    if streak_count > longest_streak:
                        longest_streak = streak_count
                latest_date = tracker_date
        elif interval.lower() == "weekly":
            for tracker in all_trackers:
                clean_date = re.sub("[^0-9]","",tracker[3])
                tracker_date = date(int(clean_date[0:4]), int(clean_date[4:6]), int(clean_date[6:8]))
                if (tracker_date - latest_date).days > 7:
                    streak_broken.append(clean_date)
                    streak_count = 0
                else:
                    streak_count += 1
                    if streak_count > longest_streak:
                        longest_streak = streak_count
                latest_date = tracker_date
        elif interval.lower() == "monthly":
            if latest_date.month in [4,6,9,11]:
                number_of_days = 30
            elif latest_date.month == 2:
                number_of_days = 28
            else:
                number_of_days = 31
            for tracker in all_trackers:
                clean_date = re.sub("[^0-9]","",tracker[3])
                tracker_date = date(int(clean_date[0:4]), int(clean_date[4:6]), int(clean_date[6:8]))
                if (tracker_date - latest_date).days > number_of_days:
                    streak_broken.append(clean_date)
                    streak_count = 0
                else:
                    streak_count += 1
                    if streak_count > longest_streak:
                        longest_streak = streak_count
                latest_date = tracker_date

        self.longest_streak = f"'{str(longest_streak)}'"
        self.current_streak = f"'{str(streak_count)}'"
        streak_broken_str = ""
        for streak in streak_broken:
            if streak_broken_str == "":
                streak_broken_str += streak
            else:
                streak_broken_str += f", {streak}"
        print(streak_broken_str)
        self.streak_broken = f"'{streak_broken_str}'"    
       
        edit_streak(db, "longest_streak", self.longest_streak, self.habit_id)
        edit_streak(db, "current_streak", self.current_streak, self.habit_id)
        edit_streak(db, "streak_broken", self.streak_broken, self.habit_id)

    def push_streak_one(self, db, track_data, previous_data):
        habit, headers = retrieve_one(db, "habit", self.habit_id)
        interval = habit[0][3]
        tracker_date = track_data[3]
        tracker_date = date(int(tracker_date[0:4]), int(tracker_date[4:6]), int(tracker_date[6:8]))
        streak, headers = retrieve_one(db, "streak", self.habit_id)
        if streak[0][1] != None and streak[0][1] != "":
            current_streak = int(streak[0][1])
            streak_broken = list(streak[0][2].split(", "))
            longest_streak = int(streak[0][3])
        else:
            current_streak = 0
            streak_broken = []
            longest_streak = 0
        if previous_data:
            previous_date = previous_data[3]
            print("PREVIOUS", previous_data)
            latest_date = date(int(previous_date[0:4]), int(previous_date[4:6]), int(previous_date[6:8]))
        else:
            previous_date = re.sub("[^0-9]","",habit[0][5])
            latest_date = date(int(previous_date[0:4]), int(previous_date[4:6]), int(previous_date[6:8]))
        
        if interval.lower() == "daily":
            if (tracker_date - latest_date).days > 1:
                streak_broken.append(track_data[3])
                current_streak = 0
            else:
                current_streak += 1

        elif interval.lower() == "weekly":
            if (tracker_date - latest_date).days > 1:
                streak_broken.append(track_data[3])
                current_streak = 0
            else:
                current_streak += 1
        elif interval.lower() == "monthly":
            if latest_date.month in [4,6,9,11]:
                number_of_days = 30
            elif latest_date.month == 2:
                number_of_days = 28
            else:
                number_of_days = 31
            if (tracker_date - latest_date).days > number_of_days:
                streak_broken.append(track_data[3])
                current_streak = 0
            else:
                current_streak += 1
        if current_streak > longest_streak:
            longest_streak = current_streak
        
        self.longest_streak = f"'{str(longest_streak)}'"
        self.current_streak = f"'{str(current_streak)}'"
        streak_broken_str = ""
        for streak in streak_broken:
            if streak_broken_str == "":
                streak_broken_str += streak
            else:
                streak_broken_str += f", {streak}"
        print(streak_broken_str)
        self.streak_broken = f"'{streak_broken_str}'"    
        edit_streak(db, "longest_streak", self.longest_streak, self.habit_id)
        edit_streak(db, "current_streak", self.current_streak, self.habit_id)
        edit_streak(db, "streak_broken", self.streak_broken, self.habit_id)

    def delete_streak(db, self):
        remove_streak(db, self.habit_id)