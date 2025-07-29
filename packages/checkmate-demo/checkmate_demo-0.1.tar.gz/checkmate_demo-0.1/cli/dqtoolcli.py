import argparse
import sys
import threading
import uuid
from Checks.Freshness_Check.freshness_monitor import FreshnessMonitor
from Checks.check_runner import CheckRunner
from Config_parser.configService import ConfigLoader
from Connectors.connector_factory import ConnectorFactory
from Profilers.database_profiler import DatabaseProfiler
from Utils.profile_store import *
from audit.results_auditing import  ResultAuditor
import traceback

from cli.render_profiling_html import render_profiling_html
from logger.custom_logs import LoggerConfigurator
from rule_mining.orchestrator import RuleMiningOrchestrator
from Utils.query_executor import QueryExecutor    


# Configure logger
logger_configurator = LoggerConfigurator()
logger = logger_configurator.get_logger()

def run_check_with_rule_mining(config_loc):
    try:
        print("=" * 60)
        print(" AUTO CHECK GENERATION PROCESS STARTED")
        print("=" * 60)
        logger.info("Starting auto check generation process...")

        # 1. Load configuration using ConfigLoader
        print("\n STEP 1: Loading Configuration...")
        #base_path = os.path.dirname(os.path.abspath(__file__))
        #config_path = os.path.join(base_path, config_loc)
        config_path = config_loc
        print(f"   Config path: {config_path}")
        
        # Use ConfigLoader singleton to load and validate config
        config_loader = ConfigLoader()
        user_cfg = config_loader.load_config(config_path)

        data_source = user_cfg.get("data_source", {}).get("type", None) 
        
        print(" Configuration loaded and validated successfully")
        logger.info(f"Successfully loaded and validated config from {config_path}")
        
        # 2. Validate configuration sections
        print("\n STEP 2: Validating Configuration Sections...")
        profiling_config = user_cfg['profiling']
        profiling_database = profiling_config.get('profiling_database')
        profiling_schema = profiling_config.get('profiling_schema')
        if 'table' in profiling_config:
            profiling_table = profiling_config.get('table')
        
        print(f"   Target Database: {profiling_database}")
        print(f"   Target Schema: {profiling_schema}")
        
        # 3. Check rule mining configuration using ConfigLoader
        print("\n  STEP 3: Checking Rule Mining Configuration...")
        rule_mining_config = user_cfg.get('rule_mining', {})
        
        # Check if rule mining is enabled
        is_rule_mining_enabled = rule_mining_config.get('enabled', False)
        print(f"   Rule Mining Enabled: {is_rule_mining_enabled}")
        
        if not is_rule_mining_enabled:
            print(" Rule mining is not enabled in configuration")
            logger.warning("Rule mining is not enabled in configuration")
            return
        
        # Get rule mining configuration details
        enabled_checks = rule_mining_config.get('enabled_checks', [])
        intensity = rule_mining_config.get('intensity', 'medium')
        
        print(f"   Enabled Checks: {enabled_checks}")
        print(f"   Mining Intensity: {intensity}")
        
        if not enabled_checks:
            print(" No enabled checks specified in rule_mining.enabled_checks")
            logger.warning("No enabled checks specified in rule_mining.enabled_checks")
            return
        
        print(" Rule mining configuration validated")
        logger.debug(f"Rule mining configuration loaded - enabled: {is_rule_mining_enabled}, checks: {enabled_checks}, intensity: {intensity}")
        
        # 4. Build connector
        print("\n STEP 4: Creating Database Connector...")
        logger.debug("Creating database connector...")
        connector = ConnectorFactory.get_connector(user_cfg)
        print(" Database connector created successfully")
        
        # 5. Set up profiling
        print("\n STEP 5: Setting Up Database Profiler...")
        logger.info("Setting up database profiler...")
        executor = QueryExecutor(
            connector,
            user_cfg['data_source']['type'],
            user_cfg['data_source']
        )
        
        db_profiler = DatabaseProfiler(executor)
        print(" Database profiler initialized")
        
        # 6. Run profiling
        print(f"\n STEP 6: Running Database Profiling...")
        print(f"   Profiling target: {profiling_database}.{profiling_schema}.{profiling_table}")
        logger.info(f"Starting profiling for {profiling_database}.{profiling_schema}.{profiling_table}")
        
        raw_profile = db_profiler.profile(profiling_database, profiling_schema, profiling_table)
        
        print(" Profiling completed successfully!")

        audit_connector = ConnectorFactory.get_connector(user_cfg, usage='audit')
        res=ResultAuditor(audit_connector)
        res.insert_profiling_results(raw_profile,data_source)

        print("Inserted profiling results to Audit table!")

        logger.info("Profiling completed successfully")
        logger.debug(f"Raw profile structure keys: {list(raw_profile.keys())}")
        
        if 'results' in raw_profile:
            num_tables = len(raw_profile['results'])
            print(f" Profiled {num_tables} tables:")
            logger.info(f"Profiled {num_tables} tables")
            
            for i, table_name in enumerate(raw_profile['results'].keys(), 1):
                print(f"      {i}. {table_name}")
                logger.debug(f"Profiled table details available for: {table_name}")
        
        # 7. Use the Orchestrator for rule mining - pass config_path
        print("\n STEP 7: Initializing Rule Mining Orchestrator...")
        logger.info("Initializing Rule Mining Orchestrator...")
        orchestrator = RuleMiningOrchestrator(user_cfg, config_path)
        print(" Rule Mining Orchestrator initialized")
        
        # 8. Run enhanced rule mining through orchestrator
        print("\n  STEP 8: Running Enhanced Rule Mining...")
        print("   This may take a few moments...")
        logger.info("Running enhanced rule mining through orchestrator...")
        
        result = orchestrator.run_enhanced_rule_mining(raw_profile)
        print(" Enhanced rule mining completed!")
        
        # 9. Get final configuration
        print("\n STEP 9: Processing Final Configuration...")
        final_config = result['final_config']
        final_config_path = result['final_config_path']
        use_auto_generated = result['use_auto_generated']
        
        print(f"   Final config path: {final_config_path}")
        print(f"   Using auto-generated config: {'Yes' if use_auto_generated else 'No'}")
        
        logger.info(f"Final configuration path: {final_config_path}")
        logger.debug(f"Using auto-generated config: {use_auto_generated}")
        
        # 10. Optional CheckRunner execution
        print("\n STEP 10: Optional CheckRunner Execution")
        print("-" * 40)
        logger.info("Prompting user for CheckRunner execution...")
        
        run_checks = input("\n Review the generated config and run CheckRunner with final config? (Y/N): ").lower().strip()
        
        if run_checks == 'y':
            print("\n Running CheckRunner...")
            logger.info("Running CheckRunner...")
            
            from Checks.check_runner import CheckRunner
            
            run_id = str(uuid.uuid4())
            print(f"   Run ID: {run_id}")
            
            alerting_enabled = user_cfg.get('alerts', {}).get('enabled', False)
            auditing_enabled = user_cfg.get('audit', {}).get('enabled', False)  
            data_source = user_cfg.get('data_source', {}).get('type', None)  
            
            print(f"   Alerting enabled: {alerting_enabled}")
            print(f"   Auditing enabled: {auditing_enabled}")
            print(f"   Data source type: {data_source}")
            
            runner = CheckRunner(
                full_config=final_config,     
                connector=connector,
                check_id=run_id,              
                alerting_enabled=alerting_enabled,
                auditing_enabled=auditing_enabled,
                data_source=data_source
            )    
            
            print("   Executing all checks...")
            results = runner.run_all()
            
            print(" CheckRunner completed successfully!")
            print(f"   Total results: {len(results) if results else 0}")
            
            # logger.info("CheckRunner completed")
            # for i, result_item in enumerate(results, 1):
            #     print(f"      Result {i}: {type(result_item).__name__}")
            #     logger.debug(f"Check result details: {result_item}")
        else:
            print("  Skipping CheckRunner execution")
        
        print("\n" + "=" * 60)
        print(" AUTO CHECK GENERATION PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        logger.info("Auto check generation and check execution process completed successfully")
        return results
        
    except Exception as e:
        print(f"\n ERROR: {str(e)}")
        print("Check the logs for detailed error information.")
        logger.error(f"Error in auto check generation: {str(e)}", exc_info=True)
        raise
    finally:
        print("\n Cleaning up resources...")
        # Ensure proper cleanup of logging resources
        logger_configurator.shutdown()
        print("Cleanup completed")

def run_check_main(args):
    parser = argparse.ArgumentParser(description="Run data quality checks via CLI")
    # parser.add_argument(
    #     "--table", "-t",
    #     required=True,
    #     help="Table name (e.g., public.orders)"
    # )

    parser.add_argument(
        "--check", "-k",
        nargs="*",
        required=False,
        help="Check(s) to run (e.g., null_check, pii_check)"
    )

    # parser.add_argument(
    #     "--column", "-col",
    #     help="Optional: Column to apply check on (e.g., order_id)"
    # )

    parser.add_argument(
        "--conn", "-c",
        required=True,
        help="Path to dq_config.yml or redshift.yaml"
    )

    parser.add_argument(
        "--rule_mining", "-r",
        required=False,
        help="Flag to enable or disble rule mining and auto check generation (Y/N)"
    )

    parsed_args = parser.parse_args(args)

    # Load config
    config_loader = ConfigLoader().load_config(parsed_args.conn)

    # Configuring correct connector class
    connector = ConnectorFactory.get_connector(config_loader, usage='data_source')
    check_id = str(uuid.uuid4())
    alerting_enabled = config_loader.get("alerts", {}).get("enabled", False)
    auditing_enabled = config_loader.get("audit", {}).get("enabled", False)
    data_source = config_loader.get("data_source", {}).get("type", None)
    runner = CheckRunner(full_config=config_loader, connector=connector, check_id=check_id,
                         alerting_enabled=alerting_enabled, auditing_enabled = auditing_enabled, data_source = data_source)

    if parsed_args.rule_mining == 'Y':
        results = run_check_with_rule_mining(parsed_args.conn)
    else:
        if parsed_args.check:
            results = runner.run_selected(parsed_args.check)
        else:
            results = runner.run_all()

    # html = render_check_result_html(results)



    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # html_path = f"CliCheckResult/dq_check_result_{timestamp}.html"

    # with open(html_path, "w") as f:
    #     f.write(html)

    # print(f"Data quality check report saved to {html_path}")

    # Extract failed check names
    failed_checks_set = {
        r["check_name"]
        for r in results
        if r.get("check_status", "").lower() != "pass"
    }

    failed_checks = list(failed_checks_set)

    if failed_checks:
        if len(failed_checks) == 1:
            print(f"{failed_checks[0]} failed! Check RDS audit table - dq_audit.audit_checks for more details.")
        else:
            print(f"{', '.join(failed_checks)} failed! Check RDS audit table - dq_audit.audit_checks for more details.")


def run_freshnessCheck_main(args):
    parser = argparse.ArgumentParser(description="Run data quality Freshnesschecks via CLI")

    parser.add_argument(
        "--table", "-t",
        required=True,
        help="Table name (e.g., public.orders)"
    )

    parser.add_argument(
        "--check", "-k",
        nargs="*",
        required=False,
        help="Check(s) to run (e.g., null_check, pii_check)"
    )

    parser.add_argument(
        "--conn", "-c",
        required=True,
        help="Path to dq_config.yml or redshift.yaml"
    )

    parsed_args = parser.parse_args(args)

    # Load config
    config_loader = ConfigLoader().load_config(parsed_args.conn)
    connector = ConnectorFactory.get_connector(config_loader, usage='data_source')
    check_id = str(uuid.uuid4())
    alerting_enabled = config_loader.get("alerts", {}).get("enabled", False)
    auditing_enabled = config_loader.get("audit", {}).get("enabled", False)
    data_source = config_loader.get("data_source", {}).get("type", None)
    freshness_check_cfg = [check for check in config_loader['checks'] if check['name'] == 'freshness_check'][0]
    if freshness_check_cfg:
        monitor = FreshnessMonitor(full_config=config_loader, check_cfg=freshness_check_cfg, \
                                   connector=connector, check_id=check_id,\
                                   alerting_enabled=alerting_enabled, auditing_enabled = auditing_enabled, data_source = data_source)
        # monitor.start()
        t = threading.Thread(target=monitor.start(), daemon=True)
        t.start()


    connector.close()



def run_profiling_main(args):
    parser = argparse.ArgumentParser(description="Run database profiling via CLI")
    parser.add_argument("--schema", help="Schema name to profile (e.g., public)")
    parser.add_argument("--table", help="Table to profile (e.g., orders)")
    parser.add_argument("--column", help="Optional: Column to profile (e.g., order_id)")
    parser.add_argument("--conn", "-c", required=True, help="Path to dq_config.yml or redshift.yaml")
    parsed_args = parser.parse_args(args)
    config_loader = ConfigLoader().load_config(parsed_args.conn)
    data_source = config_loader.get("data_source", {}).get("type", None) 
    # Configuring correct connector class
    connector = ConnectorFactory.get_connector(config_loader, usage='data_source')

    executor = QueryExecutor(
        connector,
        config_loader['data_source']['type'],
        config_loader['data_source']
    )
    profiler = DatabaseProfiler(executor)
    print("Starting profiling...")
    results = run_profiling(profiler, config_loader)

    audit_connector = ConnectorFactory.get_connector(config_loader, usage='audit')

    print("Inserting results to Audit table...")
    res=ResultAuditor(audit_connector)
    res.insert_profiling_results(results,data_source)

    html = render_profiling_html(results)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = f"CliProfilerResult/dq_profiler_result_{timestamp}.html"

    with open(html_path, "w") as f:
        f.write(html)


    print(f"HTML Profiling report available in {html_path}!")

    # Clean up
    connector.close()


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        sub_args = sys.argv[2:]

        if command == "run-check":
            run_check_main(sub_args)
        elif command == "run-profile":
            run_profiling_main(sub_args)
        elif command == "run-freshnessCheck":
            run_freshnessCheck_main(sub_args)
        else:
            print(f"\nUnknown command: {command}")
            print_usage()
    else:
        print_usage()


def print_usage():
    print("""
Usage:
  dqtoolss run-check   --table <table> --check <check(s)> --conn <config_path>
  dqtoolss run-profile --schema <schema> --table <table> --conn <config_path>

Examples:
  dqtool run-check --table public.users --check null_check uniqueness_check --conn dq_config.yml
  dqtool run-profile --schema public --table employees --conn dq_config.yml
""")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"{str(e)}\n{traceback.format_exc()}")
        raise e
