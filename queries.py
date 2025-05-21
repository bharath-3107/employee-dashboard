import sqlite3

def connect():
    return sqlite3.connect('employee.db')

def add_employee(emp_id, name, dept, doj):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Employees VALUES (?, ?, ?, ?)", (emp_id, name, dept, doj))
    conn.commit()
    conn.close()

def view_employees():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Employees")
    data = cur.fetchall()
    conn.close()
    return data

def add_performance(emp_id, score, review_date):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Performance(emp_id, score, review_date) VALUES (?, ?, ?)", (emp_id, score, review_date))
    conn.commit()
    conn.close()

def add_attendance(emp_id, date, status):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Attendance(emp_id, date, status) VALUES (?, ?, ?)", (emp_id, date, status))
    conn.commit()
    conn.close()

def calculate_kpis():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.emp_id, e.name,
            ROUND(AVG(p.score), 2) AS avg_score,
            ROUND(SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END)*100.0/COUNT(a.status), 2) AS attendance_percent
        FROM Employees e
        LEFT JOIN Performance p ON e.emp_id = p.emp_id
        LEFT JOIN Attendance a ON e.emp_id = a.emp_id
        GROUP BY e.emp_id
    """)
    data = cur.fetchall()
    conn.close()
    return data
