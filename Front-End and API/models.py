from sqlalchemy import Column, Integer, String, Float,Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    sub_code = Column(String,  nullable=False)
    sub_name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship("Student", back_populates="subject")
    
    
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sem = Column(String, nullable=False)
    srn = Column(String, unique=True, nullable=False)
    cgpa = Column(Float, nullable=False)
    isa = relationship("ISA", back_populates="student")
    subject = relationship("Subject", back_populates="student")



class ISA(Base):
    __tablename__ = 'isa'

    id = Column(Integer, primary_key=True, index=True)
    no_of_isa = Column(Integer, nullable=False)
    isa_score = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    student = relationship("Student",back_populates="isa")


class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    placements_id = Column(Integer, ForeignKey('placements.id'))

class Placements(Base):
    __tablename__ = 'placements'

    id = Column(Integer, primary_key=True, index=True)
    current = Column(String)
    offered = Column(String)

class Remainder(Base):
    __tablename__ = 'remainder'

    id = Column(Integer, primary_key=True, index=True)
    noremainder = Column(Boolean, nullable=False)
