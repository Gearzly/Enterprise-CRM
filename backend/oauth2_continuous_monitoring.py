#!/usr/bin/env python3
"""
OAuth2+PKCE Continuous Monitoring System
Provides real-time monitoring, alerting, and health checks for OAuth2 authentication system
"""
import asyncio
import time
import json
import logging
import smtplib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import requests
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

# Configuration
MONITOR_CONFIG = {
    "base_url": "http://localhost:5173",
    "check_interval": 30,  # seconds
    "alert_threshold": 3,  # consecutive failures before alert
    "performance_threshold": {
        "response_time_ms": 1000,
        "success_rate_percent": 95,
        "throughput_rps": 10
    },
    "retention_hours": 24,
    "email_alerts": {
        "enabled": False,  # Set to True to enable email alerts
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "from_email": "alerts@crm.com",
        "to_emails": ["admin@crm.com"],
        "password": "your_app_password"
    }
}

class AlertLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    RESOLVED = "RESOLVED"

@dataclass
class HealthCheck:
    endpoint: str
    method: str = "GET"
    expected_status: int = 200
    timeout: int = 5
    data: Optional[Dict] = None

@dataclass
class MonitorResult:
    timestamp: datetime
    endpoint: str
    success: bool
    response_time_ms: float
    status_code: int
    error_message: Optional[str] = None

@dataclass
class Alert:
    timestamp: datetime
    level: AlertLevel
    message: str
    endpoint: str
    consecutive_failures: int = 0
    resolved: bool = False

