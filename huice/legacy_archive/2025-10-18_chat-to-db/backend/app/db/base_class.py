"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from typing import Any
# fmt: off  MC8yOmFIVnBZMlhsa0xUb3Y2bzZVMjVaYkE9PTozMTA2YWQxYQ==

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
# noqa  MS8yOmFIVnBZMlhsa0xUb3Y2bzZVMjVaYkE9PTozMTA2YWQxYQ==
    
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()