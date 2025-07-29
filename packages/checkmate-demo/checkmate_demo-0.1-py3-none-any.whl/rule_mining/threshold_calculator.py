from typing import Tuple
from .models import RuleIntensity

class ThresholdCalculator:
    # Class constants for intensity mappings
    NULL_THRESHOLD_BUFFERS = {
        RuleIntensity.HIGH: 2.0,
        RuleIntensity.MEDIUM: 5.0,
        RuleIntensity.LOW: 10.0
    }
    
    ROW_COUNT_FACTORS = {
        RuleIntensity.HIGH: (0.9, 1.1),
        RuleIntensity.MEDIUM: (0.8, 1.2),
        RuleIntensity.LOW: (0.7, 1.3)
    }
    
    RANGE_BUFFER_FACTORS = {
        RuleIntensity.HIGH: 0.05,
        RuleIntensity.MEDIUM: 0.10,
        RuleIntensity.LOW: 0.20
    }
    
    @staticmethod
    def calculate_null_threshold(current_null_pct: float, is_nullable: str, intensity: RuleIntensity = RuleIntensity.MEDIUM) -> float:
        # Check if column is nullable first
        if is_nullable.upper() == "YES":
            return ThresholdCalculator.NULL_THRESHOLD_BUFFERS[RuleIntensity.MEDIUM]  # Default MEDIUM threshold if nullable
        
        # For non-nullable columns
        if current_null_pct == 0:
            return 0.0  # Strict for non-nullable with no nulls
        
        buffer = ThresholdCalculator.NULL_THRESHOLD_BUFFERS.get(intensity, ThresholdCalculator.NULL_THRESHOLD_BUFFERS[RuleIntensity.MEDIUM])
        threshold = current_null_pct + buffer
        if threshold > 50:
            threshold = 30.0

        return round(threshold)
    
    @staticmethod
    def calculate_row_count_bounds(current_count: int, intensity: RuleIntensity = RuleIntensity.MEDIUM) -> Tuple[int, int]:
        min_factor, max_factor = ThresholdCalculator.ROW_COUNT_FACTORS.get(
            intensity, 
            ThresholdCalculator.ROW_COUNT_FACTORS[RuleIntensity.MEDIUM]
        )
        return int(current_count * min_factor), int(current_count * max_factor)

    @staticmethod
    def calculate_range_bounds(min_val: float, max_val: float, intensity: RuleIntensity = RuleIntensity.MEDIUM) -> Tuple[float, float]:
        range_span = max_val - min_val
        buffer = range_span * ThresholdCalculator.RANGE_BUFFER_FACTORS.get(
            intensity, 
            ThresholdCalculator.RANGE_BUFFER_FACTORS[RuleIntensity.MEDIUM]
        )
        return min_val - buffer, max_val + buffer
