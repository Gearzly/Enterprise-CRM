"""
Comprehensive Test Runner for CRM Backend
Orchestrates all test suites and generates consolidated reports

This runner executes:
1. Comprehensive Backend Tests (functionality)
2. OAuth2+PKCE Migration Tests (security migration)
3. Security Validation Tests (OWASP compliance)
4. Performance Tests (response times)
5. Integration Tests (end-to-end)
"""
import asyncio
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Import test suites
from comprehensive_backend_tests import ComprehensiveBackendTester, TestConfig
from oauth2_migration_tests import OAuth2PKCEMigrationTester
from security_validation_tests import SecurityValidationTester

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestOrchestrator:
    """Orchestrates all test suites and generates consolidated reports"""
    
    def __init__(self, base_url: str = "http://localhost:5173"):
        self.base_url = base_url
        self.test_config = TestConfig(base_url=base_url)
        self.results = {}
        self.start_time = None
        self.end_time = None
        
    async def run_backend_functionality_tests(self):
        """Run comprehensive backend functionality tests"""
        logger.info("🚀 Starting Backend Functionality Tests")
        
        tester = ComprehensiveBackendTester(self.test_config)
        try:
            results = await tester.run_all_tests()
            self.results["backend_functionality"] = results
            logger.info("✅ Backend Functionality Tests Completed")
            return results
        except Exception as e:
            logger.error(f"❌ Backend Functionality Tests Failed: {e}")
            self.results["backend_functionality"] = {"error": str(e)}
            return {"error": str(e)}
    
    async def run_oauth2_migration_tests(self):
        """Run OAuth2+PKCE migration tests"""
        logger.info("🔐 Starting OAuth2+PKCE Migration Tests")
        
        tester = OAuth2PKCEMigrationTester(self.base_url)
        try:
            results = await tester.run_comprehensive_migration_tests()
            self.results["oauth2_migration"] = results
            logger.info("✅ OAuth2+PKCE Migration Tests Completed")
            return results
        except Exception as e:
            logger.error(f"❌ OAuth2+PKCE Migration Tests Failed: {e}")
            self.results["oauth2_migration"] = {"error": str(e)}
            return {"error": str(e)}
    
    async def run_security_validation_tests(self):
        """Run security validation tests"""
        logger.info("🔒 Starting Security Validation Tests")
        
        tester = SecurityValidationTester(self.base_url)
        try:
            results = await tester.run_comprehensive_security_tests()
            self.results["security_validation"] = results
            logger.info("✅ Security Validation Tests Completed")
            return results
        except Exception as e:
            logger.error(f"❌ Security Validation Tests Failed: {e}")
            self.results["security_validation"] = {"error": str(e)}
            return {"error": str(e)}
    
    async def run_performance_tests(self):
        """Run basic performance tests"""
        logger.info("⚡ Starting Performance Tests")
        
        import httpx
        
        performance_results = {}
        endpoints = [
            "/",
            "/health", 
            "/auth/challenge",
            "/api/superadmin",
            "/sales/",
            "/marketing/",
            "/support/"
        ]
        
        async with httpx.AsyncClient(timeout=30) as client:
            for endpoint in endpoints:
                try:
                    # Warm up
                    await client.get(f"{self.base_url}{endpoint}")
                    
                    # Test multiple requests
                    times = []
                    for _ in range(5):
                        start = time.time()
                        response = await client.get(f"{self.base_url}{endpoint}")
                        duration = time.time() - start
                        times.append(duration)
                    
                    performance_results[endpoint] = {
                        "avg_response_time": sum(times) / len(times),
                        "min_response_time": min(times),
                        "max_response_time": max(times),
                        "samples": len(times),
                        "all_successful": all(t < 5.0 for t in times)  # All under 5 seconds
                    }
                    
                except Exception as e:
                    performance_results[endpoint] = {
                        "error": str(e),
                        "accessible": False
                    }
        
        # Calculate overall performance score
        successful_tests = [r for r in performance_results.values() if "avg_response_time" in r]
        if successful_tests:
            avg_response_time = sum(r["avg_response_time"] for r in successful_tests) / len(successful_tests)
            performance_score = "EXCELLENT" if avg_response_time < 0.5 else \
                              "GOOD" if avg_response_time < 1.0 else \
                              "FAIR" if avg_response_time < 2.0 else "POOR"
        else:
            performance_score = "NO_DATA"
            avg_response_time = None
        
        self.results["performance"] = {
            "endpoint_tests": performance_results,
            "overall_avg_response_time": avg_response_time,
            "performance_score": performance_score,
            "total_endpoints_tested": len(endpoints),
            "successful_endpoints": len(successful_tests)
        }
        
        logger.info("✅ Performance Tests Completed")
        return self.results["performance"]
    
    async def run_integration_tests(self):
        """Run basic integration tests"""
        logger.info("🔗 Starting Integration Tests")
        
        import httpx
        
        integration_results = {}
        
        async with httpx.AsyncClient(timeout=30) as client:
            # Test 1: Server startup and health
            try:
                health_response = await client.get(f"{self.base_url}/health")
                integration_results["server_health"] = {
                    "status_code": health_response.status_code,
                    "healthy": health_response.status_code == 200,
                    "response_data": health_response.json() if health_response.status_code == 200 else None
                }
            except Exception as e:
                integration_results["server_health"] = {"error": str(e), "healthy": False}
            
            # Test 2: API documentation availability
            try:
                docs_response = await client.get(f"{self.base_url}/docs")
                openapi_response = await client.get(f"{self.base_url}/openapi.json")
                
                integration_results["api_documentation"] = {
                    "docs_available": docs_response.status_code == 200,
                    "openapi_available": openapi_response.status_code == 200,
                    "documentation_complete": docs_response.status_code == 200 and openapi_response.status_code == 200
                }
            except Exception as e:
                integration_results["api_documentation"] = {"error": str(e)}
            
            # Test 3: Module integration
            modules = [
                ("/sales/", "Sales"),
                ("/marketing/", "Marketing"), 
                ("/support/", "Support"),
                ("/api/superadmin", "SuperAdmin"),
                ("/auth/challenge", "Authentication")
            ]
            
            module_results = {}
            for endpoint, module_name in modules:
                try:
                    response = await client.get(f"{self.base_url}{endpoint}")
                    module_results[module_name] = {
                        "accessible": response.status_code in [200, 401, 403],  # 401/403 means working but protected
                        "status_code": response.status_code,
                        "integrated": response.status_code != 404
                    }
                except Exception as e:
                    module_results[module_name] = {"error": str(e), "integrated": False}
            
            integration_results["module_integration"] = module_results
            
            # Test 4: Database integration (via health check or simple query)
            try:
                # Test a simple endpoint that likely uses database
                root_response = await client.get(f"{self.base_url}/")
                integration_results["database_integration"] = {
                    "accessible": root_response.status_code == 200,
                    "no_db_errors": root_response.status_code != 500
                }
            except Exception as e:
                integration_results["database_integration"] = {"error": str(e)}
        
        # Calculate integration score
        total_tests = len(integration_results)
        passed_tests = 0
        
        for test_name, test_result in integration_results.items():
            if isinstance(test_result, dict):
                if test_name == "server_health" and test_result.get("healthy"):
                    passed_tests += 1
                elif test_name == "api_documentation" and test_result.get("documentation_complete"):
                    passed_tests += 1
                elif test_name == "module_integration":
                    integrated_modules = sum(1 for module in test_result.values() 
                                           if isinstance(module, dict) and module.get("integrated"))
                    if integrated_modules >= len(modules) * 0.8:  # 80% of modules working
                        passed_tests += 1
                elif test_name == "database_integration" and test_result.get("accessible"):
                    passed_tests += 1
        
        integration_score = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        self.results["integration"] = {
            "test_results": integration_results,
            "integration_score": f"{integration_score:.1f}%",
            "passed_tests": passed_tests,
            "total_tests": total_tests
        }
        
        logger.info("✅ Integration Tests Completed")
        return self.results["integration"]
    
    def generate_consolidated_report(self):
        """Generate consolidated test report"""
        logger.info("📊 Generating Consolidated Test Report")
        
        # Calculate overall statistics
        total_tests = 0
        total_passed = 0
        total_failed = 0
        
        # Collect statistics from each test suite
        suite_summaries = {}
        
        for suite_name, suite_results in self.results.items():
            if isinstance(suite_results, dict) and "error" not in suite_results:
                if suite_name == "backend_functionality":
                    total_tests += suite_results.get("total_tests", 0)
                    total_passed += suite_results.get("passed", 0)
                    total_failed += suite_results.get("failed", 0)
                    suite_summaries[suite_name] = {
                        "status": "COMPLETED",
                        "tests": suite_results.get("total_tests", 0),
                        "passed": suite_results.get("passed", 0),
                        "pass_rate": suite_results.get("pass_rate", "0%")
                    }
                
                elif suite_name == "oauth2_migration":
                    migration_summary = suite_results.get("migration_test_summary", {})
                    total_tests += migration_summary.get("total_tests", 0)
                    total_passed += migration_summary.get("passed", 0)
                    total_failed += migration_summary.get("failed", 0)
                    suite_summaries[suite_name] = {
                        "status": suite_results.get("migration_status", "UNKNOWN"),
                        "tests": migration_summary.get("total_tests", 0),
                        "passed": migration_summary.get("passed", 0),
                        "pass_rate": migration_summary.get("pass_rate", "0%")
                    }
                
                elif suite_name == "security_validation":
                    security_summary = suite_results.get("security_test_summary", {})
                    total_tests += security_summary.get("total_tests", 0)
                    total_passed += security_summary.get("passed", 0)
                    total_failed += security_summary.get("failed", 0)
                    suite_summaries[suite_name] = {
                        "status": "COMPLETED",
                        "tests": security_summary.get("total_tests", 0),
                        "passed": security_summary.get("passed", 0),
                        "security_score": security_summary.get("overall_security_score", "0%"),
                        "security_level": security_summary.get("security_level", "UNKNOWN")
                    }
                
                elif suite_name == "performance":
                    suite_summaries[suite_name] = {
                        "status": "COMPLETED",
                        "performance_score": suite_results.get("performance_score", "NO_DATA"),
                        "avg_response_time": suite_results.get("overall_avg_response_time"),
                        "endpoints_tested": suite_results.get("total_endpoints_tested", 0)
                    }
                
                elif suite_name == "integration":
                    suite_summaries[suite_name] = {
                        "status": "COMPLETED",
                        "integration_score": suite_results.get("integration_score", "0%"),
                        "passed_tests": suite_results.get("passed_tests", 0),
                        "total_tests": suite_results.get("total_tests", 0)
                    }
            else:
                suite_summaries[suite_name] = {
                    "status": "FAILED",
                    "error": suite_results.get("error", "Unknown error") if isinstance(suite_results, dict) else "Unknown error"
                }
        
        # Calculate overall metrics
        overall_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        test_duration = (self.end_time - self.start_time) if self.start_time and self.end_time else 0
        
        # Determine overall system status
        if overall_pass_rate >= 90:
            system_status = "EXCELLENT"
        elif overall_pass_rate >= 75:
            system_status = "GOOD"
        elif overall_pass_rate >= 60:
            system_status = "FAIR"
        else:
            system_status = "POOR"
        
        consolidated_report = {
            "test_execution_summary": {
                "timestamp": datetime.now().isoformat(),
                "test_duration_seconds": test_duration,
                "base_url": self.base_url,
                "total_test_suites": len(self.results),
                "successful_suites": len([s for s in suite_summaries.values() if s.get("status") == "COMPLETED"])
            },
            "overall_metrics": {
                "total_tests": total_tests,
                "total_passed": total_passed,
                "total_failed": total_failed,
                "overall_pass_rate": f"{overall_pass_rate:.1f}%",
                "system_status": system_status
            },
            "suite_summaries": suite_summaries,
            "detailed_results": self.results,
            "recommendations": self.generate_recommendations(suite_summaries, overall_pass_rate)
        }
        
        return consolidated_report
    
    def generate_recommendations(self, suite_summaries: Dict, overall_pass_rate: float) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Overall system recommendations
        if overall_pass_rate < 80:
            recommendations.append("⚠️ CRITICAL: Overall pass rate is below 80%. Immediate attention required.")
        
        # Security recommendations
        security_summary = suite_summaries.get("security_validation", {})
        if security_summary.get("security_level") in ["POOR", "FAIR"]:
            recommendations.append("🔒 SECURITY: Implement missing security controls identified in security validation tests.")
        
        # OAuth2 migration recommendations
        oauth2_summary = suite_summaries.get("oauth2_migration", {})
        if oauth2_summary.get("status") == "ISSUES_FOUND":
            recommendations.append("🔐 OAUTH2: Complete OAuth2+PKCE migration issues identified. Review migration test results.")
        
        # Performance recommendations
        performance_summary = suite_summaries.get("performance", {})
        if performance_summary.get("performance_score") in ["POOR", "FAIR"]:
            recommendations.append("⚡ PERFORMANCE: Optimize slow endpoints identified in performance tests.")
        
        # Integration recommendations
        integration_summary = suite_summaries.get("integration", {})
        if integration_summary.get("status") == "COMPLETED":
            integration_score = float(integration_summary.get("integration_score", "0%").replace("%", ""))
            if integration_score < 80:
                recommendations.append("🔗 INTEGRATION: Fix module integration issues identified in integration tests.")
        
        # General recommendations
        if not recommendations:
            recommendations.append("✅ EXCELLENT: All test suites passed successfully. System is ready for production.")
        
        recommendations.append("📊 MONITORING: Set up continuous monitoring for all validated endpoints.")
        recommendations.append("🔄 AUTOMATION: Consider automating these tests in your CI/CD pipeline.")
        
        return recommendations
    
    async def run_all_tests(self):
        """Run all test suites in sequence"""
        self.start_time = time.time()
        
        logger.info("🎯 Starting Comprehensive CRM Backend Test Execution")
        logger.info(f"🌐 Target URL: {self.base_url}")
        
        try:
            # Run all test suites
            await self.run_backend_functionality_tests()
            await self.run_oauth2_migration_tests()
            await self.run_security_validation_tests()
            await self.run_performance_tests()
            await self.run_integration_tests()
            
        except Exception as e:
            logger.error(f"❌ Test execution failed: {e}")
        
        finally:
            self.end_time = time.time()
        
        # Generate consolidated report
        report = self.generate_consolidated_report()
        
        # Save report to file
        report_file = f"comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Comprehensive test report saved to: {report_file}")
        
        return report

