import sqlite3

def setup_database():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    # Create Employees Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            emp_id INTEGER PRIMARY KEY,
            name TEXT,
            dept TEXT,
            doj TEXT
        )
    ''')

    # Create Performance Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id INTEGER,
            score REAL,
            review_date TEXT,
            FOREIGN KEY(emp_id) REFERENCES Employees(emp_id)
        )
    ''')

    # Create Attendance Table
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
