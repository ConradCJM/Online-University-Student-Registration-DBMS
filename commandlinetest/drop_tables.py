from commandlinetest.helpers import run_statements

TABLES = [
    "WaitListInto", "EnrollInto", "Transcript", "Teaches", "CourseEntry",
    "Schedule", "Prerequisite", "Antirequisite", "AdminManages",
    "DepartmentUsesAdmin", "FacultyUsesAdmin",
    "Section", "Student", "Professor",
    "Course", "Department", "Faculty", "CourseCatalog",
    "Admin", "Account",
]


def drop_tables(cursor, conn):
    # Ignore errors so tables that don't exist yet are skipped quietly
    run_statements(
        cursor,
        [f"DROP TABLE {t} CASCADE CONSTRAINTS" for t in TABLES],
        ignore_errors=True,
    )
    conn.commit()
    print("Tables dropped.")