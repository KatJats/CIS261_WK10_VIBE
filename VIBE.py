import os
import sys

DATA_FILE = "student_grades.txt"


class Student:
    def __init__(self, name: str, student_id: str, test_scores: list[float]):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.test_scores = test_scores
        self.average = self.calculate_average()
        self.grade = self.calculate_letter_grade()

    def calculate_average(self) -> float:
        if not self.test_scores:
            return 0.0
        return sum(self.test_scores) / len(self.test_scores)

    def calculate_letter_grade(self) -> str:
        avg = self.average
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    def to_record(self) -> str:
        return "|".join([
            self.name,
            self.student_id,
            f"{self.test_scores[0]:.2f}",
            f"{self.test_scores[1]:.2f}",
            f"{self.test_scores[2]:.2f}",
            f"{self.average:.2f}",
            self.grade,
        ])


def load_student_records(filename: str) -> list[Student]:
    students: list[Student] = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) != 7:
                    print(f"Skipping invalid record on line {line_number}: wrong number of fields")
                    continue
                name, student_id, *score_parts, average_str, grade = parts
                try:
                    scores = [float(score_parts[0]), float(score_parts[1]), float(score_parts[2])]
                    student = Student(name, student_id, scores)
                    students.append(student)
                except ValueError:
                    print(f"Skipping invalid scores on line {line_number}: {line}")
    except IOError as error:
        print(f"Error loading student records from {filename}: {error}")
    return students


def save_student_records(filename: str, students: list[Student]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_record() + "\n")
        print(f"Saved {len(students)} student record(s) to {filename}.")
    except IOError as error:
        print(f"Error saving student records to {filename}: {error}")


def prompt_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            raise KeyboardInterrupt
        try:
            score = float(value)
            if score < 0 or score > 100:
                print("Please enter a score between 0 and 100.")
                continue
            return score
        except ValueError:
            print("Invalid number. Please enter a valid numeric score.")


def prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            raise KeyboardInterrupt
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def add_new_student(students: list[Student]) -> None:
    print("\nAdd New Student Record")
    print("Enter ESC at any prompt to return to the main menu.")
    try:
        name = prompt_non_empty("Student name: ")
        student_id = prompt_non_empty("Student ID: ")
        test_scores = [
            prompt_float("Test 1 score: "),
            prompt_float("Test 2 score: "),
            prompt_float("Test 3 score: "),
        ]
    except KeyboardInterrupt:
        print("Returning to main menu.")
        return

    student = Student(name, student_id, test_scores)
    students.append(student)
    print(f"Added {student.name} with average {student.average:.2f} and grade {student.grade}.")


def display_students(students: list[Student]) -> None:
    if not students:
        print("\nNo student records available.")
        return

    print("\nStudent Records")
    print("--------------------------------------------------------------------------------")
    print("Name                 | ID        | Test 1 | Test 2 | Test 3 | Average | Grade")
    print("--------------------------------------------------------------------------------")
    for student in students:
        print(
            f"{student.name:<20} | {student.student_id:<9} | "
            f"{student.test_scores[0]:>6.2f} | {student.test_scores[1]:>6.2f} | "
            f"{student.test_scores[2]:>6.2f} | {student.average:>7.2f} | {student.grade}"
        )
    print("--------------------------------------------------------------------------------")


def display_statistics(students: list[Student]) -> None:
    if not students:
        print("\nNo class statistics available because there are no student records.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_avg = sum(averages) / len(averages)

    print("\nClass Statistics")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_avg:.2f}")


def search_student(students: list[Student]) -> None:
    if not students:
        print("\nNo student records available to search.")
        return

    search_name = input("Enter student name to search (case-insensitive): ").strip()
    if not search_name:
        print("Search term cannot be empty.")
        return

    print(f"\nSearch results for '{search_name}':")
    found = [student for student in students if search_name.lower() in student.name.lower()]
    if not found:
        print("No matching student records found.")
        return

    for student in found:
        print(
            f"Name: {student.name}, ID: {student.student_id}, "
            f"Avg: {student.average:.2f}, Grade: {student.grade}"
        )


def display_menu() -> None:
    print("\nStudent Grade Calculator")
    print("1. Add new student record")
    print("2. Display all student records")
    print("3. Display class statistics")
    print("4. Search student by name")
    print("5. Save student records")
    print("ESC. Exit program")


def get_menu_choice() -> str:
    prompt = "Choose an option (1-5) or press ESC to exit: "
    try:
        choice = input(prompt).strip()
        if choice.upper() == "ESC":
            return "ESC"
        return choice
    except (KeyboardInterrupt, EOFError):
        return "ESC"


def main() -> None:
    students = load_student_records(DATA_FILE)
    if students:
        print(f"Loaded {len(students)} student record(s) from {DATA_FILE}.")
    else:
        print("No existing student records found. Starting with an empty class list.")

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "ESC":
            print("Exiting program.")
            break
        if choice == "1":
            add_new_student(students)
            continue
        if choice == "2":
            display_students(students)
            continue
        if choice == "3":
            display_statistics(students)
            continue
        if choice == "4":
            search_student(students)
            continue
        if choice == "5":
            save_student_records(DATA_FILE, students)
            continue

        print("Invalid option. Please choose 1-5 or press ESC to exit.")

    print("Saving records before exit...")
    save_student_records(DATA_FILE, students)
    print("Goodbye!")


if __name__ == "__main__":
    main()
