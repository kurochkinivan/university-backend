from pydantic import BaseModel
from datetime import datetime

class TaskCreateDTO(BaseModel):
    title: str 
    description: str | None = None

class TaskUpdateDTO(BaseModel):
    title: str | None = None  
    description: str | None = None

class TaskCompleteDTO(BaseModel):
    is_completed: bool

class TaskResponseDTO(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  