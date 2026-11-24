import oracledb


def run_statements(cursor, statements, ignore_errors=False):
    """Execute a list of SQL statements (no trailing semicolons)."""
    for sql in statements:
        try:
            cursor.execute(sql)
        except oracledb.DatabaseError as e:
            if ignore_errors:
                continue
            first_line = sql.strip().splitlines()[0]
            print(f"Error running: {first_line}\n  {e}")


def print_query(cursor, title, sql, note=None):
    """Run a SELECT and print the result as a simple table."""
    print(f"\n===== {title} =====")
    if note:
        print(note)
    try:
        cursor.execute(sql)
        cols = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
    except oracledb.DatabaseError as e:
        print(f"Error: {e}")
        return

    str_rows = [["" if v is None else str(v) for v in r] for r in rows]
    widths = [len(c) for c in cols]
    for r in str_rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(v))

    print("  ".join(c.ljust(widths[i]) for i, c in enumerate(cols)))
    print("  ".join("-" * w for w in widths))
    for r in str_rows:
        print("  ".join(v.ljust(widths[i]) for i, v in enumerate(r)))
    print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")