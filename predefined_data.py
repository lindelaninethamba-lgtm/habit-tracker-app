from datetime import datetime, timedelta
from habit import Habit


def load_predefined_data(storage): #
    """loads predefined data. skips loading if any habits already exist in the database.
    #delete habits.db first to reload predefined data."""
    existing = storage.load_habits()
    if existing:
        print("Predefined data already loaded.")
        return

    print("Loading predefined habits and 4 weeks of data...")

    start_date = datetime(2026, 1, 1)

    #  5 Predefined Habits 
    habits = [
        Habit("Outdoor Activity",
              "1 hour walk outside", "weekly"),
        Habit("Gym Session",
              "2 hour gym session", "daily"),
        Habit("Studying",
              "2 hours study", "daily"),
        Habit("Reading",
              "Read 2 chapters", "weekly"),
        Habit("Healthy Diet",
              "Stick to healthy diet", "daily"),
    ]

    for habit in habits:
        storage.save_habit(habit, user_id=1)

    #  4 Weeks of Check-off Data 

    # Outdoor Activity — weekly — every week for 4 weeks
    for i in range(4):
        storage.check_off_habit(
            habits[0].habit_id,
            check_off_date=start_date + timedelta(weeks=i))

    # Gym Session — daily — perfect streak all 28 days
    for i in range(28):
        storage.check_off_habit(
            habits[1].habit_id,
            check_off_date=start_date + timedelta(days=i))

    # Studying — daily — missed day 10 and 11
    for i in range(28):
        if i not in [9, 10]:
            storage.check_off_habit(
                habits[2].habit_id,
                check_off_date=start_date + timedelta(days=i))

    # Reading — weekly — first 2 weeks only, streak broke after week 3 and 4
    for i in range(4):
        storage.check_off_habit(
            habits[3].habit_id,
            check_off_date=start_date + timedelta(weeks=i))

    # Healthy Diet — daily — randomly inconsistent
    for i in [0, 1, 5, 6, 7, 14, 15, 20]:
        storage.check_off_habit(
            habits[4].habit_id,
            check_off_date=start_date + timedelta(days=i))

    print("✓ 5 habits loaded")
    print("✓ 4 weeks of tracking data loaded")
    print("✓ Ready to use!")
    