
from pydantic import BaseModel, ConfigDict, Field


class ServerCreate(BaseModel):
    hostname: str = Field(min_length=2, max_length=50)
    ip: str = Field(min_length=1, max_length=45)
    cpu_cores: int = Field(gt=0, le=256)
    memory_gb: int = Field(gt=0, le=4096)


class ServerUpdate(BaseModel):
    ip: str | None = Field(default=None, max_length=45)
    cpu_cores: int | None = Field(default=None, gt=0, le=256)
    memory_gb: int | None = Field(default=None, gt=0, le=4096)


class ServerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hostname: str
    ip: str
    cpu_cores: int
    memory_gb: int
