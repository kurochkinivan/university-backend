from models.task import Task
from sqlalchemy.orm import Session
from dto.task import TaskCreateDTO, TaskUpdateDTO, TaskCompleteDTO

def create_task(data: TaskCreateDTO, db: Session) -> Task:
    task = Task(
        title=data.title,
        description=data.description,
        is_completed=False
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()

def get_task(id: int, db: Session) -> Task | None:
    return db.query(Task).get(id)

def update_task(id: int, data: TaskUpdateDTO, db: Session) -> Task | None:
    task = db.query(Task).get(id)
    if not task:
        return None
    
    if data.title is not None:
        task.title = data.title
    if data.description is not None:
        task.description = data.description
    
    db.commit()
    db.refresh(task)
    return task

def complete_task(id: int, data: TaskCompleteDTO, db: Session) -> Task | None:
    task = db.query(Task).get(id)
    if not task:
        return None
    
    task.is_completed = data.is_completed
    db.commit()
    db.refresh(task)
    return task

def remove_task(id: int, db: Session) -> Task | None:
    task = db.query(Task).get(id)
    if not task:
        return None
    
    db.delete(task)
    db.commit()
    return task