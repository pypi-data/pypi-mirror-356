from typing import Any

from verse.core import DataModel


class UserCredential(DataModel):
    username: str
    password: str | None = None
    info: dict[str, Any] = dict()


class AuthResult(DataModel):
    token: str
    id: str | None = None
    email: str | None = None
    refresh_token: str | None = None
    info: dict[str, Any] = dict()


class UserInfo(DataModel):
    id: str
    email: str | None = None
    name: str | None = None
    info: dict[str, Any] = dict()
