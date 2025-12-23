"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.db_connection import DBConnection  # noqa
from app.models.schema_table import SchemaTable  # noqa
from app.models.schema_column import SchemaColumn  # noqa
from app.models.schema_relationship import SchemaRelationship  # noqa
from app.models.value_mapping import ValueMapping  # noqa
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZWMGRWT1E9PTpjZjE3NjBjMA==