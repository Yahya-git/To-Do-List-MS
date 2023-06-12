import json
from datetime import datetime

import httpx
from config import settings
from dtos import dto_misc, dto_reports, dto_tasks, dto_users
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from utils import validate_user

app = FastAPI()


users_url = settings.users_service_url
tasks_url = settings.tasks_service_url


depends = Depends()
validated_user = Depends(validate_user)


@app.get("/")
def root():
    return {"Hello World!"}


async def make_request(
    method,
    url,
    current_user: int = None,
    params=None,
    data=None,
    json=None,
):
    if current_user:
        headers = {"email": current_user.email, "uid": str(current_user.id)}
    else:
        headers = None
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        response = await client.request(
            method, url, params=params, data=data, json=json
        )
        if response.status_code == 204:
            return response
        if response.status_code >= 400:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        response_data = response.json()
    return response_data


@app.post("/users", response_model=dto_misc.UserSingleResponse[dto_users.UserResponse])
async def create_user(user: dto_users.CreateUserRequest):
    response_data = await make_request("POST", f"{users_url}/users", json=user.dict())
    return response_data


@app.post("/login", response_model=dto_misc.TokenResponse)
async def login(user: OAuth2PasswordRequestForm = depends):
    response_data = await make_request("POST", f"{users_url}/login", data=user.__dict__)
    return response_data


@app.get("/verify-email")
async def verify_email(token: int):
    params = {"token": token}
    response_data = await make_request(
        "GET", f"{users_url}/users/verify-email", params=params
    )
    return response_data


@app.get("/users/{id}/reset-password-request")
async def reset_password_request(id: int):
    params = {"id": id}
    response_data = await make_request(
        "GET", f"{users_url}/users/{id}/reset-password-request", params=params
    )
    return response_data


@app.get("/users/{id}/reset-password")
async def reset_password(id: int, token: int):
    params = {"id": id, "token": token}
    response_data = await make_request(
        "GET", f"{users_url}/users/{id}/reset-password", params=params
    )
    return response_data


@app.put(
    "/users/{id}", response_model=dto_misc.UserSingleResponse[dto_users.UserResponse]
)
async def update_user(
    id: int, user: dto_users.UpdateUserRequest, current_user: int = validated_user
):
    response_data = await make_request(
        "PUT",
        f"{users_url}/users/{id}",
        params={"id": id},
        json=user.dict(),
        current_user=current_user,
    )
    return response_data


def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


@app.post("/tasks", response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse])
async def create_task(
    task: dto_tasks.CreateTaskRequest, current_user: int = validated_user
):
    json_data = json.dumps(task.dict(), default=custom_encoder)
    response_data = await make_request(
        "POST", f"{tasks_url}/tasks", data=json_data, current_user=current_user
    )
    return response_data


@app.put(
    "/tasks/{id}", response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse]
)
async def update_task(
    id: int, task: dto_tasks.UpdateTaskRequest, current_user: int = validated_user
):
    json_data = json.dumps(task.dict(), default=custom_encoder)
    response_data = await make_request(
        "PUT", f"{tasks_url}/tasks/{id}", data=json_data, current_user=current_user
    )
    return response_data


@app.delete("/tasks/{id}")
async def delete_task(id: int, current_user: int = validated_user):
    response = await make_request(
        "DELETE", f"{tasks_url}/tasks/{id}", current_user=current_user
    )
    if response.status_code == 204:
        return {"message": "successfully deleted task"}


@app.get("/tasks", response_model=dto_misc.TaskMultipleResponse[dto_tasks.TaskResponse])
async def get_tasks(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/tasks", current_user=current_user
    )
    return response_data


@app.get("/tasks/all")
async def get_tasks_and_user(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/tasks/all", current_user=current_user
    )
    return response_data


@app.get(
    "/tasks/similar",
    response_model=dto_misc.TaskMultipleResponse[dto_tasks.SimilarTaskResponse],
)
async def get_similar_tasks(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/tasks/similar", current_user=current_user
    )
    return response_data


@app.get(
    "/tasks/{id}", response_model=dto_misc.TaskSingleResponse[dto_tasks.TaskResponse]
)
async def get_task(id: int, current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/tasks/{id}", current_user=current_user
    )
    return response_data


@app.get(
    "/reports/count",
    response_model=dto_misc.ReportSingleResponse[dto_reports.CountReportResponse],
)
async def get_count_report(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/reports/count", current_user=current_user
    )
    return response_data


@app.get(
    "/reports/average",
    response_model=dto_misc.ReportSingleResponse[dto_reports.AverageReportResponse],
)
async def get_average_report(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/reports/average", current_user=current_user
    )
    return response_data


@app.get(
    "/reports/overdue",
    response_model=dto_misc.ReportSingleResponse[dto_reports.OverdueReportResponse],
)
async def get_overdue_report(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/reports/overdue", current_user=current_user
    )
    return response_data


@app.get(
    "/reports/max",
    response_model=dto_misc.ReportSingleResponse[dto_reports.DateMaxReportResponse],
)
async def get_max_report(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/reports/max", current_user=current_user
    )
    return response_data


@app.get(
    "/reports/day",
    response_model=dto_misc.ReportMultipleResponse[dto_reports.DayTasksReportResponse],
)
async def get_day_report(current_user: int = validated_user):
    response_data = await make_request(
        "GET", f"{tasks_url}/reports/day", current_user=current_user
    )
    return response_data
