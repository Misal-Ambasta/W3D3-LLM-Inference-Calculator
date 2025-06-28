
"""
Advanced Analysis Example for LLM Inference Calculator

This script demonstrates advanced usage patterns including:
- Comprehensive cost analysis
- Performance optimization
- Deployment strategy comparison
- Risk assessment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference_calculator import LLMInferenceCalculator
from typing import Dict, List, Tuple


class AdvancedAnalyzer:
    """Advanced analysis class for LLM deployment planning"""
    
    def __init__(self):
        self.calculator = LLMInferenceCalculator()
    
    def analyze_deployment_strategies(self, tokens: int, requests_per_day: int) -> Dict:
        """Analyze different deployment strategies for a given workload"""
        print(f"=== Deployment Strategy Analysis ===")
        print(f"Workload: {tokens} tokens, {requests_per_day} requests/day\n")
        
        strategies = {
            "local_7b": {
                "name": "Mistral 7B (Local)",
                "model": "7B",
                "deployment": "local",
                "hardware": "GPU_16GB"
            },
            "api_13b": {
                "name": "LangChain 13B (API)",
                "model": "13B",
                "deployment": "api",
                "hardware": "GPU_8GB"  # Not used
            },
            "api_gpt4": {
                "name": "GPT-4 (API)",
                "model": "GPT-4",
                "deployment": "api",
                "hardware": "GPU_8GB"  # Not used
            }
        }
        
        results = {}
        
        for key, strategy in strategies.items():
            result = self.calculator.calculate(
                model_size=strategy["model"],
                tokens=tokens,
                hardware_type=strategy["hardware"],
                deployment_mode=strategy["deployment"]
            )
            
            # Calculate daily costs
            daily_cost = result.cost_per_request_usd * requests_per_day
            monthly_cost = daily_cost * 30
            yearly_cost = daily_cost * 365
            
            # Calculate total processing time
            total_daily_time = result.latency_seconds * requests_per_day
            total_daily_time_hours = total_daily_time / 3600
            
            results[key] = {
                "strategy": strategy["name"],
                "per_request": {
                    "latency": result.latency_seconds,
                    "cost": result.cost_per_request_usd,
                    "memory": result.memory_usage_gb if strategy["deployment"] == "local" else "N/A"
                },
                "daily": {
                    "cost": daily_cost,
                    "processing_time_hours": total_daily_time_hours,
                    "requests_per_hour": requests_per_day / 24
                },
                "monthly": {
                    "cost": monthly_cost
                },
                "yearly": {
                    "cost": yearly_cost
                },
                "compatible": result.hardware_compatible,
                "recommendations": result.recommendations
            }
        
        return results
    
    def print_strategy_comparison(self, results: Dict):
        """Print a formatted comparison of deployment strategies"""
        print("Strategy Comparison:")
        print("-" * 80)
        print(f"{'Strategy':<25} {'Latency':<10} {'Cost/Req':<12} {'Daily Cost':<12} {'Monthly':<12}")
        print("-" * 80)
        
        for key, data in results.items():
            latency = f"{data['per_request']['latency']:.1f}s"
            cost_req = f"${data['per_request']['cost']:.6f}"
            daily_cost = f"${data['daily']['cost']:.2f}"
            monthly_cost = f"${data['monthly']['cost']:.2f}"
            
            print(f"{data['strategy']:<25} {latency:<10} {cost_req:<12} {daily_cost:<12} {monthly_cost:<12}")
        
        print()
    
    def analyze_cost_breakdown(self, results: Dict):
        """Analyze cost breakdown and optimization opportunities"""
        print("Cost Analysis:")
        print("-" * 50)
        
        for key, data in results.items():
            print(f"\n{data['strategy']}:")
            print(f"  Per Request: ${data['per_request']['cost']:.6f}")
            print(f"  Daily: ${data['daily']['cost']:.2f}")
            print(f"  Monthly: ${data['monthly']['cost']:.2f}")
            print(f"  Yearly: ${data['yearly']['cost']:.2f}")
            
            # Cost optimization suggestions
            if data['per_request']['cost'] > 0.01:
                print("  ⚠️  High cost - consider optimization")
            elif data['per_request']['cost'] < 0.001:
                print("  ✅ Cost-effective")
            else:
                print("  ⚖️  Moderate cost")
    
    def analyze_performance_requirements(self, results: Dict, max_latency: float = 30.0):
        """Analyze if strategies meet performance requirements"""
        print(f"\nPerformance Analysis (Max Latency: {max_latency}s):")
        print("-" * 60)
        
        for key, data in results.items():
            latency = data['per_request']['latency']
            status = "✅ Meets" if latency <= max_latency else "❌ Exceeds"
            
            print(f"{data['strategy']}: {latency:.1f}s {status}")
            
            if latency > max_latency:
                print(f"  ⚠️  Consider faster hardware or API")
    
    def analyze_scalability(self, results: Dict, target_requests_per_hour: int = 100):
        """Analyze scalability of different strategies"""
        print(f"\nScalability Analysis (Target: {target_requests_per_hour} req/hour):")
        print("-" * 70)
        
        for key, data in results.items():
            current_rph = data['daily']['requests_per_hour']
            status = "✅ Scalable" if current_rph >= target_requests_per_hour else "❌ Limited"
            
            print(f"{data['strategy']}: {current_rph:.1f} req/hour {status}")
            
            if current_rph < target_requests_per_hour:
                print(f"  ⚠️  Consider parallel processing or API scaling")
    
    def generate_recommendations(self, results: Dict, budget: float = 100.0) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Find best cost option
        best_cost = min(results.values(), key=lambda x: x['monthly']['cost'])
        best_performance = min(results.values(), key=lambda x: x['per_request']['latency'])
        
        recommendations.append(f"Best cost option: {best_cost['strategy']} (${best_cost['monthly']['cost']:.2f}/month)")
        recommendations.append(f"Best performance: {best_performance['strategy']} ({best_performance['per_request']['latency']:.1f}s)")
        
        # Budget considerations
        affordable_options = [k for k, v in results.items() if v['monthly']['cost'] <= budget]
        if affordable_options:
            recommendations.append(f"Options within ${budget}/month budget: {len(affordable_options)}")
        else:
            recommendations.append(f"⚠️  All options exceed ${budget}/month budget")
        
        # Hybrid recommendations
        local_options = [k for k, v in results.items() if 'local' in k.lower()]
        api_options = [k for k, v in results.items() if 'api' in k.lower()]
        
        if local_options and api_options:
            recommendations.append("Consider hybrid approach: local for development, API for production")
        
        return recommendations
    
    def run_comprehensive_analysis(self, tokens: int, requests_per_day: int, 
                                 max_latency: float = 30.0, budget: float = 100.0):
        """Run comprehensive analysis"""
        print("=== COMPREHENSIVE LLM DEPLOYMENT ANALYSIS ===\n")
        
        # Run analysis
        results = self.analyze_deployment_strategies(tokens, requests_per_day)
        
        # Print results
        self.print_strategy_comparison(results)
        self.analyze_cost_breakdown(results)
        self.analyze_performance_requirements(results, max_latency)
        self.analyze_scalability(results)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(results, budget)
        
        print("\nRecommendations:")
        print("-" * 30)
        for rec in recommendations:
            print(f"• {rec}")
        
        return results


def main():
    """Run advanced analysis examples"""
    analyzer = AdvancedAnalyzer()
    
    # Example 1: Small workload analysis
    print("Example 1: Small Workload (1000 tokens, 50 requests/day)")
    print("=" * 60)
    analyzer.run_comprehensive_analysis(
        tokens=1000,
        requests_per_day=50,
        max_latency=60.0,
        budget=50.0
    )
    
    print("\n" + "="*80 + "\n")
    
    # Example 2: Medium workload analysis
    print("Example 2: Medium Workload (500 tokens, 200 requests/day)")
    print("=" * 60)
    analyzer.run_comprehensive_analysis(
        tokens=500,
        requests_per_day=200,
        max_latency=30.0,
        budget=100.0
    )
    
    print("\n" + "="*80 + "\n")
    
    # Example 3: Large workload analysis
    print("Example 3: Large Workload (2000 tokens, 100 requests/day)")
    print("=" * 60)
    analyzer.run_comprehensive_analysis(
        tokens=2000,
        requests_per_day=100,
        max_latency=120.0,
        budget=500.0
    )


if __name__ == "__main__":
    main() 