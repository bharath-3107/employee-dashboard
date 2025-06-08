# app.py
import streamlit as st
import sqlite3
import pandas as pd 
import os

DB_PATH = DB_PATH = os.path.join(os.getcwd(), "employee.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            dept TEXT,
            doj TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER,
            score REAL,
            review_date TEXT,
            FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER,
            date TEXT,
            status TEXT CHECK(status IN ('Present', 'Absent')),
            FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
        )
    ''')

    conn.commit()
    conn.close()

def add_employee(emp_id, name, dept, doj):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO Employees VALUES (?, ?, ?, ?)", (emp_id, name, dept, doj))
    conn.commit()
    conn.close()

def add_performance(emp_id, score, review_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Performance(emp_id, score, review_date) VALUES (?, ?, ?)", (emp_id, score, review_date))
    conn.commit()
    conn.close()

def add_attendance(emp_id, date, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO Attendance(emp_id, date, status) VALUES (?, ?, ?)", (emp_id, date, status))
    conn.commit()
    conn.close()

def fetch_employees():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM Employees", conn)
    conn.close()
    return df

def fetch_kpis():
    conn = get_connection()
    query = """
        SELECT e.emp_id, e.name, e.dept,
            ROUND(AVG(p.score), 2) AS avg_score,
            ROUND(SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END)*100.0/COUNT(a.status), 2) AS attendance_percent
        FROM Employees e
        LEFT JOIN Performance p ON e.emp_id = p.emp_id
        LEFT JOIN Attendance a ON e.emp_id = a.emp_id
        GROUP BY e.emp_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def main():
    st.title("🚀 Employee Performance Dashboard")

    init_db()

    menu = ["Add Employee", "Add Performance", "Add Attendance", "View Employees", "View KPIs"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add Employee":
        st.header("Add New Employee")
        with st.form("employee_form"):
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            name = st.text_input("Name")
            dept = st.text_input("Department")
            doj = st.date_input("Date of Joining")
            submitted = st.form_submit_button("Add Employee")

            if submitted:
                add_employee(emp_id, name, dept, doj.strftime('%Y-%m-%d'))
                st.success(f"Employee {name} added.")

    elif choice == "Add Performance":
        st.header("Add Performance Record")
        with st.form("performance_form"):
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            score = st.slider("Performance Score", 0.0, 10.0, 5.0, 0.1)
            review_date = st.date_input("Review Date")
            submitted = st.form_submit_button("Add Performance")

            if submitted:
                add_performance(emp_id, score, review_date.strftime('%Y-%m-%d'))
                st.success("Performance record added.")

    elif choice == "Add Attendance":
        st.header("Add Attendance Record")
        with st.form("attendance_form"):
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            date = st.date_input("Date")
            status = st.selectbox("Status", ["Present", "Absent"])
            submitted = st.form_submit_button("Add Attendance")

            if submitted:
                add_attendance(emp_id, date.strftime('%Y-%m-%d'), status)
                st.success("Attendance record added.")

    elif choice == "View Employees":
        st.header("All Employees")
        df = fetch_employees()
        st.dataframe(df)

    elif choice == "View KPIs":
        st.header("KPI Dashboard")
        df = fetch_kpis()
        st.dataframe(df)

if __name__ == "__main__":
    main()
