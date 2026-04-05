import sqlite3
from datetime import datetime
from habit import Habit
from check_log import CheckLog
from user import User

class Storage: #manages database operations
    def __init__(self, db_path:str = "habits.db"):
        self.db_path = db_path
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
        cursor.execute("""CREATE TABLE IF NOT EXISTS check_logs(log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       habit_id INTEGER NOT NULL,
                       check_off_date TEXT NOT NULL,
                       FOREIGN KEY(habit_id) REFERENCES habits(habit_id))""")#creates a checklog table
        
        self.conn.commit()#saves changes

    def save_habit(self, habit:Habit, user_id:int):#saves a new habit to database
        cursor = self.conn.cursor() #writes to database
        cursor.execute("""
            INSERT INTO habits (user_id, habit_name, task_description,
            periodicity, creation_date) VALUES (?, ?, ?, ?, ?)
                       """, (user_id, habit.habit_name, habit.task_description,
              habit.periodicity,
              habit.creation_date.strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit() #saves changes
    
    def load_habits(self): #returns all habits saved in the database
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM habits""")
        rows = cursor.fetchall()
        habits = []
        for row in rows:
            h = Habit(habit_id = row[0], habit_name = row[2], 
                      task_description= row[3], periodicity= row[4],
                      creation_date= datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'))
            habits.append(h)
        return habits
    
    def delete_habit(self, habit_id: int): #delete a habit
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM habits WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM logs WHERE habit_id = ?", (habit_id,))
        self.conn.commit()

    def check_off_habit(self, habit_id: int): #checks off habit
        cursor = self.conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""INSERT INTO logs(habit_id, check_off_date)
                       VALUES(?,?))""", (habit_id, now))
        self.conn.commit()

    def load_logs(self, habit_id:int):#loads all logs for a particular habit
        cursor= self.conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE habit_id = ?", (habit_id))
        rows = cursor.fetchall()
        logs = []
        for row in rows:
            log = CheckLog(log_id = row[0],
                           habit_id=row[1], 
                           check_off_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S'))
            logs.append(log)
            return logs


    