import pytest
import os
from storage import Storage #to implement storage functions
from habit import Habit


@pytest.fixture #providing sample data to enable testing
def storage():
    """creating a temporary database for testing"""
    s = Storage("test_habits.db")
    yield s
    s.conn.close()
    os.remove("test_habits.db") #removes the database


def test_save_and_load_habit(storage):#test save and load habits
    h = Habit("Gym Session", "Go to gym", "daily") #creates the temporary habit instance
    storage.save_habit(h, 1) #saves with the user_id 1
    habits = storage.load_habits() #returns habit list 
    assert len(habits) == 1
    assert habits[0].habit_name == "Gym Session"


def test_habit_id_assigned_after_save(storage):#test habit id
    h = Habit("Reading", "Read 20 pages", "daily")
    storage.save_habit(h, 1)
    assert h.habit_id is not None


def test_delete_habit(storage): #test deleting habit
    h = Habit("Studying", "Study 1 hour", "daily")
    storage.save_habit(h, 1)
    storage.delete_habit(h.habit_id)
    habits = storage.load_habits() #returns habits list
    assert len(habits) == 0 #must assert empty list


def test_check_off_and_load_logs(storage):#test check off and loading logs
    h = Habit("Gym Session", "Go to gym", "daily")
    storage.save_habit(h, 1)
    storage.check_off_habit(h.habit_id) #marks habit as complete
    logs = storage.load_logs(h.habit_id) #must return logs list
    assert len(logs) == 1
    assert logs[0].habit_id == h.habit_id