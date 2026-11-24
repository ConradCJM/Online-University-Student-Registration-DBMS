

from connection.core.OracleConnection import Connection
from commandlinetest.create_tables import create_tables
from commandlinetest.drop_tables import drop_tables
from commandlinetest.populate_tables import populate_tables
from commandlinetest.queries import run_queries

MENU = """
=================================================================
|                   Oracle All Inclusive Tool                   |
|              Main Menu - Select Desired Operation(s):         |
-----------------------------------------------------------------
  M) View Manual

  1) Drop Tables
  2) Create Tables
  3) Populate Tables
  4) Query Tables

  E) End/Exit
"""

MANUAL = """
Manual
------
1) Drop Tables      - removes every table (and its constraints)
2) Create Tables    - creates the schema
3) Populate Tables  - inserts the sample data
4) Query Tables     - runs the queries and creates the views
E) Exit             - closes the database session
"""


def pause():
    input("Press Enter to continue...")


connection = Connection()
cursor, conn = connection.create_session()

# Loop
try:
    while True:
        print(MENU)
        choice = input("Choose: ").strip().upper()

        if choice == "M":
            print(MANUAL)
            pause()
        elif choice == "1":
            drop_tables(cursor, conn)
            pause()
        elif choice == "2":
            create_tables(cursor, conn)
            pause()
        elif choice == "3":
            populate_tables(cursor, conn)
            pause()
        elif choice == "4":
            run_queries(cursor, conn)
            pause()
        elif choice == "E":
            break
        else:
            print("Invalid choice.")
except KeyboardInterrupt:
    print("\nInterrupted.")
finally:
    connection.close_session()