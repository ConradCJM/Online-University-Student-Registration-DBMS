import oracledb


# (table name, primary-key columns)
TABLE_KEYS = [
    ("Account", ("AccountID",)),
    ("Admin", ("AccountID",)),
    ("CourseCatalog", ("CatalogID",)),
    ("Faculty", ("FacultyID",)),
    ("Department", ("DepartmentID",)),
    ("Professor", ("ProfessorID",)),
    ("Student", ("AccountID",)),
    ("Course", ("CourseID",)),
    ("FacultyUsesAdmin", ("FacultyID", "AccountID")),
    ("DepartmentUsesAdmin", ("DepartmentID", "AccountID")),
    ("AdminManages", ("AccountID", "CatalogID")),
    ("Antirequisite", ("CourseID", "AntirequisiteID")),
    ("Prerequisite", ("CourseID", "PrerequisiteID")),
    ("Section", ("CourseID", "SectionNumber")),
    ("Schedule", ("CourseID", "SectionNumber", "DayName", "StartTime")),
    ("CourseEntry", ("CatalogID", "CourseID")),
    ("Teaches", ("ProfessorID", "CourseID", "SectionNumber")),
    ("Transcript", ("AccountID", "CourseID", "Year", "Semester")),
    ("EnrollInto", ("StudentNumber", "CourseID", "SectionNumber")),
    ("WaitListInto", ("StudentNumber", "CourseID", "SectionNumber")),
]

NUMBER_COLUMNS = {"CatalogID", "FacultyID", "DepartmentID", "ProfessorID",
                  "SectionNumber", "Year", "StudentNumber"}


def delete_rows(cursor, conn):
    print("\n===== DELETE ROW =====")
    for index, (table, _) in enumerate(TABLE_KEYS, start=1):
        print(f"{index}) {table}")
    print("0) Cancel")

    try:
        choice = int(input("Choose table: ").strip())
        if choice == 0:
            return
        table, keys = TABLE_KEYS[choice - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return

    values = {}
    try:
        for column in keys:
            prompt = f"{column} (days hh:mm:ss, e.g. 0 09:00:00): " if column == "StartTime" else f"{column}: "
            raw_value = input(prompt).strip()
            values[column] = int(raw_value) if column in NUMBER_COLUMNS else raw_value
    except ValueError:
        print("Invalid number.")
        return

    where = " AND ".join(
        f"{column} = TO_DSINTERVAL(:{column})" if column == "StartTime"
        else f"{column} = :{column}"
        for column in keys
    )
    sql = f"DELETE FROM {table} WHERE {where}"
    try:
        cursor.execute(sql, values)
        deleted = cursor.rowcount
        if deleted:
            conn.commit()
            print(f"Deleted {deleted} row(s) from {table}.")
        else:
            conn.rollback()
            print(f"No matching row found in {table}.")
    except oracledb.DatabaseError as error:
        conn.rollback()
        print(f"Could not delete from {table}: {error}")
