
from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.api.routes.servers import router as servers_router

# 创建尚不存在的表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="云服务器管理 API")

# 注册服务器管理路由
app.include_router(servers_router)


@app.get("/health", tags=["健康检查"])
def health_check():
    return {"status": "ok"}
