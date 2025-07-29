import os
import yaml
from datetime import datetime
from typing import Dict, List, Any
from .models import CheckConfig, RuleIntensity
from .rule_miner import RuleMiner
from Config_parser.configService import ConfigLoader
from .conflict_resolver import ConflictResolver
from logger.custom_logs import LoggerConfigurator

logger_configurator = LoggerConfigurator(name="auto_check_generator")
logger = logger_configurator.get_logger()

#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)

class RuleMiningOrchestrator:
    """Rule mining Orchestrator to be used with auto_check_generator """

    def __init__(self, config: Dict, config_path: str = None):
        self.config = config
        self.config_path = config_path  # Store original config path
        self.config_manager = ConfigLoader()

        intensity_str = config.get('rule_mining', {}).get('intensity', 'medium')
        self.intensity = RuleIntensity(intensity_str.lower())
        self.rule_miner = RuleMiner(self.intensity)

    def _extract_user_checks(self) -> List[CheckConfig]:
        """Extract existing user checks from config and convert to CheckConfig objects"""
        existing_user_checks = []
        if 'checks' in self.config:
            for i, check_dict in enumerate(self.config['checks']):
                # Build table name
                table_name = f"{check_dict.get('database', '')}.{check_dict.get('schema', '')}.{check_dict.get('table', '')}"
                
                # Handle column name
                columns = check_dict.get('columns', [])
                column_name = columns[0] if columns else None
                
                check_config = CheckConfig(
                    check_id=f"user_{check_dict.get('name')}_{check_dict.get('table', '')}_{i}",
                    check_name=f"User {check_dict.get('name', 'check')} for {check_dict.get('table', '')}",
                    table_name=table_name,
                    column_name=column_name,
                    check_type=check_dict.get('name', 'unknown_check'),
                    threshold=check_dict.get('threshold', {}),
                    source="user_defined"
                )
                existing_user_checks.append(check_config)
        
        logger.info(f"Extracted {len(existing_user_checks)} user-defined checks")
        return existing_user_checks

    def _safe_extract_numeric_value(self, value: Any) -> int:
        """Safely extract numeric value from various data types"""
        if isinstance(value, dict):
            # Try common keys that might contain the actual value
            for key in ['value', 'min', 'max', 'count', 'threshold', 'expected']:
                if key in value:
                    return self._safe_extract_numeric_value(value[key])
            # If no known key found, try to get the first numeric value
            for v in value.values():
                if isinstance(v, (int, float, str)):
                    try:
                        return int(float(v))
                    except (ValueError, TypeError):
                        continue
            # If nothing works, return 0 as default
            logger.warning(f"Could not extract numeric value from dict: {value}")
            return 0
        elif isinstance(value, (int, float)):
            return int(value)
        elif isinstance(value, str):
            try:
                return int(float(value))
            except (ValueError, TypeError):
                logger.warning(f"Could not convert string to int: {value}")
                return 0
        else:
            logger.warning(f"Unexpected value type: {type(value)}, value: {value}")
            return 0

    def _convert_to_checkrunner_config(self, checks: List[CheckConfig]) -> List[Dict[str, Any]]:
        """Convert CheckConfig objects to CheckRunner format"""
        logger.info(f"Converting {len(checks)} checks to CheckRunner format...")
        
        grouped = []
        
        for c in checks:
            logger.debug(f"Converting check: {c.check_id} of type {c.check_type}")
            
            # Parse fully qualified table name
            fully_qualified = c.table_name
            parts = fully_qualified.split('.')
            if len(parts) >= 3:
                database, schema, table = parts[-3], parts[-2], parts[-1]
            else:
                # Fallback for incomplete table names
                database = parts[0] if len(parts) > 0 else "unknown"
                schema = parts[1] if len(parts) > 1 else "unknown" 
                table = parts[2] if len(parts) > 2 else parts[-1]
            
            if c.check_type == "null_check":
                val = {
                    'name': 'null_check',
                    'database': database,
                    'schema': schema,
                    'table': table,
                    'columns': [c.column_name],
                    'threshold': c.threshold
                }
                grouped.append(val)
            
            elif c.check_type == "row_count_check":
                val = {
                    'name': 'row_count_check',
                    'database': database,
                    'schema': schema,
                    'table': table,
                    'threshold': c.threshold
                }
                grouped.append(val)
            
            else:
                logger.warning(f"Unknown check type: {c.check_type}")
                continue
        
        logger.info(f"Successfully converted {len(grouped)} checks")
        return grouped
    
    def _create_final_merged_config(self, user_cfg: Dict[str, Any], final_checks: List[Dict[str, Any]], 
                                  conflict_summary: Dict[str, Any], mining_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Create final merged configuration maintaining user's structure and sequence"""
        logger.info("Creating final merged configuration...")
        
        # Start with empty merged config to control order
        merged_config = {}
        
        # Preserve exact order from original user config 
        config_order = [
            'data_source', 'checks', 'audit', 'alerts', 'profiling', 'rule_mining'
        ]
        
        # Copy sections in order, preserving user structure
        for section in config_order:
            if section in user_cfg:
                if section == 'checks':
                    # Merge user checks with auto-generated ones
                    user_checks = user_cfg.get('checks', [])
                    merged_config['checks'] = user_checks + final_checks
                else:
                    merged_config[section] = user_cfg[section]
        
        # Add any remaining sections not in our predefined order
        for key, value in user_cfg.items():
            if key not in merged_config:
                merged_config[key] = value
        
        # Create metadata
        metadata = {
            'generation_timestamp': datetime.now().isoformat(),
            'summary': {
                'user_checks': mining_stats.get('user_checks_count', 0),
                'auto_checks_generated': mining_stats.get('auto_checks_count', 0),
                'auto_checks_added': conflict_summary.get('auto_checks_added', 0),
                'final_total_checks': conflict_summary.get('final_checks_count', 0)
            }
        }
        
        # Only add conflicts info if there were actual conflicts
        if conflict_summary.get('total_conflicts', 0) > 0:
            metadata['conflicts_resolved'] = conflict_summary.get('total_conflicts', 0)
            metadata['affected_tables'] = conflict_summary.get('affected_tables', [])
        
        # Only add generation details if there were failures
        generation_stats = mining_stats.get('generation_stats', {})
        if generation_stats.get('failed_generations', []):
            metadata['failed_generations'] = generation_stats.get('failed_generations', [])
        
        # Only add check type breakdown if useful (more than one type)
        checks_by_type = generation_stats.get('checks_by_type', {})
        if len(checks_by_type) > 1:
            metadata['checks_by_type'] = checks_by_type
        
        merged_config['rule_mining_metadata'] = metadata
        
        return merged_config

    def _transform_profiler_output(self, raw_profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Transform raw profiler output to RuleMiner format"""
        logger.info("Transforming profiler output...")
        
        out = {}
        results = raw_profile.get('results', {})
        
        logger.debug(f"Raw profile results keys: {list(results.keys())}")
        
        for table_key, tbl in results.items():
            logger.debug(f"Processing table: {table_key}")
            
            row_count = tbl.get('row_count', 0)
            columns = tbl.get('columns', {})
            
            logger.debug(f"Table {table_key} has {row_count} rows and {len(columns)} columns")
            
            # Build column_data for RuleMiner
            col_data = {}
            for col_name, col_meta in columns.items():
                data_type = col_meta.get('data_type', '')
                
                # Compute null_percentage if null_count is present
                null_pct = 0.0
                if 'null_count' in col_meta and row_count > 0:
                    null_pct = (col_meta['null_count'] / float(row_count)) * 100.0
                elif 'null_percentage' in col_meta:
                    null_pct = col_meta['null_percentage']
                
                # Get min/max values
                min_val = col_meta.get('min_value') or col_meta.get('min')
                max_val = col_meta.get('max_value') or col_meta.get('max')
                
                # Build column data with all relevant fields
                col_data[col_name] = {
                    'data_type': data_type,
                    'null_percentage': null_pct,
                    'is_nullable': col_meta.get('is_nullable', 'NO'),  # Add nullable info
                    'distinct_count': col_meta.get('distinct_count', 0),  # Add distinct count
                    'non_null_count': col_meta.get('non_null_count', 0),  # Add non-null count
                    'null_count': col_meta.get('null_count', 0)  # Add null count
                }
                
                # Add min/max values if available
                if min_val is not None and max_val is not None:
                    col_data[col_name]['min_value'] = min_val
                    col_data[col_name]['max_value'] = max_val
                
                # Add other profiling fields that might be useful
                for field in ['avg_length', 'max_length', 'min_length', 'empty_count']:
                    if field in col_meta:
                        col_data[col_name][field] = col_meta[field]
                
                logger.debug(f"Column {col_name}: type={data_type}, null_pct={null_pct}, distinct_count={col_meta.get('distinct_count', 0)}")
            
            out[table_key] = {
                'table_data': {'row_count': row_count},
                'column_data': col_data
            }
        
        logger.info(f"Transformed profiling data for {len(out)} tables")
        return out

    def run_enhanced_rule_mining(self, raw_profiling_results: Dict) -> Dict:
        """
        Main orchestration method - Rule mining with proper conflict resolution and metadata
        """
        logger.info("Starting enhanced rule mining process...")
        
        try:
            # 1. Transform profiling results
            profiling_results = self._transform_profiler_output(raw_profiling_results)
            
            # 2. Get rule mining configuration
            rule_conf = self.config.get('rule_mining', {})
            enabled_checks = rule_conf.get('enabled_checks', [])
            
            if not enabled_checks:
                logger.warning("No enabled checks specified in rule_mining.enabled_checks")
            
            logger.info(f"Enabled checks: {enabled_checks}")
            
            # 3. Extract existing user checks
            existing_user_checks = self._extract_user_checks()
            
            # 4. Run rule mining
            logger.info("Running rule mining...")
            mining_result = self.rule_miner.mine_rules(profiling_results, enabled_checks, existing_user_checks)
            
            logger.info(f"Rule mining completed. Generated {len(mining_result['checks'])} total checks")
            
            # 5. Conflict resolution
            logger.info("Starting conflict resolution...")
            auto_generated_checks = [c for c in mining_result['checks'] if c.source == 'auto_generated']
            
            final_checks, detailed_conflicts = ConflictResolver.resolve_conflicts_detailed(
                existing_user_checks, 
                auto_generated_checks
            )
            
            conflict_summary = ConflictResolver.get_conflict_summary(
                detailed_conflicts, existing_user_checks, 
                auto_generated_checks, final_checks
            )
            
            # Log conflict resolution results 
            logger.info(f"Conflict resolution completed:")
            logger.info(f"  - User checks preserved: {conflict_summary['user_checks_preserved']}")
            logger.info(f"  - Auto checks added: {conflict_summary['auto_checks_added']}")
            logger.info(f"  - Actual conflicts resolved: {conflict_summary['total_conflicts']}")
            
            # 6. Convert only auto-generated checks to CheckRunner format
            auto_generated_final_checks = [c for c in final_checks if c.source == 'auto_generated']
            runner_ready_auto_checks = self._convert_to_checkrunner_config(auto_generated_final_checks)
            
            # 7. Create final merged configuration with proper sequence
            final_merged_config = self._create_final_merged_config(
                self.config, runner_ready_auto_checks, conflict_summary, mining_result['stats']
            )
            
            # 8. Save only the auto-generated merged config 
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            auto_filename = f"auto_generated_merged_config_{timestamp}.yaml"
            auto_path = self.config_manager.save_config(final_merged_config, auto_filename)
            
            logger.info(f"Auto-generated config saved to: {auto_path}")
            
            # 9. Get user confirmation - use original config path instead of creating new one
            original_path = self.config_path if self.config_path else "original_config.yaml"
            use_auto_generated = self.config_manager.get_user_confirmation(auto_path, original_path)
            
            if use_auto_generated:
                final_config_path = auto_path
                final_config = final_merged_config
            else:
                final_config_path = original_path
                final_config = self.config
            
            # 10. Display summary 
            logger.info("\n" + "="*60)
            logger.info("RULE MINING SUMMARY")
            logger.info("="*60)
            logger.info(f"Original user checks: {len(existing_user_checks)}")
            logger.info(f"Auto-checks generated: {mining_result['stats']['auto_checks_count']}")
            logger.info(f"Actual conflicts resolved: {conflict_summary['total_conflicts']}")
            logger.info("")

            logger.info("Final Results:")
            logger.info(f"  - User checks preserved: {conflict_summary['user_checks_preserved']}")
            logger.info(f"  - Auto-checks added: {conflict_summary['auto_checks_added']}")
            logger.info(f"  - Auto-checks rejected due to conflicts: {conflict_summary['auto_checks_rejected']}")
            logger.info("")

            if conflict_summary['total_conflicts'] > 0:
                logger.info("Resolved Conflicts:")
                for conflict in detailed_conflicts:
                    logger.info(f"  - {conflict['conflict_key']}: User check preserved")
            else:
                logger.info("No conflicts detected - all auto-checks added successfully")
                
            logger.info("")
            logger.info(f"Final total checks: {conflict_summary['final_checks_count']}")
            logger.info("="*60)
            
            return {
                'final_config': final_config,
                'final_config_path': final_config_path,
                'mining_stats': mining_result['stats'],
                'conflict_summary': conflict_summary,
                'detailed_conflicts': detailed_conflicts,
                'use_auto_generated': use_auto_generated,
                'auto_config_path': auto_path,
                'original_config_path': original_path,
                'profiling_results': profiling_results
            }
            
        except Exception as e:
            logger.error(f"Error in enhanced rule mining: {e}", exc_info=True)
            raise        