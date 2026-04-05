import pytest
import os
from storage import Storage
from habit import Habit


@pytest.fixture
def storage():
    #creating a temporary database
    s = Storage("test_habits.db")
    yield s
    s.conn.close()
    os.remove("test_habits.db")


def test_save_and_load_habit(storage):#test save and load habits
    h = Habit("Gym Session", "Go to gym", "daily")
    storage.save_habit(h, 1)
    habits = storage.load_habits()
    assert len(habits) == 1
    assert habits[0].habit_name == "Gym Session"


def test_habit_id_assigned_after_save(storage):
    """Test that habit_id is assigned by database after save."""
    h = Habit("Reading", "Read 20 pages", "daily")
    storage.save_habit(h, 1)
    assert h.habit_id is not None


def test_delete_habit(storage): #test saving habit
    h = Habit("Studying", "Study 1 hour", "daily")
    storage.save_habit(h, 1)
    storage.delete_habit(h.habit_id)
    habits = storage.load_habits()
    assert len(habits) == 0


def test_check_off_and_load_logs(storage):#test check off and loading logs
    h = Habit("Gym Session", "Go to gym", "daily")
    storage.save_habit(h, 1)
    storage.check_off_habit(h.habit_id)
    logs = storage.load_logs(h.habit_id)
    assert len(logs) == 1
    assert logs[0].habit_id == h.habit_id