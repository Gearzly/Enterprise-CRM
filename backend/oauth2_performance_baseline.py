#!/usr/bin/env python3
"""
OAuth2+PKCE Performance Baseline Testing Script
Establishes performance benchmarks for OAuth2 authentication endpoints
"""
import requests
import json
import time
import statistics
import concurrent.futures
from typing import Dict, List, Any
from datetime import datetime

BASE_URL = "http://localhost:5173"

class OAuth2PerformanceProfiler:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.performance_data = {}
        self.baseline_results = {}
    
    def log_performance(self, endpoint: str, response_times: List[float], 
                       success_count: int, total_requests: int):
        """Log performance metrics for an endpoint"""
        if response_times:
            avg_time = statistics.mean(response_times)
            median_time = statistics.median(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            p95_time = sorted(response_times)[int(0.95 * len(response_times))] if len(response_times) > 20 else max_time
            p99_time = sorted(response_times)[int(0.99 * len(response_times))] if len(response_times) > 100 else max_time
        else:
            avg_time = median_time = min_time = max_time = p95_time = p99_time = 0
        
        success_rate = (success_count / total_requests) * 100 if total_requests > 0 else 0
        
        self.performance_data[endpoint] = {
            "total_requests": total_requests,
            "successful_requests": success_count,
            "success_rate": success_rate,
            "response_times": {
                "average_ms": round(avg_time * 1000, 2),
                "median_ms": round(median_time * 1000, 2),
                "min_ms": round(min_time * 1000, 2),
                "max_ms": round(max_time * 1000, 2),
                "p95_ms": round(p95_time * 1000, 2),
                "p99_ms": round(p99_time * 1000, 2)
            },
            "throughput_rps": round(success_count / sum(response_times), 2) if response_times and sum(response_times) > 0 else 0
        }
    
    def test_endpoint_performance(self, endpoint: str, method: str = "GET", 
                                data: Dict = None, iterations: int = 50) -> List[float]:
        """Test performance of a single endpoint"""
        response_times = []
        successful_requests = 0
        
        print(f"🔄 Testing {endpoint} performance ({iterations} iterations)...")
        
        for i in range(iterations):
            start_time = time.time()
            try:
                if method.upper() == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                elif method.upper() == "POST":
                    response = self.session.post(f"{self.base_url}{endpoint}", json=data or {})
                
                end_time = time.time()
                response_time = end_time - start_time
                response_times.append(response_time)
                
                if response.status_code < 400:
                    successful_requests += 1
                    
            except Exception as e:
                print(f"   Error in iteration {i+1}: {e}")
                continue
            
            # Show progress
            if (i + 1) % 10 == 0:
                print(f"   Completed {i+1}/{iterations} requests...")
        
        self.log_performance(endpoint, response_times, successful_requests, iterations)
        return response_times
    
    def test_concurrent_load(self, endpoint: str, method: str = "GET", 
                           data: Dict = None, concurrent_users: int = 10, 
                           requests_per_user: int = 5) -> Dict[str, Any]:
        """Test concurrent load on an endpoint"""
        print(f"🚀 Testing concurrent load: {concurrent_users} users, {requests_per_user} requests each")
        
        def make_request():
            response_times = []
            successful_requests = 0
            
            for _ in range(requests_per_user):
                start_time = time.time()
                try:
                    if method.upper() == "GET":
                        response = self.session.get(f"{self.base_url}{endpoint}")
                    elif method.upper() == "POST":
                        response = self.session.post(f"{self.base_url}{endpoint}", json=data or {})
                    
                    end_time = time.time()
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    
                    if response.status_code < 400:
                        successful_requests += 1
                        
                except Exception:
                    continue
            
            return response_times, successful_requests
        
        # Execute concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(make_request) for _ in range(concurrent_users)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # Aggregate results
        all_response_times = []
        total_successful = 0
        
        for response_times, successful in results:
            all_response_times.extend(response_times)
            total_successful += successful
        
        total_requests = concurrent_users * requests_per_user
        
        return {
            "concurrent_users": concurrent_users,
            "requests_per_user": requests_per_user,
            "total_requests": total_requests,
            "successful_requests": total_successful,
            "success_rate": (total_successful / total_requests) * 100,
            "avg_response_time_ms": round(statistics.mean(all_response_times) * 1000, 2) if all_response_times else 0,
            "max_response_time_ms": round(max(all_response_times) * 1000, 2) if all_response_times else 0
        }
    
    def establish_oauth2_baselines(self):
        """Establish performance baselines for OAuth2 endpoints"""
        print("=" * 70)
        print("🎯 OAUTH2+PKCE PERFORMANCE BASELINE ESTABLISHMENT")
        print("=" * 70)
        print()
        
        # Test 1: Health Check Performance
        print("📊 1. Health Check Endpoint")
        self.test_endpoint_performance("/health", "GET", iterations=100)
        print()
        
        # Test 2: PKCE Challenge Generation Performance
        print("📊 2. PKCE Challenge Generation")
        self.test_endpoint_performance("/auth/challenge", "POST", {}, iterations=100)
        print()
        
        # Test 3: OAuth2 Discovery Performance
        print("📊 3. OAuth2 Discovery Metadata")
        self.test_endpoint_performance("/auth/.well-known/oauth-authorization-server", "GET", iterations=50)
        print()
        
        # Test 4: Root API Performance
        print("📊 4. Root API Endpoint")
        self.test_endpoint_performance("/", "GET", iterations=50)
        print()
        
        # Test 5: Concurrent Load Test on PKCE Challenge
        print("📊 5. Concurrent PKCE Challenge Load Test")
        concurrent_results = self.test_concurrent_load("/auth/challenge", "POST", {}, 
                                                     concurrent_users=20, requests_per_user=5)
        self.performance_data["/auth/challenge_concurrent"] = concurrent_results
        print()
        
        # Test 6: API Documentation Performance
        print("📊 6. API Documentation Access")
        self.test_endpoint_performance("/docs", "GET", iterations=20)
        print()
        
        # Test 7: OpenAPI Schema Performance
        print("📊 7. OpenAPI Schema Generation")
        self.test_endpoint_performance("/openapi.json", "GET", iterations=20)
        print()
    
    def generate_baseline_report(self):
        """Generate comprehensive baseline performance report"""
        print("=" * 70)
        print("📋 OAUTH2+PKCE PERFORMANCE BASELINE REPORT")
        print("=" * 70)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Server: {self.base_url}")
        print()
        
        # Summary table
        print("📊 PERFORMANCE SUMMARY")
        print("-" * 70)
        print(f"{'Endpoint':<35} {'Success%':<10} {'Avg(ms)':<10} {'P95(ms)':<10} {'RPS':<8}")
        print("-" * 70)
        
        for endpoint, data in self.performance_data.items():
            if "concurrent" not in endpoint and "response_times" in data:
                print(f"{endpoint:<35} {data['success_rate']:<10.1f} "
                      f"{data['response_times']['average_ms']:<10.2f} "
                      f"{data['response_times']['p95_ms']:<10.2f} "
                      f"{data['throughput_rps']:<8.2f}")
        
        print("-" * 70)
        print()
        
        # Detailed metrics for key endpoints
        key_endpoints = ["/health", "/auth/challenge", "/auth/.well-known/oauth-authorization-server", "/"]
        
        for endpoint in key_endpoints:
            if endpoint in self.performance_data:
                data = self.performance_data[endpoint]
                print(f"🔍 DETAILED METRICS: {endpoint}")
                print(f"   Total Requests: {data['total_requests']}")
                print(f"   Success Rate: {data['success_rate']:.1f}%")
                print(f"   Response Times:")
                print(f"     - Average: {data['response_times']['average_ms']:.2f}ms")
                print(f"     - Median: {data['response_times']['median_ms']:.2f}ms")
                print(f"     - Min: {data['response_times']['min_ms']:.2f}ms")
                print(f"     - Max: {data['response_times']['max_ms']:.2f}ms")
                print(f"     - 95th Percentile: {data['response_times']['p95_ms']:.2f}ms")
                print(f"     - 99th Percentile: {data['response_times']['p99_ms']:.2f}ms")
                print(f"   Throughput: {data['throughput_rps']:.2f} RPS")
                print()
        
        # Concurrent load test results
        if "/auth/challenge_concurrent" in self.performance_data:
            concurrent_data = self.performance_data["/auth/challenge_concurrent"]
            print("🚀 CONCURRENT LOAD TEST RESULTS")
            print(f"   Test Configuration: {concurrent_data['concurrent_users']} users, "
                  f"{concurrent_data['requests_per_user']} requests each")
            print(f"   Total Requests: {concurrent_data['total_requests']}")
            print(f"   Success Rate: {concurrent_data['success_rate']:.1f}%")
            print(f"   Average Response Time: {concurrent_data['avg_response_time_ms']:.2f}ms")
            print(f"   Max Response Time: {concurrent_data['max_response_time_ms']:.2f}ms")
            print()
        
        # Performance recommendations
        self.generate_performance_recommendations()
    
    def generate_performance_recommendations(self):
        """Generate performance optimization recommendations"""
        print("💡 PERFORMANCE RECOMMENDATIONS")
        print("-" * 70)
        
        recommendations = []
        
        # Check response times
        if "/auth/challenge" in self.performance_data:
            challenge_avg = self.performance_data["/auth/challenge"]["response_times"]["average_ms"]
            if challenge_avg > 100:
                recommendations.append("⚠️  PKCE Challenge generation is slow (>100ms). Consider optimizing cryptographic operations.")
            elif challenge_avg > 50:
                recommendations.append("⚡ PKCE Challenge could be faster. Consider caching or optimization.")
            else:
                recommendations.append("✅ PKCE Challenge generation performance is excellent (<50ms).")
        
        # Check success rates
        for endpoint, data in self.performance_data.items():
            if "concurrent" not in endpoint and data["success_rate"] < 95:
                recommendations.append(f"❌ {endpoint} has low success rate ({data['success_rate']:.1f}%). Investigate error handling.")
        
        # Check throughput
        if "/health" in self.performance_data:
            health_rps = self.performance_data["/health"]["throughput_rps"]
            if health_rps < 100:
                recommendations.append("⚠️  Health endpoint throughput is low. Consider optimizations for monitoring systems.")
        
        # Concurrent load analysis
        if "/auth/challenge_concurrent" in self.performance_data:
            concurrent_success = self.performance_data["/auth/challenge_concurrent"]["success_rate"]
            if concurrent_success < 90:
                recommendations.append("⚠️  System struggles under concurrent load. Consider scaling or optimization.")
            else:
                recommendations.append("✅ System handles concurrent load well.")
        
        if not recommendations:
            recommendations.append("🎉 All performance metrics look good! System is well-optimized.")
        
        for recommendation in recommendations:
            print(f"   {recommendation}")
        
        print()
        print("🎯 BASELINE ESTABLISHMENT COMPLETE")
        print("   These metrics serve as performance baselines for monitoring and optimization.")
        print("=" * 70)
    
    def save_baseline_data(self, filename: str = "oauth2_performance_baseline.json"):
        """Save baseline data to file for future comparison"""
        baseline_data = {
            "timestamp": datetime.now().isoformat(),
            "server_url": self.base_url,
            "performance_data": self.performance_data,
            "test_configuration": {
                "single_endpoint_iterations": 50,
                "concurrent_users": 20,
                "requests_per_user": 5
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(baseline_data, f, indent=2)
        
        print(f"💾 Baseline data saved to {filename}")

def main():
    """Main performance testing execution"""
    profiler = OAuth2PerformanceProfiler()
    
    try:
        # Establish baselines
        profiler.establish_oauth2_baselines()
        
        # Generate comprehensive report
        profiler.generate_baseline_report()
        
        # Save baseline data
        profiler.save_baseline_data()
        
    except KeyboardInterrupt:
        print("\n⏹️  Performance testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Performance testing failed: {e}")

if __name__ == "__main__":
    main()