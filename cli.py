from analytics import (get_all_habits, filter_by_periodicity,
                       longest_streak_for_habit, longest_streak_all, habit_struggled_most)
from habit import Habit
from storage import Storage


class CLI: 
    """user and app interface class handling command line"""

    def __init__(self, storage: Storage): 
        """initialise cli class with storage class """
        self.storage = storage

    def run(self): 
        """shows user menu"""
        
        print("HABIT TRACKER APP")
        

        while True:
            self.display_menu() #displays menu ay run
            choice = input("Enter your choice: ").strip() #input prompt to user
            """Based on user input, different classes run"""
            if choice == "1":
                self.create_habit()
            elif choice == "2":
                self.delete_habit()
            elif choice == "3":
                self.check_off_habit()
            elif choice == "4":
                self.display_streak()
            elif choice == "5":
                self.display_all_habits()
            elif choice == "6":
                self.display_longest_streak()
            elif choice == "7":
                self.display_struggled_most()
            elif choice == "0":
                print("\nGoodbye! Keep up your habits!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")

    def display_menu(self): 
        """displays menu options to user"""
        print("\n------------------------")
        print("1. Create Habit")
        print("2. Delete Habit")
        print("3. Check-off Habit")
        print("4. View Streak for a Habit")
        print("5. View All Habits")
        print("6. View Longest Streak")
        print("7. View Struggled Habit")
        print("0. Exit")
        print("------------------------")

    def display_habit_list(self): 
        """displays all habits in a numbered list"""
        habits = self.storage.load_habits()
        if not habits:
            print("\n❌ No habits found.")
            return None
        print("\nYour habits:")
        for i, habit in enumerate(habits, 1):
            print(f"{i}. {habit.habit_name} ({habit.periodicity})")
        return habits

    def select_habit(self): 
        """Shows habit list and asks user to pick one.
        Returns the selected Habit object or None."""
        habits = self.display_habit_list()
        if not habits:
            return None
        try:
            choice = int(input("Enter number: ").strip())
            if 1 <= choice <= len(habits):
                return habits[choice - 1]
            else:
                print("\n❌ Invalid number.")
                return None
        except ValueError:
            print("\n❌ Please enter a number.")
            return None

    def create_habit(self): 
        """propmts user to enter habit details"""
        print("\n--- Create New Habit ---")
        name = input("Habit name: ").strip()
        description = input("Description: ").strip()
        print("Periodicity options: daily / weekly")
        periodicity = input("Periodicity: ").strip().lower()

        if periodicity not in ["daily", "weekly"]:
            print("\n❌ Invalid periodicity.")
            return

        habit = Habit(name, description, periodicity)
        self.storage.save_habit(habit, user_id=1)
        print(f"\n✓ Habit '{name}' created successfully!")

    def delete_habit(self): 
        """deletes habit by allowing user to select habit and 
        delete through delete function in storage"""
        print("\n--- Delete Habit ---")
        habit = self.select_habit()
        if not habit:
            return
        confirm = input(
            f"Delete '{habit.habit_name}'? (yes/no): ").strip().lower()
        if confirm == "yes":
            self.storage.delete_habit(habit.habit_id)
            print(f"\n✓ Habit '{habit.habit_name}' deleted.")
        else:
            print("\nDeletion cancelled.")

    def check_off_habit(self): 
        """checks off habit by allowing user to select habit and check 
         it off through delete function in storage"""
        print("\n--- Check-off Habit ---")
        habit = self.select_habit()
        if not habit:
            return
        self.storage.check_off_habit(habit.habit_id)
        print(f"\n✓ '{habit.habit_name}' checked off!")

    def display_streak(self): 
        """displays habit streakby allowing user to select 
        habit and load logs function in storage"""
        print("\n--- View Streak ---")
        habit = self.select_habit()
        if not habit:
            return
        logs = self.storage.load_logs(habit.habit_id)
        streak = longest_streak_for_habit(habit, logs)
        print(f"\n Longest streak for "
              f"'{habit.habit_name}': {streak} "
              f"{'days' if habit.periodicity == 'daily' else 'weeks'}")

    def display_all_habits(self): 
        """displays habits from load habits in storage """
        print("\n--- All Habits ---")
        habits = self.storage.load_habits()
        if not habits:
            print("No habits found.")
            return
        all_habits = get_all_habits(habits)
        for habit in all_habits:
            print(f"  {habit}")

    def display_longest_streak(self): 
        """display longest streak for all habits stored"""
        print("\n--- Longest Streak ---")
        habits = self.storage.load_habits()
        if not habits:
            print("No habits found.")
            return
        all_logs = []
        for habit in habits:
            all_logs.extend(self.storage.load_logs(habit.habit_id))
        habit, streak = longest_streak_all(habits, all_logs)
        if habit:
            print(f"\n '{habit.habit_name}' has the longest "
                  f"streak: {streak} "
                  f"{'days' if habit.periodicity == 'daily' else 'weeks'}")
        
    def display_struggled_most(self): 
        """displays habit with lowest longest streak"""
        print("\n--- Most Struggled Habit ---")
        habits = self.storage.load_habits()
        if not habits:
            print("No habits found.")
            return

        all_logs = []
        for habit in habits:
            all_logs.extend(self.storage.load_logs(habit.habit_id))

            habit, streak = habit_struggled_most(habits, all_logs)
        if habit:
            print(f"\n '{habit.habit_name}' was the most struggled habit "
              f"with a longest streak of only {streak} "
              f"{'days' if habit.periodicity == 'daily' else 'weeks'}")
            