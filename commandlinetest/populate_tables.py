from commandlinetest.helpers import run_statements

STATEMENTS = [
    # ACCOUNTS
    "INSERT INTO Account VALUES ('A1001', 'John Smith', 'jsmith', 'pass1')",
    "INSERT INTO Account VALUES ('A1002', 'Sarah Lee', 'slee', 'pass2')",
    "INSERT INTO Account VALUES ('A1003', 'Mike Chen', 'mchen', 'pass3')",
    "INSERT INTO Account VALUES ('A1004', 'Emma Davis', 'edavis', 'pass4')",
    "INSERT INTO Account VALUES ('A1005', 'David Brown', 'dbrown', 'pass5')",
    "INSERT INTO Account VALUES ('A1006', 'Sophia Wilson', 'swilson', 'pass6')",
    # ADMINS
    "INSERT INTO Admin VALUES ('A1001')",
    "INSERT INTO Admin VALUES ('A1002')",
    # FACULTY
    "INSERT INTO Faculty VALUES (1, 'Science', 'Kerr Hall')",
    "INSERT INTO Faculty VALUES (2, 'Engineering', 'ENG Building')",
    "INSERT INTO Faculty VALUES (3, 'Business', 'TRSM')",
    # DEPARTMENT
    "INSERT INTO Department VALUES (101, 'Computer Science', 1)",
    "INSERT INTO Department VALUES (102, 'Mathematics', 1)",
    "INSERT INTO Department VALUES (201, 'Electrical Engineering', 2)",
    "INSERT INTO Department VALUES (301, 'Accounting', 3)",
    # FACULTYUSESADMIN
    "INSERT INTO FacultyUsesAdmin VALUES (1, 'A1001')",
    "INSERT INTO FacultyUsesAdmin VALUES (2, 'A1001')",
    "INSERT INTO FacultyUsesAdmin VALUES (3, 'A1002')",
    # DEPARTMENTUSESADMIN
    "INSERT INTO DepartmentUsesAdmin VALUES (101, 'A1001')",
    "INSERT INTO DepartmentUsesAdmin VALUES (102, 'A1001')",
    "INSERT INTO DepartmentUsesAdmin VALUES (201, 'A1002')",
    "INSERT INTO DepartmentUsesAdmin VALUES (301, 'A1002')",
    # COURSE CATALOGS
    "INSERT INTO CourseCatalog VALUES (1, 'Fall 2026 Catalog')",
    "INSERT INTO CourseCatalog VALUES (2, 'Winter 2027 Catalog')",
    # ADMIN MANAGES
    "INSERT INTO AdminManages VALUES ('A1001', 1, 'Created Catalog', TIMESTAMP '2026-08-01 10:00:00')",
    "INSERT INTO AdminManages VALUES ('A1002', 2, 'Updated Catalog', TIMESTAMP '2026-08-15 14:30:00')",
    # PROFESSORS
    "INSERT INTO Professor VALUES (1001, 'Dr. Kumar', 101)",
    "INSERT INTO Professor VALUES (1002, 'Dr. Wilson', 101)",
    "INSERT INTO Professor VALUES (1003, 'Dr. Johnson', 102)",
    "INSERT INTO Professor VALUES (1004, 'Dr. Taylor', 201)",
    # STUDENTS
    "INSERT INTO Student VALUES ('A1003', 'Computer Science', 2, DATE '2005-03-15', 50001)",
    "INSERT INTO Student VALUES ('A1004', 'Computer Science', 3, DATE '2004-09-20', 50002)",
    "INSERT INTO Student VALUES ('A1005', 'Mathematics', 1, DATE '2006-01-11', 50003)",
    "INSERT INTO Student VALUES ('A1006', 'Computer Science', 4, DATE '2003-11-25', 50004)",
    # COURSES
    "INSERT INTO Course VALUES ('CPS510', 'Database Systems', 4.0, 101)",
    "INSERT INTO Course VALUES ('CPS420', 'Discrete Mathematics', 3.0, 101)",
    "INSERT INTO Course VALUES ('MTH110', 'Calculus I', 3.0, 102)",
    "INSERT INTO Course VALUES ('ELE202', 'Circuit Analysis', 4.0, 201)",
    # COURSE ENTRIES
    "INSERT INTO CourseEntry VALUES (1, 'CPS510')",
    "INSERT INTO CourseEntry VALUES (1, 'CPS420')",
    "INSERT INTO CourseEntry VALUES (1, 'MTH110')",
    "INSERT INTO CourseEntry VALUES (2, 'CPS510')",
    "INSERT INTO CourseEntry VALUES (2, 'ELE202')",
    # PREREQUISITES / ANTIREQUISITES
    "INSERT INTO Prerequisite VALUES ('CPS510', 'CPS420')",
    "INSERT INTO Antirequisite VALUES ('CPS420', 'MTH110')",
    # SECTIONS
    "INSERT INTO Section VALUES ('CPS510', 1, 2026, 'Fall')",
    "INSERT INTO Section VALUES ('CPS510', 2, 2026, 'Fall')",
    "INSERT INTO Section VALUES ('CPS420', 1, 2026, 'Fall')",
    "INSERT INTO Section VALUES ('MTH110', 1, 2026, 'Fall')",
    "INSERT INTO Section VALUES ('ELE202', 1, 2026, 'Fall')",
    # SCHEDULES
    """INSERT INTO Schedule VALUES ('CPS510', 1, 'Monday',
        INTERVAL '09:00:00' HOUR TO SECOND, INTERVAL '12:00:00' HOUR TO SECOND, 'ENG201')""",
    """INSERT INTO Schedule VALUES ('CPS510', 2, 'Wednesday',
        INTERVAL '14:00:00' HOUR TO SECOND, INTERVAL '17:00:00' HOUR TO SECOND, 'ENG202')""",
    """INSERT INTO Schedule VALUES ('CPS420', 1, 'Monday',
        INTERVAL '10:00:00' HOUR TO SECOND, INTERVAL '12:00:00' HOUR TO SECOND, 'KHE101')""",
    """INSERT INTO Schedule VALUES ('MTH110', 1, 'Friday',
        INTERVAL '08:00:00' HOUR TO SECOND, INTERVAL '10:00:00' HOUR TO SECOND, 'KHE202')""",
    # TEACHES
    "INSERT INTO Teaches VALUES (1001, 'CPS510', 1)",
    "INSERT INTO Teaches VALUES (1002, 'CPS510', 2)",
    "INSERT INTO Teaches VALUES (1001, 'CPS420', 1)",
    "INSERT INTO Teaches VALUES (1003, 'MTH110', 1)",
    # ENROLLMENTS
    "INSERT INTO EnrollInto VALUES (50001, 'CPS510', 1)",
    "INSERT INTO EnrollInto VALUES (50002, 'CPS510', 1)",
    "INSERT INTO EnrollInto VALUES (50004, 'CPS510', 2)",
    "INSERT INTO EnrollInto VALUES (50001, 'CPS420', 1)",
    "INSERT INTO EnrollInto VALUES (50002, 'CPS420', 1)",
    "INSERT INTO EnrollInto VALUES (50003, 'MTH110', 1)",
    # WAITLIST
    "INSERT INTO WaitListInto VALUES (50003, 'CPS510', 1)",
    "INSERT INTO WaitListInto VALUES (50004, 'CPS420', 1)",
    # TRANSCRIPTS
    "INSERT INTO Transcript VALUES ('A1003', 'CPS420', 2025, 'Fall', 'A')",
    "INSERT INTO Transcript VALUES ('A1003', 'CPS510', 2025, 'Fall', 'B-')",
    "INSERT INTO Transcript VALUES ('A1004', 'CPS420', 2025, 'Fall', 'B+')",
    "INSERT INTO Transcript VALUES ('A1004', 'CPS510', 2025, 'Fall', 'A+')",
    "INSERT INTO Transcript VALUES ('A1004', 'MTH110', 2025, 'Fall', 'C+')",
    "INSERT INTO Transcript VALUES ('A1005', 'MTH110', 2025, 'Winter', 'A-')",
    "INSERT INTO Transcript VALUES ('A1005', 'CPS420', 2025, 'Winter', 'D-')",
]


def populate_tables(cursor, conn):
    run_statements(cursor, STATEMENTS)
    conn.commit()
    print("Tables populated.")