import pytest
from datetime import datetime, timedelta
from analytics import (get_all_habits, filter_by_periodicity,
                       longest_streak_for_habit, longest_streak_all)
from habit import Habit
from check_log import CheckLog


# ── FIXTURES ─────────────────────────────────────────────

@pytest.fixture
def four_week_habits():
    """5 predefined habits with IDs assigned."""
    outdoor = Habit("Outdoor Activity",
                    "1 hour walk outside", "weekly")
    gym = Habit("Gym Session",
                "2 hour gym session", "daily")
    studying = Habit("Studying",
                     "2 hours study", "daily")
    reading = Habit("Reading",
                    "Read 2 chapters", "weekly")
    diet = Habit("Healthy Diet",
                 "Stick to healthy diet", "daily")

    outdoor.habit_id = 1
    gym.habit_id = 2
    studying.habit_id = 3
    reading.habit_id = 4
    diet.habit_id = 5

    return [outdoor, gym, studying, reading, diet]


@pytest.fixture
def four_week_logs():
    """4 weeks of check-off logs for all 5 habits."""
    logs = []
    start = datetime(2026, 1, 1)

    # Outdoor Activity — weekly — checked every week
    for i in range(4):
        logs.append(CheckLog(
            habit_id=1,
            check_off_date=start + timedelta(weeks=i)
        ))

    # Gym Session — daily — perfect streak all 28 days
    for i in range(28):
        logs.append(CheckLog(
            habit_id=2,
            check_off_date=start + timedelta(days=i)
        ))

    # Studying — daily — missed day 10 and 11
    for i in range(28):
        if i not in [9, 10]:
            logs.append(CheckLog(
                habit_id=3,
                check_off_date=start + timedelta(days=i)
            ))

    # Reading — weekly — first 2 weeks only
    for i in range(2):
        logs.append(CheckLog(
            habit_id=4,
            check_off_date=start + timedelta(weeks=i)
        ))

    # Healthy Diet — daily — sporadic
    for i in [0, 1, 5, 6, 7, 14, 15, 20]:
        logs.append(CheckLog(
            habit_id=5,
            check_off_date=start + timedelta(days=i)
        ))

    return logs


# ── TESTS ─────────────────────────────────────────────────

def test_get_all_habits(four_week_habits):
    """Test that all 5 habits are returned."""
    result = get_all_habits(four_week_habits)
    assert len(result) == 5


def test_filter_daily(four_week_habits):
    """Test that only daily habits are returned."""
    result = filter_by_periodicity(four_week_habits, "daily")
    assert len(result) == 3
    for h in result:
        assert h.periodicity == "daily"


def test_filter_weekly(four_week_habits):
    """Test that only weekly habits are returned."""
    result = filter_by_periodicity(four_week_habits, "weekly")
    assert len(result) == 2
    for h in result:
        assert h.periodicity == "weekly"


def test_perfect_streak_gym(four_week_habits, four_week_logs):
    """Test that gym session has a perfect 28 day streak."""
    gym = four_week_habits[1]
    logs = [l for l in four_week_logs if l.habit_id == 2]
    streak = longest_streak_for_habit(gym, logs)
    assert streak == 28


def test_streak_breaks_when_missed(four_week_habits, four_week_logs):
    """Test that studying longest streak is 17 after missing days."""
    studying = four_week_habits[2]
    logs = [l for l in four_week_logs if l.habit_id == 3]
    streak = longest_streak_for_habit(studying, logs)
    assert streak == 17


def test_outdoor_weekly_streak(four_week_habits, four_week_logs):
    """Test that outdoor activity has a 4 week streak."""
    outdoor = four_week_habits[0]
    logs = [l for l in four_week_logs if l.habit_id == 1]
    streak = longest_streak_for_habit(outdoor, logs)
    assert streak == 4


def test_reading_weekly_streak(four_week_habits, four_week_logs):
    """Test that reading streak is 2 weeks."""
    reading = four_week_habits[3]
    logs = [l for l in four_week_logs if l.habit_id == 4]
    streak = longest_streak_for_habit(reading, logs)
    assert streak == 2


def test_no_logs_returns_zero(four_week_habits):
    """Test that a habit with no logs returns streak of 0."""
    gym = four_week_habits[1]
    streak = longest_streak_for_habit(gym, [])
    assert streak == 0


def test_longest_streak_all(four_week_habits, four_week_logs):
    """Test that gym session wins longest streak across all habits."""
    habit, streak = longest_streak_all(
        four_week_habits, four_week_logs)
    assert habit.habit_name == "Gym Session"
    assert streak == 28