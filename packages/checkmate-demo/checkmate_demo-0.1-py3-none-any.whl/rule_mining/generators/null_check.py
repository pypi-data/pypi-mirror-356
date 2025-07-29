
from ..models import CheckConfig, RuleIntensity
from .base import CheckGenerator
from datetime import datetime


class NullCheckGenerator(CheckGenerator):
    def generate_checks(self, table_name, table_data, column_data):
        checks = []
        exclusion_patterns = ['_id', '_key', 'created_', 'updated_', 'timestamp']
        
        for column_name, column_info in column_data.items():
            # Skip columns without meaningful data
            if not self.has_meaningful_data(column_info):
                continue
                
            if not self.should_generate_check(column_name, column_info.get('data_type', ''), exclusion_patterns):
                continue
                
            current_null_pct = column_info.get('null_percentage', 0)
            is_nullable = column_info.get('is_nullable', 'NO')  # Get nullable constraint
            
            # Pass is_nullable to threshold calculation
            threshold_value = self.threshold_calculator.calculate_null_threshold(
                current_null_pct, 
                is_nullable, 
                self.intensity
            )
            
            # Store threshold as dict matching expected format
            threshold_dict = {
                "max_null_percentage": threshold_value
            }
            
            
            checks.append(CheckConfig(
                check_id=f"auto_null_{table_name}_{column_name}",
                check_name=f"Auto Null Check for {table_name}.{column_name}",
                table_name=table_name,
                column_name=column_name,
                check_type="null_check",
                threshold=threshold_dict,
                source="auto_generated",
                generated_by="rule_mining",
                intensity=self.intensity.value,
                metadata={
                    "current_null_percentage": current_null_pct,
                    "is_nullable": is_nullable,
                    "distinct_count": column_info.get('distinct_count'),
                    "non_null_count": column_info.get('non_null_count'),
                    "generation_timestamp": datetime.now().isoformat()
                }
            ))
        return checks
