import oracledb

from commandlinetest.delete_rows import NUMBER_COLUMNS, TABLE_KEYS


# Columns that can be changed for each table. Primary-key columns identify the row.
UPDATE_COLUMNS = {
    "Account": ("Name", "Username", "Password"),
    "Admin": (),
    "CourseCatalog": ("CatalogName",),
    "Faculty": ("Name", "Location"),
    "Department": ("Name", "FacultyID"),
    "Professor": ("Name", "DepartmentID"),
    "Student": ("DeclaredMajor", "CurrentAcademicYear", "DateOfBirth", "StudentNumber"),
    "Course": ("CourseName", "CreditHours", "DepartmentID"),
    "FacultyUsesAdmin": (),
    "DepartmentUsesAdmin": (),
    "AdminManages": ("ActionType", "TimeStamp"),
    "Antirequisite": (),
    "Prerequisite": (),
    "Section": ("Year", "Semester"),
    "Schedule": ("EndTime", "Location"),
    "CourseEntry": (),
    "Teaches": (),
    "Transcript": ("Grade",),
    "EnrollInto": (),
    "WaitListInto": (),
}

NUMBER_COLUMNS = NUMBER_COLUMNS | {"CurrentAcademicYear"}


def _read_value(column):
    prompt = f"{column} (days hh:mm:ss, e.g. 0 09:00:00): " if column in {"StartTime", "EndTime"} else f"{column}: "
    value = input(prompt).strip()
    if column in NUMBER_COLUMNS:
        return int(value)
    if column == "CreditHours":
        return float(value)
    return value


def _sql_value(column):
    if column in {"StartTime", "EndTime"}:
        return f"TO_DSINTERVAL(:{column})"
    if column == "DateOfBirth":
        return f"TO_DATE(:{column}, 'YYYY-MM-DD')"
    if column == "TimeStamp":
        return f"TO_TIMESTAMP(:{column}, 'YYYY-MM-DD HH24:MI:SS')"
    return f":{column}"


def update_rows(cursor, conn):
    print("\n===== UPDATE ROW =====")
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

    columns = UPDATE_COLUMNS[table]
    if not columns:
        print(f"{table} has no non-key columns to update.")
        return

    values = {}
    try:
        for column in keys:
            values[column] = _read_value(column)
        print("Columns:")
        for index, column in enumerate(columns, start=1):
            print(f"{index}) {column}")
        column_choice = int(input("Choose column: ").strip())
        column = columns[column_choice - 1]
        values[column] = _read_value(column)
    except (ValueError, IndexError):
        print("Invalid choice or value.")
        return

    where = " AND ".join(f"{key} = {_sql_value(key)}" for key in keys)
    sql = f"UPDATE {table} SET {column} = {_sql_value(column)} WHERE {where}"
    try:
        cursor.execute(sql, values)
        updated = cursor.rowcount
        if updated:
            conn.commit()
            print(f"Updated {updated} row(s) in {table}.")
        else:
            conn.rollback()
            print(f"No matching row found in {table}.")
    except oracledb.DatabaseError as error:
        conn.rollback()
        print(f"Could not update {table}: {error}")
