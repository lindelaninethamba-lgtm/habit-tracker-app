from functools import reduce
from habit import Habit
from check_log import CheckLog
from datetime import datetime, timedelta


def get_all_habits(habits: list) -> list: 
    """returns list of all habits"""
    return list(habits)


def filter_by_periodicity(habits: list, period: str) -> list: 
    """takes two arguments and returns filtered habits by periodiocity"""
    def matches_period(habit): 
        """matches every habit with matching periodicity call"""
        return habit.periodicity == period
    return list(filter(matches_period, habits)) 
""" returns list of habits with same periodicity as call"""


def longest_streak_for_habit(habit: Habit, logs: list) -> int: 
    """returns longest streak"""
    if not logs: #condition if there are no logs for the habit
        return 0

    if habit.periodicity == "daily": #extracts only daily habits
        periods = sorted(set(
            log.check_off_date.date() for log in logs 
        ))#creates a sorted set from the log list
    else: #all other habits not daily
        periods = sorted(set(
            log.check_off_date.isocalendar()[:2] for log in logs #uses iso date standard but extracts year and week number[:2]
        ))

    if not periods: 
        return 0

    longest = 1 #sets streak to 1
    current = 1

    for i in range(1, len(periods)): #loop for n times  
        if habit.periodicity == "daily":
            diff = (periods[i] - periods[i - 1]).days #check difference between two periods
            consecutive = diff == 1 #defining consequtive to enforce streak to be exactly one day
        else:
            #defining consecutive for weekly habits
            prev = datetime.fromisocalendar(periods[i-1][0], periods[i-1][1], 1)
            curr = datetime.fromisocalendar(periods[i][0], periods[i][1], 1)
            consecutive = (curr - prev).days == 7
            #defining consecutive to enforce streak to be exactly one week

        if consecutive: #if condition of consecutive is met
            current += 1 #add 1 to current streaks
            longest = max(longest, current) #compares with current streak
        else:
            current = 1

    return longest


def longest_streak_all(habits: list, all_logs: list) -> tuple: 
    """returns longest streak overall in a tuple"""
    if not habits:
        return None, 0 #return zero if habit list is empty

    def get_streak(habit): 
        """nested function to returnstreak number"""
        def get_logs_for_habit(log):
            return log.habit_id == habit.habit_id #compares if log matches to habit and returns true
        logs = list(filter(get_logs_for_habit, all_logs))
        return longest_streak_for_habit(habit, logs) #calls streak calculation

    def make_streak_tuple(habit): 
        """makes streak a tuple"""
        return (habit, get_streak(habit)) #calls habit for which streak it belongs 

    def compare_streaks(a, b): 
        """compares streaks"""
        return a if a[1] >= b[1] else b #returns streak with higher number

    streaks = list(map(make_streak_tuple, habits)) #matches each streak to corresponding habit, makes tuple
    return reduce(compare_streaks, streaks) #checks habit with hightest steak to compute best one and returns that

def habit_struggled_most(habits: list, all_logs: list) -> tuple: 
    """returns the habit with the lowest longest streak."""
    if not habits:
        return None, 0

    def get_logs_for_habit(habit):
        """identifies habit passed and returns all logs for that particular habit"""
        return list(filter(lambda log: log.habit_id == habit.habit_id, all_logs))

    def make_streak_tuple(habit):
        """makes a tuple for the habit streak"""
        return (habit, longest_streak_for_habit(habit, get_logs_for_habit(habit)))

    streaks = list(map(make_streak_tuple, habits))
    return min(streaks, key=lambda t: t[1])

