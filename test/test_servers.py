from akshare.fund.fund_amac import headers
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.database import Base, get_db
from app.main import app


# 使用独立的内存数据库，避免修改真实练习数据
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    with TestingSessionLocal() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
TOKEN = "dev-only-change-me"
AUTH_HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def setup_function():
    # 每个测试开始前重建测试表
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


def test_auth_required():
    response = client.get("/servers")
    assert response.status_code == 401


def test_create_and_list_servers():
    payload = {
        "hostname": "ecs-test-01",
        "ip": "192.168.1.10",
        "cpu_cores": 8,
        "memory_gb": 16,
    }

    response = client.post(
        "/servers",
        json=payload,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 201
    created = response.json()
    assert created["hostname"] == "ecs-test-01"
    assert created["id"] > 0

    response = client.get("/servers", headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["hostname"] == "ecs-test-01"


def test_duplicate_hostname_returns_409():
    payload = {
        "hostname": "ecs-test-01",
        "ip": "192.168.1.10",
        "cpu_cores": 8,
        "memory_gb": 16,
    }

    first = client.post(
        "/servers",
        json=payload,
        headers=AUTH_HEADERS,
    )
    second = client.post(
        "/servers",
        json=payload,
        headers=AUTH_HEADERS,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_missing_server_returns_404():
    response = client.get(
        "/servers/99999",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 404

def test_patch_server():
    payload = {
        "hostname": "ecs-test-01",
        "ip": "192.168.1.10",
        "cpu_cores": 8,
        "memory_gb": 16,
    }

    first = client.post(
        "/servers",
        json=payload,
        headers=AUTH_HEADERS,
    )
    server_id=first.json()["id"]

    response = client.patch(
        f"/servers/{server_id}",
        headers=AUTH_HEADERS,
        json= payload,
    )
    assert response.json()["hostname"]=="ecs-test-01"
    assert len(response.json()) == 5
    assert response.status_code == 200

def test_delete_server():
    payload = {
        "hostname": "ecs-test-01",
        "ip": "192.168.1.10",
        "cpu_cores": 8,
        "memory_gb": 16,
    }

    first = client.post(
        "/servers",
        json=payload,
        headers=AUTH_HEADERS,
    )
    server_id = first.json()["id"]

    response = client.delete(
        f"/servers/{server_id}",
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 204

    response = client.get(
        f"/servers/{server_id}",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 404