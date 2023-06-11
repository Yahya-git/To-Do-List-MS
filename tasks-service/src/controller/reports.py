import pickle

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from src.config import settings
from src.database import get_db
from src.dtos import dto_misc, dto_reports
from src.handler import reports as handler
from src.redis import redis_client

router = APIRouter(prefix="/reports", tags=["Reports"])

get_db_session = Depends(get_db)
users_url = settings.users_service_url


@router.get(
    "/count",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.ReportSingleResponse[dto_reports.CountReportResponse],
)
def count_tasks(request: Request, db: Session = get_db_session):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    cache_key = f"task_count_report_user_{current_user.id}"
    cache_data = redis_client.get(cache_key)
    if cache_data:
        print("Cache Hit!")
        report = pickle.loads(cache_data)
    else:
        print("Cache Miss!!!")
        report = handler.count_tasks(db, current_user)
        redis_client.setex(cache_key, settings.cache_expiry_time, pickle.dumps(report))
    response = {"status": "success", "data": {"report": report}}
    return response


@router.get(
    "/average",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.ReportSingleResponse[dto_reports.AverageReportResponse],
)
async def average_tasks(request: Request, db: Session = get_db_session):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    headers = {"email": current_user.email, "id": str(current_user.id)}
    async with httpx.AsyncClient(headers=headers, follow_redirects=True) as client:
        response = await client.get(f"{users_url}/users")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        current_user = response.json()
    current_user = dto_misc.UserResponse(**current_user)
    cache_key = f"task_average_report_user_{current_user.id}"
    cache_data = redis_client.get(cache_key)
    if cache_data:
        print("Cache Hit!")
        report = pickle.loads(cache_data)
    else:
        print("Cache Miss!!!")
        report = handler.average_tasks(db, current_user)
        redis_client.setex(cache_key, settings.cache_expiry_time, pickle.dumps(report))
    response = {"status": "success", "data": {"report": report}}
    return response


@router.get(
    "/overdue",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.ReportSingleResponse[dto_reports.OverdueReportResponse],
)
def overdue_tasks(request: Request, db: Session = get_db_session):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    cache_key = f"task_overdue_report_user_{current_user.id}"
    cache_data = redis_client.get(cache_key)
    if cache_data:
        print("Cache Hit!")
        report = pickle.loads(cache_data)
    else:
        print("Cache Miss!!!")
        report = handler.overdue_tasks(db, current_user)
        redis_client.setex(cache_key, settings.cache_expiry_time, pickle.dumps(report))
    response = {"status": "success", "data": {"report": report}}
    return response


@router.get(
    "/max",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.ReportSingleResponse[dto_reports.DateMaxReportResponse],
)
def date_max_tasks(request: Request, db: Session = get_db_session):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    cache_key = f"task_date_max_report_user_{current_user.id}"
    cache_data = redis_client.get(cache_key)
    if cache_data:
        print("Cache Hit!")
        report = pickle.loads(cache_data)
    else:
        print("Cache Miss!!!")
        report = handler.date_max_tasks(db, current_user)
        redis_client.setex(cache_key, settings.cache_expiry_time, pickle.dumps(report))
    response = {"status": "success", "data": {"report": report}}
    return response


@router.get(
    "/day",
    status_code=status.HTTP_200_OK,
    response_model=dto_misc.ReportMultipleResponse[dto_reports.DayTasksReportResponse],
)
def day_of_week_tasks(request: Request, db: Session = get_db_session):
    headers = request.headers
    user_email = headers.get("email")
    user_id = int(headers.get("id"))
    current_user = dto_misc.CurrentUser(email=user_email, id=user_id)
    cache_key = f"task_day_of_week_report_user_{current_user.id}"
    cache_data = redis_client.get(cache_key)
    if cache_data:
        print("Cache Hit!")
        reports = pickle.loads(cache_data)
    else:
        print("Cache Miss!!!")
        reports = handler.day_of_week_tasks(db, current_user)
        redis_client.setex(cache_key, settings.cache_expiry_time, pickle.dumps(reports))
    response = {"status": "success", "data": {"reports": reports}}
    return response
