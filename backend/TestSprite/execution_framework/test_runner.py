"""
TestSprite Test Runner
Comprehensive test execution framework for CRM backend system
"""

import os
import sys
import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import subprocess
import threading
from pathlib import Path

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"

@dataclass
class TestResult:
    test_name: str
    status: TestStatus
    duration: float
    message: str = ""
    traceback: str = ""
    output: str = ""

@dataclass
class TestSuite:
    name: str
    category: str
    file_path: str
    tests: List[str]
    results: List[TestResult]
    total_duration: float = 0.0

class TestSpiteRunner:
    """
    Comprehensive test runner for TestSprite MCP server integration
    """
    
    def __init__(self, project_path: str, config_path: Optional[str] = None):
        self.project_path = Path(project_path)
        self.backend_path = self.project_path / "backend"
        self.testsprite_path = self.backend_path / "TestSprite"
        self.config = self._load_config(config_path)
        self.test_suites = []
        self.results = {}
        self.is_running = False
        
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load test configuration"""
        default_config = {
            "local_port": 8000,
            "test_scope": "codebase",
            "type": "backend",
            "iterative_mode": True,
            "parallel_execution": True,
            "auto_fix": True,
            "max_iterations": 10,
            "timeout_per_test": 300,
            "retry_count": 3,
            "parallel_workers": 4,
            "memory_limit": "2GB",
            "coverage_threshold": 90,
            "performance_threshold": 200,  # ms
            "test_categories": ["unit", "integration", "e2e"],
            "required_pass_rate": 100.0
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                custom_config = json.load(f)
                default_config.update(custom_config)
                
        return default_config
    
    def discover_tests(self) -> List[TestSuite]:
        """Discover all test files and test cases"""
        test_suites = []
        
        # Unit tests
        unit_test_dir = self.testsprite_path / "unit_tests"
        if unit_test_dir.exists():
            for test_file in unit_test_dir.glob("test_*.py"):
                suite = self._create_test_suite("unit", test_file)
                test_suites.append(suite)
        
        # Integration tests
        integration_test_dir = self.testsprite_path / "integration_tests"
        if integration_test_dir.exists():
            for test_file in integration_test_dir.glob("test_*.py"):
                suite = self._create_test_suite("integration", test_file)
                test_suites.append(suite)
        
        # E2E tests
        e2e_test_dir = self.testsprite_path / "e2e_tests"
        if e2e_test_dir.exists():
            for test_file in e2e_test_dir.glob("test_*.py"):
                suite = self._create_test_suite("e2e", test_file)
                test_suites.append(suite)
        
        self.test_suites = test_suites
        return test_suites
    
    def _create_test_suite(self, category: str, test_file: Path) -> TestSuite:
        """Create a test suite from a test file"""
        test_methods = self._extract_test_methods(test_file)
        return TestSuite(
            name=test_file.stem,
            category=category,
            file_path=str(test_file),
            tests=test_methods,
            results=[]
        )
    
    def _extract_test_methods(self, test_file: Path) -> List[str]:
        """Extract test method names from a test file"""
        test_methods = []
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('def test_') and '(' in line:
                        method_name = line.split('(')[0].replace('def ', '')
                        test_methods.append(method_name)
        except Exception as e:
            print(f"Error extracting test methods from {test_file}: {e}")
        
        return test_methods
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """
        Run comprehensive test suite with iterative fixing
        """
        print("🚀 Starting comprehensive TestSprite test execution...")
        
        self.is_running = True
        iteration = 0
        max_iterations = self.config["max_iterations"]
        
        while iteration < max_iterations and self.is_running:
            iteration += 1
            print(f"\n📊 Test Iteration {iteration}/{max_iterations}")
            
            # Discover tests
            test_suites = self.discover_tests()
            print(f"📝 Discovered {len(test_suites)} test suites")
            
            # Run tests based on configuration
            if self.config["parallel_execution"]:
                results = await self._run_tests_parallel(test_suites)
            else:
                results = await self._run_tests_sequential(test_suites)
            
            # Analyze results
            analysis = self._analyze_results(results)
            
            # Check if we achieved 100% success
            if analysis["pass_rate"] >= self.config["required_pass_rate"]:
                print(f"✅ SUCCESS! Achieved {analysis['pass_rate']:.1f}% pass rate")
                break
            
            # Auto-fix failures if enabled
            if self.config["auto_fix"] and analysis["failures"]:
                print(f"🔧 Auto-fixing {len(analysis['failures'])} failures...")
                await self._auto_fix_failures(analysis["failures"])
            else:
                print(f"❌ Test failures detected. Pass rate: {analysis['pass_rate']:.1f}%")
                break
        
        # Generate final report
        final_report = self._generate_final_report(iteration, max_iterations)
        
        self.is_running = False
        return final_report
    
    async def _run_tests_parallel(self, test_suites: List[TestSuite]) -> Dict[str, TestResult]:
        """Run tests in parallel"""
        print("🔄 Running tests in parallel mode...")
        
        # Create semaphore to limit concurrent workers
        semaphore = asyncio.Semaphore(self.config["parallel_workers"])
        
        async def run_suite_with_semaphore(suite):
            async with semaphore:
                return await self._run_test_suite(suite)
        
        # Execute all suites
        tasks = [run_suite_with_semaphore(suite) for suite in test_suites]
        suite_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Collect results
        all_results = {}
        for i, result in enumerate(suite_results):
            if isinstance(result, Exception):
                print(f"❌ Suite {test_suites[i].name} failed with exception: {result}")
            else:
                all_results.update(result)
        
        return all_results
    
    async def _run_tests_sequential(self, test_suites: List[TestSuite]) -> Dict[str, TestResult]:
        """Run tests sequentially"""
        print("🔄 Running tests in sequential mode...")
        
        all_results = {}
        for suite in test_suites:
            suite_results = await self._run_test_suite(suite)
            all_results.update(suite_results)
        
        return all_results
    
    async def _run_test_suite(self, suite: TestSuite) -> Dict[str, TestResult]:
        """Run a single test suite"""
        print(f"  🧪 Running {suite.category} tests: {suite.name}")
        
        results = {}
        start_time = time.time()
        
        try:
            # Run pytest on the test file
            cmd = [
                sys.executable, "-m", "pytest",
                suite.file_path,
                "-v",
                "--tb=short",
                f"--timeout={self.config['timeout_per_test']}",
                "--capture=no"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.backend_path)
            )
            
            stdout, stderr = await process.communicate()
            
            # Parse pytest output
            results = self._parse_pytest_output(
                stdout.decode('utf-8', errors='ignore'),
                stderr.decode('utf-8', errors='ignore'),
                suite
            )
            
        except Exception as e:
            print(f"❌ Error running suite {suite.name}: {e}")
            # Create error result for all tests in suite
            for test_name in suite.tests:
                results[f"{suite.name}::{test_name}"] = TestResult(
                    test_name=test_name,
                    status=TestStatus.ERROR,
                    duration=0.0,
                    message=str(e)
                )
        
        suite.total_duration = time.time() - start_time
        suite.results = list(results.values())
        
        return results
    
    def _parse_pytest_output(self, stdout: str, stderr: str, suite: TestSuite) -> Dict[str, TestResult]:
        """Parse pytest output to extract test results"""
        results = {}
        
        # Simple parsing - look for test outcomes
        lines = stdout.split('\n') + stderr.split('\n')
        
        for line in lines:
            if '::test_' in line:
                if ' PASSED ' in line:
                    test_name = self._extract_test_name(line)
                    if test_name:
                        results[f"{suite.name}::{test_name}"] = TestResult(
                            test_name=test_name,
                            status=TestStatus.PASSED,
                            duration=self._extract_duration(line),
                            message="Test passed"
                        )
                elif ' FAILED ' in line:
                    test_name = self._extract_test_name(line)
                    if test_name:
                        results[f"{suite.name}::{test_name}"] = TestResult(
                            test_name=test_name,
                            status=TestStatus.FAILED,
                            duration=self._extract_duration(line),
                            message="Test failed",
                            output=stderr
                        )
                elif ' ERROR ' in line:
                    test_name = self._extract_test_name(line)
                    if test_name:
                        results[f"{suite.name}::{test_name}"] = TestResult(
                            test_name=test_name,
                            status=TestStatus.ERROR,
                            duration=self._extract_duration(line),
                            message="Test error",
                            output=stderr
                        )
        
        # If no results parsed, create default results
        if not results:
            for test_name in suite.tests:
                results[f"{suite.name}::{test_name}"] = TestResult(
                    test_name=test_name,
                    status=TestStatus.SKIPPED,
                    duration=0.0,
                    message="No result parsed"
                )
        
        return results
    
    def _extract_test_name(self, line: str) -> Optional[str]:
        """Extract test name from pytest output line"""
        try:
            if '::test_' in line:
                parts = line.split('::')
                for part in parts:
                    if part.startswith('test_'):
                        return part.split()[0]
        except:
            pass
        return None
    
    def _extract_duration(self, line: str) -> float:
        """Extract test duration from pytest output"""
        try:
            if 's]' in line:
                duration_part = line.split('[')[1].split(']')[0]
                if 's' in duration_part:
                    return float(duration_part.replace('s', ''))
        except:
            pass
        return 0.0
    
    def _analyze_results(self, results: Dict[str, TestResult]) -> Dict[str, Any]:
        """Analyze test results and generate summary"""
        total_tests = len(results)
        if total_tests == 0:
            return {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "errors": 0,
                "skipped": 0,
                "pass_rate": 0.0,
                "failures": [],
                "performance_issues": []
            }
        
        passed = sum(1 for r in results.values() if r.status == TestStatus.PASSED)
        failed = sum(1 for r in results.values() if r.status == TestStatus.FAILED)
        errors = sum(1 for r in results.values() if r.status == TestStatus.ERROR)
        skipped = sum(1 for r in results.values() if r.status == TestStatus.SKIPPED)
        
        pass_rate = (passed / total_tests) * 100
        
        failures = [r for r in results.values() if r.status in [TestStatus.FAILED, TestStatus.ERROR]]
        
        performance_issues = [
            r for r in results.values()
            if r.duration > (self.config["performance_threshold"] / 1000)
        ]
        
        return {
            "total": total_tests,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "pass_rate": pass_rate,
            "failures": failures,
            "performance_issues": performance_issues
        }
    
    async def _auto_fix_failures(self, failures: List[TestResult]) -> None:
        """Attempt to auto-fix test failures"""
        print(f"🔧 Attempting to auto-fix {len(failures)} failures...")
        
        for failure in failures:
            try:
                await self._fix_individual_failure(failure)
            except Exception as e:
                print(f"❌ Failed to auto-fix {failure.test_name}: {e}")
    
    async def _fix_individual_failure(self, failure: TestResult) -> None:
        """Attempt to fix an individual test failure"""
        # This is a placeholder for auto-fix logic
        # In practice, this would analyze the failure and apply common fixes
        
        print(f"  🔍 Analyzing failure: {failure.test_name}")
        
        # Common fixes could include:
        # - Missing dependencies
        # - Database connection issues
        # - Import path problems
        # - Configuration issues
        
        # For now, just log the failure details
        if failure.output:
            print(f"    Error output: {failure.output[:200]}...")
    
    def _generate_final_report(self, iterations_run: int, max_iterations: int) -> Dict[str, Any]:
        """Generate comprehensive final test report"""
        
        # Collect all results from the last run
        all_results = {}
        for suite in self.test_suites:
            for result in suite.results:
                all_results[f"{suite.name}::{result.test_name}"] = result
        
        analysis = self._analyze_results(all_results)
        
        # Calculate suite-level statistics
        suite_stats = {}
        for suite in self.test_suites:
            suite_analysis = self._analyze_results({
                f"{suite.name}::{r.test_name}": r for r in suite.results
            })
            suite_stats[suite.name] = {
                "category": suite.category,
                "total_tests": suite_analysis["total"],
                "pass_rate": suite_analysis["pass_rate"],
                "duration": suite.total_duration
            }
        
        # Performance metrics
        total_duration = sum(suite.total_duration for suite in self.test_suites)
        avg_test_duration = total_duration / max(analysis["total"], 1)
        
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "iterations_run": iterations_run,
            "max_iterations": max_iterations,
            "completed_successfully": analysis["pass_rate"] >= self.config["required_pass_rate"],
            "overall_statistics": analysis,
            "suite_statistics": suite_stats,
            "performance_metrics": {
                "total_duration": total_duration,
                "average_test_duration": avg_test_duration,
                "performance_threshold": self.config["performance_threshold"],
                "performance_issues_count": len(analysis["performance_issues"])
            },
            "configuration": self.config,
            "recommendations": self._generate_recommendations(analysis)
        }
        
        # Save report to file
        report_path = self.testsprite_path / "reports" / f"test_report_{int(time.time())}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📊 Final report saved to: {report_path}")
        
        return report
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        if analysis["pass_rate"] < 100:
            recommendations.append(f"Address {analysis['failed'] + analysis['errors']} failing tests to achieve 100% pass rate")
        
        if analysis["performance_issues"]:
            recommendations.append(f"Optimize {len(analysis['performance_issues'])} slow tests for better performance")
        
        if analysis["skipped"] > 0:
            recommendations.append(f"Investigate {analysis['skipped']} skipped tests")
        
        if not recommendations:
            recommendations.append("All tests passing! Consider adding more comprehensive test coverage")
        
        return recommendations
    
    def stop_testing(self):
        """Stop the test execution"""
        self.is_running = False
        print("🛑 Test execution stopped by user")

# Utility functions for external usage
def create_test_runner(project_path: str) -> TestSpiteRunner:
    """Create a new TestSprite runner instance"""
    return TestSpiteRunner(project_path)

async def run_full_test_suite(project_path: str, config_path: Optional[str] = None) -> Dict[str, Any]:
    """Run the complete test suite and return results"""
    runner = create_test_runner(project_path)
    if config_path:
        runner.config.update(runner._load_config(config_path))
    
    return await runner.run_comprehensive_tests()

if __name__ == "__main__":
    # Command line execution
    import argparse
    
    parser = argparse.ArgumentParser(description="TestSprite Test Runner")
    parser.add_argument("--project-path", required=True, help="Path to the project root")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    # Run tests
    runner = TestSpiteRunner(args.project_path, args.config)
    result = asyncio.run(runner.run_comprehensive_tests())
    
    # Exit with appropriate code
    exit_code = 0 if result.get("completed_successfully", False) else 1
    sys.exit(exit_code)