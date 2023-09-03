from pydantic import BaseModel
from typing import Dict, List, Union

class StudentModel(BaseModel):
    id: int
    name: str
    sem: int
    srn: str
    cgpa: float
    class Config:
        from_attributes = True
    
class SubjectModel(BaseModel):
    sub_code: str
    sub_name: str
    student_id:int
    class Config:
        from_attributes = True


class ISAModel(BaseModel):
    no_of_isa: int
    isa_score: int
    student_id: int
    class Config:
        from_attributes = True


class PlacementModel(BaseModel):
    current: List[str]
    offered: List[str]

class NotificationsModel(BaseModel):
    placements: PlacementModel

class RemainderModel(BaseModel):
    noremainder: bool

class StudentShowModel(BaseModel):
    name: str
    sem: int
    srn: str
    cgpa: float
    isa: List[ISAModel] = []
    class Config:
        from_attributes = True
    # placement_info:PlacementModel
    # notifications: NotificationsModel
    # remainder: RemainderModel
