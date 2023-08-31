import os
from db import get_db, create_tables, retrieve_all, retrieve_one, edit_tracker, edit_habit_db
from habit import Habit
from datetime import date
from sample_data import add_sample_data
from tracker import Tracker
from streak import Streak

class TestCode:

    def setup_method(self):
        #Tests db creation and create_tables
        self.db = get_db("test.db")
        create_tables(self.db)

    def test_sample_data(self):
        #Tests sample_data addition, including streak calculation
        add_sample_data(self.db)
        habits, headers = retrieve_all(self.db, "habit")
        assert len(habits) > 1
        assert len(headers) > 1
        trackers, headers = retrieve_all(self.db, "tracker")
        assert len(trackers) > 1
        assert len(headers) > 1
        streaks, headers = retrieve_all(self.db, "streak")
        assert len(streaks) > 1
        assert len(headers) > 1

    def test_habit(self):
        #tests Habit, store_habit, retrieve_all
        habits_before, headers = retrieve_all(self.db, "habit")
        habits_before = len(habits_before)
        habit = Habit(None, "Test", "Test", "test",  "test", date.today().strftime("%Y%m%d"))
        habit.store_habit(self.db)
        habits, headers = retrieve_all(self.db, "habit")
        assert len(habits) == habits_before + 1

    def test_streak(self):
        #Tests current streak and longest streak calculations as well as streak broken dates
        streak_data, headers = retrieve_one(self.db, "streak", 2) 
        current_broken_streaks = len(streak_data[0][2])
        #Adds a tracker more than one day from last daily demo data
        description = "test_streak"
        notes = ""
        track = Tracker(2, None, description, "20230829", notes )
        track.store_tracker(self.db)
        data_pushed, headers = retrieve_all(self.db, "tracker", 2, no_order=True)
        data_pushed = data_pushed[-1]
        track.tracker_id = data_pushed[0]
        trackers_ob_date, headers = retrieve_all(self.db, "tracker", 2)
        index = trackers_ob_date.index(data_pushed)
        if index != 0:
            previous_data = trackers_ob_date[(index-1)]
        else:
            previous_data = None    
        streak = Streak(data_pushed[1])
        streak.push_streak_one(self.db, data_pushed, previous_data)
        new_streak, headers = retrieve_one(self.db, "streak", 2)
        #Ensure current streak is reset
        assert int(new_streak[0][1]) == 0
        #Ensure date is added to streak_broken (+10 chars)
        assert len(new_streak[0][2]) == current_broken_streaks + 10

        #Add another tracker 1 day after previous
        description = "test_streak_2"
        notes = ""
        track = Tracker(2, None, description, "20230830", notes )
        track.store_tracker(self.db)
        data_pushed, headers = retrieve_all(self.db, "tracker", 2, no_order=True)
        data_pushed = data_pushed[-1]
        track.tracker_id = data_pushed[0]
        trackers_ob_date, headers = retrieve_all(self.db, "tracker", 2)
        index = trackers_ob_date.index(data_pushed)
        if index != 0:
            previous_data = trackers_ob_date[(index-1)]
        else:
            previous_data = None    
        streak = Streak(data_pushed[1])
        streak.push_streak_one(self.db, data_pushed, previous_data)
        new_streak, headers = retrieve_one(self.db, "streak", 2)
        #Check that current streak is updated accordingly
        assert int(new_streak[0][1]) == 1
        
        current_streak_data, headers = retrieve_one(self.db, "streak", 5)
        list_dates = ["20230801","20230802","20230803","20230804","20230805","20230806","20230807","20230808",
                      "20230809","20230810","20230811","20230812","20230813","20230814","20230815","20230816" ]
        for i in range(16):
            track = Tracker(5, None, description, list_dates[i-1], notes)
            track.store_tracker(self.db)
            data_pushed, headers = retrieve_all(self.db, "tracker", 5, no_order=True)
            data_pushed = data_pushed[-1]
            track.tracker_id = data_pushed[0]
            trackers_ob_date, headers = retrieve_all(self.db, "tracker", 5)
            index = trackers_ob_date.index(data_pushed)
            if index != 0:
                previous_data = trackers_ob_date[(index-1)]
            else:
                previous_data = None    
            streak = Streak(data_pushed[1])
            streak.push_streak_one(self.db, data_pushed, previous_data)
        new_streak_data, headers = retrieve_one(self.db, "streak", 5)
        #Check that longest_streak data is replaced
        assert int(current_streak_data[0][3]) < int(new_streak_data[0][3])
        #Check that longest_streak data is correct
        assert int(new_streak_data[0][3]) == 15

    def test_tracker(self):
        #Tests Tracker, store_tracker, delete_single_tracker, delete_all_trackers retrieve_all(db)
        tracker = Tracker(1, None, "description_test_tracker", "20230506", None)
        tracker.store_tracker(self.db)
        trackers, headers = retrieve_all(self.db, "tracker")
        exists = False
        for track in trackers:
            if track[2] == "description_test_tracker":
                exists = True
                tracker.tracker_id = track[0]
        assert exists
        tracker.delete_single_tracker(self.db)
        trackers, headers = retrieve_all(self.db, "tracker")
        exists = False
        for track in trackers:
            if track[2] == "description_test_tracker":
                exists = True
        assert exists == False
        tracker.delete_all_trackers(self.db)
        trackers, headers = retrieve_all(self.db, "tracker")
        for track in trackers:
            if track[1] == tracker.habit_id:
                exists = True
            else:
                exists = False
        assert exists == False
    
    def test_db_functions(self):
        #Tests edit tracker, retrieve_one, retrieve all
        edit_tracker(self.db, "notes", "'New pillow'", 60 )
        tracker, headers = retrieve_one(self.db, "tracker", 60)
        print(tracker)
        assert tracker[0][4] == "New pillow"
        edit_habit_db(self.db, "description", "'test_descr'", 4)
        habit, headers = retrieve_one(self.db, "habit", 4)
        assert habit[0][2] == "test_descr"
        habits = retrieve_all(self.db, "habit")
        assert len(habits) >= 1


def test_teardown_method():
    #Deletes test.db
    #Removed from class due to db removed before all tests were asserted
    #To view data in database, comment out this function
    os.remove("test.db")

# NOTE: For the scope of this project, all other functionality was tested in a modular fashion in-line during code creation.