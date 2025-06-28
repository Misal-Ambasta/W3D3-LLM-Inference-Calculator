#!/usr/bin/env python3
"""
Scenario Testing Framework for LLM Inference Calculator

Automates testing of different deployment scenarios and generates detailed reports.
"""

from inference_calculator import LLMInferenceCalculator, HardwareType, ModelSize, DeploymentMode
from typing import Dict, List, Any
import json
from datetime import datetime


class ScenarioTester:
    """Framework for testing different LLM deployment scenarios"""
    
    def __init__(self):
        self.calculator = LLMInferenceCalculator()
        self.results = {}
    
    def test_scenario_1_local_deployment(self) -> Dict[str, Any]:
        """Test Scenario 1: Small-Scale Local Deployment (Mistral 7B)"""
        print("Testing Scenario 1: Small-Scale Local Deployment (Mistral 7B)")
        
        scenario_config = {
            "name": "Small-Scale Local Deployment (Mistral 7B via Ollama)",
            "use_case": "Individual developer or small team running inference locally for development and testing",
            "model": "7B",
            "tokens": 1000,
            "batch_size": 1,
            "deployment": "local"
        }
        
        # Test all hardware configurations
        hardware_configs = [
            "CPU", "GPU_4GB", "GPU_8GB", "GPU_12GB", 
            "GPU_16GB", "GPU_24GB", "GPU_32GB"
        ]
        
        results = []
        for hardware in hardware_configs:
            try:
                result = self.calculator.calculate(
                    model_size=scenario_config["model"],
                    tokens=scenario_config["tokens"],
                    batch_size=scenario_config["batch_size"],
                    hardware_type=hardware,
                    deployment_mode=scenario_config["deployment"]
                )
                
                results.append({
                    "hardware": hardware,
                    "latency_seconds": result.latency_seconds,
                    "memory_gb": result.memory_usage_gb,
                    "cost_usd": result.cost_per_request_usd,
                    "compatible": result.hardware_compatible,
                    "recommendations": result.recommendations
                })
                
            except Exception as e:
                results.append({
                    "hardware": hardware,
                    "error": str(e)
                })
        
        return {
            "scenario": scenario_config,
            "results": results,
            "summary": self._analyze_local_scenario(results)
        }
    
    def test_scenario_2_api_deployment(self) -> Dict[str, Any]:
        """Test Scenario 2: Medium-Scale API Deployment (LangChain 13B)"""
        print("Testing Scenario 2: Medium-Scale API Deployment (LangChain 13B)")
        
        scenario_config = {
            "name": "Medium-Scale API Deployment (LangChain 13B API)",
            "use_case": "Small to medium business using cloud API for production workloads",
            "model": "13B",
            "tokens": 500,
            "batch_size": 1,
            "deployment": "api"
        }
        
        try:
            result = self.calculator.calculate(
                model_size=scenario_config["model"],
                tokens=scenario_config["tokens"],
                batch_size=scenario_config["batch_size"],
                hardware_type="GPU_8GB",  # Not used for API
                deployment_mode=scenario_config["deployment"]
            )
            
            # Calculate cost breakdown
            input_tokens = int(scenario_config["tokens"] * 0.7)
            output_tokens = int(scenario_config["tokens"] * 0.3)
            
            cost_breakdown = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "input_cost": (input_tokens / 1000) * 0.0002,
                "output_cost": (output_tokens / 1000) * 0.0004,
                "total_cost": result.cost_per_request_usd
            }
            
            return {
                "scenario": scenario_config,
                "result": {
                    "latency_seconds": result.latency_seconds,
                    "memory_gb": "N/A (cloud-based)",
                    "cost_usd": result.cost_per_request_usd,
                    "compatible": True,
                    "recommendations": result.recommendations,
                    "cost_breakdown": cost_breakdown
                },
                "summary": self._analyze_api_scenario(result, "LangChain 13B")
            }
            
        except Exception as e:
            return {
                "scenario": scenario_config,
                "error": str(e)
            }
    
    def test_scenario_3_enterprise_api(self) -> Dict[str, Any]:
        """Test Scenario 3: Large-Scale API Usage (GPT-4)"""
        print("Testing Scenario 3: Large-Scale API Usage (GPT-4)")
        
        scenario_config = {
            "name": "Large-Scale API Usage (GPT-4 OpenAI API)",
            "use_case": "Enterprise application requiring high-quality outputs with significant budget",
            "model": "GPT-4",
            "tokens": 2000,
            "batch_size": 1,
            "deployment": "api"
        }
        
        try:
            result = self.calculator.calculate(
                model_size=scenario_config["model"],
                tokens=scenario_config["tokens"],
                batch_size=scenario_config["batch_size"],
                hardware_type="GPU_8GB",  # Not used for API
                deployment_mode=scenario_config["deployment"]
            )
            
            # Calculate cost breakdown
            input_tokens = int(scenario_config["tokens"] * 0.7)
            output_tokens = int(scenario_config["tokens"] * 0.3)
            
            cost_breakdown = {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "input_cost": (input_tokens / 1000) * 0.01,
                "output_cost": (output_tokens / 1000) * 0.03,
                "total_cost": result.cost_per_request_usd
            }
            
            return {
                "scenario": scenario_config,
                "result": {
                    "latency_seconds": result.latency_seconds,
                    "memory_gb": "N/A (cloud-based)",
                    "cost_usd": result.cost_per_request_usd,
                    "compatible": True,
                    "recommendations": result.recommendations,
                    "cost_breakdown": cost_breakdown
                },
                "summary": self._analyze_api_scenario(result, "GPT-4")
            }
            
        except Exception as e:
            return {
                "scenario": scenario_config,
                "error": str(e)
            }
    
    def _analyze_local_scenario(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze local deployment scenario results"""
        compatible_results = [r for r in results if r.get("compatible", False) and "error" not in r]
        
        if not compatible_results:
            return {
                "status": "No compatible hardware found",
                "recommendations": ["Upgrade to GPU with 16GB+ VRAM"]
            }
        
        # Find best performing hardware
        best_performance = min(compatible_results, key=lambda x: x["latency_seconds"])
        min_cost = min(compatible_results, key=lambda x: x["cost_usd"])
        
        return {
            "status": "Compatible hardware available",
            "best_performance": best_performance["hardware"],
            "lowest_cost": min_cost["hardware"],
            "performance_range": f"{min(r['latency_seconds'] for r in compatible_results):.1f}-{max(r['latency_seconds'] for r in compatible_results):.1f}s",
            "cost_range": f"${min(r['cost_usd'] for r in compatible_results):.6f}-${max(r['cost_usd'] for r in compatible_results):.6f}",
            "recommendations": [
                f"Use {best_performance['hardware']} for best performance",
                f"Use {min_cost['hardware']} for lowest cost",
                "Consider hardware investment for production use"
            ]
        }
    
    def _analyze_api_scenario(self, result, model_name: str) -> Dict[str, Any]:
        """Analyze API deployment scenario results"""
        tokens_per_second = 1000 / result.latency_seconds if result.latency_seconds > 0 else 0
        
        return {
            "status": "API deployment viable",
            "tokens_per_second": f"{tokens_per_second:.1f}",
            "cost_per_1000_tokens": f"${result.cost_per_request_usd * (1000 / 500):.6f}",
            "recommendations": [
                f"{model_name} API suitable for production workloads",
                "Monitor costs and implement rate limiting",
                "Consider caching for repeated requests"
            ]
        }
    
    def run_all_scenarios(self) -> Dict[str, Any]:
        """Run all three scenarios and generate comprehensive report"""
        print("Running all scenarios...")
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "scenarios": {
                "scenario_1": self.test_scenario_1_local_deployment(),
                "scenario_2": self.test_scenario_2_api_deployment(),
                "scenario_3": self.test_scenario_3_enterprise_api()
            }
        }
        
        # Generate comparative analysis
        self.results["comparative_analysis"] = self._generate_comparative_analysis()
        
        return self.results
    
    def _generate_comparative_analysis(self) -> Dict[str, Any]:
        """Generate comparative analysis across all scenarios"""
        scenarios = self.results["scenarios"]
        
        # Extract key metrics for comparison
        comparison_data = []
        
        # Scenario 1 - get best local result
        if "scenario_1" in scenarios and "results" in scenarios["scenario_1"]:
            local_results = scenarios["scenario_1"]["results"]
            compatible_local = [r for r in local_results if r.get("compatible", False) and "error" not in r]
            if compatible_local:
                best_local = min(compatible_local, key=lambda x: x["latency_seconds"])
                comparison_data.append({
                    "scenario": "Mistral 7B (Local)",
                    "latency_per_1000_tokens": best_local["latency_seconds"],
                    "cost_per_1000_tokens": best_local["cost_usd"],
                    "deployment_type": "Local",
                    "hardware_requirement": best_local["hardware"]
                })
        
        # Scenario 2
        if "scenario_2" in scenarios and "result" in scenarios["scenario_2"]:
            result = scenarios["scenario_2"]["result"]
            comparison_data.append({
                "scenario": "LangChain 13B (API)",
                "latency_per_1000_tokens": result["latency_seconds"] * 2,  # 500 tokens to 1000
                "cost_per_1000_tokens": result["cost_usd"] * 2,
                "deployment_type": "API",
                "hardware_requirement": "None"
            })
        
        # Scenario 3
        if "scenario_3" in scenarios and "result" in scenarios["scenario_3"]:
            result = scenarios["scenario_3"]["result"]
            comparison_data.append({
                "scenario": "GPT-4 (API)",
                "latency_per_1000_tokens": result["latency_seconds"] / 2,  # 2000 tokens to 1000
                "cost_per_1000_tokens": result["cost_usd"] / 2,
                "deployment_type": "API",
                "hardware_requirement": "None"
            })
        
        return {
            "comparison_data": comparison_data,
            "recommendations": self._generate_recommendations(comparison_data)
        }
    
    def _generate_recommendations(self, comparison_data: List[Dict]) -> List[str]:
        """Generate recommendations based on comparative analysis"""
        recommendations = []
        
        if not comparison_data:
            return ["No valid comparison data available"]
        
        # Find best cost option
        best_cost = min(comparison_data, key=lambda x: x["cost_per_1000_tokens"])
        best_latency = min(comparison_data, key=lambda x: x["latency_per_1000_tokens"])
        
        recommendations.append(f"Best cost option: {best_cost['scenario']} (${best_cost['cost_per_1000_tokens']:.6f} per 1000 tokens)")
        recommendations.append(f"Best performance: {best_latency['scenario']} ({best_latency['latency_per_1000_tokens']:.1f}s per 1000 tokens)")
        
        # Specific recommendations
        local_options = [d for d in comparison_data if d["deployment_type"] == "Local"]
        api_options = [d for d in comparison_data if d["deployment_type"] == "API"]
        
        if local_options and api_options:
            recommendations.append("Consider hybrid approach: local for development, API for production")
        
        if local_options:
            recommendations.append("Local deployment requires hardware investment but offers lowest ongoing costs")
        
        if api_options:
            recommendations.append("API deployment offers scalability but incurs ongoing costs")
        
        return recommendations
    
    def save_results(self, filename: str = "scenario_test_results.json"):
        """Save test results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"Results saved to {filename}")
    
    def print_summary(self):
        """Print a summary of all test results"""
        print("\n" + "="*60)
        print("SCENARIO TESTING SUMMARY")
        print("="*60)
        
        for scenario_name, scenario_data in self.results["scenarios"].items():
            print(f"\n{scenario_name.upper()}:")
            print(f"  Name: {scenario_data.get('scenario', {}).get('name', 'N/A')}")
            
            if "summary" in scenario_data:
                summary = scenario_data["summary"]
                print(f"  Status: {summary.get('status', 'N/A')}")
                if "recommendations" in summary:
                    print("  Recommendations:")
                    for rec in summary["recommendations"]:
                        print(f"    - {rec}")
        
        if "comparative_analysis" in self.results:
            print(f"\nCOMPARATIVE ANALYSIS:")
            for rec in self.results["comparative_analysis"]["recommendations"]:
                print(f"  - {rec}")


def main():
    """Main function to run scenario testing"""
    tester = ScenarioTester()
    
    # Run all scenarios
    results = tester.run_all_scenarios()
    
    # Save results
    tester.save_results()
    
    # Print summary
    tester.print_summary()
    
    print(f"\nDetailed results saved to scenario_test_results.json")
    print(f"Scenario analysis saved to scenario_analysis.md")


if __name__ == "__main__":
    main() 