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

    def test_habit(self):
        #tests Habit, store_habit, retrieve_all
        habit = Habit(None, "Test", "Test", "test",  "test", date.today().strftime("%Y%m%d"))
        habit.store_habit(self.db)
        habits, headers = retrieve_all(self.db, "habit")
        assert len(habits) == 1

    def test_sample_data(self):
        #Tests sample_data addition
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

    def test_streak(self):
        pass
    
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
    #Removed from class due to db removed before all tests were asserted
    os.remove("test.db")

# NOTE: For the scope of this project, all other functionality was tested in a modular fashion in-line during code creation.