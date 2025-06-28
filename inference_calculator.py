#!/usr/bin/env python3
"""
LLM Inference Calculator

A comprehensive calculator for estimating LLM inference costs, latency, and memory usage
for different models and deployment scenarios.

This module provides:
- Model specifications for Mistral 7B, LangChain 13B, and GPT-4
- Hardware compatibility checking
- Memory usage calculations
- Latency estimation
- Cost analysis for both local and API deployments
- Smart recommendations for optimization

Author: LLM Inference Calculator Team
Version: 1.0.0
License: MIT
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ModelSize(Enum):
    """
    Supported model sizes for inference calculations.
    
    Attributes:
        SEVEN_B: Mistral 7B model (7.3 billion parameters)
        THIRTEEN_B: LangChain 13B model (~13 billion parameters)
        GPT4: OpenAI GPT-4 model (~1.76 trillion parameters)
    """
    SEVEN_B = "7B"
    THIRTEEN_B = "13B"
    GPT4 = "GPT-4"


class HardwareType(Enum):
    """
    Supported hardware types for local deployment.
    
    Hardware configurations with their VRAM capacity and typical use cases.
    CPU is included for development/testing but not recommended for production.
    """
    CPU = "CPU"              # 0GB VRAM - Development/testing only
    GPU_4GB = "GPU_4GB"      # 4GB VRAM - Small models only
    GPU_8GB = "GPU_8GB"      # 8GB VRAM - Limited compatibility
    GPU_12GB = "GPU_12GB"    # 12GB VRAM - Good for 7B models
    GPU_16GB = "GPU_16GB"    # 16GB VRAM - Recommended minimum
    GPU_24GB = "GPU_24GB"    # 24GB VRAM - Excellent performance
    GPU_32GB = "GPU_32GB"    # 32GB VRAM - Best performance


class DeploymentMode(Enum):
    """
    Deployment modes for LLM inference.
    
    Attributes:
        LOCAL: Self-hosted deployment (requires hardware)
        API: Cloud API deployment (no hardware required)
    """
    LOCAL = "local"
    API = "api"


@dataclass
class ModelSpecs:
    """
    Model specifications for calculation purposes.
    
    Contains architectural details needed for memory and performance calculations.
    
    Attributes:
        parameters: Number of model parameters
        layers: Number of transformer layers
        heads: Number of attention heads
        head_dim: Dimension of each attention head
        context_length: Maximum context length in tokens
        vocabulary_size: Size of the vocabulary
    """
    parameters: int
    layers: int
    heads: int
    head_dim: int
    context_length: int
    vocabulary_size: int


@dataclass
class HardwareSpecs:
    """
    Hardware specifications for performance calculations.
    
    Contains performance characteristics needed for latency and cost calculations.
    
    Attributes:
        vram_gb: GPU VRAM in gigabytes
        memory_bandwidth_gbps: Memory bandwidth in GB/s
        compute_flops: Compute capability in FLOPS
        power_watts: Power consumption in watts
        cost_usd: Hardware cost in USD
    """
    vram_gb: float
    memory_bandwidth_gbps: float
    compute_flops: float
    power_watts: float
    cost_usd: float


@dataclass
class CalculationResult:
    """
    Result of inference calculations.
    
    Contains all calculated metrics and recommendations for a given configuration.
    
    Attributes:
        latency_seconds: Estimated inference time in seconds
        memory_usage_gb: Memory requirements in GB (local only)
        cost_per_request_usd: Cost per request in USD
        hardware_compatible: Whether hardware supports the model
        recommendations: List of optimization suggestions
    """
    latency_seconds: float
    memory_usage_gb: float
    cost_per_request_usd: float
    hardware_compatible: bool
    recommendations: List[str]


class LLMInferenceCalculator:
    """
    Main calculator class for LLM inference estimates.
    
    Provides comprehensive calculations for latency, memory usage, cost, and
    hardware compatibility across different models and deployment scenarios.
    
    The calculator uses empirically derived performance baselines and current
    pricing data to provide realistic estimates for planning purposes.
    """
    
    def __init__(self):
        """
        Initialize the calculator with model and hardware specifications.
        
        Sets up:
        - Model specifications (parameters, architecture details)
        - Hardware specifications (performance characteristics)
        - API pricing (current as of 2024)
        - Performance baselines (tokens per second for each model/hardware combination)
        """
        # Model specifications based on research and documentation
        self.model_specs = {
            ModelSize.SEVEN_B: ModelSpecs(
                parameters=7_300_000_000,  # 7.3B parameters (Mistral 7B)
                layers=32,                 # 32 transformer layers
                heads=32,                  # 32 attention heads
                head_dim=128,              # 128 dimensions per head
                context_length=8192,       # 8K context window
                vocabulary_size=32000      # 32K vocabulary
            ),
            ModelSize.THIRTEEN_B: ModelSpecs(
                parameters=13_000_000_000,  # 13B parameters (LangChain 13B)
                layers=40,                  # 40 transformer layers
                heads=40,                   # 40 attention heads
                head_dim=128,               # 128 dimensions per head
                context_length=4096,        # 4K context window
                vocabulary_size=32000       # 32K vocabulary
            ),
            ModelSize.GPT4: ModelSpecs(
                parameters=1_760_000_000_000,  # 1.76T parameters (estimated)
                layers=96,                      # 96 transformer layers
                heads=96,                       # 96 attention heads
                head_dim=128,                   # 128 dimensions per head
                context_length=8192,            # 8K context window
                vocabulary_size=100000          # 100K vocabulary
            )
        }
        
        # Hardware specifications based on real-world benchmarks
        self.hardware_specs = {
            HardwareType.CPU: HardwareSpecs(
                vram_gb=0,                    # No VRAM
                memory_bandwidth_gbps=50,     # DDR4-3200 bandwidth
                compute_flops=100_000_000_000,  # 100 GFLOPS (typical CPU)
                power_watts=65,               # CPU power consumption
                cost_usd=200                  # CPU cost
            ),
            HardwareType.GPU_4GB: HardwareSpecs(
                vram_gb=4,                    # 4GB VRAM (GTX 1650)
                memory_bandwidth_gbps=112,    # GTX 1650 bandwidth
                compute_flops=2_000_000_000_000,  # 2 TFLOPS
                power_watts=75,               # GPU power consumption
                cost_usd=150                  # GPU cost
            ),
            HardwareType.GPU_8GB: HardwareSpecs(
                vram_gb=8,                    # 8GB VRAM (RTX 3070)
                memory_bandwidth_gbps=448,    # RTX 3070 bandwidth
                compute_flops=20_000_000_000_000,  # 20 TFLOPS
                power_watts=220,              # GPU power consumption
                cost_usd=500                  # GPU cost
            ),
            HardwareType.GPU_12GB: HardwareSpecs(
                vram_gb=12,                   # 12GB VRAM (RTX 3080)
                memory_bandwidth_gbps=504,    # RTX 3080 bandwidth
                compute_flops=30_000_000_000_000,  # 30 TFLOPS
                power_watts=320,              # GPU power consumption
                cost_usd=700                  # GPU cost
            ),
            HardwareType.GPU_16GB: HardwareSpecs(
                vram_gb=16,                   # 16GB VRAM (RTX 4080)
                memory_bandwidth_gbps=760,    # RTX 4080 bandwidth
                compute_flops=40_000_000_000_000,  # 40 TFLOPS
                power_watts=320,              # GPU power consumption
                cost_usd=1200                 # GPU cost
            ),
            HardwareType.GPU_24GB: HardwareSpecs(
                vram_gb=24,                   # 24GB VRAM (RTX 4090)
                memory_bandwidth_gbps=1008,   # RTX 4090 bandwidth
                compute_flops=83_000_000_000_000,  # 83 TFLOPS
                power_watts=450,              # GPU power consumption
                cost_usd=1600                 # GPU cost
            ),
            HardwareType.GPU_32GB: HardwareSpecs(
                vram_gb=32,                   # 32GB VRAM (RTX 4090 + system RAM)
                memory_bandwidth_gbps=1008,   # RTX 4090 bandwidth
                compute_flops=83_000_000_000_000,  # 83 TFLOPS
                power_watts=450,              # GPU power consumption
                cost_usd=1600                 # GPU cost
            )
        }
        
        # API pricing (current as of 2024)
        # Prices are per 1000 tokens
        self.api_pricing = {
            ModelSize.SEVEN_B: {"input": 0.0, "output": 0.0},  # Local deployment only
            ModelSize.THIRTEEN_B: {"input": 0.0002, "output": 0.0004},  # LangChain API pricing
            ModelSize.GPT4: {"input": 0.01, "output": 0.03}  # GPT-4 Turbo pricing
        }
        
        # Performance baselines (tokens per second)
        # Based on empirical testing and benchmarks
        self.performance_baselines = {
            ModelSize.SEVEN_B: {
                HardwareType.CPU: 3,        # Very slow on CPU
                HardwareType.GPU_4GB: 8,    # Limited by VRAM
                HardwareType.GPU_8GB: 15,   # Good performance
                HardwareType.GPU_12GB: 25,  # Better performance
                HardwareType.GPU_16GB: 35,  # Excellent performance
                HardwareType.GPU_24GB: 45,  # Outstanding performance
                HardwareType.GPU_32GB: 50   # Best performance
            },
            ModelSize.THIRTEEN_B: {
                HardwareType.CPU: 1,        # Extremely slow on CPU
                HardwareType.GPU_4GB: 3,    # Very limited
                HardwareType.GPU_8GB: 6,    # Limited performance
                HardwareType.GPU_12GB: 10,  # Moderate performance
                HardwareType.GPU_16GB: 15,  # Good performance
                HardwareType.GPU_24GB: 25,  # Excellent performance
                HardwareType.GPU_32GB: 30   # Best performance
            },
            ModelSize.GPT4: {
                # GPT-4 is API-only, so hardware performance is not applicable
                # These values are placeholders for calculation consistency
                HardwareType.CPU: 0.1,
                HardwareType.GPU_4GB: 0.1,
                HardwareType.GPU_8GB: 0.1,
                HardwareType.GPU_12GB: 0.1,
                HardwareType.GPU_16GB: 0.1,
                HardwareType.GPU_24GB: 0.1,
                HardwareType.GPU_32GB: 0.1
            }
        }

    def calculate_memory_usage(self, model_size: ModelSize, tokens: int, 
                              batch_size: int, hardware_type: HardwareType) -> float:
        """
        Calculate memory usage in GB for local deployment.
        
        Memory calculation includes:
        - Model weights (FP16 precision assumed)
        - KV cache for attention mechanism
        - Activation memory for forward pass
        - Safety margin for stability
        
        Args:
            model_size: The model to calculate memory for
            tokens: Number of tokens in the sequence
            batch_size: Number of requests to process together
            hardware_type: Hardware configuration (for validation)
            
        Returns:
            Total memory usage in GB
            
        Note:
            This calculation assumes FP16 precision for model weights.
            For INT8 or INT4 quantization, memory usage would be reduced.
        """
        specs = self.model_specs[model_size]
        
        # Model weights memory (FP16 = 2 bytes per parameter)
        model_memory_gb = (specs.parameters * 2) / (1024**3)
        
        # KV cache memory calculation
        # Formula: 2 × layers × heads × head_dim × sequence_length × batch_size × bytes_per_token
        kv_cache_bytes = (2 * specs.layers * specs.heads * specs.head_dim * 
                         min(tokens, specs.context_length) * batch_size * 2)
        kv_cache_gb = kv_cache_bytes / (1024**3)
        
        # Activation memory (rough estimate based on model size and sequence length)
        # Typically 10% of the model size for intermediate activations
        activation_memory_gb = (tokens * specs.parameters * 2) / (1024**3) * 0.1
        
        # Total memory calculation
        total_memory = model_memory_gb + kv_cache_gb + activation_memory_gb
        
        # Add 20% safety margin for stability and overhead
        return total_memory * 1.2

    def calculate_latency(self, model_size: ModelSize, tokens: int, 
                         batch_size: int, hardware_type: HardwareType,
                         deployment_mode: DeploymentMode) -> float:
        """
        Calculate latency in seconds for inference.
        
        For API deployment, includes network latency and processing time.
        For local deployment, includes compute time and memory overhead.
        
        Args:
            model_size: The model to calculate latency for
            tokens: Number of tokens to process
            batch_size: Number of requests to process together
            hardware_type: Hardware configuration (for local deployment)
            deployment_mode: Local or API deployment
            
        Returns:
            Estimated latency in seconds
        """
        if deployment_mode == DeploymentMode.API:
            # API latency includes network + processing
            base_latency = 2.0  # Base network latency (typical RTT)
            processing_time = tokens / 50  # Assume 50 tokens/sec processing on server
            return base_latency + processing_time
        
        # Local deployment latency calculation
        specs = self.model_specs[model_size]
        hardware = self.hardware_specs[hardware_type]
        
        # Get performance baseline (tokens per second)
        tokens_per_sec = self.performance_baselines[model_size][hardware_type]
        
        # Calculate compute time based on tokens and performance
        compute_time = tokens / tokens_per_sec
        
        # Add memory access overhead (typically 10% for memory operations)
        memory_overhead = 0.1
        
        return compute_time * (1 + memory_overhead)

    def calculate_cost(self, model_size: ModelSize, tokens: int, 
                      batch_size: int, hardware_type: HardwareType,
                      deployment_mode: DeploymentMode) -> float:
        """
        Calculate cost per request in USD.
        
        For API deployment, calculates based on token pricing.
        For local deployment, calculates hardware and electricity costs.
        
        Args:
            model_size: The model to calculate cost for
            tokens: Number of tokens to process
            batch_size: Number of requests to process together
            hardware_type: Hardware configuration (for local deployment)
            deployment_mode: Local or API deployment
            
        Returns:
            Cost per request in USD
        """
        if deployment_mode == DeploymentMode.API:
            # API cost based on token pricing
            pricing = self.api_pricing[model_size]
            
            # Assume 70% input tokens, 30% output tokens (typical ratio)
            input_tokens = tokens * 0.7
            output_tokens = tokens * 0.3
            
            # Calculate costs based on per-1000-token pricing
            input_cost = (input_tokens / 1000) * pricing["input"]
            output_cost = (output_tokens / 1000) * pricing["output"]
            
            return input_cost + output_cost
        
        # Local deployment cost calculation
        hardware = self.hardware_specs[hardware_type]
        latency = self.calculate_latency(model_size, tokens, batch_size, 
                                       hardware_type, deployment_mode)
        
        # Hardware cost per hour (assuming 3-year lifetime, 8 hours/day usage)
        # This amortizes the hardware cost over its useful life
        hardware_cost_per_hour = hardware.cost_usd / (3 * 365 * 8)
        
        # Electricity cost (assuming $0.12/kWh average rate)
        electricity_cost_per_hour = (hardware.power_watts / 1000) * 0.12
        
        # Total cost per hour
        total_cost_per_hour = hardware_cost_per_hour + electricity_cost_per_hour
        
        # Cost per request based on time used
        cost_per_request = (total_cost_per_hour / 3600) * latency
        
        return cost_per_request

    def check_hardware_compatibility(self, model_size: ModelSize, 
                                   hardware_type: HardwareType) -> bool:
        """
        Check if hardware is compatible with the model.
        
        For CPU, always returns True (but performance will be poor).
        For GPU, checks if available VRAM meets model requirements.
        
        Args:
            model_size: The model to check compatibility for
            hardware_type: Hardware configuration to check
            
        Returns:
            True if hardware is compatible, False otherwise
        """
        if hardware_type == HardwareType.CPU:
            # CPU can run any model (slowly)
            return True
        
        # Calculate required memory for the model
        required_memory = self.calculate_memory_usage(model_size, 2048, 1, hardware_type)
        available_memory = self.hardware_specs[hardware_type].vram_gb
        
        return available_memory >= required_memory

    def generate_recommendations(self, model_size: ModelSize, tokens: int,
                               batch_size: int, hardware_type: HardwareType,
                               deployment_mode: DeploymentMode) -> List[str]:
        """
        Generate recommendations based on configuration.
        
        Provides smart suggestions for optimization, cost reduction,
        and performance improvement based on the current setup.
        
        Args:
            model_size: The model being used
            tokens: Number of tokens in the request
            batch_size: Batch size for processing
            hardware_type: Hardware configuration
            deployment_mode: Deployment mode
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        if deployment_mode == DeploymentMode.LOCAL:
            # Local deployment recommendations
            if not self.check_hardware_compatibility(model_size, hardware_type):
                recommendations.append("Hardware incompatible - consider GPU with more VRAM")
            
            if hardware_type == HardwareType.CPU and model_size != ModelSize.SEVEN_B:
                recommendations.append("CPU inference will be very slow for this model size")
            
            if tokens > 2048:
                recommendations.append("Long sequences may cause memory issues")
        
        elif deployment_mode == DeploymentMode.API:
            # API deployment recommendations
            if model_size == ModelSize.GPT4 and tokens > 1000:
                recommendations.append("GPT-4 costs can be high for long sequences")
            
            if batch_size > 1:
                recommendations.append("API deployment typically doesn't support batching")
        
        # General recommendations
        if batch_size > 4:
            recommendations.append("Large batch sizes may cause memory issues")
        
        if tokens > 4096:
            recommendations.append("Consider chunking long sequences")
        
        return recommendations

    def calculate(self, model_size: str, tokens: int, batch_size: int = 1,
                 hardware_type: str = "GPU_8GB", deployment_mode: str = "local") -> CalculationResult:
        """
        Main calculation method that provides comprehensive inference estimates.
        
        This is the primary interface for the calculator. It validates inputs,
        performs all calculations, and returns a comprehensive result object.
        
        Args:
            model_size: Model size as string ("7B", "13B", "GPT-4")
            tokens: Number of tokens (input + output)
            batch_size: Number of requests per batch (default: 1)
            hardware_type: Hardware configuration (default: "GPU_8GB")
            deployment_mode: Deployment mode (default: "local")
            
        Returns:
            CalculationResult object with all metrics and recommendations
            
        Raises:
            ValueError: If input parameters are invalid
            
        Example:
            >>> calculator = LLMInferenceCalculator()
            >>> result = calculator.calculate("7B", 1000, hardware_type="GPU_16GB")
            >>> print(f"Latency: {result.latency_seconds:.2f}s")
            >>> print(f"Cost: ${result.cost_per_request_usd:.6f}")
        """
        # Convert string inputs to enums with validation
        try:
            model_enum = ModelSize(model_size)
            hardware_enum = HardwareType(hardware_type)
            deployment_enum = DeploymentMode(deployment_mode)
        except ValueError as e:
            raise ValueError(f"Invalid input parameter: {e}")
        
        # Validate numeric inputs
        if tokens <= 0:
            raise ValueError("Tokens must be positive")
        if batch_size <= 0:
            raise ValueError("Batch size must be positive")
        
        # Perform all calculations
        memory_usage = self.calculate_memory_usage(model_enum, tokens, batch_size, hardware_enum)
        latency = self.calculate_latency(model_enum, tokens, batch_size, hardware_enum, deployment_enum)
        cost = self.calculate_cost(model_enum, tokens, batch_size, hardware_enum, deployment_enum)
        hardware_compatible = self.check_hardware_compatibility(model_enum, hardware_enum)
        recommendations = self.generate_recommendations(model_enum, tokens, batch_size, 
                                                      hardware_enum, deployment_enum)
        
        # Return comprehensive result
        return CalculationResult(
            latency_seconds=latency,
            memory_usage_gb=memory_usage,
            cost_per_request_usd=cost,
            hardware_compatible=hardware_compatible,
            recommendations=recommendations
        )


