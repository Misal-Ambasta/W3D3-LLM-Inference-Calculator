#!/usr/bin/env python3
"""
Demo script for Interactive CLI

Demonstrates the interactive CLI features and capabilities.
"""

import sys
import os
from interactive_cli import InteractiveCLI
from inference_calculator import ModelSize, HardwareType, DeploymentMode, CalculationResult

def demo_interactive_cli():
    """Demonstrate the interactive CLI features."""
    print("🎬 Interactive CLI Demo")
    print("=" * 60)
    
    # Create CLI instance
    cli = InteractiveCLI()
    
    # Demo 1: Show header and menu
    print("\n📋 Demo 1: Application Header and Menu")
    print("-" * 40)
    cli.print_header()
    cli.print_menu()
    
    # Demo 2: Show model selection
    print("\n🤖 Demo 2: Model Selection Interface")
    print("-" * 40)
    print("This is what users would see when selecting a model:")
    print("1. Mistral 7B (Local via Ollama)")
    print("2. LangChain 13B (API)")
    print("3. GPT-4 (OpenAI API)")
    
    # Demo 3: Show token input guidance
    print("\n📝 Demo 3: Token Input Guidance")
    print("-" * 40)
    print("Users get helpful guidance for token counts:")
    print("• Short response: 100-500 tokens")
    print("• Medium response: 500-1000 tokens")
    print("• Long response: 1000-2000 tokens")
    print("• Document analysis: 2000+ tokens")
    
    # Demo 4: Show hardware selection
    print("\n💻 Demo 4: Hardware Selection")
    print("-" * 40)
    print("Hardware options with clear descriptions:")
    print("1. CPU (Development/testing only - very slow)")
    print("2. GPU 4GB (Small models only)")
    print("3. GPU 8GB (Limited compatibility)")
    print("4. GPU 12GB (Good for 7B models)")
    print("5. GPU 16GB (Recommended minimum)")
    print("6. GPU 24GB (Excellent performance)")
    print("7. GPU 32GB (Best performance)")
    
    # Demo 5: Show deployment mode selection
    print("\n🌐 Demo 5: Deployment Mode Selection")
    print("-" * 40)
    print("Clear deployment options:")
    print("1. Local (Self-hosted - requires hardware)")
    print("2. API (Cloud-based - no hardware needed)")
    
    # Demo 6: Show calculation results
    print("\n📊 Demo 6: Calculation Results Display")
    print("-" * 40)
    
    # Set up a demo configuration
    cli.current_config = {
        'model_size': ModelSize.SEVEN_B,
        'tokens': 1000,
        'batch_size': 1,
        'hardware_type': HardwareType.GPU_16GB,
        'deployment_mode': DeploymentMode.LOCAL
    }
    
    # Perform calculation
    result = cli.calculator.calculate(
        model_size="7B",
        tokens=1000,
        batch_size=1,
        hardware_type="GPU_16GB",
        deployment_mode="local"
    )
    
    # Display results
    cli.display_results(result)
    
    # Demo 7: Show scenario comparison
    print("\n📊 Demo 7: Scenario Comparison")
    print("-" * 40)
    print("Users can compare different configurations:")
    print("• Development (Mistral 7B Local)")
    print("• Production API (LangChain 13B)")
    print("• Enterprise (GPT-4 API)")
    
    # Demo 8: Show recommendations
    print("\n💡 Demo 8: Recommendations")
    print("-" * 40)
    print("Smart recommendations based on configuration:")
    for i, rec in enumerate(result.recommendations, 1):
        print(f"  {i}. {rec}")
    
    # Demo 9: Show help information
    print("\n📖 Demo 9: Help & Information")
    print("-" * 40)
    print("Comprehensive help system available:")
    print("• About the Calculator")
    print("• What it calculates")
    print("• Supported Models")
    print("• Hardware Options")
    print("• Deployment Modes")
    print("• Usage Tips")
    
    print("\n🎉 Demo Complete!")
    print("The Interactive CLI provides:")
    print("✅ User-friendly guided input")
    print("✅ Input validation and error handling")
    print("✅ Helpful explanations and recommendations")
    print("✅ Scenario comparison capabilities")
    print("✅ Comprehensive help system")
    print("✅ Professional formatting and emojis")

if __name__ == "__main__":
    demo_interactive_cli() 