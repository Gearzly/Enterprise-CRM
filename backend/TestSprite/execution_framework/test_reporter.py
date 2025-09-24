"""
TestSprite Test Reporter
Comprehensive reporting system for test execution results
"""

import json
import time
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
import xml.etree.ElementTree as ET

@dataclass
class TestMetrics:
    total_tests: int
    passed: int
    failed: int
    errors: int
    skipped: int
    duration: float
    pass_rate: float
    performance_issues: int
    security_issues: int
    coverage_percentage: float

@dataclass
class SuiteReport:
    name: str
    category: str
    metrics: TestMetrics
    test_results: List[Dict[str, Any]]
    start_time: str
    end_time: str
    duration: float

class TestReporter:
    """
    Comprehensive test reporting system for TestSprite execution
    """
    
    def __init__(self, output_dir: str, project_name: str = "CRM"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.project_name = project_name
        self.reports = []
        self.overall_metrics = None
        self.start_time = datetime.now()
        
    def add_suite_report(self, suite_report: SuiteReport) -> None:
        """Add a test suite report"""
        self.reports.append(suite_report)
    
    def calculate_overall_metrics(self) -> TestMetrics:
        """Calculate overall metrics from all suite reports"""
        if not self.reports:
            return TestMetrics(0, 0, 0, 0, 0, 0.0, 0.0, 0, 0, 0.0)
        
        total_tests = sum(r.metrics.total_tests for r in self.reports)
        passed = sum(r.metrics.passed for r in self.reports)
        failed = sum(r.metrics.failed for r in self.reports)
        errors = sum(r.metrics.errors for r in self.reports)
        skipped = sum(r.metrics.skipped for r in self.reports)
        total_duration = sum(r.metrics.duration for r in self.reports)
        
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0.0
        performance_issues = sum(r.metrics.performance_issues for r in self.reports)
        security_issues = sum(r.metrics.security_issues for r in self.reports)
        
        # Average coverage (weighted by test count)
        total_coverage = 0.0
        total_weight = 0
        for report in self.reports:
            if report.metrics.total_tests > 0:
                total_coverage += report.metrics.coverage_percentage * report.metrics.total_tests
                total_weight += report.metrics.total_tests
        
        avg_coverage = (total_coverage / total_weight) if total_weight > 0 else 0.0
        
        self.overall_metrics = TestMetrics(
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            errors=errors,
            skipped=skipped,
            duration=total_duration,
            pass_rate=pass_rate,
            performance_issues=performance_issues,
            security_issues=security_issues,
            coverage_percentage=avg_coverage
        )
        
        return self.overall_metrics
    
    def generate_json_report(self) -> str:
        """Generate comprehensive JSON report"""
        end_time = datetime.now()
        
        # Calculate overall metrics
        overall_metrics = self.calculate_overall_metrics()
        
        report_data = {
            "metadata": {
                "project_name": self.project_name,
                "report_type": "TestSprite Comprehensive Report",
                "generated_at": end_time.isoformat(),
                "execution_start": self.start_time.isoformat(),
                "execution_end": end_time.isoformat(),
                "total_execution_time": (end_time - self.start_time).total_seconds(),
                "report_version": "1.0.0"
            },
            "summary": {
                "overall_metrics": asdict(overall_metrics),
                "test_categories": len(set(r.category for r in self.reports)),
                "test_suites": len(self.reports),
                "success_rate": overall_metrics.pass_rate,
                "recommendation": self._get_overall_recommendation(overall_metrics)
            },
            "suite_reports": [
                {
                    "suite_name": report.name,
                    "category": report.category,
                    "metrics": asdict(report.metrics),
                    "execution": {
                        "start_time": report.start_time,
                        "end_time": report.end_time,
                        "duration": report.duration
                    },
                    "test_results": report.test_results
                }
                for report in self.reports
            ],
            "category_breakdown": self._generate_category_breakdown(),
            "performance_analysis": self._generate_performance_analysis(),
            "security_analysis": self._generate_security_analysis(),
            "recommendations": self._generate_detailed_recommendations()
        }
        
        # Save JSON report
        json_path = self.output_dir / f"testsprite_report_{int(time.time())}.json"
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return str(json_path)
    
    def generate_html_report(self) -> str:
        """Generate HTML report"""
        overall_metrics = self.calculate_overall_metrics()
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TestSprite Report - {self.project_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .info {{ color: #17a2b8; }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
        }}
        .section h2 {{
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .suite-grid {{
            display: grid;
            gap: 20px;
        }}
        .suite-card {{
            border: 1px solid #eee;
            border-radius: 8px;
            padding: 20px;
            background: #f8f9fa;
        }}
        .suite-header {{
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .suite-name {{
            font-size: 1.2em;
            font-weight: bold;
        }}
        .suite-category {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }}
        .progress-bar {{
            background: #eee;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            transition: width 0.3s ease;
        }}
        .recommendations {{
            background: #e9ecef;
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 0 8px 8px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            border-top: 1px solid #eee;
        }}
        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        .status-passed {{ background: #d4edda; color: #155724; }}
        .status-failed {{ background: #f8d7da; color: #721c24; }}
        .status-warning {{ background: #fff3cd; color: #856404; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 TestSprite Report</h1>
            <p>{self.project_name} - Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value passed">{overall_metrics.passed}</div>
                <div class="metric-label">Tests Passed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value failed">{overall_metrics.failed + overall_metrics.errors}</div>
                <div class="metric-label">Tests Failed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value info">{overall_metrics.total_tests}</div>
                <div class="metric-label">Total Tests</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {'passed' if overall_metrics.pass_rate >= 95 else 'warning' if overall_metrics.pass_rate >= 80 else 'failed'}">{overall_metrics.pass_rate:.1f}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value info">{overall_metrics.coverage_percentage:.1f}%</div>
                <div class="metric-label">Coverage</div>
            </div>
            <div class="metric-card">
                <div class="metric-value info">{overall_metrics.duration:.1f}s</div>
                <div class="metric-label">Duration</div>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 Test Suite Results</h2>
                <div class="suite-grid">
                    {self._generate_suite_html()}
                </div>
            </div>
            
            <div class="section">
                <h2>📈 Category Breakdown</h2>
                {self._generate_category_html()}
            </div>
            
            <div class="section">
                <h2>💡 Recommendations</h2>
                <div class="recommendations">
                    {self._generate_recommendations_html()}
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by TestSprite MCP Server - Comprehensive Testing Framework</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Save HTML report
        html_path = self.output_dir / f"testsprite_report_{int(time.time())}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)
    
    def generate_junit_xml(self) -> str:
        """Generate JUnit XML report for CI/CD integration"""
        root = ET.Element("testsuites")
        root.set("name", f"{self.project_name} TestSprite Report")
        root.set("tests", str(self.overall_metrics.total_tests if self.overall_metrics else 0))
        root.set("failures", str(self.overall_metrics.failed if self.overall_metrics else 0))
        root.set("errors", str(self.overall_metrics.errors if self.overall_metrics else 0))
        root.set("skipped", str(self.overall_metrics.skipped if self.overall_metrics else 0))
        root.set("time", str(self.overall_metrics.duration if self.overall_metrics else 0))
        
        for report in self.reports:
            testsuite = ET.SubElement(root, "testsuite")
            testsuite.set("name", f"{report.category}.{report.name}")
            testsuite.set("tests", str(report.metrics.total_tests))
            testsuite.set("failures", str(report.metrics.failed))
            testsuite.set("errors", str(report.metrics.errors))
            testsuite.set("skipped", str(report.metrics.skipped))
            testsuite.set("time", str(report.metrics.duration))
            
            for test_result in report.test_results:
                testcase = ET.SubElement(testsuite, "testcase")
                testcase.set("name", test_result.get("name", "unknown"))
                testcase.set("classname", f"{report.category}.{report.name}")
                testcase.set("time", str(test_result.get("duration", 0)))
                
                status = test_result.get("status", "unknown")
                if status == "failed":
                    failure = ET.SubElement(testcase, "failure")
                    failure.set("message", test_result.get("message", "Test failed"))
                    failure.text = test_result.get("output", "")
                elif status == "error":
                    error = ET.SubElement(testcase, "error")
                    error.set("message", test_result.get("message", "Test error"))
                    error.text = test_result.get("output", "")
                elif status == "skipped":
                    skipped = ET.SubElement(testcase, "skipped")
                    skipped.set("message", test_result.get("message", "Test skipped"))
        
        # Save XML report
        xml_path = self.output_dir / f"junit_report_{int(time.time())}.xml"
        tree = ET.ElementTree(root)
        tree.write(xml_path, encoding='utf-8', xml_declaration=True)
        
        return str(xml_path)
    
    def _generate_category_breakdown(self) -> Dict[str, Any]:
        """Generate breakdown by test category"""
        categories = {}
        
        for report in self.reports:
            category = report.category
            if category not in categories:
                categories[category] = {
                    "total_tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 0,
                    "skipped": 0,
                    "duration": 0.0,
                    "suites": []
                }
            
            cat_data = categories[category]
            cat_data["total_tests"] += report.metrics.total_tests
            cat_data["passed"] += report.metrics.passed
            cat_data["failed"] += report.metrics.failed
            cat_data["errors"] += report.metrics.errors
            cat_data["skipped"] += report.metrics.skipped
            cat_data["duration"] += report.metrics.duration
            cat_data["suites"].append(report.name)
        
        # Calculate pass rates
        for category, data in categories.items():
            if data["total_tests"] > 0:
                data["pass_rate"] = (data["passed"] / data["total_tests"]) * 100
            else:
                data["pass_rate"] = 0.0
        
        return categories
    
    def _generate_performance_analysis(self) -> Dict[str, Any]:
        """Generate performance analysis"""
        total_performance_issues = sum(r.metrics.performance_issues for r in self.reports)
        avg_duration = sum(r.metrics.duration for r in self.reports) / len(self.reports) if self.reports else 0
        
        slowest_suites = sorted(self.reports, key=lambda r: r.metrics.duration, reverse=True)[:5]
        
        return {
            "total_performance_issues": total_performance_issues,
            "average_suite_duration": avg_duration,
            "slowest_suites": [
                {
                    "name": suite.name,
                    "category": suite.category,
                    "duration": suite.metrics.duration
                }
                for suite in slowest_suites
            ],
            "performance_recommendation": (
                "Performance is good" if total_performance_issues == 0
                else f"Address {total_performance_issues} performance issues"
            )
        }
    
    def _generate_security_analysis(self) -> Dict[str, Any]:
        """Generate security analysis"""
        total_security_issues = sum(r.metrics.security_issues for r in self.reports)
        
        return {
            "total_security_issues": total_security_issues,
            "security_status": "SECURE" if total_security_issues == 0 else "ISSUES_FOUND",
            "security_recommendation": (
                "No security issues detected" if total_security_issues == 0
                else f"Address {total_security_issues} security issues immediately"
            )
        }
    
    def _generate_detailed_recommendations(self) -> List[str]:
        """Generate detailed recommendations"""
        recommendations = []
        overall_metrics = self.overall_metrics or self.calculate_overall_metrics()
        
        if overall_metrics.pass_rate < 100:
            recommendations.append(
                f"Increase test pass rate from {overall_metrics.pass_rate:.1f}% to 100%"
            )
        
        if overall_metrics.coverage_percentage < 90:
            recommendations.append(
                f"Improve code coverage from {overall_metrics.coverage_percentage:.1f}% to at least 90%"
            )
        
        if overall_metrics.performance_issues > 0:
            recommendations.append(
                f"Optimize {overall_metrics.performance_issues} performance issues"
            )
        
        if overall_metrics.security_issues > 0:
            recommendations.append(
                f"Address {overall_metrics.security_issues} security vulnerabilities"
            )
        
        if not recommendations:
            recommendations.append("Excellent! All tests are passing with good coverage and performance.")
        
        return recommendations
    
    def _get_overall_recommendation(self, metrics: TestMetrics) -> str:
        """Get overall recommendation based on metrics"""
        if metrics.pass_rate >= 100 and metrics.security_issues == 0:
            return "EXCELLENT - All tests passing, no security issues"
        elif metrics.pass_rate >= 95:
            return "GOOD - Minor issues to address"
        elif metrics.pass_rate >= 80:
            return "NEEDS_IMPROVEMENT - Several failing tests"
        else:
            return "CRITICAL - Major issues requiring immediate attention"
    
    def _generate_suite_html(self) -> str:
        """Generate HTML for test suites"""
        html_parts = []
        
        for report in self.reports:
            pass_rate = report.metrics.pass_rate
            status_class = "passed" if pass_rate >= 95 else "warning" if pass_rate >= 80 else "failed"
            
            html_parts.append(f"""
                <div class="suite-card">
                    <div class="suite-header">
                        <div class="suite-name">{report.name}</div>
                        <span class="suite-category">{report.category}</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill {status_class}" style="width: {pass_rate}%"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                        <span>Pass Rate: <strong>{pass_rate:.1f}%</strong></span>
                        <span>Duration: <strong>{report.metrics.duration:.1f}s</strong></span>
                    </div>
                    <div style="margin-top: 10px;">
                        <span class="status-badge status-passed">{report.metrics.passed} Passed</span>
                        <span class="status-badge status-failed">{report.metrics.failed + report.metrics.errors} Failed</span>
                        <span class="status-badge status-warning">{report.metrics.skipped} Skipped</span>
                    </div>
                </div>
            """)
        
        return "\n".join(html_parts)
    
    def _generate_category_html(self) -> str:
        """Generate HTML for category breakdown"""
        categories = self._generate_category_breakdown()
        html_parts = []
        
        for category, data in categories.items():
            pass_rate = data["pass_rate"]
            status_class = "passed" if pass_rate >= 95 else "warning" if pass_rate >= 80 else "failed"
            
            html_parts.append(f"""
                <div class="metric-card">
                    <h3>{category.upper()}</h3>
                    <div class="metric-value {status_class}">{pass_rate:.1f}%</div>
                    <div class="metric-label">Pass Rate</div>
                    <div style="margin-top: 10px; font-size: 0.9em;">
                        {data['passed']}/{data['total_tests']} tests passed<br>
                        {len(data['suites'])} test suites
                    </div>
                </div>
            """)
        
        return f'<div class="metrics-grid">{"".join(html_parts)}</div>'
    
    def _generate_recommendations_html(self) -> str:
        """Generate HTML for recommendations"""
        recommendations = self._generate_detailed_recommendations()
        html_parts = ["<ul>"]
        
        for rec in recommendations:
            html_parts.append(f"<li>{rec}</li>")
        
        html_parts.append("</ul>")
        return "\n".join(html_parts)
    
    def generate_all_reports(self) -> Dict[str, str]:
        """Generate all report formats"""
        reports = {}
        
        try:
            reports["json"] = self.generate_json_report()
        except Exception as e:
            print(f"Error generating JSON report: {e}")
        
        try:
            reports["html"] = self.generate_html_report()
        except Exception as e:
            print(f"Error generating HTML report: {e}")
        
        try:
            reports["junit"] = self.generate_junit_xml()
        except Exception as e:
            print(f"Error generating JUnit XML: {e}")
        
        return reports