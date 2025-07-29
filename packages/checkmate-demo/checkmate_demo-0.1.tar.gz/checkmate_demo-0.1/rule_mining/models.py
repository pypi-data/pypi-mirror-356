from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict

class RuleIntensity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class CheckConfig:
    check_id: str
    check_name: str
    table_name: str
    column_name: Optional[str]
    check_type: str
    threshold: float
    source: str = "user_defined"
    generated_by: Optional[str] = None
    intensity: str = "medium"
    metadata: Optional[Dict] = None
