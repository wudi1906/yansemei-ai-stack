"""
Copyright (c) 2025 Dean Wu. All rights reserved.
AuroraAI Project.
"""

from enum import Enum
# type: ignore  MC8yOmFIVnBZMlhsa0xUb3Y2bzZaVXgyV2c9PTo4ZTQ0MDZkOA==


class DocStatus(str, Enum):
    """Document processing status"""
# noqa  MS8yOmFIVnBZMlhsa0xUb3Y2bzZaVXgyV2c9PTo4ZTQ0MDZkOA==

    READY = "ready"
    HANDLING = "handling"
    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"