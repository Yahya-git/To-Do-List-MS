from typing import Optional

import httpx
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session
from src.config import settings
from src.database import get_db
from src.dtos import dto_misc, dto_tasks
from src.handler import tasks as handler

router = APIRouter(prefix="/tasks", tags=["Tasks"])

get_db_session = Depends(get_db)
users_url = settings.users_service_url


# Create Task Endpoint
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse],
)
async def create_task(
    task_data: dto_tasks.CreateTaskRequest,
    request: Request,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    task = handler.create_task(task_data, db, current_user)
    return {"status": "successfully created task", "data": {"task": task}}


# Update Task Endpoint
@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse],
)
async def update_task(
    id: int,
    task_data: dto_tasks.UpdateTaskRequest,
    request: Request,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    task = handler.update_task(id, task_data, db, current_user)
    return {"status": "successfully updated task", "data": {"task": task}}


# Delete Task Endpoint
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: int,
    request: Request,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    return handler.delete_task(id, db, current_user)


# Get Tasks Endpoint
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.TaskMultipleResponse[dto_tasks.TaskResponse],
)
async def get_tasks(
    request: Request,
    db: Session = get_db_session,
    search: Optional[str] = "",
    sort: Optional[str] = "due_date",
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    tasks = handler.get_tasks(db, current_user, search, sort)
    return {"status": "success", "data": {"tasks": tasks}}


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
)
async def get_tasks_and_user(request: Request, db: Session = get_db_session):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    tasks = handler.get_tasks(db, current_user)
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(f"{users_url}/users")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        user = response.json()
    return {"tasks": tasks, "user": user}


@router.get(
    "/similar",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.TaskMultipleResponse[dto_tasks.SimilarTaskResponse],
)
async def get_similar_tasks(
    request: Request,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    tasks = handler.get_similar_tasks(db, current_user)
    return {"status": "similar tasks found", "data": {"tasks": tasks}}


# Get Task Endpoint
@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse],
)
async def get_task(
    id: int,
    request: Request,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    task = handler.get_task(id, db, current_user)
    return {"status": "success", "data": {"task": task}}


file = File(...)


# Upload File to Task Endpoint
@router.post(
    "/{task_id}/file",
    status_code=status.HTTP_201_CREATED,
)
async def upload_file(
    task_id: int,
    request: Request,
    file: UploadFile = file,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    return await handler.upload_file(task_id, file, db, current_user)


# Download File from Task Endpoint
@router.get(
    "/{task_id}/file/{file_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def download_file(
    task_id: int,
    file_id: int,
    request: Request,
    db: Session = get_db_session,
):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    return await handler.download_file(task_id, file_id, db, current_user)
