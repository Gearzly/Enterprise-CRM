"""
TestSprite Configuration Management
Configuration settings for comprehensive test execution
"""

import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class TestConfig:
    """
    Centralized configuration management for TestSprite tests
    """
    
    DEFAULT_CONFIG = {
        # Server Configuration
        "local_port": 8000,
        "test_scope": "codebase",
        "type": "backend",
        "project_name": "CRM",
        
        # Execution Configuration
        "iterative_mode": True,
        "parallel_execution": True,
        "auto_fix": True,
        "max_iterations": 10,
        "timeout_per_test": 300,  # seconds
        "retry_count": 3,
        "parallel_workers": 4,
        
        # Resource Limits
        "memory_limit": "2GB",
        "cpu_limit": "80%",
        "disk_limit": "10GB",
        
        # Quality Thresholds
        "coverage_threshold": 90.0,
        "performance_threshold": 200,  # milliseconds
        "required_pass_rate": 100.0,
        "security_threshold": 100.0,
        
        # Test Categories
        "test_categories": {
            "unit": {
                "enabled": True,
                "priority": 1,
                "timeout_multiplier": 1.0,
                "parallel_safe": True
            },
            "integration": {
                "enabled": True,
                "priority": 2,
                "timeout_multiplier": 2.0,
                "parallel_safe": True
            },
            "e2e": {
                "enabled": True,
                "priority": 3,
                "timeout_multiplier": 5.0,
                "parallel_safe": False
            }
        },
        
        # Database Configuration
        "database": {
            "test_db_url": "sqlite:///test_crm.db",
            "use_memory_db": True,
            "reset_between_tests": True,
            "transaction_isolation": True
        },
        
        # Security Configuration
        "security": {
            "enable_security_tests": True,
            "check_vulnerabilities": True,
            "sanitization_tests": True,
            "authentication_tests": True,
            "authorization_tests": True
        },
        
        # Performance Configuration
        "performance": {
            "enable_performance_tests": True,
            "response_time_threshold": 200,  # ms
            "concurrent_users": 10,
            "load_test_duration": 60,  # seconds
            "memory_usage_threshold": 512  # MB
        },
        
        # Reporting Configuration
        "reporting": {
            "detailed_output": True,
            "save_logs": True,
            "generate_html_report": True,
            "generate_json_report": True,
            "generate_junit_xml": True,
            "report_directory": "reports"
        },
        
        # TestSprite MCP Configuration
        "testsprite": {
            "bootstrap_required": True,
            "generate_prd": True,
            "generate_test_plan": True,
            "additional_instructions": [
                "Run comprehensive test suite with iterative fixing",
                "Achieve 100% pass rate before completion",
                "Fix issues in parallel with test execution",
                "Generate detailed reports for all test categories"
            ]
        },
        
        # Environment Variables
        "environment": {
            "TESTING": "true",
            "LOG_LEVEL": "DEBUG",
            "DATABASE_URL": "sqlite:///test_crm.db",
            "REDIS_URL": "redis://localhost:6379/0",
            "SECRET_KEY": "test-secret-key-for-testing-only"
        },
        
        # Dependencies
        "dependencies": {
            "required_packages": [
                "pytest>=7.0.0",
                "pytest-asyncio>=0.21.0",
                "pytest-cov>=4.0.0",
                "pytest-timeout>=2.1.0",
                "httpx>=0.24.0",
                "fastapi[all]>=0.100.0",
                "sqlalchemy>=2.0.0",
                "redis>=4.5.0"
            ],
            "optional_packages": [
                "pytest-xdist",
                "pytest-html",
                "pytest-benchmark",
                "pytest-mock"
            ]
        },
        
        # Auto-fix Configuration
        "auto_fix": {
            "enabled": True,
            "fix_types": [
                "import_errors",
                "dependency_issues",
                "configuration_errors",
                "database_connection",
                "simple_syntax_errors"
            ],
            "max_fix_attempts": 3,
            "rollback_on_failure": True
        }
    }
    
    def __init__(self, config_path: Optional[str] = None, project_path: Optional[str] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        self.project_path = Path(project_path) if project_path else Path.cwd()
        
        if config_path:
            self.load_config_file(config_path)
        else:
            # Try to find config file in project
            self._auto_discover_config()
        
        # Update paths based on project
        self._update_project_paths()
    
    def load_config_file(self, config_path: str) -> None:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                custom_config = json.load(f)
                self._merge_config(custom_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_path}: {e}")
    
    def _auto_discover_config(self) -> None:
        """Auto-discover configuration files in project"""
        possible_configs = [
            self.project_path / "testsprite.json",
            self.project_path / "backend" / "testsprite.json",
            self.project_path / "backend" / "TestSprite" / "config.json",
            self.project_path / ".testsprite.json"
        ]
        
        for config_path in possible_configs:
            if config_path.exists():
                self.load_config_file(str(config_path))
                break
    
    def _merge_config(self, custom_config: Dict[str, Any]) -> None:
        """Merge custom configuration with defaults"""
        def merge_dicts(base: Dict, custom: Dict) -> Dict:
            result = base.copy()
            for key, value in custom.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = merge_dicts(result[key], value)
                else:
                    result[key] = value
            return result
        
        self.config = merge_dicts(self.config, custom_config)
    
    def _update_project_paths(self) -> None:
        """Update configuration paths based on project structure"""
        backend_path = self.project_path / "backend"
        testsprite_path = backend_path / "TestSprite"
        
        # Update database path
        if self.config["database"]["test_db_url"] == "sqlite:///test_crm.db":
            self.config["database"]["test_db_url"] = f"sqlite:///{backend_path}/test_crm.db"
        
        # Update report directory
        if self.config["reporting"]["report_directory"] == "reports":
            self.config["reporting"]["report_directory"] = str(testsprite_path / "reports")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation"""
        keys = key.split('.')
        config_ref = self.config
        
        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]
        
        config_ref[keys[-1]] = value
    
    def save_config(self, output_path: str) -> None:
        """Save current configuration to file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config to {output_path}: {e}")
    
    def get_testsprite_params(self) -> Dict[str, Any]:
        """Get parameters for TestSprite MCP server calls"""
        return {
            "localPort": self.config["local_port"],
            "type": self.config["type"],
            "projectPath": str(self.project_path),
            "testScope": self.config["test_scope"],
            "projectName": self.config.get("project_name", "CRM"),
            "additionalInstruction": " | ".join(self.config["testsprite"]["additional_instructions"])
        }
    
    def get_pytest_args(self) -> list:
        """Get pytest command line arguments based on configuration"""
        args = ["-v"]
        
        # Coverage
        if self.config["coverage_threshold"] > 0:
            args.extend([
                "--cov=.",
                f"--cov-report=term-missing",
                f"--cov-fail-under={self.config['coverage_threshold']}"
            ])
        
        # Timeout
        if self.config["timeout_per_test"] > 0:
            args.append(f"--timeout={self.config['timeout_per_test']}")
        
        # Parallel execution
        if self.config["parallel_execution"] and self.config["parallel_workers"] > 1:
            args.extend(["-n", str(self.config["parallel_workers"])])
        
        # Output options
        if self.config["reporting"]["detailed_output"]:
            args.append("--tb=short")
        
        # XML output for CI/CD
        if self.config["reporting"]["generate_junit_xml"]:
            args.extend(["--junit-xml", f"{self.config['reporting']['report_directory']}/junit.xml"])
        
        # HTML report
        if self.config["reporting"]["generate_html_report"]:
            args.extend(["--html", f"{self.config['reporting']['report_directory']}/report.html"])
        
        return args
    
    def validate_config(self) -> list:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Check required values
        required_keys = [
            "local_port",
            "test_scope", 
            "type",
            "required_pass_rate"
        ]
        
        for key in required_keys:
            if not self.get(key):
                issues.append(f"Missing required configuration: {key}")
        
        # Validate ranges
        if not (1 <= self.config["local_port"] <= 65535):
            issues.append("local_port must be between 1 and 65535")
        
        if not (0 <= self.config["required_pass_rate"] <= 100):
            issues.append("required_pass_rate must be between 0 and 100")
        
        if not (1 <= self.config["parallel_workers"] <= 32):
            issues.append("parallel_workers must be between 1 and 32")
        
        # Validate paths
        if not self.project_path.exists():
            issues.append(f"Project path does not exist: {self.project_path}")
        
        return issues
    
    def get_environment_vars(self) -> Dict[str, str]:
        """Get environment variables for test execution"""
        return {k: str(v) for k, v in self.config["environment"].items()}
    
    def is_category_enabled(self, category: str) -> bool:
        """Check if a test category is enabled"""
        return self.config["test_categories"].get(category, {}).get("enabled", False)
    
    def get_category_config(self, category: str) -> Dict[str, Any]:
        """Get configuration for a specific test category"""
        return self.config["test_categories"].get(category, {})
    
    def __str__(self) -> str:
        """String representation of configuration"""
        return json.dumps(self.config, indent=2)

# Global configuration instance
_global_config = None

def get_config(project_path: Optional[str] = None, config_path: Optional[str] = None) -> TestConfig:
    """Get global configuration instance"""
    global _global_config
    if _global_config is None:
        _global_config = TestConfig(config_path, project_path)
    return _global_config

def set_config(config: TestConfig) -> None:
    """Set global configuration instance"""
    global _global_config
    _global_config = config

# Configuration templates for different scenarios
PRODUCTION_CONFIG = {
    "parallel_execution": False,
    "auto_fix": False,
    "timeout_per_test": 600,
    "required_pass_rate": 100.0,
    "security.check_vulnerabilities": True,
    "performance.enable_performance_tests": True
}

DEVELOPMENT_CONFIG = {
    "parallel_execution": True,
    "auto_fix": True,
    "timeout_per_test": 300,
    "required_pass_rate": 90.0,
    "reporting.detailed_output": True
}

QUICK_TEST_CONFIG = {
    "test_categories.e2e.enabled": False,
    "performance.enable_performance_tests": False,
    "timeout_per_test": 60,
    "parallel_workers": 8
}