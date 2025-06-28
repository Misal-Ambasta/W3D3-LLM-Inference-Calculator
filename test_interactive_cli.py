#!/usr/bin/env python3
"""
Test script for Interactive CLI

Tests the interactive CLI functionality without requiring user input.
"""

import sys
import os
from interactive_cli import InteractiveCLI
from inference_calculator import ModelSize, HardwareType, DeploymentMode

def test_interactive_cli():
    """Test the interactive CLI functionality."""
    print("🧪 Testing Interactive CLI...")
    
    try:
        # Create CLI instance
        cli = InteractiveCLI()
        print("✅ CLI instance created successfully")
        
        # Test configuration
        cli.current_config = {
            'model_size': ModelSize.SEVEN_B,
            'tokens': 1000,
            'batch_size': 1,
            'hardware_type': HardwareType.GPU_16GB,
            'deployment_mode': DeploymentMode.LOCAL
        }
        print("✅ Configuration set successfully")
        
        # Test calculation
        result = cli.calculator.calculate(
            model_size="7B",
            tokens=1000,
            batch_size=1,
            hardware_type="GPU_16GB",
            deployment_mode="local"
        )
        print("✅ Calculation performed successfully")
        
        # Test result display
        cli.display_results(result)
        print("✅ Results displayed successfully")
        
        print("\n🎉 All tests passed! Interactive CLI is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_interactive_cli()
    sys.exit(0 if success else 1) 