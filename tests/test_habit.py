import pytest
from  habit import Habit

def test_habit_creation(): #Testing habit creation with correction with correct attributes
    habit1 = Habit("Gym session", "weightlifting for 2 hours", "daily")
    assert habit1.habit_name == "Gym session"
    assert habit1.task_description == "weightlifting for 2 hours"
    assert habit1.periodicity == "daily"

def test_habit_creation_date_on_auto(): #Testing habit creation date automatically
    habit1 = Habit("Studying", "Studying 4 hours", "daily")
    assert habit1.creation_date is not None

def test_daily_periodicity():
    habit1 = Habit("Gym session", "weightlifting for 2 hours", "daily")
    assert habit1.validate_periodicity() == True

def test_weekly_periodicity():
    habit1 = Habit("Studying", "Studying 4 hours", "weekly")
    assert habit1.validate_periodicity() == True

def test_invalid_periodicity():
    habit1 = Habit("Gym session", "weightlifting", "bi-weekly")
    assert habit1.validate_periodicity() == False


