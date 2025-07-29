from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models import CheckConfig, RuleIntensity
from ..threshold_calculator import ThresholdCalculator

class CheckGenerator(ABC):
    def __init__(self, intensity: RuleIntensity = RuleIntensity.MEDIUM):
        self.intensity = intensity
        self.threshold_calculator = ThresholdCalculator()

    @abstractmethod
    def generate_checks(self, table_name: str, table_data: Dict, column_data: Dict) -> List[CheckConfig]:
        pass

    def should_generate_check(self, column_name: str, data_type: str, exclusion_patterns: List[str] = None) -> bool:
        if exclusion_patterns:
            for pattern in exclusion_patterns:
                if pattern.replace('*', '') in column_name.lower():
                    return False
        return True
    
    def has_meaningful_data(self, column_info: Dict[str, Any]) -> bool:
        """
        Check if column has meaningful data for rule generation
        Returns False if:
        - distinct_count is 0 (no unique values)
        - non_null_count is 0 (all values are null)
        """
        distinct_count = column_info.get('distinct_count', None)
        non_null_count = column_info.get('non_null_count', None)
        
        # If distinct_count is 0, skip (no unique values)
        if distinct_count is not None and distinct_count == 0:
            return False
            
        # If non_null_count is 0, skip (all values are null)
        if non_null_count is not None and non_null_count == 0:
            return False
            
        return True
    
