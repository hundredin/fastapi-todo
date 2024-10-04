from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.db import get_db
import api.cruds.done as done_crud

router = APIRouter()


@router.put("/tasks/{task_id}/done")
async def mark_task_as_done(task_id: int, db: Session = Depends(get_db)):
    done = await done_crud.get_done(db, task_id)
    if done is not None:
        raise HTTPException(status_code=400, detail="Task already done")

    return await done_crud.create_done(db, task_id)


@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done(task_id: int, db: Session = Depends(get_db)):
    done = await done_crud.get_done(db, task_id=task_id)
    if done is None:
        raise HTTPException(status_code=404, detail="Task not done")

    return await done_crud.delete_done(db, original=done)
