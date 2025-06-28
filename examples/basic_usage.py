#!/usr/bin/env python3
"""
Basic Usage Example for LLM Inference Calculator

This script demonstrates the fundamental usage of the calculator
for common scenarios.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference_calculator import LLMInferenceCalculator


def main():
    """Demonstrate basic calculator usage"""
    print("=== LLM Inference Calculator - Basic Usage Example ===\n")
    
    # Initialize calculator
    calculator = LLMInferenceCalculator()
    
    # Example 1: Check hardware compatibility
    print("1. Hardware Compatibility Check")
    print("-" * 40)
    
    hardware_configs = ["GPU_8GB", "GPU_16GB", "GPU_24GB"]
    
    for hardware in hardware_configs:
        result = calculator.calculate(
            model_size="7B",
            tokens=1000,
            hardware_type=hardware,
            deployment_mode="local"
        )
        
        status = "✅ Compatible" if result.hardware_compatible else "❌ Incompatible"
        print(f"{hardware}: {status}")
        print(f"  Latency: {result.latency_seconds:.1f}s")
        print(f"  Memory: {result.memory_usage_gb:.1f}GB")
        print(f"  Cost: ${result.cost_per_request_usd:.6f}")
        print()
    
    # Example 2: Cost comparison across models
    print("2. Cost Comparison Across Models")
    print("-" * 40)
    
    models = [
        ("7B", "local", "GPU_16GB"),
        ("13B", "api", "GPU_8GB"),  # Not used for API
        ("GPT-4", "api", "GPU_8GB")  # Not used for API
    ]
    
    for model, deployment, hardware in models:
        result = calculator.calculate(
            model_size=model,
            tokens=1000,
            hardware_type=hardware,
            deployment_mode=deployment
        )
        
        print(f"{model} ({deployment}): ${result.cost_per_request_usd:.6f}")
        print(f"  Latency: {result.latency_seconds:.1f}s")
        if deployment == "local":
            print(f"  Memory: {result.memory_usage_gb:.1f}GB")
        print()
    
    # Example 3: Token count impact
    print("3. Token Count Impact Analysis")
    print("-" * 40)
    
    token_counts = [100, 500, 1000, 2000]
    
    for tokens in token_counts:
        result = calculator.calculate(
            model_size="7B",
            tokens=tokens,
            hardware_type="GPU_16GB",
            deployment_mode="local"
        )
        
        print(f"{tokens} tokens:")
        print(f"  Latency: {result.latency_seconds:.1f}s")
        print(f"  Memory: {result.memory_usage_gb:.1f}GB")
        print(f"  Cost: ${result.cost_per_request_usd:.6f}")
        print()
    
    # Example 4: Batch processing analysis
    print("4. Batch Processing Analysis")
    print("-" * 40)
    
    batch_sizes = [1, 2, 4, 8]
    
    for batch_size in batch_sizes:
        result = calculator.calculate(
            model_size="7B",
            tokens=500,
            batch_size=batch_size,
            hardware_type="GPU_24GB",
            deployment_mode="local"
        )
        
        print(f"Batch size {batch_size}:")
        print(f"  Latency: {result.latency_seconds:.1f}s")
        print(f"  Memory: {result.memory_usage_gb:.1f}GB")
        print(f"  Cost per request: ${result.cost_per_request_usd:.6f}")
        print(f"  Total cost: ${result.cost_per_request_usd * batch_size:.6f}")
        print()
    
    print("=== Basic Usage Example Complete ===")


if __name__ == "__main__":
    main() 