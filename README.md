fastapi快速开始的一个学习项目

安装依赖包
python -m pip install "fastapi[standard]"
python -m pip install sqlalchemy

启动
cd d:\dev\python\fastapi-demo
fastapi dev  app\main.py
或者
python -m uvicorn fastapi-demo.main:app --reload

执行测试
python -m pip install  pytest httpx2
python -m pytest -q

来自极维空间 https://jiweisys.com/
