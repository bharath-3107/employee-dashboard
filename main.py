from db_setup import setup_database
import queries as q
from utils import print_table

def main():
    setup_database()

    while True:
        print("\n📊 EMPLOYEE DASHBOARD")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Add Performance Record")
        print("4. Add Attendance Record")
        print("5. Show KPI Dashboard")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            eid = int(input("Employee ID: "))
            name = input("Name: ")
            dept = input("Department: ")
            doj = input("Date of Joining (YYYY-MM-DD): ")
            q.add_employee(eid, name, dept, doj)

        elif choice == '2':
            data = q.view_employees()
            print_table(data, ["ID", "Name", "Dept", "DOJ"])

        elif choice == '3':
            eid = int(input("Employee ID: "))
            score = float(input("Performance Score (0-10): "))
            date = input("Review Date (YYYY-MM-DD): ")
            q.add_performance(eid, score, date)

        elif choice == '4':
            eid = int(input("Employee ID: "))
            date = input("Date (YYYY-MM-DD): ")
            status = input("Status (Present/Absent): ")
            q.add_attendance(eid, date, status)

        elif choice == '5':
            data = q.calculate_kpis()
            print_table(data, ["ID", "Name", "Avg Score", "Attendance %"])

        elif choice == '6':
            print("Exiting... 🚀")
            break

        else:
            print("Invalid input. Try again.")

if __name__ == "__main__":
    main()
