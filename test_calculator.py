#!/usr/bin/env python3
"""
Test script for LLM Inference Calculator
"""

from inference_calculator import LLMInferenceCalculator

def test_calculator():
    """Test the calculator with various scenarios"""
    calculator = LLMInferenceCalculator()
    
    print("=== LLM Inference Calculator Test ===\n")
    
    # Test scenarios
    test_cases = [
        {
            "name": "Mistral 7B Local (GPU_8GB)",
            "model": "7B",
            "tokens": 1000,
            "batch_size": 1,
            "hardware": "GPU_8GB",
            "deployment": "local"
        },
        {
            "name": "LangChain 13B API",
            "model": "13B",
            "tokens": 500,
            "batch_size": 1,
            "hardware": "GPU_8GB",
            "deployment": "api"
        },
        {
            "name": "GPT-4 API",
            "model": "GPT-4",
            "tokens": 2000,
            "batch_size": 1,
            "hardware": "GPU_8GB",
            "deployment": "api"
        },
        {
            "name": "Mistral 7B CPU",
            "model": "7B",
            "tokens": 500,
            "batch_size": 1,
            "hardware": "CPU",
            "deployment": "local"
        }
    ]
    
    for test_case in test_cases:
        print(f"Test: {test_case['name']}")
        print(f"Parameters: {test_case['model']}, {test_case['tokens']} tokens, "
              f"{test_case['hardware']}, {test_case['deployment']}")
        
        try:
            result = calculator.calculate(
                model_size=test_case['model'],
                tokens=test_case['tokens'],
                batch_size=test_case['batch_size'],
                hardware_type=test_case['hardware'],
                deployment_mode=test_case['deployment']
            )
            
            print(f"  Latency: {result.latency_seconds:.2f} seconds")
            print(f"  Memory Usage: {result.memory_usage_gb:.2f} GB")
            print(f"  Cost per Request: ${result.cost_per_request_usd:.6f}")
            print(f"  Hardware Compatible: {result.hardware_compatible}")
            
            if result.recommendations:
                print("  Recommendations:")
                for rec in result.recommendations:
                    print(f"    - {rec}")
            
        except Exception as e:
            print(f"  Error: {e}")
        
        print()

if __name__ == "__main__":
    test_calculator() 