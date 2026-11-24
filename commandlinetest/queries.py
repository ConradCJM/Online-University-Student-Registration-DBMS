from commandlinetest.helpers import print_query, run_statements

# (title, sql, optional description)
BASIC_QUERIES = [
    ("ACCOUNT", "SELECT DISTINCT Name FROM Account ORDER BY Name ASC"),
    ("ADMIN", """SELECT Account.Name FROM Admin adm, Account
                 WHERE adm.AccountID = Account.AccountID
                 ORDER BY Account.Name ASC"""),
    ("FACULTY USES ADMIN", "SELECT FacultyID, AccountID FROM FacultyUsesAdmin ORDER BY FacultyID ASC"),
    ("DEPARTMENT USES ADMIN", "SELECT DepartmentID, AccountID FROM DepartmentUsesAdmin ORDER BY DepartmentID ASC"),
    ("FACULTY", "SELECT FacultyID, Name FROM Faculty ORDER BY Name ASC"),
    ("DEPARTMENT", "SELECT DepartmentID, Name FROM Department ORDER BY Name ASC"),
    ("ADMIN MANAGES", """SELECT CatalogID, AccountID, TimeStamp FROM AdminManages
                         WHERE ActionType = 'Updated Catalog'
                         ORDER BY CatalogID ASC, TimeStamp DESC"""),
    ("ALL ADMIN ACTIONS", """SELECT CatalogID, AccountID, TimeStamp FROM AdminManages
                             ORDER BY CatalogID ASC, TimeStamp DESC"""),
    ("COURSE CATALOG", """SELECT cc.CatalogID, COUNT(ce.CourseID) AS CourseCount
                          FROM CourseCatalog cc, CourseEntry ce
                          WHERE cc.CatalogID = ce.CatalogID
                          GROUP BY cc.CatalogID ORDER BY cc.CatalogID ASC"""),
    ("CATALOG ENTRIES", "SELECT CourseID FROM CourseEntry WHERE CatalogID = 1 ORDER BY CourseID ASC"),
    ("STUDENT", """SELECT * FROM Student WHERE DeclaredMajor = 'Computer Science'
                   ORDER BY StudentNumber ASC"""),
    ("ENROLLMENT COUNTS", """SELECT CourseID, COUNT(StudentNumber) AS Enrolled FROM EnrollInto
                             GROUP BY CourseID ORDER BY COUNT(StudentNumber) DESC"""),
    ("WAITLIST COUNTS", """SELECT CourseID, COUNT(StudentNumber) AS Waitlisted FROM WaitListInto
                           GROUP BY CourseID ORDER BY COUNT(StudentNumber) DESC"""),
    ("TRANSCRIPT", """SELECT AccountID, CourseID, Grade FROM Transcript
                      WHERE Grade IS NOT NULL ORDER BY AccountID"""),
    ("PROFESSORS", "SELECT ProfessorID, Name FROM Professor WHERE DepartmentID = 101 ORDER BY Name ASC"),
    ("TEACHES", """SELECT ProfessorID, CourseID, SectionNumber FROM Teaches
                   WHERE CourseID = 'CPS510' ORDER BY ProfessorID ASC"""),
    ("COURSES IN FALL", """SELECT CourseID, CourseName FROM Course
                           WHERE CourseID IN (SELECT CourseID FROM Section WHERE Semester = 'Fall')
                           ORDER BY CourseID ASC"""),
    ("ANTIREQUISITES", "SELECT CourseID FROM Antirequisite WHERE AntirequisiteID = 'MTH110' ORDER BY CourseID ASC"),
    ("PREREQUISITES", "SELECT CourseID FROM Prerequisite WHERE PrerequisiteID = 'CPS420' ORDER BY CourseID ASC"),
    ("CPS510 SECTIONS", "SELECT CourseID, SectionNumber FROM Section WHERE CourseID = 'CPS510' ORDER BY SectionNumber ASC"),
    ("MONDAY CLASSES", "SELECT CourseID, SectionNumber FROM Schedule WHERE DayName = 'Monday' ORDER BY SectionNumber ASC"),
    ("ADVANCED QUERY 1", """SELECT a.AccountID FROM Admin a, FacultyUsesAdmin fua, Faculty f
                            WHERE f.Name = 'Science'
                            AND a.AccountID = fua.AccountID
                            AND fua.FacultyID = f.FacultyID"""),
    ("ADVANCED QUERY 2", """SELECT a.AccountID FROM Admin a, DepartmentUsesAdmin dua, Department d
                            WHERE d.Name = 'Computer Science'
                            AND a.AccountID = dua.AccountID
                            AND dua.DepartmentID = d.DepartmentID"""),
    ("ADVANCED QUERY 3", """SELECT a.AccountID FROM Admin a, AdminManages am, CourseCatalog cc
                            WHERE cc.CatalogName = 'Fall 2026 Catalog'
                            AND a.AccountID = am.AccountID
                            AND am.CatalogID = cc.CatalogID"""),
]

# (title, CREATE VIEW sql, SELECT sql to show it)
VIEWS = [
    ("CREATE VIEW: CATALOG COURSES",
     """CREATE OR REPLACE VIEW CatalogCourses AS
        SELECT CourseCatalog.CatalogID, Course.CourseID, Course.CourseName
        FROM CourseCatalog
        JOIN CourseEntry ON CourseCatalog.CatalogID = CourseEntry.CatalogID
        JOIN Course ON CourseEntry.CourseID = Course.CourseID""",
     "SELECT * FROM CatalogCourses ORDER BY CatalogID, CourseID"),
    ("CREATE VIEW: COURSE SECTIONS",
     """CREATE OR REPLACE VIEW CourseSections AS
        SELECT c.CourseID, c.CourseName, s.SectionNumber, s.Semester
        FROM Course c
        JOIN Section s ON c.CourseID = s.CourseID""",
     "SELECT * FROM CourseSections"),
    ("CREATE VIEW: TRANSLATED GRADES",
     """CREATE OR REPLACE VIEW TranslatedGrades AS
        SELECT AccountID, CourseID, Grade,
               CASE Grade
                   WHEN 'A+' THEN 4.33 WHEN 'A' THEN 4.00 WHEN 'A-' THEN 3.67
                   WHEN 'B+' THEN 3.33 WHEN 'B' THEN 3.00 WHEN 'B-' THEN 2.67
                   WHEN 'C+' THEN 2.33 WHEN 'C' THEN 2.00 WHEN 'C-' THEN 1.67
                   WHEN 'D+' THEN 1.33 WHEN 'D' THEN 1.00 WHEN 'D-' THEN 0.67
                   WHEN 'F' THEN 0
                   ELSE 0
               END AS GPA
        FROM Transcript""",
     "SELECT * FROM TranslatedGrades"),
    ("CREATE VIEW: CGPA TABLE",
     """CREATE OR REPLACE VIEW CGPATable AS
        SELECT tg.AccountID,
               SUM(tg.GPA * c.CreditHours) / SUM(c.CreditHours) AS CGPA
        FROM TranslatedGrades tg
        JOIN Course c ON tg.CourseID = c.CourseID
        GROUP BY tg.AccountID""",
     "SELECT * FROM CGPATable ORDER BY AccountID"),
]

# (title, description, sql)
SHOWCASE_QUERIES = [
    ("EXISTS QUERY", "Students enrolled in at least one course",
     """SELECT s.StudentNumber, a.Name FROM Student s, Account a
        WHERE EXISTS (SELECT 1 FROM EnrollInto e
                      WHERE e.StudentNumber = s.StudentNumber
                      AND a.AccountID = s.AccountID)"""),
    ("UNION QUERY", "Courses that have enrolled or waitlisted students",
     """SELECT CourseID FROM EnrollInto
        UNION
        SELECT CourseID FROM WaitListInto"""),
    ("MINUS QUERY", "Courses with enrolled students but no waitlist",
     """SELECT CourseID FROM EnrollInto
        MINUS
        SELECT CourseID FROM WaitListInto"""),
    ("COUNT GROUP BY HAVING QUERY", "Courses with more than one enrolled student",
     """SELECT CourseID, COUNT(StudentNumber) AS TotalStudents
        FROM EnrollInto GROUP BY CourseID HAVING COUNT(StudentNumber) > 1"""),
    ("AVG QUERY", "Average academic year per major",
     """SELECT DeclaredMajor, AVG(CurrentAcademicYear) AS AvgYear
        FROM Student GROUP BY DeclaredMajor"""),
    ("VIEW + AVG QUERY", "Average CGPA by major using CGPATable view",
     """SELECT s.DeclaredMajor, ROUND(AVG(cg.CGPA), 2) AS AverageCGPA
        FROM CGPATable cg, Student s
        WHERE cg.AccountID = s.AccountID
        GROUP BY s.DeclaredMajor
        ORDER BY AverageCGPA DESC"""),
]


def run_queries(cursor, conn):
    for item in BASIC_QUERIES:
        print_query(cursor, *item)

    for title, create_sql, select_sql in VIEWS:
        print(f"\n===== {title} =====")
        run_statements(cursor, [create_sql])
        print_query(cursor, title.replace("CREATE VIEW: ", "VIEW: "), select_sql)

    for title, description, sql in SHOWCASE_QUERIES:
        print_query(cursor, title, sql, note=description)