async def main():
    """Main execution function"""
    try:
        # Initialize test orchestrator
        orchestrator = TestOrchestrator()
        
        # Run all tests
        report = await orchestrator.run_all_tests()
        
        # Print summary
        print("\n" + "="*100)
        print("COMPREHENSIVE CRM BACKEND TEST EXECUTION SUMMARY")
        print("="*100)
        
        overall_metrics = report["overall_metrics"]
        print(f"🎯 System Status: {overall_metrics['system_status']}")
        print(f"📊 Overall Pass Rate: {overall_metrics['overall_pass_rate']}")
        print(f"✅ Total Passed: {overall_metrics['total_passed']}")
        print(f"❌ Total Failed: {overall_metrics['total_failed']}")
        print(f"📈 Total Tests: {overall_metrics['total_tests']}")
        
        print(f"\n📋 TEST SUITE BREAKDOWN:")
        print("-"*100)
        for suite_name, summary in report["suite_summaries"].items():
            status_icon = "✅" if summary.get("status") == "COMPLETED" else "❌"
            print(f"{status_icon} {suite_name.replace('_', ' ').title()}: {summary.get('status', 'UNKNOWN')}")
            
            if "tests" in summary:
                print(f"   Tests: {summary['passed']}/{summary['tests']} passed ({summary.get('pass_rate', 'N/A')})")
            
            if "security_level" in summary:
                print(f"   Security Level: {summary['security_level']}")
            
            if "performance_score" in summary:
                print(f"   Performance: {summary['performance_score']}")
            
            if "integration_score" in summary:
                print(f"   Integration: {summary['integration_score']}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print("-"*100)
        for i, recommendation in enumerate(report["recommendations"], 1):
            print(f"{i}. {recommendation}")
        
        print(f"\n⏱️ Test Duration: {report['test_execution_summary']['test_duration_seconds']:.2f} seconds")
        print(f"📅 Executed At: {report['test_execution_summary']['timestamp']}")
        
        return report
        
    except Exception as e:
        logger.error(f"❌ Test orchestration failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    asyncio.run(main())