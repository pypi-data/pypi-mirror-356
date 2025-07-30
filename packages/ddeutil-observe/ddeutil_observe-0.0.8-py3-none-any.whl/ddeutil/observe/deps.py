# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import AsyncSession

from .db import sessionmanager

PARENT_PATH: Path = Path(__file__).parent


def get_templates(request: Request) -> Jinja2Templates:
    """Dynamic multi-templating Jinja2 loader that support templates inside
    APIRouter.
    """
    choices: list[FileSystemLoader] = [
        FileSystemLoader(PARENT_PATH / "templates")
    ]
    if request.url.path != "/":
        route: str = request.url.path.strip("/").split("/")[0]
        route_path: Path = PARENT_PATH / f"routes/{route}/templates"

        # NOTE: Check route path exists on the current request.
        if route_path.exists():
            choices.insert(0, FileSystemLoader(route_path))
        else:
            auth_path: Path = PARENT_PATH / "auth/templates"
            if auth_path.exists():
                choices.insert(0, FileSystemLoader(auth_path))

    return Jinja2Templates(
        directory="templates",
        loader=ChoiceLoader(choices),
    )


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """Return the database local session instance."""
    async with sessionmanager.session() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise
