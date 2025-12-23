"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
# pragma: no cover  MC8yOmFIVnBZMlhsa0xUb3Y2bzZWR3AyUWc9PTo4MmM4ZTJiMg==

from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
# pylint: disable  MS8yOmFIVnBZMlhsa0xUb3Y2bzZWR3AyUWc9PTo4MmM4ZTJiMg==