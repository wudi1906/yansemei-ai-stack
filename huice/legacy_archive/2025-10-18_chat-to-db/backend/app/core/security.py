"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from passlib.context import CryptContext
# fmt: off  MC8yOmFIVnBZMlhsa0xUb3Y2bzZTMnQxWmc9PTplZDdjMTNlZA==

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# fmt: off  MS8yOmFIVnBZMlhsa0xUb3Y2bzZTMnQxWmc9PTplZDdjMTNlZA==


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)