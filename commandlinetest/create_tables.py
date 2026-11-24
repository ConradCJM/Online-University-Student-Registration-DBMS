from commandlinetest.helpers import run_statements

STATEMENTS = [
    """CREATE TABLE Account(
        AccountID VARCHAR2(10) PRIMARY KEY,
        Name VARCHAR2(50) NOT NULL,
        Username VARCHAR2(50) NOT NULL,
        Password VARCHAR2(255) NOT NULL
    )""",
    """CREATE TABLE Admin(
        AccountID VARCHAR2(10) PRIMARY KEY,
        FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
    )""",
    """CREATE TABLE CourseCatalog(
        CatalogID INT PRIMARY KEY,
        CatalogName VARCHAR2(255) NOT NULL
    )""",
    """CREATE TABLE Faculty(
        FacultyID INT PRIMARY KEY,
        Name VARCHAR2(50) NOT NULL,
        Location VARCHAR2(255) NOT NULL
    )""",
    """CREATE TABLE Department(
        DepartmentID INT PRIMARY KEY,
        Name VARCHAR2(50) NOT NULL,
        FacultyID INT REFERENCES Faculty(FacultyID)
    )""",
    """CREATE TABLE Professor(
        ProfessorID INT PRIMARY KEY,
        Name VARCHAR2(50) NOT NULL,
        DepartmentID INT REFERENCES Department(DepartmentID)
    )""",
    """CREATE TABLE Student(
        AccountID VARCHAR2(10) PRIMARY KEY REFERENCES Account(AccountID),
        DeclaredMajor VARCHAR2(30) NOT NULL,
        CurrentAcademicYear INT NOT NULL,
        DateOfBirth DATE NOT NULL,
        StudentNumber INT UNIQUE NOT NULL
    )""",
    """CREATE TABLE Course(
        CourseID VARCHAR2(10) PRIMARY KEY,
        CourseName VARCHAR2(255) NOT NULL,
        CreditHours DECIMAL(2,1) NOT NULL,
        DepartmentID INT REFERENCES Department(DepartmentID)
    )""",
    """CREATE TABLE FacultyUsesAdmin(
        FacultyID INT REFERENCES Faculty(FacultyID),
        AccountID VARCHAR2(10) REFERENCES Admin(AccountID),
        PRIMARY KEY(FacultyID, AccountID)
    )""",
    """CREATE TABLE DepartmentUsesAdmin(
        DepartmentID INT REFERENCES Department(DepartmentID),
        AccountID VARCHAR2(10) REFERENCES Admin(AccountID),
        PRIMARY KEY(DepartmentID, AccountID)
    )""",
    """CREATE TABLE AdminManages(
        AccountID VARCHAR2(10) REFERENCES Admin(AccountID),
        CatalogID INT REFERENCES CourseCatalog(CatalogID),
        ActionType VARCHAR2(255) NOT NULL,
        TimeStamp TIMESTAMP,
        PRIMARY KEY(AccountID, CatalogID)
    )""",
    """CREATE TABLE Antirequisite(
        CourseID VARCHAR2(10) REFERENCES Course(CourseID) ON DELETE CASCADE,
        AntirequisiteID VARCHAR2(10) REFERENCES Course(CourseID) ON DELETE CASCADE,
        PRIMARY KEY(CourseID, AntirequisiteID)
    )""",
    """CREATE TABLE Prerequisite(
        CourseID VARCHAR2(10) REFERENCES Course(CourseID) ON DELETE CASCADE,
        PrerequisiteID VARCHAR2(10) REFERENCES Course(CourseID) ON DELETE CASCADE,
        PRIMARY KEY(CourseID, PrerequisiteID)
    )""",
    """CREATE TABLE Section(
        CourseID VARCHAR2(10),
        SectionNumber INT,
        Year INT NOT NULL,
        Semester VARCHAR2(255) NOT NULL,
        PRIMARY KEY(CourseID, SectionNumber),
        FOREIGN KEY(CourseID) REFERENCES Course(CourseID) ON DELETE CASCADE
    )""",
    """CREATE TABLE Schedule(
        CourseID VARCHAR2(10),
        SectionNumber INT,
        DayName VARCHAR2(10),
        StartTime INTERVAL DAY(0) TO SECOND(0),
        EndTime INTERVAL DAY(0) TO SECOND(0) NOT NULL,
        Location VARCHAR2(50) NOT NULL,
        PRIMARY KEY(CourseID, SectionNumber, DayName, StartTime),
        FOREIGN KEY(CourseID, SectionNumber)
            REFERENCES Section(CourseID, SectionNumber) ON DELETE CASCADE
    )""",
    """CREATE TABLE CourseEntry(
        CatalogID INT REFERENCES CourseCatalog(CatalogID) ON DELETE CASCADE,
        CourseID VARCHAR2(10) REFERENCES Course(CourseID) ON DELETE CASCADE,
        PRIMARY KEY(CatalogID, CourseID)
    )""",
    """CREATE TABLE Teaches(
        ProfessorID INT REFERENCES Professor(ProfessorID),
        CourseID VARCHAR2(10),
        SectionNumber INT,
        PRIMARY KEY(ProfessorID, CourseID, SectionNumber),
        FOREIGN KEY(CourseID, SectionNumber)
            REFERENCES Section(CourseID, SectionNumber) ON DELETE CASCADE
    )""",
    """CREATE TABLE Transcript(
        AccountID VARCHAR2(10) REFERENCES Account(AccountID),
        CourseID VARCHAR2(10) REFERENCES Course(CourseID),
        Year INT,
        Semester VARCHAR2(255),
        Grade VARCHAR2(2),
        PRIMARY KEY(AccountID, CourseID, Year, Semester)
    )""",
    """CREATE TABLE EnrollInto(
        StudentNumber INT REFERENCES Student(StudentNumber),
        CourseID VARCHAR2(10),
        SectionNumber INT,
        PRIMARY KEY(StudentNumber, CourseID, SectionNumber),
        FOREIGN KEY(CourseID, SectionNumber)
            REFERENCES Section(CourseID, SectionNumber) ON DELETE CASCADE
    )""",
    """CREATE TABLE WaitListInto(
        StudentNumber INT REFERENCES Student(StudentNumber),
        CourseID VARCHAR2(10),
        SectionNumber INT,
        PRIMARY KEY(StudentNumber, CourseID, SectionNumber),
        FOREIGN KEY(CourseID, SectionNumber)
            REFERENCES Section(CourseID, SectionNumber) ON DELETE CASCADE
    )""",
]


def create_tables(cursor, conn):
    run_statements(cursor, STATEMENTS)
    conn.commit()
    print("Tables created.")