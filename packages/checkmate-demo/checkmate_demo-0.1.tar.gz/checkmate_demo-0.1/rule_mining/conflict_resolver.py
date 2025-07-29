from typing import List, Dict, Any, Tuple
from .models import CheckConfig

class ConflictResolver:
    """
    Comprehensive conflict resolution with analysis, resolution, and reporting capabilities.
    """
    
    @staticmethod
    def get_check_key(check: CheckConfig) -> str:
        """Generate a unique key for a check based on table, column, and check type"""
        column_part = f".{check.column_name}" if check.column_name else ""
        return f"{check.table_name}{column_part}.{check.check_type}"

    @staticmethod
    def analyze_potential_conflicts(user_checks: List[CheckConfig], 
                                   auto_checks: List[CheckConfig]) -> Dict[str, Any]:
        """
        Detailed analysis of potential conflicts before resolution
        """
        user_keys = {ConflictResolver.get_check_key(c): c for c in user_checks}
        auto_keys = {ConflictResolver.get_check_key(c): c for c in auto_checks}
        
        # Find overlapping keys (potential conflicts)
        overlapping_keys = set(user_keys.keys()) & set(auto_keys.keys())
        
        conflicts = []
        for key in overlapping_keys:
            user_check = user_keys[key]
            auto_check = auto_keys[key]
            
            conflict_detail = {
                "conflict_key": key,
                "table": auto_check.table_name,
                "column": auto_check.column_name,
                "check_type": auto_check.check_type,
                "user_check": {
                    "id": user_check.check_id,
                    "name": user_check.check_name,
                    "threshold": user_check.threshold,
                    "source": user_check.source
                },
                "auto_check": {
                    "id": auto_check.check_id,
                    "name": auto_check.check_name,
                    "threshold": auto_check.threshold,
                    "source": auto_check.source
                },
                "threshold_different": user_check.threshold != auto_check.threshold
            }
            conflicts.append(conflict_detail)
        
        return {
            "total_potential_conflicts": len(overlapping_keys),
            "user_check_keys": list(user_keys.keys()),
            "auto_check_keys": list(auto_keys.keys()),
            "overlapping_keys": list(overlapping_keys),
            "conflicts": conflicts,
            "analysis": {
                "user_checks_count": len(user_checks),
                "auto_checks_count": len(auto_checks),
                "unique_user_keys": len(user_keys),
                "unique_auto_keys": len(auto_keys),
                "duplicate_keys_in_user": len(user_checks) - len(user_keys),
                "duplicate_keys_in_auto": len(auto_checks) - len(auto_keys)
            }
        }

    @staticmethod
    def resolve_conflicts_detailed(user_checks: List[CheckConfig], 
                                 auto_checks: List[CheckConfig]) -> Tuple[List[CheckConfig], List[Dict[str, Any]]]:
        """
        Conflict resolution with detailed reporting.
        Returns:
            - Final list of checks after resolution
            - List of conflict details
        """
        user_keys = {ConflictResolver.get_check_key(c): c for c in user_checks}
        final_checks = list(user_checks)  # Start with user checks (they have precedence)
        detailed_conflicts = []
        added_auto_checks = []

        for auto in auto_checks:
            key = ConflictResolver.get_check_key(auto)
            if key not in user_keys:
                final_checks.append(auto)
                added_auto_checks.append(auto)
            else:
                user_check = user_keys[key]
                if user_check.threshold != auto.threshold:
                    conflict_info = {
                        "table": auto.table_name,
                        "column": auto.column_name,
                        "check_type": auto.check_type,
                        "reason": "user_precedence",
                        "auto_check_id": auto.check_id,
                        "user_check_id": user_check.check_id,
                        "auto_threshold": auto.threshold,
                        "user_threshold": user_check.threshold,
                        "conflict_key": key,
                        "resolution": "kept_user_check"
                    }
                    detailed_conflicts.append(conflict_info)
                else:
                    # Same key and same threshold - no actual conflict
                    final_checks.append(auto)
                    added_auto_checks.append(auto)

        return final_checks, detailed_conflicts
    
    @staticmethod
    def get_conflict_summary(conflicts: List[Dict[str, Any]], 
                           user_checks: List[CheckConfig], 
                           auto_checks: List[CheckConfig], 
                           final_checks: List[CheckConfig]) -> Dict[str, Any]:
        """
        Generate a comprehensive summary of the resolution process
        """
        added_auto_checks = len(final_checks) - len(user_checks)
        rejected_auto_checks = len(auto_checks) - added_auto_checks
        
        return {
            "total_conflicts": len(conflicts),
            "user_checks_preserved": len(user_checks),
            "auto_checks_added": added_auto_checks,
            "auto_checks_rejected": rejected_auto_checks,
            "final_checks_count": len(final_checks),
            "conflict_types": {
                ctype: len([c for c in conflicts if c["check_type"] == ctype])
                for ctype in set(c["check_type"] for c in conflicts)
            } if conflicts else {},
            "affected_tables": list(set(c["table"] for c in conflicts)),
            "conflicts": conflicts
        }

    @staticmethod
    def full_resolution_process(user_checks: List[CheckConfig], 
                              auto_checks: List[CheckConfig]) -> Dict[str, Any]:
        """
        Complete conflict resolution workflow with analysis, resolution, and reporting
        """
        # Step 1: Analyze potential conflicts
        analysis = ConflictResolver.analyze_potential_conflicts(user_checks, auto_checks)
        
        # Step 2: Perform actual resolution
        final_checks, conflicts = ConflictResolver.resolve_conflicts_detailed(user_checks, auto_checks)
        
        # Step 3: Generate summary report
        summary = ConflictResolver.get_conflict_summary(
            conflicts, user_checks, auto_checks, final_checks
        )
        
        return {
            "analysis": analysis,
            "resolution_summary": summary,
            "final_checks": final_checks,
            "conflicts": conflicts
        }

