import json
from datetime import datetime

import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from utils import validate_user

from config import settings
from dtos import dto_misc, dto_tasks, dto_users

app = FastAPI()


users_url = settings.users_service_url
tasks_url = settings.tasks_service_url


depends = Depends()
validated_user = Depends(validate_user)


@app.get("/")
def root():
    return {"Hello World!"}


@app.post("/users", response_model=dto_misc.UserSingleResponse[dto_users.UserResponse])
async def create_user(user: dto_users.CreateUserRequest):
    async with httpx.AsyncClient() as client:
        client.follow_redirects = False
        response = await client.post(f"{users_url}/users", json=user.dict())
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.post(redirect_url, json=user.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.post("/login", response_model=dto_misc.TokenResponse)
async def login(user: OAuth2PasswordRequestForm = depends):
    async with httpx.AsyncClient() as client:
        client.follow_redirects = False
        response = await client.post(f"{users_url}/login", data=user.__dict__)
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.post(redirect_url, data=user.__dict__)
        if response.status_code != 202:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.get("/verify-email")
async def verify_email(token: int):
    async with httpx.AsyncClient() as client:
        client.follow_redirects = False
        params = {"token": token}
        response = await client.get(f"{users_url}/users/verify-email", params=params)
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.get(redirect_url, params=params)
        if response.status_code != 202:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.get("/users/{id}/reset-password-request")
async def reset_password_request(id: int):
    async with httpx.AsyncClient() as client:
        client.follow_redirects = False
        params = {"id": id}
        response = await client.get(
            f"{users_url}/users/{id}/reset-password-request", params=params
        )
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.get(redirect_url, params=params)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.get("/users/{id}/reset-password")
async def reset_password(id: int, token: int):
    async with httpx.AsyncClient() as client:
        client.follow_redirects = False
        params = {"id": id, "token": token}
        response = await client.get(
            f"{users_url}/users/{id}/reset-password", params=params
        )
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.get(redirect_url, params=params)
        if response.status_code != 202:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.put(
    "/users/{id}", response_model=dto_misc.UserSingleResponse[dto_users.UserResponse]
)
async def update_user(
    id: int, user: dto_users.UpdateUserRequest, current_user: int = validated_user
):
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized for this",
        )
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        params = {"id": id}
        response = await client.put(
            f"{users_url}/users/{id}", params=params, json=user.dict()
        )
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.put(redirect_url, params=params, json=user.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


@app.post("/tasks", response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse])
async def create_task(
    task: dto_tasks.CreateTaskRequest, current_user: int = validated_user
):
    headers = {"email": current_user.email, "id": str(current_user.id)}
    json_data = json.dumps(task.dict(), default=custom_encoder)
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        response = await client.post(f"{tasks_url}/tasks", data=json_data)
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.post(redirect_url, data=json_data)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.put(
    "/tasks/{id}", response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse]
)
async def update_task(
    id: int, task: dto_tasks.UpdateTaskRequest, current_user: int = validated_user
):
    headers = {"email": current_user.email, "id": str(current_user.id)}
    json_data = json.dumps(task.dict(), default=custom_encoder)
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        response = await client.put(f"{tasks_url}/tasks/{id}", data=json_data)
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.put(redirect_url, data=json_data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.delete("/tasks/{id}")
async def delete_task(id: int, current_user: int = validated_user):
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        response = await client.delete(f"{tasks_url}/tasks/{id}")
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.delete(redirect_url)
        if response.status_code != 204:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"message": "successfully deleted task"}


@app.get("/tasks", response_model=dto_misc.TaskMultipleResponse[dto_tasks.TaskResponse])
async def get_tasks(current_user: int = validated_user):
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        response = await client.get(f"{tasks_url}/tasks")
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.get(redirect_url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.get(
    "/tasks/similar",
    response_model=dto_misc.TaskMultipleResponse[dto_tasks.SimilarTaskResponse],
)
async def get_similar_tasks(current_user: int = validated_user):
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        response = await client.get(f"{tasks_url}/tasks/similar")
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.get(redirect_url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.get(
    "/tasks/{id}", response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse]
)
async def get_task(id: int, current_user: int = validated_user):
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers) as client:
        client.follow_redirects = False
        response = await client.get(f"{tasks_url}/tasks/{id}")
        if response.status_code == 307:
            redirect_url = response.headers["location"]
            response = await client.get(redirect_url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data