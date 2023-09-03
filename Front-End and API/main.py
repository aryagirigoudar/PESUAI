from fastapi import FastAPI, Depends

from database import Base, SessionLocal
import models, schemas
from sqlalchemy.orm import Session
from database import engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/Admin/Student', tags =["Admin"])
def create_student(request:schemas.StudentModel, db : Session = Depends(get_db)):
    new_student = models.Student(name=request.name,sem=request.sem,srn=request.srn,cgpa=request.cgpa)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.post('/Admin/Subject', tags =["Admin"])
def create_student(request:schemas.SubjectModel, db : Session = Depends(get_db)):
    sub_new = models.Subject(sub_code=request.sub_code,sub_name=request.sub_name,student_id=request.student_id)
    db.add(sub_new)
    db.commit()
    db.refresh(sub_new)
    return sub_new

@app.post('/Admin/ISA', tags =["Admin"])
def create_student(request:schemas.ISAModel, db : Session = Depends(get_db)):
    isa_result = models.ISA(no_of_isa=request.no_of_isa,isa_score=request.isa_score,student_id=request.student_id)
    db.add(isa_result)
    db.commit()
    db.refresh(isa_result)
    return isa_result

@app.get('/Show_Student_data/{id}',response_model=schemas.StudentShowModel, tags =["Student"])
def show_student_data(id:int,db:Session = Depends(get_db)):
    error = "ERROR"
    user = db.query(models.Student).filter(models.Student.id == id).first()
    if not user:
        return error
    return user




