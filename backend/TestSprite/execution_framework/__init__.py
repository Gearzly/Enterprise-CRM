"""
TestSprite Execution Framework Package
Main entry point for TestSprite MCP server integration
"""

from .test_runner import TestSpiteRunner, create_test_runner, run_full_test_suite
from .test_config import TestConfig, get_config, set_config
from .test_reporter import TestReporter, TestMetrics, SuiteReport

__version__ = "1.0.0"
__author__ = "TestSprite Framework"

__all__ = [
    "TestSpiteRunner",
    "TestConfig", 
    "TestReporter",
    "TestMetrics",
    "SuiteReport",
    "create_test_runner",
    "run_full_test_suite",
    "get_config",
    "set_config"
]

# Default configuration for CRM project
DEFAULT_CRM_CONFIG = {
    "project_name": "CRM Backend",
    "local_port": 8000,
    "test_scope": "codebase",
    "type": "backend",
    "required_pass_rate": 100.0,
    "iterative_mode": True,
    "auto_fix": True,
    "parallel_execution": True,
    "max_iterations": 10
}