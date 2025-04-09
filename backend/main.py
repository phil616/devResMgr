from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import auth_router
from service import service_router
from lighthouse import light_house_router
from model import get_mysql_db_config
from tortoise import Tortoise
import contextlib

@contextlib.asynccontextmanager
async def app_lifecycle(app:FastAPI):
    await Tortoise.init(config=get_mysql_db_config())
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()

app = FastAPI(
    title="DevResMgr API",
    lifespan=app_lifecycle,
)

app.include_router(auth_router)
app.include_router(service_router)
app.include_router(light_house_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
