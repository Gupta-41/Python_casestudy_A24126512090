# Smart Library Management System
# Anil Neerukonda Institute of Technology & Sciences (Autonomous)
# Case Study Assignment - Python

# Unit-I: Import statement (Modules)
import json
import re
import os
from datetime import datetime

DATA_FILE = "library_data.json"


# Unit-V: RegEx - Validate Student ID format like STU001
def validate_student_id(student_id):
    pattern = r"^STU\d{3}$"  # Unit-V: Regular Expression pattern
    return bool(re.match(pattern, student_id))


# Unit-IV: Class definition with Constructor and Methods (OOP)
class Library:

    # Unit-IV: Constructor (__init__)
    def __init__(self):
        # Unit-II: Dictionary data structure to store books and students
        self.books = {}       # { book_id: {title, author, available} }
        self.students = {}    # { student_id: name }
        self.borrows = {}     # { book_id: student_id }
        self.borrow_log = []  # Unit-II: List to store borrow history
        self.load_data()      # Unit-V: File Handling - load saved data on startup

    # Unit-IV: Method - Add Book
    def add_book(self, book_id, title, author):
        # Unit-II: Membership test using 'in' operator
        if book_id in self.books:
            print(f"  [!] Book ID '{book_id}' already exists.")
            return
        # Unit-II: Dictionary - adding key-value pair
        self.books[book_id] = {
            "title": title,
            "author": author,
            "available": True  # Unit-I: Boolean data type
        }
        print(f"  [+] Book '{title}' by {author} added successfully (ID: {book_id}).")
        self.save_data()

    # Unit-IV: Method - Display all Books
    def display_books(self):
        # Unit-II: if condition to check empty dictionary
        if not self.books:
            print("  [!] No books in the library yet.")
            return
        print("\n  ID         Title                     Author             Status")
        print("  " + "-" * 63)
        # Unit-II: for loop with dictionary iteration
        for bid, info in self.books.items():
            # Unit-II: if-else for conditional status display
            status = "Available" if info["available"] else "Issued"
            print(f"  {bid:<10} {info['title']:<25} {info['author']:<18} {status}")

    # Unit-IV: Method - Add Student
    def add_student(self, student_id, name):
        # Unit-V: RegEx validation
        if not validate_student_id(student_id):
            print(f"  [!] Invalid Student ID '{student_id}'. Format must be STU followed by 3 digits. Example: STU001")
            return
        # Unit-II: Membership test
        if student_id in self.students:
            print(f"  [!] Student ID '{student_id}' already registered.")
            return
        # Unit-II: Dictionary - adding new student
        self.students[student_id] = name
        print(f"  [+] Student '{name}' registered successfully (ID: {student_id}).")
        self.save_data()

    # Unit-IV: Method - Display all Students
    def display_students(self):
        # Unit-II: if condition
        if not self.students:
            print("  [!] No students registered yet.")
            return
        print("\n  Student ID      Name")
        print("  " + "-" * 30)
        # Unit-II: for loop with dictionary iteration
        for sid, name in self.students.items():
            print(f"  {sid:<15} {name}")

    # Unit-IV: Method - Issue Book to Student
    def issue_book(self, book_id, student_id):
        # Unit-II: Nested if conditions for validation
        if book_id not in self.books:
            print(f"  [!] Book ID '{book_id}' not found.")
            return
        if student_id not in self.students:
            print(f"  [!] Student ID '{student_id}' not registered.")
            return
        # Unit-II: if condition - check availability before issuing
        if not self.books[book_id]["available"]:
            issued_to = self.borrows.get(book_id, "Unknown")
            print(f"  [!] '{self.books[book_id]['title']}' is already issued to student {issued_to}. Cannot issue again.")
            return
        # Unit-I: Assignment - update book availability
        self.books[book_id]["available"] = False
        self.borrows[book_id] = student_id
        # Unit-V: datetime module usage
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Unit-II: List append method - add to borrow log
        self.borrow_log.append({
            "action": "ISSUED",
            "book_id": book_id,
            "book_title": self.books[book_id]["title"],
            "student_id": student_id,
            "student_name": self.students[student_id],
            "timestamp": timestamp
        })
        print(f"  [+] '{self.books[book_id]['title']}' issued to {self.students[student_id]} on {timestamp}.")
        self.save_data()

    # Unit-IV: Method - Return Book
    def return_book(self, book_id, student_id):
        # Unit-II: if-else conditions for validation
        if book_id not in self.books:
            print(f"  [!] Book ID '{book_id}' not found.")
            return
        if self.books[book_id]["available"]:
            print(f"  [!] '{self.books[book_id]['title']}' was not issued to anyone.")
            return
        if self.borrows.get(book_id) != student_id:
            actual = self.borrows.get(book_id, "someone else")
            print(f"  [!] This book was issued to student {actual}, not {student_id}.")
            return
        # Unit-I: Assignment - restore availability
        self.books[book_id]["available"] = True
        del self.borrows[book_id]
        # Unit-V: datetime module
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Unit-II: List append
        self.borrow_log.append({
            "action": "RETURNED",
            "book_id": book_id,
            "book_title": self.books[book_id]["title"],
            "student_id": student_id,
            "student_name": self.students[student_id],
            "timestamp": timestamp
        })
        print(f"  [+] '{self.books[book_id]['title']}' returned by {self.students[student_id]} on {timestamp}.")
        self.save_data()

    # Unit-IV: Method - Display Borrow Log
    def display_borrow_log(self):
        if not self.borrow_log:
            print("  [!] No borrow activity recorded yet.")
            return
        print("\n  Action     Book ID    Title                  Student ID   Name            Timestamp")
        print("  " + "-" * 80)
        # Unit-II: for loop over list
        for entry in self.borrow_log:
            print(f"  {entry['action']:<10} {entry['book_id']:<10} {entry['book_title']:<22} "
                  f"{entry['student_id']:<12} {entry['student_name']:<15} {entry['timestamp']}")

    # Unit-V: File Handling - Save all data to JSON file
    def save_data(self):
        data = {
            "books": self.books,
            "students": self.students,
            "borrows": self.borrows,
            "borrow_log": self.borrow_log
        }
        # Unit-V: File open, write, close using 'with' block
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # Unit-V: File Handling - Load data from JSON file
    def load_data(self):
        # Unit-II: if condition to check file existence
        if not os.path.exists(DATA_FILE):
            return
        # Unit-V: File open and read
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        # Unit-II: Dictionary methods to restore data
        self.books = data.get("books", {})
        self.students = data.get("students", {})
        self.borrows = data.get("borrows", {})
        self.borrow_log = data.get("borrow_log", [])
        print("  [*] Previous data loaded from file successfully.")


