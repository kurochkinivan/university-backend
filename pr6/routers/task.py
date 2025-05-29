from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dto.task import (
    TaskCreateDTO,
    TaskUpdateDTO,
    TaskCompleteDTO,
    TaskResponseDTO
)
from services import task as task_service
from database import get_db

router = APIRouter(tags=['tasks'])

@router.post('/', response_model=TaskResponseDTO)
async def create_task(data: TaskCreateDTO, db: Session = Depends(get_db)):
    return task_service.create_task(data, db)

@router.get('/', response_model=list[TaskResponseDTO])
async def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)

@router.get('/{id}', response_model=TaskResponseDTO)
async def get_task(id: int, db: Session = Depends(get_db)):
    task = task_service.get_task(id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put('/{id}', response_model=TaskResponseDTO)
async def update_task(id: int, data: TaskUpdateDTO, db: Session = Depends(get_db)):
    task = task_service.update_task(id, data, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch('/{id}/complete', response_model=TaskResponseDTO)
async def complete_task(id: int, data: TaskCompleteDTO, db: Session = Depends(get_db)):
    task = task_service.complete_task(id, data, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete('/{id}', response_model=TaskResponseDTO)
async def delete_task(id: int, db: Session = Depends(get_db)):
    task = task_service.remove_task(id, db)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task