class OAuth2MonitoringSystem:
    def __init__(self):
        self.config = MONITOR_CONFIG
        self.is_running = False
        self.results_history: List[MonitorResult] = []
        self.active_alerts: Dict[str, Alert] = {}
        self.failure_counts: Dict[str, int] = {}
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('oauth2_monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Define health checks
        self.health_checks = [
            HealthCheck("/health", "GET", 200),
            HealthCheck("/", "GET", 200),
            HealthCheck("/auth/challenge", "POST", 200, data={}),
            HealthCheck("/auth/.well-known/oauth-authorization-server", "GET", 200),
            HealthCheck("/docs", "GET", 200),
            HealthCheck("/openapi.json", "GET", 200)
        ]
    
    async def check_endpoint_health(self, check: HealthCheck) -> MonitorResult:
        """Check health of a single endpoint"""
        start_time = time.time()
        
        try:
            if check.method.upper() == "GET":
                response = requests.get(
                    f"{self.config['base_url']}{check.endpoint}",
                    timeout=check.timeout
                )
            elif check.method.upper() == "POST":
                response = requests.post(
                    f"{self.config['base_url']}{check.endpoint}",
                    json=check.data or {},
                    timeout=check.timeout
                )
            
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            
            success = response.status_code == check.expected_status
            
            return MonitorResult(
                timestamp=datetime.now(),
                endpoint=check.endpoint,
                success=success,
                response_time_ms=response_time_ms,
                status_code=response.status_code,
                error_message=None if success else f"Expected {check.expected_status}, got {response.status_code}"
            )
            
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            
            return MonitorResult(
                timestamp=datetime.now(),
                endpoint=check.endpoint,
                success=False,
                response_time_ms=response_time_ms,
                status_code=0,
                error_message=str(e)
            )
    
    def evaluate_alerts(self, result: MonitorResult):
        """Evaluate if alerts should be raised or resolved"""
        endpoint = result.endpoint
        
        if not result.success:
            # Increment failure count
            self.failure_counts[endpoint] = self.failure_counts.get(endpoint, 0) + 1
            
            # Check if we should raise an alert
            if self.failure_counts[endpoint] >= self.config["alert_threshold"]:
                if endpoint not in self.active_alerts:
                    alert = Alert(
                        timestamp=datetime.now(),
                        level=AlertLevel.CRITICAL,
                        message=f"Endpoint {endpoint} has failed {self.failure_counts[endpoint]} consecutive times",
                        endpoint=endpoint,
                        consecutive_failures=self.failure_counts[endpoint]
                    )
                    self.active_alerts[endpoint] = alert
                    self.send_alert(alert)
        else:
            # Reset failure count on success
            if endpoint in self.failure_counts:
                del self.failure_counts[endpoint]
            
            # Resolve any active alerts
            if endpoint in self.active_alerts and not self.active_alerts[endpoint].resolved:
                alert = self.active_alerts[endpoint]
                alert.resolved = True
                alert.level = AlertLevel.RESOLVED
                alert.message = f"Endpoint {endpoint} has recovered"
                self.send_alert(alert)
        
        # Check performance thresholds
        if (result.success and 
            result.response_time_ms > self.config["performance_threshold"]["response_time_ms"]):
            
            perf_alert = Alert(
                timestamp=datetime.now(),
                level=AlertLevel.WARNING,
                message=f"Endpoint {endpoint} response time ({result.response_time_ms:.2f}ms) exceeds threshold",
                endpoint=endpoint
            )
            self.send_alert(perf_alert)
    
    def send_alert(self, alert: Alert):
        """Send alert notification"""
        self.logger.warning(f"ALERT [{alert.level.value}] {alert.message}")
        
        # Send email alert if configured
        if self.config["email_alerts"]["enabled"]:
            self.send_email_alert(alert)
        
        # Log to file
        alert_data = {
            "timestamp": alert.timestamp.isoformat(),
            "level": alert.level.value,
            "message": alert.message,
            "endpoint": alert.endpoint,
            "consecutive_failures": alert.consecutive_failures,
            "resolved": alert.resolved
        }
        
        with open('oauth2_alerts.log', 'a') as f:
            f.write(json.dumps(alert_data) + '\n')
    
    def send_email_alert(self, alert: Alert):
        """Send email alert notification"""
        try:
            config = self.config["email_alerts"]
            
            msg = MimeMultipart()
            msg['From'] = config["from_email"]
            msg['To'] = ", ".join(config["to_emails"])
            msg['Subject'] = f"OAuth2 Alert [{alert.level.value}] - {alert.endpoint}"
            
            body = f"""
OAuth2 Monitoring Alert

Level: {alert.level.value}
Endpoint: {alert.endpoint}
Message: {alert.message}
Timestamp: {alert.timestamp}
Consecutive Failures: {alert.consecutive_failures}
Resolved: {alert.resolved}

Please check the OAuth2 system status.
"""
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(config["smtp_server"], config["smtp_port"])
            server.starttls()
            server.login(config["from_email"], config["password"])
            text = msg.as_string()
            server.sendmail(config["from_email"], config["to_emails"], text)
            server.quit()
            
            self.logger.info(f"Email alert sent for {alert.endpoint}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def cleanup_old_results(self):
        """Remove old monitoring results to prevent memory growth"""
        cutoff_time = datetime.now() - timedelta(hours=self.config["retention_hours"])
        self.results_history = [
            result for result in self.results_history 
            if result.timestamp > cutoff_time
        ]
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get current health summary"""
        if not self.results_history:
            return {"status": "No data", "endpoints": {}}
        
        # Get recent results (last 5 minutes)
        recent_cutoff = datetime.now() - timedelta(minutes=5)
        recent_results = [r for r in self.results_history if r.timestamp > recent_cutoff]
        
        if not recent_results:
            return {"status": "Stale data", "endpoints": {}}
        
        # Group by endpoint
        endpoint_stats = {}
        for result in recent_results:
            if result.endpoint not in endpoint_stats:
                endpoint_stats[result.endpoint] = {
                    "success_count": 0,
                    "total_count": 0,
                    "avg_response_time": 0,
                    "last_check": None
                }
            
            stats = endpoint_stats[result.endpoint]
            stats["total_count"] += 1
            if result.success:
                stats["success_count"] += 1
            stats["avg_response_time"] = (
                (stats["avg_response_time"] * (stats["total_count"] - 1) + result.response_time_ms) 
                / stats["total_count"]
            )
            if not stats["last_check"] or result.timestamp > stats["last_check"]:
                stats["last_check"] = result.timestamp
        
        # Calculate overall health
        total_success = sum(stats["success_count"] for stats in endpoint_stats.values())
        total_checks = sum(stats["total_count"] for stats in endpoint_stats.values())
        overall_success_rate = (total_success / total_checks * 100) if total_checks > 0 else 0
        
        status = "HEALTHY"
        if overall_success_rate < 50:
            status = "CRITICAL"
        elif overall_success_rate < 90:
            status = "WARNING"
        
        return {
            "status": status,
            "overall_success_rate": round(overall_success_rate, 2),
            "total_active_alerts": len([a for a in self.active_alerts.values() if not a.resolved]),
            "endpoints": {
                endpoint: {
                    "success_rate": round(stats["success_count"] / stats["total_count"] * 100, 2),
                    "avg_response_time_ms": round(stats["avg_response_time"], 2),
                    "last_check": stats["last_check"].isoformat() if stats["last_check"] else None,
                    "status": "UP" if stats["success_count"] > 0 else "DOWN"
                }
                for endpoint, stats in endpoint_stats.items()
            }
        }
    
    async def monitoring_loop(self):
        """Main monitoring loop"""
        self.logger.info("OAuth2 Monitoring System started")
        
        while self.is_running:
            try:
                # Run health checks
                for check in self.health_checks:
                    result = await self.check_endpoint_health(check)
                    self.results_history.append(result)
                    self.evaluate_alerts(result)
                    
                    # Log result
                    status = "✅" if result.success else "❌"
                    self.logger.info(
                        f"{status} {check.endpoint}: {result.response_time_ms:.2f}ms "
                        f"(Status: {result.status_code})"
                    )
                
                # Cleanup old results
                self.cleanup_old_results()
                
                # Print health summary every 10 minutes
                current_time = datetime.now()
                if current_time.minute % 10 == 0 and current_time.second < 30:
                    summary = self.get_health_summary()
                    self.logger.info(f"Health Summary: {summary['status']} - "
                                   f"Success Rate: {summary['overall_success_rate']}%")
                
                # Wait for next check
                await asyncio.sleep(self.config["check_interval"])
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Short wait before retrying
    
    def start_monitoring(self):
        """Start the monitoring system"""
        self.is_running = True
        try:
            asyncio.run(self.monitoring_loop())
        except KeyboardInterrupt:
            self.logger.info("Monitoring stopped by user")
        finally:
            self.is_running = False
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.is_running = False
        self.logger.info("OAuth2 Monitoring System stopped")
    
    def generate_monitoring_report(self) -> str:
        """Generate a comprehensive monitoring report"""
        summary = self.get_health_summary()
        
        report = f"""
# OAuth2+PKCE Monitoring Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall System Health
- **Status**: {summary['status']}
- **Success Rate**: {summary.get('overall_success_rate', 0):.2f}%
- **Active Alerts**: {summary.get('total_active_alerts', 0)}

## Endpoint Health Details
"""
        
        for endpoint, stats in summary.get('endpoints', {}).items():
            report += f"""
### {endpoint}
- Status: {stats['status']}
- Success Rate: {stats['success_rate']:.2f}%
- Avg Response Time: {stats['avg_response_time_ms']:.2f}ms
- Last Check: {stats['last_check']}
"""
        
        # Add active alerts
        active_alerts = [a for a in self.active_alerts.values() if not a.resolved]
        if active_alerts:
            report += "\n## Active Alerts\n"
            for alert in active_alerts:
                report += f"- **{alert.level.value}**: {alert.message} (Since: {alert.timestamp})\n"
        
        # Add performance recommendations
        report += "\n## Recommendations\n"
        if summary.get('overall_success_rate', 0) < 95:
            report += "- ⚠️ Overall success rate is below 95%. Investigate failing endpoints.\n"
        
        for endpoint, stats in summary.get('endpoints', {}).items():
            if stats['avg_response_time_ms'] > 500:
                report += f"- ⚡ {endpoint} response time is high ({stats['avg_response_time_ms']:.2f}ms). Consider optimization.\n"
        
        if not active_alerts:
            report += "- ✅ No active alerts. System is performing well.\n"
        
        return report

def main():
    """Main monitoring execution"""
    monitor = OAuth2MonitoringSystem()
    
    print("🔍 OAuth2+PKCE Continuous Monitoring System")
    print("=" * 50)
    print(f"Base URL: {monitor.config['base_url']}")
    print(f"Check Interval: {monitor.config['check_interval']} seconds")
    print(f"Alert Threshold: {monitor.config['alert_threshold']} consecutive failures")
    print("=" * 50)
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
        
        # Generate final report
        report = monitor.generate_monitoring_report()
        print("\n📋 Final Monitoring Report:")
        print(report)
        
        # Save report to file
        with open(f'oauth2_monitoring_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md', 'w') as f:
            f.write(report)
        print("\n💾 Report saved to file")

if __name__ == "__main__":
    main()