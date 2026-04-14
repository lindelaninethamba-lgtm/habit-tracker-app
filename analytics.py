from functools import reduce
from habit import Habit
from check_log import CheckLog
from datetime import datetime, timedelta


def get_all_habits(habits: list) -> list: #returns list of all habits
    return list(habits)


def filter_by_periodicity(habits: list, period: str) -> list: #returns filtered habits
    def matches_period(habit):
        return habit.periodicity == period
    return list(filter(matches_period, habits))


def longest_streak_for_habit(habit: Habit, logs: list) -> int: #returns longest streak
    if not logs:# empty checklog
        return 0

    if habit.periodicity == "daily": #extracts only daily habits
        periods = sorted(set(
            log.check_off_date.date() for log in logs
        ))#computes a set for each daily entry
    else: #all other habits not daily
        periods = sorted(set(
            log.check_off_date.isocalendar()[:2] for log in logs
        ))#compuutes a set for each weekly entry

    if not periods: 
        return 0

    longest = 1
    current = 1

    for i in range(1, len(periods)):
        if habit.periodicity == "daily":
            diff = (periods[i] - periods[i - 1]).days
            consecutive = diff == 1 #defining consequtive to enforce streak
        else:
            consecutive = ( #defining consequtive for weekly habits
                periods[i][0] == periods[i - 1][0] and
                periods[i][1] == periods[i - 1][1] + 1
            )

        if consecutive: 
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return longest


def longest_streak_all(habits: list, all_logs: list) -> tuple: #returns longest streak overall
    if not habits:
        return None, 0

    def get_streak(habit):
        def get_logs_for_habit(log):
            return log.habit_id == habit.habit_id
        logs = list(filter(get_logs_for_habit, all_logs))
        return longest_streak_for_habit(habit, logs)

    def make_streak_tuple(habit):
        return (habit, get_streak(habit))

    def compare_streaks(a, b):
        return a if a[1] >= b[1] else b

    streaks = list(map(make_streak_tuple, habits))
    return reduce(compare_streaks, streaks)