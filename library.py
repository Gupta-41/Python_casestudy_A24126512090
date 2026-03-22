import json
import re
import os
from datetime import datetime

# Smart Library Management System
# Anil Neerukonda Institute of Technology & Sciences


# Helper - Regex validation
# Student ID must match pattern: STU followed by 3 digits
# e.g. STU001, STU123
def validate_student_id(student_id: str) -> bool:
    pattern = r"^STU\d{3}$"
    return bool(re.match(pattern, student_id))


class Library:

    # Constructor
    def __init__(self):
        self.books = {}
        self.students = {}
        self.borrows = {}
        self.borrow_log = []
        self.load_data()

    # 1 - Add Book
    def add_book(self, book_id: str, title: str, author: str) -> None:
        if book_id in self.books:
            print(f"  [!] Book ID '{book_id}' already exists.")
            return
        self.books[book_id] = {
            "title": title,
            "author": author,
            "available": True
        }
        print(f"  [+] Book '{title}' by {author} added successfully (ID: {book_id}).")
        self.save_data()

    # 2 - Display Books
    def display_books(self) -> None:
        if not self.books:
            print("  [!] No books in the library yet.")
            return
        print("\n" + "-" * 65)
        print(f"  {'ID':<10} {'Title':<25} {'Author':<18} {'Status'}")
        print("-" * 65)
        for bid, info in self.books.items():
            status = "Available" if info["available"] else "Issued"
            print(f"  {bid:<10} {info['title']:<25} {info['author']:<18} {status}")
        print("-" * 65)

    # 3 - Add Student
    def add_student(self, student_id: str, name: str) -> None:
        if not validate_student_id(student_id):
            print(f"  [!] Invalid Student ID '{student_id}'. Format must be STU followed by 3 digits (e.g. STU001).")
            return
        if student_id in self.students:
            print(f"  [!] Student ID '{student_id}' already registered.")
            return
        self.students[student_id] = name
        print(f"  [+] Student '{name}' registered successfully (ID: {student_id}).")
        self.save_data()

    # 4 - Display Students
    def display_students(self) -> None:
        if not self.students:
            print("  [!] No students registered yet.")
            return
        print("\n" + "-" * 40)
        print(f"  {'Student ID':<15} {'Name'}")
        print("-" * 40)
        for sid, name in self.students.items():
            print(f"  {sid:<15} {name}")
        print("-" * 40)

    # 5 - Issue Book
    def issue_book(self, book_id: str, student_id: str) -> None:
        if book_id not in self.books:
            print(f"  [!] Book ID '{book_id}' not found.")
            return
        if student_id not in self.students:
            print(f"  [!] Student ID '{student_id}' not registered.")
            return
        if not self.books[book_id]["available"]:
            issued_to = self.borrows.get(book_id, "Unknown")
            print(f"  [!] Book '{self.books[book_id]['title']}' is currently issued to student {issued_to}. Cannot issue again.")
            return
        self.books[book_id]["available"] = False
        self.borrows[book_id] = student_id
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.borrow_log.append({
            "action": "ISSUED",
            "book_id": book_id,
            "book_title": self.books[book_id]["title"],
            "student_id": student_id,
            "student_name": self.students[student_id],
            "timestamp": timestamp
        })
        print(f"  [+] Book '{self.books[book_id]['title']}' issued to {self.students[student_id]} on {timestamp}.")
        self.save_data()

    # 6 - Return Book
    def return_book(self, book_id: str, student_id: str) -> None:
        if book_id not in self.books:
            print(f"  [!] Book ID '{book_id}' not found.")
            return
        if self.books[book_id]["available"]:
            print(f"  [!] Book '{self.books[book_id]['title']}' was not issued.")
            return
        if self.borrows.get(book_id) != student_id:
            actual = self.borrows.get(book_id, "someone else")
            print(f"  [!] This book was issued to {actual}, not {student_id}.")
            return
        self.books[book_id]["available"] = True
        del self.borrows[book_id]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.borrow_log.append({
            "action": "RETURNED",
            "book_id": book_id,
            "book_title": self.books[book_id]["title"],
            "student_id": student_id,
            "student_name": self.students[student_id],
            "timestamp": timestamp
        })
        print(f"  [+] Book '{self.books[book_id]['title']}' returned by {self.students[student_id]} on {timestamp}.")
        self.save_data()

    # 7 - Display Borrow Log
    def display_borrow_log(self) -> None:
        if not self.borrow_log:
            print("  [!] No borrow activity recorded yet.")
            return
        print("\n" + "-" * 80)
        print(f"  {'Action':<10} {'Book ID':<10} {'Title':<22} {'Student ID':<12} {'Name':<15} {'Timestamp'}")
        print("-" * 80)
        for entry in self.borrow_log:
            print(f"  {entry['action']:<10} {entry['book_id']:<10} {entry['book_title']:<22} {entry['student_id']:<12} {entry['student_name']:<15} {entry['timestamp']}")
        print("-" * 80)

    # 8 - Save Data to File
    def save_data(self) -> None:
        data = {
            "books": self.books,
            "students": self.students,
            "borrows": self.borrows,
            "borrow_log": self.borrow_log
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    # 9 - Load Data from File
    def load_data(self) -> None:
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        self.books = data.get("books", {})
        self.students = data.get("students", {})
        self.borrows = data.get("borrows", {})
        self.borrow_log = data.get("borrow_log", [])
        print("  [+] Previous data loaded from file.")


DATA_FILE = "library_data.json"


# Menu driven program
def main():
    lib = Library()

    # Sample data - preloaded for demonstration
    # Books
    if not lib.books:
        lib.add_book("B001", "Python Basics", "Guido Van Rossum")
        lib.add_book("B002", "Data Structures", "Mark Allen")
        lib.add_book("B003", "DBMS Concepts", "Korth Silberschatz")

    # Students - updated names as requested
    if not lib.students:
        lib.add_student("STU001", "Gupta")
        lib.add_student("STU002", "Kuldeep")
        lib.add_student("STU003", "Varateja")

    while True:
        print("\n=========================================")
        print("     SMART LIBRARY MANAGEMENT SYSTEM     ")
        print("=========================================")
        print("  1. Add Book")
        print("  2. Display All Books")
        print("  3. Add Student")
        print("  4. Display All Students")
        print("  5. Issue Book")
        print("  6. Return Book")
        print("  7. View Borrow Log")
        print("  8. Exit")
        print("-----------------------------------------")

        choice = input("  Enter your choice (1-8): ").strip()

        if choice == "1":
            print("\n-- Add Book --")
            book_id = input("  Enter Book ID: ").strip()
            title = input("  Enter Title: ").strip()
            author = input("  Enter Author: ").strip()
            lib.add_book(book_id, title, author)

        elif choice == "2":
            print("\n-- All Books --")
            lib.display_books()

        elif choice == "3":
            print("\n-- Add Student --")
            student_id = input("  Enter Student ID (e.g. STU001): ").strip()
            name = input("  Enter Student Name: ").strip()
            lib.add_student(student_id, name)

        elif choice == "4":
            print("\n-- All Students --")
            lib.display_students()

        elif choice == "5":
            print("\n-- Issue Book --")
            book_id = input("  Enter Book ID: ").strip()
            student_id = input("  Enter Student ID: ").strip()
            lib.issue_book(book_id, student_id)

        elif choice == "6":
            print("\n-- Return Book --")
            book_id = input("  Enter Book ID: ").strip()
            student_id = input("  Enter Student ID: ").strip()
            lib.return_book(book_id, student_id)

        elif choice == "7":
            print("\n-- Borrow Log --")
            lib.display_borrow_log()

        elif choice == "8":
            print("\n  Exiting... Goodbye!")
            break

        else:
            print("\n  [!] Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