# Unit-III: Function - Display main menu
def display_menu():
    print("\n  *** Smart Library Management System ***")
    print("  1. Add Book")
    print("  2. Display All Books")
    print("  3. Add Student")
    print("  4. Display All Students")
    print("  5. Issue Book")
    print("  6. Return Book")
    print("  7. View Borrow Log")
    print("  8. Exit")
    print("  " + "-" * 40)


# Unit-III: Function - Get non-empty input from user
def get_input(prompt):
    # Unit-II: while loop with break
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] Input cannot be empty. Please try again.")


# Unit-III: Main function - Entry point of the program
def main():
    # Unit-IV: Creating an object (instance) of Library class
    lib = Library()

    # Unit-II: while loop for menu-driven program
    while True:
        display_menu()
        # Unit-I: Input and type conversion
        choice = get_input("  Enter your choice (1-8): ")

        # Unit-II: if-elif-else for menu selection
        if choice == "1":
            print("\n  -- Add Book --")
            book_id = get_input("  Enter Book ID: ")
            title = get_input("  Enter Book Title: ")
            author = get_input("  Enter Author Name: ")
            lib.add_book(book_id, title, author)

        elif choice == "2":
            print("\n  -- All Books --")
            lib.display_books()

        elif choice == "3":
            print("\n  -- Add Student --")
            student_id = get_input("  Enter Student ID (format: STU001): ")
            name = get_input("  Enter Student Name: ")
            lib.add_student(student_id, name)

        elif choice == "4":
            print("\n  -- All Students --")
            lib.display_students()

        elif choice == "5":
            print("\n  -- Issue Book --")
            book_id = get_input("  Enter Book ID to issue: ")
            student_id = get_input("  Enter Student ID: ")
            lib.issue_book(book_id, student_id)

        elif choice == "6":
            print("\n  -- Return Book --")
            book_id = get_input("  Enter Book ID to return: ")
            student_id = get_input("  Enter Student ID: ")
            lib.return_book(book_id, student_id)

        elif choice == "7":
            print("\n  -- Borrow Log --")
            lib.display_borrow_log()

        elif choice == "8":
            print("\n  Thank you for using the Smart Library Management System. Goodbye!")
            break

        else:
            # Unit-II: else block for invalid input
            print("  [!] Invalid choice. Please enter a number between 1 and 8.")


# Unit-I: Entry point check using __name__
if __name__ == "__main__":
    main()


# =============================================================
# CONCEPTS USED - UNIT WISE EXPLANATION
# =============================================================
#
# UNIT-I (Introduction):
#   - Keywords: if, else, elif, while, for, return, break, del, not, in
#   - Variables and Constants: book_id, student_id, DATA_FILE, etc.
#   - Data Types: str, bool, int
#   - I/O: input() for user input, print() for output
#   - Import: import json, re, os, datetime
#   - Operators: Comparison (==, !=), Logical (not), Membership (in)
#   - Namespace: if __name__ == "__main__"
#
# UNIT-II (Flow Control & Collections):
#   - if, elif, else: menu selection, validation checks
#   - while loop: main menu loop, get_input loop
#   - for loop: iterating books, students, borrow_log
#   - break: exit menu loop on choice 8
#   - Dictionary: self.books, self.students, self.borrows
#   - List: self.borrow_log, list.append()
#   - Membership Test: 'in' operator for checking existing IDs
#   - Dictionary Methods: .items(), .get()
#   - String Methods: .strip()
#
# UNIT-III (Functions):
#   - display_menu(): separate function for menu display
#   - get_input(): reusable input validation function
#   - main(): main entry-point function
#   - Function arguments: prompt parameter in get_input()
#
# UNIT-IV (Object Oriented Programming):
#   - Class: Library class
#   - Constructor: __init__() to initialize attributes
#   - Methods: add_book, display_books, add_student, display_students,
#              issue_book, return_book, display_borrow_log, save_data, load_data
#   - Object: lib = Library()
#   - Encapsulation: all data (books, students, borrows) inside the class
#
# UNIT-V (Advanced Topics):
#   - RegEx: re.match() to validate Student ID format (STU + 3 digits)
#   - File Handling: open(), read, write, close via 'with' block
#   - JSON file: json.dump() to save, json.load() to load data
#   - datetime module: datetime.now().strftime() for timestamps
#   - os module: os.path.exists() to check if file exists
#
# =============================================================
