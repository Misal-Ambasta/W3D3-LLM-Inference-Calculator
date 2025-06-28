#!/usr/bin/env python3
"""
Interactive CLI for LLM Inference Calculator

Provides a user-friendly interactive interface for calculating LLM inference metrics.
Features include guided input, validation, and helpful explanations.
"""

import sys
import os
from typing import Optional, Tuple
from inference_calculator import (
    LLMInferenceCalculator, 
    ModelSize, 
    HardwareType, 
    DeploymentMode,
    CalculationResult
)


class InteractiveCLI:
    """Interactive command-line interface for the LLM Inference Calculator."""
    
    def __init__(self):
        self.calculator = LLMInferenceCalculator()
        self.current_config = {
            'model_size': None,
            'tokens': None,
            'batch_size': None,
            'hardware_type': None,
            'deployment_mode': None
        }
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        print("=" * 60)
        print("🤖 LLM Inference Calculator - Interactive Mode")
        print("=" * 60)
        print("Calculate costs, latency, and memory usage for LLM inference")
        print("=" * 60)
    
    def print_menu(self):
        """Print the main menu."""
        print("\n📋 Main Menu:")
        print("1. 🚀 Quick Calculation")
        print("2. ⚙️  Configure Settings")
        print("3. 📊 Compare Scenarios")
        print("4. 💡 View Recommendations")
        print("5. 📖 Help & Information")
        print("6. 🚪 Exit")
        print("-" * 40)
    
    def get_user_choice(self, min_choice: int, max_choice: int, prompt: str = "Enter your choice") -> int:
        """Get and validate user choice."""
        while True:
            try:
                choice = input(f"{prompt} ({min_choice}-{max_choice}): ").strip()
                choice_int = int(choice)
                if min_choice <= choice_int <= max_choice:
                    return choice_int
                else:
                    print(f"❌ Please enter a number between {min_choice} and {max_choice}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_model_size(self) -> ModelSize:
        """Get model size from user."""
        print("\n🤖 Select Model Size:")
        print("1. Mistral 7B (Local via Ollama)")
        print("2. LangChain 13B (API)")
        print("3. GPT-4 (OpenAI API)")
        print("-" * 40)
        
        choice = self.get_user_choice(1, 3, "Select model")
        
        model_map = {
            1: ModelSize.SEVEN_B,
            2: ModelSize.THIRTEEN_B,
            3: ModelSize.GPT4
        }
        
        model = model_map[choice]
        print(f"✅ Selected: {model.value}")
        return model
    
    def get_tokens(self) -> int:
        """Get number of tokens from user."""
        print("\n📝 Token Count:")
        print("Enter the total number of tokens (input + output)")
        print("Typical values:")
        print("  • Short response: 100-500 tokens")
        print("  • Medium response: 500-1000 tokens")
        print("  • Long response: 1000-2000 tokens")
        print("  • Document analysis: 2000+ tokens")
        print("-" * 40)
        
        while True:
            try:
                tokens = input("Enter token count: ").strip()
                tokens_int = int(tokens)
                if tokens_int > 0:
                    print(f"✅ Tokens: {tokens_int}")
                    return tokens_int
                else:
                    print("❌ Token count must be positive")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_batch_size(self) -> int:
        """Get batch size from user."""
        print("\n📦 Batch Size:")
        print("Number of requests to process together")
        print("• 1: Single request (most common)")
        print("• 2-4: Small batch (good for efficiency)")
        print("• 5+: Large batch (may cause memory issues)")
        print("-" * 40)
        
        while True:
            try:
                batch = input("Enter batch size (default: 1): ").strip()
                if not batch:
                    print("✅ Batch size: 1 (default)")
                    return 1
                
                batch_int = int(batch)
                if batch_int > 0:
                    print(f"✅ Batch size: {batch_int}")
                    return batch_int
                else:
                    print("❌ Batch size must be positive")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_hardware_type(self) -> HardwareType:
        """Get hardware type from user."""
        print("\n💻 Select Hardware (for local deployment):")
        print("1. CPU (Development/testing only - very slow)")
        print("2. GPU 4GB (Small models only)")
        print("3. GPU 8GB (Limited compatibility)")
        print("4. GPU 12GB (Good for 7B models)")
        print("5. GPU 16GB (Recommended minimum)")
        print("6. GPU 24GB (Excellent performance)")
        print("7. GPU 32GB (Best performance)")
        print("-" * 40)
        
        choice = self.get_user_choice(1, 7, "Select hardware")
        
        hardware_map = {
            1: HardwareType.CPU,
            2: HardwareType.GPU_4GB,
            3: HardwareType.GPU_8GB,
            4: HardwareType.GPU_12GB,
            5: HardwareType.GPU_16GB,
            6: HardwareType.GPU_24GB,
            7: HardwareType.GPU_32GB
        }
        
        hardware = hardware_map[choice]
        print(f"✅ Selected: {hardware.value}")
        return hardware
    
    def get_deployment_mode(self) -> DeploymentMode:
        """Get deployment mode from user."""
        print("\n🌐 Select Deployment Mode:")
        print("1. Local (Self-hosted - requires hardware)")
        print("2. API (Cloud-based - no hardware needed)")
        print("-" * 40)
        
        choice = self.get_user_choice(1, 2, "Select deployment mode")
        
        deployment_map = {
            1: DeploymentMode.LOCAL,
            2: DeploymentMode.API
        }
        
        deployment = deployment_map[choice]
        print(f"✅ Selected: {deployment.value}")
        return deployment
    
    def configure_settings(self):
        """Configure all settings interactively."""
        print("\n⚙️  Configuration Mode")
        print("Configure your inference settings step by step")
        print("-" * 40)
        
        # Get model size
        self.current_config['model_size'] = self.get_model_size()
        
        # Get tokens
        self.current_config['tokens'] = self.get_tokens()
        
        # Get batch size
        self.current_config['batch_size'] = self.get_batch_size()
        
        # Get deployment mode
        self.current_config['deployment_mode'] = self.get_deployment_mode()
        
        # Get hardware type (only for local deployment)
        if self.current_config['deployment_mode'] == DeploymentMode.LOCAL:
            self.current_config['hardware_type'] = self.get_hardware_type()
        else:
            self.current_config['hardware_type'] = None
            print("\n💡 Hardware not needed for API deployment")
        
        print("\n✅ Configuration complete!")
        self.show_current_config()
    
    def show_current_config(self):
        """Display current configuration."""
        print("\n📋 Current Configuration:")
        print("-" * 40)
        print(f"Model: {self.current_config['model_size'].value if self.current_config['model_size'] else 'Not set'}")
        print(f"Tokens: {self.current_config['tokens'] if self.current_config['tokens'] else 'Not set'}")
        print(f"Batch Size: {self.current_config['batch_size'] if self.current_config['batch_size'] else 'Not set'}")
        print(f"Deployment: {self.current_config['deployment_mode'].value if self.current_config['deployment_mode'] else 'Not set'}")
        if self.current_config['hardware_type']:
            print(f"Hardware: {self.current_config['hardware_type'].value}")
        print("-" * 40)
    
    def quick_calculation(self):
        """Perform a quick calculation with guided input."""
        print("\n🚀 Quick Calculation Mode")
        print("Let's get your inference estimates quickly!")
        print("-" * 40)
        
        # Check if we have a complete configuration
        if all(self.current_config.values()):
            print("✅ Using saved configuration")
            self.show_current_config()
            
            choice = input("\nUse saved configuration? (y/n): ").strip().lower()
            if choice != 'y':
                self.configure_settings()
        else:
            print("❌ No saved configuration found")
            self.configure_settings()
        
        # Perform calculation
        self.perform_calculation()
    
    def perform_calculation(self):
        """Perform the actual calculation and display results."""
        try:
            # Prepare parameters for calculation
            model_size = self.current_config['model_size'].value
            tokens = self.current_config['tokens']
            batch_size = self.current_config['batch_size']
            deployment_mode = self.current_config['deployment_mode'].value
            
            # Handle hardware type
            if self.current_config['hardware_type']:
                hardware_type = self.current_config['hardware_type'].value
            else:
                hardware_type = "GPU_8GB"  # Default for API calculations
            
            # Perform calculation
            result = self.calculator.calculate(
                model_size=model_size,
                tokens=tokens,
                batch_size=batch_size,
                hardware_type=hardware_type,
                deployment_mode=deployment_mode
            )
            
            # Display results
            self.display_results(result)
            
        except Exception as e:
            print(f"\n❌ Error during calculation: {e}")
            print("Please check your configuration and try again.")
    
    def display_results(self, result: CalculationResult):
        """Display calculation results in a formatted way."""
        print("\n" + "=" * 60)
        print("📊 CALCULATION RESULTS")
        print("=" * 60)
        
        # Configuration summary
        print(f"Model: {self.current_config['model_size'].value}")
        print(f"Tokens: {self.current_config['tokens']:,}")
        print(f"Batch Size: {self.current_config['batch_size']}")
        print(f"Deployment: {self.current_config['deployment_mode'].value}")
        if self.current_config['hardware_type']:
            print(f"Hardware: {self.current_config['hardware_type'].value}")
        
        print("\n" + "-" * 40)
        
        # Results
        print("📈 Performance Metrics:")
        print(f"  ⏱️  Latency: {result.latency_seconds:.2f} seconds")
        
        if self.current_config['deployment_mode'] == DeploymentMode.LOCAL:
            print(f"  💾 Memory Usage: {result.memory_usage_gb:.2f} GB")
        
        print(f"  💰 Cost per Request: ${result.cost_per_request_usd:.6f}")
        
        # Cost analysis
        cost_per_1k = (result.cost_per_request_usd / self.current_config['tokens']) * 1000
        print(f"  📊 Cost per 1K tokens: ${cost_per_1k:.6f}")
        
        # Hardware compatibility
        if self.current_config['deployment_mode'] == DeploymentMode.LOCAL:
            status = "✅ Compatible" if result.hardware_compatible else "❌ Incompatible"
            print(f"  🔧 Hardware: {status}")
        
        # Recommendations
        if result.recommendations:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(result.recommendations, 1):
                print(f"  {i}. {rec}")
        
        print("\n" + "=" * 60)
    
    def compare_scenarios(self):
        """Compare different scenarios."""
        print("\n📊 Scenario Comparison")
        print("Compare different configurations side by side")
        print("-" * 40)
        
        # Define scenarios to compare
        scenarios = [
            {
                'name': 'Development (Mistral 7B Local)',
                'model': '7B',
                'tokens': 1000,
                'batch_size': 1,
                'hardware': 'GPU_16GB',
                'deployment': 'local'
            },
            {
                'name': 'Production API (LangChain 13B)',
                'model': '13B',
                'tokens': 1000,
                'batch_size': 1,
                'hardware': 'GPU_8GB',
                'deployment': 'api'
            },
            {
                'name': 'Enterprise (GPT-4 API)',
                'model': 'GPT-4',
                'tokens': 1000,
                'batch_size': 1,
                'hardware': 'GPU_8GB',
                'deployment': 'api'
            }
        ]
        
        results = []
        
        print("🔄 Calculating scenarios...")
        for scenario in scenarios:
            try:
                result = self.calculator.calculate(
                    model_size=scenario['model'],
                    tokens=scenario['tokens'],
                    batch_size=scenario['batch_size'],
                    hardware_type=scenario['hardware'],
                    deployment_mode=scenario['deployment']
                )
                results.append((scenario, result))
            except Exception as e:
                print(f"❌ Error calculating {scenario['name']}: {e}")
        
        # Display comparison table
        print("\n" + "=" * 100)
        print("📊 SCENARIO COMPARISON (1000 tokens)")
        print("=" * 100)
        
        print(f"{'Scenario':<30} {'Latency (s)':<12} {'Memory (GB)':<12} {'Cost/Req ($)':<12} {'Cost/1K ($)':<12}")
        print("-" * 100)
        
        for scenario, result in results:
            memory_str = f"{result.memory_usage_gb:.2f}" if scenario['deployment'] == 'local' else "N/A"
            cost_per_1k = (result.cost_per_request_usd / scenario['tokens']) * 1000
            
            print(f"{scenario['name']:<30} {result.latency_seconds:<12.2f} {memory_str:<12} "
                  f"{result.cost_per_request_usd:<12.6f} {cost_per_1k:<12.6f}")
        
        print("=" * 100)
        
        # Recommendations
        print("\n💡 Key Insights:")
        print("• Local deployment has lowest cost but requires hardware investment")
        print("• API deployment offers convenience but ongoing costs")
        print("• GPT-4 provides best quality but highest cost")
        print("• Consider your use case and budget when choosing")
    
    def show_recommendations(self):
        """Show general recommendations and best practices."""
        print("\n💡 Recommendations & Best Practices")
        print("=" * 60)
        
        print("\n🚀 For Development & Testing:")
        print("• Use Mistral 7B locally for cost-free development")
        print("• Minimum hardware: RTX 4080 (16GB VRAM)")
        print("• Consider quantization for memory efficiency")
        
        print("\n🏭 For Production (Low-Medium Volume):")
        print("• Use LangChain 13B API for good balance of cost/quality")
        print("• Implement request caching to reduce costs")
        print("• Monitor usage and set rate limits")
        
        print("\n🏢 For Enterprise (High Quality Required):")
        print("• Use GPT-4 API for best-in-class performance")
        print("• Implement proper error handling and retries")
        print("• Consider hybrid approach for cost optimization")
        
        print("\n💰 Cost Optimization Tips:")
        print("• Optimize prompts to reduce token usage")
        print("• Use smaller models for simple tasks")
        print("• Implement streaming for long outputs")
        print("• Batch requests when possible")
        
        print("\n⚡ Performance Tips:")
        print("• Use appropriate hardware for local deployment")
        print("• Implement proper caching strategies")
        print("• Monitor latency and optimize bottlenecks")
        print("• Consider model quantization for efficiency")
    
    def show_help(self):
        """Show help information."""
        print("\n📖 Help & Information")
        print("=" * 60)
        
        print("\n🤖 About the Calculator:")
        print("This tool helps you estimate the costs, latency, and memory")
        print("requirements for running Large Language Models (LLMs).")
        
        print("\n📊 What it calculates:")
        print("• Latency: How long inference takes")
        print("• Memory: How much RAM/VRAM is needed")
        print("• Cost: Price per request")
        print("• Compatibility: Whether your hardware supports the model")
        
        print("\n🔧 Supported Models:")
        print("• Mistral 7B: Local deployment via Ollama")
        print("• LangChain 13B: API-based deployment")
        print("• GPT-4: OpenAI API deployment")
        
        print("\n💻 Hardware Options:")
        print("• CPU: Development/testing only (very slow)")
        print("• GPU 4GB-32GB: Various performance levels")
        print("• Higher VRAM = better performance")
        
        print("\n🌐 Deployment Modes:")
        print("• Local: Self-hosted (requires hardware)")
        print("• API: Cloud-based (no hardware needed)")
        
        print("\n💡 Tips:")
        print("• Start with Quick Calculation for simple estimates")
        print("• Use Configure Settings for detailed setup")
        print("• Compare Scenarios to see different options")
        print("• Check Recommendations for optimization tips")
    
    def run(self):
        """Main application loop."""
        while True:
            self.clear_screen()
            self.print_header()
            self.print_menu()
            
            choice = self.get_user_choice(1, 6, "Select option")
            
            if choice == 1:
                self.quick_calculation()
            elif choice == 2:
                self.configure_settings()
            elif choice == 3:
                self.compare_scenarios()
            elif choice == 4:
                self.show_recommendations()
            elif choice == 5:
                self.show_help()
            elif choice == 6:
                print("\n👋 Thank you for using LLM Inference Calculator!")
                print("Goodbye! 🚀")
                break
            
            if choice != 6:
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    try:
        cli = InteractiveCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using LLM Inference Calculator!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue if it persists.")


if __name__ == "__main__":
    main() 