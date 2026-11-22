from fastapi import FastAPI,Request,BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.routers import products, user,auth
from app.database import engine, Base
from app import models
from app.tasks import send_notification

app = FastAPI()
#CORS跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#请求日志中间件
@app.middleware("http")
async def log_request(request: Request, call_next):
    print(f"请求进入：{request.method}{request.url.path}")

    response = await call_next(request)

    print(f"响应状态码：{response.status_code}")

    return response

#注册用户路由(把user.py中的路由注册到主应用中)
app.include_router(user.router)

app.include_router(products.router)

app.include_router(auth.router)


# 创建数据库表
Base.metadata.create_all(bind=engine)


@app.post("/send-email")
def send_email_background(
    username: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        send_notification,
        username
    )

    return {
        "message": "请求成功，邮件将在后台发送"
    }