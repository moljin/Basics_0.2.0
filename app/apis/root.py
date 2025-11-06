import datetime
import os
from typing import Optional

from dns.edns import COOKIE
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request, Depends

from app.core.settings import templates, ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME, ADMINS
from app.dependencies.auth import get_optional_current_user
from app.models import User
from app.utils.commons import get_times
from app.utils.user import is_admin

router = APIRouter()


@router.get("/", response_class=HTMLResponse,
            summary="시작 페이지", description="여기는 Root 페이지입니다.")
async def get_root(request: Request,
                   current_user: Optional[User] = Depends(get_optional_current_user)):
    access_token = request.cookies.get(ACCESS_COOKIE_NAME)
    csrf_token = request.cookies.get("csrf_token")
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)

    now_time_utc, now_time = get_times()
    _NOW_TIME_UTC = now_time_utc.strftime('%Y-%m-%d %H:%M:%S.%f')
    _NOW_TIME = now_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    template = "common/index.html"
    context = {'request': request,
               "now_time_utc": _NOW_TIME_UTC,
               "now_time": _NOW_TIME,
               'current_user': current_user,
               'admin': is_admin(current_user)}
    return templates.TemplateResponse(template, context)


@router.get("/server", response_class=HTMLResponse,
            summary="서버 개발 페이지", description="여기는 서버 셋팅관련 페이지입니다.")
async def related_server(request: Request,
                   current_user: Optional[User] = Depends(get_optional_current_user)):
    now_time_utc, now_time = get_times()
    _NOW_TIME_UTC = now_time_utc.strftime('%Y-%m-%d %H:%M:%S.%f')
    _NOW_TIME = now_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    template = "common/server.html"
    context = {'request': request,
               "now_time_utc": _NOW_TIME_UTC,
               "now_time": _NOW_TIME,
               'current_user': current_user,
               'admin': is_admin(current_user)}
    return templates.TemplateResponse(template, context)


@router.get("/docker", response_class=HTMLResponse,
            summary="도커 개발 페이지", description="여기는 우분투 서버에 도커 셋팅관련 페이지입니다.")
async def related_server(request: Request,
                   current_user: Optional[User] = Depends(get_optional_current_user)):
    now_time_utc, now_time = get_times()
    _NOW_TIME_UTC = now_time_utc.strftime('%Y-%m-%d %H:%M:%S.%f')
    _NOW_TIME = now_time.strftime('%Y-%m-%d %H:%M:%S.%f')

    template = "common/docker.html"
    context = {'request': request,
               "now_time_utc": _NOW_TIME_UTC,
               "now_time": _NOW_TIME,
               'current_user': current_user,
               'admin': is_admin(current_user)}
    return templates.TemplateResponse(template, context)


