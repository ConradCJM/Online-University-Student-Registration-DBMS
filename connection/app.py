from core.OracleConnection import Connection
from schemas.course_schema import CourseCreate
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import oracledb

connection = Connection()
cursor, conn = connection.create_session()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health/db")
def check_database():
    try:
        cursor.execute("SELECT 1 FROM DUAL")
        return {"database": "connected"}
    except oracledb.Error as error:
        raise HTTPException(status_code=503, detail="Oracle Database query failed.") from error

@app.get("/courses")
def get_courses():
    cursor.execute("SELECT CourseID, CourseName FROM COURSE")
    return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

@app.post("/courses")
def create_course(crs: CourseCreate):
    try:
        cursor.execute(
            "INSERT INTO COURSE VALUES (:1, :2, :3, :4)",
            [crs.id, crs.name, crs.creditHours, crs.department_id]
        )
        conn.commit()
        return {"message": "Course added"}
    except oracledb.IntegrityError:
        # Catches ORA-02291 if the frontend sends a department_id that doesn't exist
        raise HTTPException(status_code=400, detail="Invalid department_id: Department does not exist.")
