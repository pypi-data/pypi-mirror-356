from typing import List, Dict
from .models import RuleIntensity, CheckConfig
from .conflict_resolver import ConflictResolver
from .generators.null_check import NullCheckGenerator
from .generators.row_count_check import RowCountCheckGenerator

class RuleMiner:
    """Enhanced RuleMiner with integrated conflict analysis"""
    
    def __init__(self, intensity: RuleIntensity = RuleIntensity.MEDIUM):
        self.intensity = intensity
        self.generators = {
            'null_check': NullCheckGenerator(intensity),
            'row_count_check': RowCountCheckGenerator(intensity),
        }

    def add_check_generator(self, check_type: str, generator):
        """Add custom check generator"""
        self.generators[check_type] = generator

    def mine_rules(self, profiling_results: Dict, enabled_checks: List[str], user_checks: List[CheckConfig] = None) -> Dict:
        """Comprehensive rule mining with conflict analysis"""
        if user_checks is None:
            user_checks = []
            
        auto_checks = []
        generation_stats = {
            'tables_processed': 0,
            'checks_by_type': {},
            'failed_generations': []
        }

        # Generate auto checks
        for table_name, table_info in profiling_results.items():
            generation_stats['tables_processed'] += 1
            
            for check_type in enabled_checks:
                if check_type in self.generators:
                    try:
                        checks = self.generators[check_type].generate_checks(
                            table_name,
                            table_info.get('table_data', {}),
                            table_info.get('column_data', {})
                        )
                        auto_checks.extend(checks)
                        
                        # Track statistics
                        if check_type not in generation_stats['checks_by_type']:
                            generation_stats['checks_by_type'][check_type] = 0
                        generation_stats['checks_by_type'][check_type] += len(checks)
                        
                    except Exception as e:
                        error_info = {
                            'table': table_name,
                            'check_type': check_type,
                            'error': str(e)
                        }
                        generation_stats['failed_generations'].append(error_info)

        # Run full conflict resolution process
        resolution_report = ConflictResolver.full_resolution_process(user_checks, auto_checks)

        # Get the actual conflicts that were resolved (not just potential overlaps)
        actual_conflicts = resolution_report.get('conflicts', [])

        return {
            'checks': resolution_report.get('final_checks', []),
            'conflicts': actual_conflicts,
            'detailed_conflicts': actual_conflicts,
            'conflict_analysis': resolution_report.get('analysis', {}),
            'stats': {
                'user_checks_count': len(user_checks),
                'auto_checks_count': len(auto_checks),
                'final_checks_count': len(resolution_report.get('final_checks', [])),
                'conflicts_count': len(actual_conflicts),  # Use actual conflicts, not potential
                'generation_stats': generation_stats,
                'conflict_stats': {
                    'potential_overlaps': resolution_report.get('analysis', {}).get('total_potential_conflicts', 0),
                    'actual_conflicts_resolved': len(actual_conflicts),
                    'unique_user_keys': resolution_report.get('analysis', {}).get('unique_user_keys', 0),
                    'unique_auto_keys': resolution_report.get('analysis', {}).get('unique_auto_keys', 0)
                }
            }
        }
