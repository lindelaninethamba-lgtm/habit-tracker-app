import sqlite3
from datetime import datetime
from habit import Habit
from check_log import CheckLog
from user import User

class Storage: #manages database operations
    def __init__(self, db_path:str = "habits.db"):
        self.db_path = db_path #storing the database path
        self.conn = sqlite3.connect(self.db_path)
        self.initialise_db()

    def initialise_db(self):#initialising the database
        cursor = self.conn.cursor() #open and writing to the database

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL, 
                       email_address TEXT NOT NULL,
                       is_active BOOLEAN NOT NULL)""")#creates users table in SQL
        cursor.execute("""CREATE TABLE IF NOT EXISTS habits(habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       user_id INTEGER NOT NULL,
                       habit_name TEXT NOT NULL, 
                       task_description TEXT NOT NULL,
                       periodicity TEXT NOT NULL,
                       creation_date TEXT NOT NULL,
                       FOREIGN KEY(user_id) REFERENCES users(user_id))""")#creates a habits table
        cursor.execute("""CREATE TABLE IF NOT EXISTS logs(log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       habit_id INTEGER NOT NULL,
                       check_off_date TEXT NOT NULL,
                       FOREIGN KEY(habit_id) REFERENCES habits(habit_id))""")#creates a logs table
        
        self.conn.commit()#saves changes

    def save_habit(self, habit:Habit, user_id:int):#saves a new habit to database
        cursor = self.conn.cursor() #writes to database
        cursor.execute("""
            INSERT INTO habits (user_id, habit_name, task_description,
            periodicity, creation_date) VALUES (?, ?, ?, ?, ?) 
                       """, (user_id, habit.habit_name, habit.task_description,
              habit.periodicity,
              habit.creation_date.strftime('%Y-%m-%d %H:%M:%S'))) #creates a row in the habit table with placeholders
        self.conn.commit() #saves changes
        habit.habit_id = cursor.lastrowid #takes the assigned id by database into the habit object
    
    def load_habits(self): #returns all habits saved in the database
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM habits""") #selects every row entry in habits table
        rows = cursor.fetchall() #fetches all rows
        habits = [] #creates an empty list
        for row in rows:
            h = Habit(habit_id = row[0], habit_name = row[2], 
                      task_description= row[3], periodicity= row[4],
                      creation_date= datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'))
            habits.append(h) #populates list from database row entries
        return habits
    
    def delete_habit(self, habit_id: int): #delete a habit
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM logs WHERE habit_id = ?", (habit_id,)) #deletes logs
        cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,)) #then deletes habits
        self.conn.commit()

    def check_off_habit(self, habit_id: int, check_off_date=None): #marks habit as complete
        cursor = self.conn.cursor()
        if check_off_date is None:
            check_off_date = datetime.now() #uses current timestamp to check off habit
        now = check_off_date.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO logs (habit_id, check_off_date)
            VALUES (?, ?) 
        """, (habit_id, now))#saves the completion check_off into logs table
        self.conn.commit()
        log_id = cursor.lastrowid #assign a unuique id from database to new log

    def load_logs(self, habit_id:int):#returns all logs for a particular habit
        cursor= self.conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE habit_id = ?", (habit_id,))
        rows = cursor.fetchall()
        logs = [] #create empty list
        for row in rows:
            log = CheckLog(log_id = row[0],
                           habit_id=row[1], 
                           check_off_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'))
            logs.append(log) #populates logs into the list
        return logs


    