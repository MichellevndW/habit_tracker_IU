from db import get_db, create_tables, add_habit, add_tracker, add_streak

db = get_db("habit_tracker.db")
create_tables(db)

sample_data_habits = [("DEMO_DATA", "DEMO", "DEMO", "DEMO", "DEMO DATA INSERTED"),
                      ("sleep","Daily","health","2023,07,15", "Get 8 hours of quality sleep"),
                      ("read", "Daily", "intellectual", "2023,07,15", "Read a minimum of 15 minutes"),
                      ("budget", "Weekly", "financial", "2023,07,15", "Do a weekly recon of my budget"),
                      ("Eat clean", "Daily", "health", "2023,07,15", "Eat healthy, balanced meals"),
                      ("Skill building", "Monthly", "career", "2023,07,15", "Actively apply self in building a new skill")
]

sample_data_tracker = [(1,"Slept 8 hours", "2023,07,16", "No screens after 9"),
                       (1,"Slept 8 hours", "2023,07,17", " "),
                       (1,"Slept 9 hours", "2023,07,18", " "),
                       (1,"Slept 8 hours", "2023,07,19", " "),
                       (1,"Slept 8 hours", "2023,07,20", " "),
                       (1,"Slept 9 hours", "2023,07,21", " "),
                       (1,"Slept 8 hours", "2023,07,22", " "),
                       (1,"Slept 8 hours", "2023,07,23", " "),
                       (1,"Slept 8 hours", "2023,07,25", " "),
                       (1,"Slept 8.5 hours", "2023,07,26", " "),
                       (1,"Slept 8 hours", "2023,07,27", " "),
                       (1,"Slept 8 hours", "2023,07,28", "White Noise"),
                       (1,"Slept 8 hours", "2023,07,29", "White Noise"),
                       (1,"Slept 8 hours", "2023,07,30", "White Noise"),
                       (1,"Slept 8 hours", "2023,07,31", "White Noise"),
                       (1,"Slept 10 hours", "2023,08,01", "White Noise"),
                       (1,"Slept 8 hours", "2023,08,02", "White Noise"),
                       (1,"Slept 8 hours", "2023,08,03", "White Noise"),
                       (1,"Slept 8 hours", "2023,08,04", " "),
                       (1,"Slept 8 hours", "2023,08,05", " "),
                       (1,"Slept 9 hours", "2023,08,06", " "),
                       (1,"Slept 8 hours", "2023,08,07", " "),
                       (1,"Slept 8 hours", "2023,08,08", " "),
                       (1,"Slept 8 hours", "2023,08,09", "Sleeping tablet"),
                       (1,"Slept 8 hours", "2023,08,11", " "),
                       (1,"Slept 8 hours", "2023,08,13", " "),
                       (1,"Slept 8 hours", "2023,08,14", " "),
                       (2,"Read x book, 20 pages", "2023,07,16", "good read"),
                       (2,"Read x book, 15 pages", "2023,07,17", " "),
                       (2,"Read x book, 22 pages", "2023,07,19", " "),
                       (2,"Read x book, 32 pages", "2023,07,22", " "),
                       (2,"Read x book, 20 pages", "2023,07,23", " "),
                       (2,"Read x book, 15 pages", "2023,07,24", "Couldn't concentrate"),
                       (2,"Read x book, 15 pages", "2023,07,25", " "),
                       (2,"Read x book, 15 pages", "2023,07,27", " "),
                       (2,"Read x book, 30 pages", "2023,07,28", " "),
                       (2,"Read x book, 34 pages", "2023,07,29", " "),
                       (2,"Read x book, 20 pages", "2023,07,30", " "),
                       (2,"Read x book, 23 pages", "2023,07,31", " "),
                       (2,"Read x book, 25 pages", "2023,08,01", "Need a new book"),
                       (2,"Read x book, 15 pages", "2023,08,05", " "),
                       (2,"Read x book, 15 pages", "2023,08,06", " "),
                       (2,"Read x book, 25 pages", "2023,08,07", " "),
                       (2,"Read x book, 20 pages", "2023,08,08", " "),
                       (2,"Read x book, 200 pages", "2023,08,09", "Couldn't put it down"),
                       (2,"Read x book, 15 pages", "2023,08,14", "Slow start"),
                       (3,"Completed budget", "2023,07,22", "Need to cut back on entertainment"),
                       (3,"Completed budget", "2023,07,29", "Looking good"),
                       (3,"Completed budget", "2023,08,05", " "),
                       (3,"Completed budget", "2023,08,12", " "),
                       (4,"Clean day", "2023,07,16", "Good start"),
                       (4,"Clean day", "2023,07,17", " "),
                       (4,"Clean day", "2023,07,23", "Resisted temptation"),
                       (4,"Clean day", "2023,07,24", " "),
                       (4,"Clean day", "2023,07,25", " "),
                       (4,"Clean day", "2023,07,26", " "),
                       (4,"Clean day", "2023,07,30", " "),
                       (4,"Clean day", "2023,07,31", "This is harder than I thought"),
                       (4,"Clean day", "2023,08,05", " "),
                       (4,"Clean day", "2023,08,07", " "),
                       (4,"Clean day", "2023,08,08", " "),
                       (4,"Clean day", "2023,08,09", " "),
                       (5,"LinkedIn course", "2023, 07, 29", "LinkedIn Course on X completed")
]

sample_data_streak = [(1, "", "", ""),
                      (2, "", "", ""),
                      (3, "", "", ""),
                      (4, "", "", ""),
                      (5, "", "", "")
]


def add_sample_data(db):
    for sample in sample_data_habits:
        add_habit(db, sample[0], sample[1], sample[2], sample[3], sample[4])
    for sample in sample_data_tracker:
        add_tracker(db, sample[0], sample[1], sample[2], sample[3])
    for sample in sample_data_streak:
        add_streak(db, sample[0], sample[1], sample[2], sample[3])

