from ..models import CheckConfig, RuleIntensity
from .base import CheckGenerator
from datetime import datetime

class RowCountCheckGenerator(CheckGenerator):
    def generate_checks(self, table_name, table_data, column_data):
        checks = []
        
        # Get current row count from table_data
        current_row_count = table_data.get('row_count', 0)
        
        if current_row_count == 0:
            # Skip generating check for empty tables
            return checks
        
        # Calculate threshold range based on current row count and intensity
        min_count, max_count = self.threshold_calculator.calculate_row_count_bounds(
            current_row_count, self.intensity
        )
        
        # FIX: Store threshold as dict matching expected format
        threshold_dict = {
            "expected_range": {
                "min": min_count,
                "max": max_count
            }
        }
        
        checks.append(CheckConfig(
            check_id=f"auto_row_count_{table_name}",
            check_name=f"Auto Row Count Check for {table_name}",
            table_name=table_name,
            column_name=None,  # Row count checks don't target specific columns
            check_type="row_count_check",
            threshold=threshold_dict,  # FIX: Use dict instead of tuple
            source="auto_generated",
            generated_by="rule_mining",
            intensity=self.intensity.value,
            metadata={
                "current_row_count": current_row_count,
                "generation_timestamp": datetime.now().isoformat(),
                "baseline_period": "current_snapshot"
            }
        ))
        
        return checks
