from pydantic import BaseModel, Field


class Scripter(BaseModel):
    name: str = Field(..., title="name")


class AddModifyScript(Scripter):

    domain: str = None
    dport: int = 8080
    gport: int = 8080
    gcontainer: str = Field(..., title="container")
    customjs: str = None
    reserve: str = None


class DelScript(Scripter):
    domain: str = None
    reserve: str = None
