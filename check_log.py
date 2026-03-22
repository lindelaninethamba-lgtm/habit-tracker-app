from datetime import datetime

class CheckLog():
    def __init__(self, habit_id:int, check_off_date:datetime = None, 
                 log_id: int = None):
        self.log_id = log_id
        self.habit_id = habit_id
        self.check_off_date = check_off_date or datetime.now()

    def __str__(self):
        return (f"Log [{self.log_id}] - Habit id: {self.habit_id} "
                f"completed on: "
                f"{self.check_off_date.strftime('%Y-%m-%d %H:%M')}")