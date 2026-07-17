import csv
import os

SUBJECTS = ["Math", "Physics", "English", "Computer", "Urdu"]
PASSING_AVERAGE = 50

students = []


def calculate_average(grades):
    return round(sum(grades.values()) / len(grades), 2)


def get_status(avg):
    return "PASS" if avg >= PASSING_AVERAGE else "FAIL"


def generate_id():
    if not students:
        return 1
    return max(student["id"] for student in students) + 1


def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Invalid name!")
        return

    for student in students:
        if student["name"].lower() == name.lower():
            print("Student already exists!")
            return

    grades = {}

    for subject in SUBJECTS:
        while True:
            try:
                marks = float(input(f"{subject}: "))
                if 0 <= marks <= 100:
                    grades[subject] = marks
                    break
                else:
                    print("Marks must be between 0 and 100.")
            except ValueError:
                print("Enter numeric value only.")

    student_record = {
        "id": generate_id(),
        "name": name,
        "grades": grades
    }

    students.append(student_record)

    avg = calculate_average(grades)
    print(f"\n{name} added successfully.")
    print("Average:", avg)
    print("Status:", get_status(avg))


def view_students():
    if not students:
        print("No student records found.")
        return

    print("\n" + "=" * 90)

    header = f"{'ID':<5}{'Name':<20}"
    for subject in SUBJECTS:
        header += f"{subject:<10}"

    header += f"{'Average':<10}{'Result'}"
    print(header)

    print("=" * 90)

    for student in students:
        row = f"{student['id']:<5}{student['name']:<20}"

        for subject in SUBJECTS:
            row += f"{student['grades']<10}"

        avg = calculate_average(student["grades"])
        row += f"{avg:<10}{get_status(avg)}"

        print(row)


def search_student():
    keyword = input("Enter student name: ").strip().lower()

    found = False

    for student in students:
        if keyword in student["name"].lower():
            found = True

            print("\nStudent Found")
            print("ID:", student["id"])
            print("Name:", student["name"])

            for subject, marks in student["grades"].items():
                print(f"{subject}: {marks}")

            avg = calculate_average(student["grades"])
            print("Average:", avg)
            print("Status:", get_status(avg))

    if not found:
        print("Student not found.")


def edit_grades():
    if not students:
        print("No records available.")
        return

    view_students()

    try:
        student_id = int(input("\nEnter ID to edit: "))
    except ValueError:
        print("Invalid ID.")
        return

    selected = None

    for student in students:
        if student["id"] == student_id:
            selected = student
            break

    if not selected:
        print("Student not found.")
        return

    subject = input("Enter subject name: ").title()

    if subject not in SUBJECTS:
        print("Invalid subject.")
        return

    try:
        new_marks = float(input("Enter new marks: "))

        if 0 <= new_marks <= 100:
            selected["grades"][subject] = new_marks
            print("Grade updated successfully.")
        else:
            print("Marks must be between 0 and 100.")

    except ValueError:
        print("Invalid input.")


def class_report():
    if not students:
        print("No data available.")
        return

    ranking = []

    for student in students:
        avg = calculate_average(student["grades"])
        ranking.append((student["name"], avg))

    ranking.sort(key=lambda item: item[1], reverse=True)

    averages = [item[1] for item in ranking]

    print("\nCLASS REPORT")
    print("-" * 30)
    print("Total Students:", len(students))
    print("Highest Average:", max(averages))
    print("Lowest Average:", min(averages))
    print("Class Average:", round(sum(averages) / len(averages), 2))

    print("\nRANKINGS")

    for index, data in enumerate(ranking, start=1):
        print(f"{index}. {data[0]} -> {data[1]}")


def save_data():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["ID", "Name"] + SUBJECTS)

        for student in students:
            row = [student["id"], student["name"]]

            for subject in SUBJECTS:
                row.append(student["grades"][subject])

            writer.writerow(row)

    print("Data saved successfully.")


def load_data():
    if not os.path.exists("students.csv"):
        return

    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            grades = {}

            for subject in SUBJECTS:
                grades[subject] = float(row[subject])

            students.append({
                "id": int(row["ID"]),
                "name": row["Name"],
                "grades": grades
            })


def delete_student():
    try:
        student_id = int(input("Enter ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            print("Student deleted.")
            return

    print("Student not found.")


def menu():
    load_data()

    while True:
        print("\n===== STUDENT GRADE MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Edit Grades")
        print("5. Class Report")
        print("6. Save Data")
        print("7. Delete Student")
        print("8. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            edit_grades()

        elif choice == "5":
            class_report()

        elif choice == "6":
            save_data()

        elif choice == "7":
            delete_student()

        elif choice == "8":
            save_data()
            print("Good Bye!")
            break

        else:
            print("Invalid choice.")


menu()
