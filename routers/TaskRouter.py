from fastapi import APIRouter
from sqlalchemy import select
from database import new_session

from models import Task
from schemas import STaskAdd, STask, STaskId


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks


@router.get("/{row_id}")
async def get_task_by_id(row_id: int) -> STask:
    task = await TaskRepository.get_by_id(row_id)
    return task


@router.post("")
async def add_task(
        task: STaskAdd
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


class TaskRepository:
    @classmethod
    async def get_by_id(cls, row_id: int) -> STask:
        async with new_session() as session:
            query = select(Task).where(Task.id == row_id)
            result = await session.execute(query)
            task_model = result.scalars().first()
            # task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            task_schema = STask.model_validate(task_model)
            return task_schema

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(Task).order_by(Task.name)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas

    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()
            task = Task(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id
