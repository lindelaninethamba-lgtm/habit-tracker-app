from analytics import (get_all_habits, filter_by_periodicity,
                       longest_streak_for_habit, longest_streak_all)
from habit import Habit
from storage import Storage


class CLI:
    """Handles all user interaction through the command line."""

    def __init__(self, storage: Storage):
        """
        Initialises the CLI with a storage instance.

        Args:
            storage (Storage): The storage instance for
                               database operations.
        """
        self.storage = storage

    def run(self):
        """
        Main loop — keeps showing menu until user exits.
        """
        print("\n===========================")
        print("    HABIT TRACKER APP")
        print("===========================")

        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()

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
            elif choice == "0":
                print("\nGoodbye! Keep up your habits!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")

    def display_menu(self):
        """Displays the main menu options."""
        print("\n---------------------------")
        print("1. Create Habit")
        print("2. Delete Habit")
        print("3. Check-off Habit")
        print("4. View Streak for a Habit")
        print("5. View All Habits")
        print("6. View Longest Streak")
        print("0. Exit")
        print("---------------------------")

    def display_habit_list(self):
        """
        Displays all habits as a numbered list.
        Returns the list of habits for selection.
        """
        habits = self.storage.load_habits()
        if not habits:
            print("\n❌ No habits found.")
            return None
        print("\nYour habits:")
        for i, habit in enumerate(habits, 1):
            print(f"{i}. {habit.habit_name} ({habit.periodicity})")
        return habits

    def select_habit(self):
        """
        Shows habit list and asks user to pick one.
        Returns the selected Habit object or None.
        """
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
        """
        Prompts user for habit details and saves to database.
        """
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
        """
        Shows habit list and deletes the selected habit.
        """
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
        """
        Shows habit list and checks off the selected habit.
        """
        print("\n--- Check-off Habit ---")
        habit = self.select_habit()
        if not habit:
            return
        self.storage.check_off_habit(habit.habit_id)
        print(f"\n✓ '{habit.habit_name}' checked off!")

    def display_streak(self):
        """
        Shows the streak for a selected habit.
        """
        print("\n--- View Streak ---")
        habit = self.select_habit()
        if not habit:
            return
        logs = self.storage.load_logs(habit.habit_id)
        streak = longest_streak_for_habit(habit, logs)
        print(f"\n🔥 Longest streak for "
              f"'{habit.habit_name}': {streak} "
              f"{'days' if habit.periodicity == 'daily' else 'weeks'}")

    def display_all_habits(self):
        """
        Displays all currently tracked habits.
        """
        print("\n--- All Habits ---")
        habits = self.storage.load_habits()
        if not habits:
            print("No habits found.")
            return
        all_habits = get_all_habits(habits)
        for habit in all_habits:
            print(f"  {habit}")

    def display_longest_streak(self):
        """
        Displays the habit with the longest streak
        across all habits.
        """
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
            print(f"\n🏆 '{habit.habit_name}' has the longest "
                  f"streak: {streak} "
                  f"{'days' if habit.periodicity == 'daily' else 'weeks'}")