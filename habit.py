from datetime import datetime
class Habit:
    """Creates a habit class which defines habits and habit details"""
    def __init__(self, habit_name:str, task_description:str, periodicity:str,
                  habit_id:int = None, creation_date:datetime = None):
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.task_description = task_description
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now()

    def validate_periodicity(self):
        """validates daily and weekly as the two valid periodicity"""
        return self.periodicity in ["daily", "weekly"]
    
    def __str__(self):
        """ganarates habit details into a comprehensive string"""
        return (f"[{self.habit_id}] {self.habit_name}"
                f"({self.periodicity}) -Created: " 
                f"{self.creation_date.strftime('%Y-%m-%d')}")

        