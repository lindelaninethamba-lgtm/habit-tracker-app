from datetime import datetime
class Habit:
    def __init__(self, habit_name:str, task_description:str, periodicity:str,
                  habit_id:int = None, creation_date:datetime = None):
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.task_description = task_description
        self.periodicity = periodicity
        self.creation_date = creation_date or datetime.now()

    def validate_periodicity(self):
        return self.periodicity in ["daily", "weekly"]
    
    def __str__(self):
        return (f"[{self.habit_id}] {self.habit_name}"
                f"({self.periodicity}) -Created: " 
                f"{self.creation_date.strftime('%Y-%m-%d')}")

        