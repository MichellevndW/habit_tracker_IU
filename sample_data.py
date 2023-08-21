from db import get_db, create_tables, add_habit, add_tracker, add_streak, retrieve_all
from streak import Streak
db = get_db("habit_tracker.db")
create_tables(db)

sample_data_habits = [("DEMO_DATA", "DEMO", "DEMO", "DEMO", "DEMO DATA INSERTED"),
                      ("sleep","Daily","health","2023,07,15", "Get 8 hours of quality sleep"),
                      ("read", "Daily", "intellectual", "2023,07,15", "Read a minimum of 15 minutes"),
                      ("budget", "Weekly", "financial", "2023,07,15", "Do a weekly recon of my budget"),
                      ("Eat clean", "Daily", "health", "2023,07,15", "Eat healthy, balanced meals"),
                      ("Skill building", "Monthly", "career", "2023,07,15", "Actively apply self in building a new skill")
]

sample_data_tracker = [(2,"Slept 8 hours", "2023,07,16", "No screens after 9"),
                       (2,"Slept 8 hours", "2023,07,17", " "),
                       (2,"Slept 9 hours", "2023,07,18", " "),
                       (2,"Slept 8 hours", "2023,07,19", " "),
                       (2,"Slept 8 hours", "2023,07,20", " "),
                       (2,"Slept 9 hours", "2023,07,21", " "),
                       (2,"Slept 8 hours", "2023,07,22", " "),
                       (2,"Slept 8 hours", "2023,07,23", " "),
                       (2,"Slept 8 hours", "2023,07,25", " "),
                       (2,"Slept 8.5 hours", "2023,07,26", " "),
                       (2,"Slept 8 hours", "2023,07,27", " "),
                       (2,"Slept 8 hours", "2023,07,28", "White Noise"),
                       (2,"Slept 8 hours", "2023,07,29", "White Noise"),
                       (2,"Slept 8 hours", "2023,07,30", "White Noise"),
                       (2,"Slept 8 hours", "2023,07,31", "White Noise"),
                       (2,"Slept 10 hours", "2023,08,01", "White Noise"),
                       (2,"Slept 8 hours", "2023,08,02", "White Noise"),
                       (2,"Slept 8 hours", "2023,08,03", "White Noise"),
                       (2,"Slept 8 hours", "2023,08,04", " "),
                       (2,"Slept 8 hours", "2023,08,05", " "),
                       (2,"Slept 9 hours", "2023,08,06", " "),
                       (2,"Slept 8 hours", "2023,08,07", " "),
                       (2,"Slept 8 hours", "2023,08,08", " "),
                       (2,"Slept 8 hours", "2023,08,09", "Sleeping tablet"),
                       (2,"Slept 8 hours", "2023,08,11", " "),
                       (2,"Slept 8 hours", "2023,08,13", " "),
                       (2,"Slept 8 hours", "2023,08,14", " "),
                       (3,"Read x book, 20 pages", "2023,07,16", "good read"),
                       (3,"Read x book, 15 pages", "2023,07,17", " "),
                       (3,"Read x book, 22 pages", "2023,07,19", " "),
                       (3,"Read x book, 32 pages", "2023,07,22", " "),
                       (3,"Read x book, 20 pages", "2023,07,23", " "),
                       (3,"Read x book, 15 pages", "2023,07,24", "Couldn't concentrate"),
                       (3,"Read x book, 15 pages", "2023,07,25", " "),
                       (3,"Read x book, 15 pages", "2023,07,27", " "),
                       (3,"Read x book, 30 pages", "2023,07,28", " "),
                       (3,"Read x book, 34 pages", "2023,07,29", " "),
                       (3,"Read x book, 20 pages", "2023,07,30", " "),
                       (3,"Read x book, 23 pages", "2023,07,31", " "),
                       (3,"Read x book, 25 pages", "2023,08,01", "Need a new book"),
                       (3,"Read x book, 15 pages", "2023,08,05", " "),
                       (3,"Read x book, 15 pages", "2023,08,06", " "),
                       (3,"Read x book, 25 pages", "2023,08,07", " "),
                       (3,"Read x book, 20 pages", "2023,08,08", " "),
                       (3,"Read x book, 200 pages", "2023,08,09", "Couldn't put it down"),
                       (3,"Read x book, 15 pages", "2023,08,14", "Slow start"),
                       (4,"Completed budget", "2023,07,22", "Need to cut back on entertainment"),
                       (4,"Completed budget", "2023,07,29", "Looking good"),
                       (4,"Completed budget", "2023,08,05", " "),
                       (4,"Completed budget", "2023,08,12", " "),
                       (5,"Clean day", "2023,07,16", "Good start"),
                       (5,"Clean day", "2023,07,17", " "),
                       (5,"Clean day", "2023,07,23", "Resisted temptation"),
                       (5,"Clean day", "2023,07,24", " "),
                       (5,"Clean day", "2023,07,25", " "),
                       (5,"Clean day", "2023,07,26", " "),
                       (5,"Clean day", "2023,07,30", " "),
                       (5,"Clean day", "2023,07,31", "This is harder than I thought"),
                       (5,"Clean day", "2023,08,05", " "),
                       (5,"Clean day", "2023,08,07", " "),
                       (5,"Clean day", "2023,08,08", " "),
                       (5,"Clean day", "2023,08,09", " "),
                       (6,"LinkedIn course", "2023, 07, 29", "LinkedIn Course on X completed")
]


def add_sample_data(db):
    for sample in sample_data_habits:
        add_habit(db, sample[0], sample[1], sample[2], sample[3], sample[4])
    for sample in sample_data_tracker:
        add_tracker(db, sample[0], sample[1], sample[2], sample[3])
    habits, headers = retrieve_all(db, "habit")
    for habit in habits:
        if habit[1].lower() != "demo_data":
            streak = Streak(habit[0])
            streak.store_streak(db)
            streak.push_streak_all(db)

