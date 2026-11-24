from pydantic import BaseModel

class CourseCreate(BaseModel):
    id: str
    name: str
    creditHours: float
    department_id: int  # Foreign key ID

class CourseResponse(BaseModel):
    id: str
    name: str
    creditHours: float
    department_id: int