def main():
    """
    CLI interface for the calculator.
    
    Provides a command-line interface for easy usage of the calculator.
    Supports all major use cases with argument parsing and formatted output.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="LLM Inference Calculator - Estimate costs, latency, and memory usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic local deployment
  python inference_calculator.py --model 7B --tokens 1000 --hardware GPU_16GB --deployment local
  
  # API deployment
  python inference_calculator.py --model 13B --tokens 500 --deployment api
  
  # Enterprise usage
  python inference_calculator.py --model GPT-4 --tokens 2000 --deployment api
        """
    )
    
    parser.add_argument("--model", choices=["7B", "13B", "GPT-4"], required=True,
                       help="Model size to analyze")
    parser.add_argument("--tokens", type=int, required=True,
                       help="Number of tokens (input + output)")
    parser.add_argument("--batch-size", type=int, default=1,
                       help="Batch size (default: 1)")
    parser.add_argument("--hardware", 
                       choices=["CPU", "GPU_4GB", "GPU_8GB", "GPU_12GB", "GPU_16GB", "GPU_24GB", "GPU_32GB"],
                       default="GPU_8GB", help="Hardware type (default: GPU_8GB)")
    parser.add_argument("--deployment", choices=["local", "api"], default="local",
                       help="Deployment mode (default: local)")
    
    args = parser.parse_args()
    
    # Initialize calculator and perform calculation
    calculator = LLMInferenceCalculator()
    
    try:
        result = calculator.calculate(
            model_size=args.model,
            tokens=args.tokens,
            batch_size=args.batch_size,
            hardware_type=args.hardware,
            deployment_mode=args.deployment
        )
        
        # Print formatted results
        print(f"\n=== LLM Inference Calculator Results ===")
        print(f"Model: {args.model}")
        print(f"Tokens: {args.tokens}")
        print(f"Batch Size: {args.batch_size}")
        print(f"Hardware: {args.hardware}")
        print(f"Deployment: {args.deployment}")
        print(f"\nResults:")
        print(f"  Latency: {result.latency_seconds:.2f} seconds")
        print(f"  Memory Usage: {result.memory_usage_gb:.2f} GB")
        print(f"  Cost per Request: ${result.cost_per_request_usd:.6f}")
        print(f"  Hardware Compatible: {result.hardware_compatible}")
        
        if result.recommendations:
            print(f"\nRecommendations:")
            for rec in result.recommendations:
                print(f"  - {rec}")
        
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 