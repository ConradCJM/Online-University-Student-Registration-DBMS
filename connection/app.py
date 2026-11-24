from core.OracleConnection import Connection
from schemas import course_schema
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import oracledb

connection = Connection()
cursor, conn = connection.create_session()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/courses")
def get_courses():
    cursor.execute("SELECT CourseID, CourseName FROM COURSE")
    return [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

@app.post("/courses")
def create_course(crs: course_schema):
    try:
        cursor.execute(
            "INSERT INTO COURSE VALUES (:1, :2, :3, :4)",
            [crs.name, crs.id, crs.creditHours, crs.department_id]
        )
        conn.commit()
        return {"message": "Course added"}
    except oracledb.IntegrityError:
        # Catches ORA-02291 if the frontend sends a department_id that doesn't exist
        raise HTTPException(status_code=400, detail="Invalid department_id: Department does not exist.")