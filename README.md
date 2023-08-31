# CLI Habit Tracker

A simple command-line-interface habit tracker, created to be run right in your terminal.  

## Description

Add your own habits, track them and see your streak grow(or break) or choose to use the pre-populated demo data to get a feel for the habit tracker. 
Skip down to the analyse menu to view your habits, see your longest streak or see when your streaks were reset.

## Getting Started

### Requirements

* Python 3.8 or later
* Libraries in requirements.txt

### Installing

* Clone from Github
* Or use: 
```
git clone https://github.com/MichellevndW/habit_tracker_IU.git
```

### Executing program

* Ensure you are in the correct habit_tracker_IU-main directory
* For best results expand the terminal to maximum size
* Run code below and follow the on-screen prompts

```
pip install -r requirements.txt
python3 main.py
```

### Testing/Demo/Sample Data Set

* The app comes with 4 weeks of predefined demo data stored in sample_data.py
* To load this data, execute main.py as above, when prompted whether you want to load the demo data, choose yes.
    * Data can now be viewed in "habit_tracker.db"
* This data set is also used when using pytest on test_habit_tracker.py
    * Testing automatically deletes test.db, comment out the last function called "test_teardown_method" if you want to view the data that was added. 
    * Please note that test_habit_tracker.py does alter this data.

```
pip install -r requirements.txt
python3 main.py
```
or
```
python3 pytest . 
```

### Testing the habit tracker

* Modular testing of the habit tracker was performed during development
* Main functions are tested utilizing pytest
* To run the tests:

```
pip install -r requirements.txt
python3 pytest . 
```

## Future Development

### Possible further improvements for this project:

* User friendly online UX/UI improvement
* User class can be created and user credentials stored for long term persistance and multi-user options
* Further verification e.g. check if a habit name already exists
* Reset tracker functionality
* More analysis options e.g viewing all habits of a category, time between streak breaks, possible connections to streak breaks etc. 

## Authors

Michelle van der Walt


