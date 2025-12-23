"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ValueMappingBase(BaseModel):
    nl_term: str
    db_value: str
# pragma: no cover  MC8yOmFIVnBZMlhsa0xUb3Y2bzZSazlNUWc9PTo4MzllNjQyNA==


# Properties to receive on mapping creation
class ValueMappingCreate(ValueMappingBase):
    column_id: int


# Properties to receive on mapping update
class ValueMappingUpdate(BaseModel):
    nl_term: Optional[str] = None
    db_value: Optional[str] = None
# type: ignore  MS8yOmFIVnBZMlhsa0xUb3Y2bzZSazlNUWc9PTo4MzllNjQyNA==


# Properties shared by models stored in DB
class ValueMappingInDBBase(ValueMappingBase):
    id: int
    column_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to return to client
class ValueMapping(ValueMappingInDBBase):
    pass