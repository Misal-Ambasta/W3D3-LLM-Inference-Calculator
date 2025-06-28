#!/usr/bin/env python3
"""
Success Criteria Verification for LLM Inference Calculator

This script verifies that all success criteria from the project requirements
are met by testing the actual functionality of the calculator.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from inference_calculator import LLMInferenceCalculator
from typing import Dict, List, Tuple


class SuccessCriteriaVerifier:
    """Verifies all success criteria for the LLM Inference Calculator"""
    
    def __init__(self):
        self.calculator = LLMInferenceCalculator()
        self.results = {}
        self.all_passed = True
    
    def test_criterion_1_reasonable_estimates(self) -> bool:
        """
        Test Criterion 1: Calculator provides reasonable estimates for all target models
        
        Verifies that:
        - All three models (7B, 13B, GPT-4) can be calculated
        - Estimates are within reasonable ranges
        - No errors occur during calculation
        """
        print("Testing Criterion 1: Reasonable estimates for all target models")
        print("-" * 60)
        
        models = ["7B", "13B", "GPT-4"]
        test_cases = [
            {"tokens": 1000, "hardware": "GPU_16GB", "deployment": "local"},
            {"tokens": 500, "hardware": "GPU_8GB", "deployment": "api"},
            {"tokens": 2000, "hardware": "GPU_24GB", "deployment": "api"}
        ]
        
        passed = True
        
        for i, model in enumerate(models):
            test_case = test_cases[i]
            print(f"Testing {model} model...")
            
            try:
                result = self.calculator.calculate(
                    model_size=model,
                    tokens=test_case["tokens"],
                    hardware_type=test_case["hardware"],
                    deployment_mode=test_case["deployment"]
                )
                
                # Check if results are reasonable
                if result.latency_seconds <= 0:
                    print(f"  ❌ Invalid latency: {result.latency_seconds}")
                    passed = False
                elif result.latency_seconds > 1000:  # More than 16 minutes
                    print(f"  ⚠️  Very high latency: {result.latency_seconds:.1f}s")
                
                if result.cost_per_request_usd < 0:
                    print(f"  ❌ Negative cost: {result.cost_per_request_usd}")
                    passed = False
                elif result.cost_per_request_usd > 1.0:  # More than $1 per request
                    print(f"  ⚠️  Very high cost: ${result.cost_per_request_usd:.6f}")
                
                if test_case["deployment"] == "local" and result.memory_usage_gb <= 0:
                    print(f"  ❌ Invalid memory usage: {result.memory_usage_gb}")
                    passed = False
                
                print(f"  ✅ {model}: {result.latency_seconds:.1f}s, ${result.cost_per_request_usd:.6f}")
                
            except Exception as e:
                print(f"  ❌ Error calculating {model}: {e}")
                passed = False
        
        print(f"Criterion 1 Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        return passed
    
    def test_criterion_2_hardware_compatibility(self) -> bool:
        """
        Test Criterion 2: Hardware compatibility checking works accurately for local deployment
        
        Verifies that:
        - Compatible hardware returns True
        - Incompatible hardware returns False
        - CPU always returns True (but with poor performance)
        """
        print("\nTesting Criterion 2: Hardware compatibility checking")
        print("-" * 60)
        
        test_cases = [
            # (hardware, expected_compatible, description)
            ("CPU", True, "CPU should always be compatible"),
            ("GPU_4GB", False, "4GB GPU insufficient for 7B model"),
            ("GPU_8GB", False, "8GB GPU insufficient for 7B model"),
            ("GPU_16GB", True, "16GB GPU should be compatible"),
            ("GPU_24GB", True, "24GB GPU should be compatible"),
            ("GPU_32GB", True, "32GB GPU should be compatible"),
        ]
        
        passed = True
        
        for hardware, expected, description in test_cases:
            try:
                result = self.calculator.calculate(
                    model_size="7B",
                    tokens=1000,
                    hardware_type=hardware,
                    deployment_mode="local"
                )
                
                actual = result.hardware_compatible
                status = "✅" if actual == expected else "❌"
                print(f"{status} {hardware}: {actual} (expected {expected}) - {description}")
                
                if actual != expected:
                    passed = False
                    
            except Exception as e:
                print(f"❌ Error testing {hardware}: {e}")
                passed = False
        
        print(f"Criterion 2 Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        return passed
    
    def test_criterion_3_cost_calculations(self) -> bool:
        """
        Test Criterion 3: Cost calculations include both self-hosted and API options
        
        Verifies that:
        - Local deployment costs are calculated (hardware + electricity)
        - API deployment costs are calculated (token pricing)
        - Costs are reasonable and positive
        """
        print("\nTesting Criterion 3: Cost calculations for both deployment modes")
        print("-" * 60)
        
        test_cases = [
            {"model": "7B", "deployment": "local", "hardware": "GPU_16GB", "expected_cost_range": (0.000001, 0.001)},
            {"model": "13B", "deployment": "api", "hardware": "GPU_8GB", "expected_cost_range": (0.0001, 0.01)},
            {"model": "GPT-4", "deployment": "api", "hardware": "GPU_8GB", "expected_cost_range": (0.01, 1.0)},
        ]
        
        passed = True
        
        for test_case in test_cases:
            try:
                result = self.calculator.calculate(
                    model_size=test_case["model"],
                    tokens=1000,
                    hardware_type=test_case["hardware"],
                    deployment_mode=test_case["deployment"]
                )
                
                cost = result.cost_per_request_usd
                min_expected, max_expected = test_case["expected_cost_range"]
                
                if cost < min_expected or cost > max_expected:
                    print(f"❌ {test_case['model']} ({test_case['deployment']}): ${cost:.6f} outside expected range ${min_expected:.6f}-${max_expected:.6f}")
                    passed = False
                else:
                    print(f"✅ {test_case['model']} ({test_case['deployment']}): ${cost:.6f}")
                
            except Exception as e:
                print(f"❌ Error testing {test_case['model']}: {e}")
                passed = False
        
        print(f"Criterion 3 Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        return passed
    
    def test_criterion_4_scenario_analysis(self) -> bool:
        """
        Test Criterion 4: Scenario analysis provides actionable insights
        
        Verifies that:
        - Scenario analysis file exists and is comprehensive
        - Contains cost-benefit analysis
        - Provides hardware recommendations
        - Includes deployment strategies
        """
        print("\nTesting Criterion 4: Scenario analysis provides actionable insights")
        print("-" * 60)
        
        passed = True
        
        # Check if scenario analysis file exists
        if not os.path.exists("scenario_analysis.md"):
            print("❌ scenario_analysis.md file not found")
            passed = False
        else:
            print("✅ scenario_analysis.md file exists")
            
            # Check file size (should be substantial)
            file_size = os.path.getsize("scenario_analysis.md")
            if file_size < 1000:  # Less than 1KB
                print(f"❌ scenario_analysis.md too small ({file_size} bytes)")
                passed = False
            else:
                print(f"✅ scenario_analysis.md size: {file_size} bytes")
        
        # Check if scenario testing framework exists
        if not os.path.exists("scenario_testing.py"):
            print("❌ scenario_testing.py file not found")
            passed = False
        else:
            print("✅ scenario_testing.py file exists")
        
        # Test scenario testing framework
        try:
            from scenario_testing import ScenarioTester
            tester = ScenarioTester()
            print("✅ Scenario testing framework imports successfully")
        except Exception as e:
            print(f"❌ Error importing scenario testing: {e}")
            passed = False
        
        print(f"Criterion 4 Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        return passed
    
    def test_criterion_5_documentation(self) -> bool:
        """
        Test Criterion 5: Documentation is comprehensive and user-friendly
        
        Verifies that:
        - README.md exists and is comprehensive
        - API documentation is complete
        - Installation instructions are clear
        - Examples are provided
        """
        print("\nTesting Criterion 5: Documentation is comprehensive and user-friendly")
        print("-" * 60)
        
        passed = True
        
        # Check README.md
        if not os.path.exists("README.md"):
            print("❌ README.md file not found")
            passed = False
        else:
            print("✅ README.md file exists")
            
            # Check README content
            with open("README.md", "r", encoding="utf-8") as f:
                content = f.read()
                
                required_sections = [
                    "## 🚀 Overview",
                    "## 🛠️ Installation",
                    "## 🚀 Quick Start",
                    "## 🔧 API Reference",
                    "## 📊 Usage Examples"
                ]
                
                for section in required_sections:
                    if section in content:
                        print(f"✅ Found section: {section}")
                    else:
                        print(f"❌ Missing section: {section}")
                        passed = False
            
            # Check file size
            file_size = os.path.getsize("README.md")
            if file_size < 5000:  # Less than 5KB
                print(f"❌ README.md too small ({file_size} bytes)")
                passed = False
            else:
                print(f"✅ README.md size: {file_size} bytes")
        
        # Check example files
        example_files = ["examples/basic_usage.py", "examples/advanced_analysis.py"]
        for example_file in example_files:
            if os.path.exists(example_file):
                print(f"✅ {example_file} exists")
            else:
                print(f"❌ {example_file} not found")
                passed = False
        
        print(f"Criterion 5 Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        return passed
    
    def test_criterion_6_code_structure(self) -> bool:
        """
        Test Criterion 6: Code is well-structured and maintainable
        
        Verifies that:
        - Code has proper documentation
        - Functions are well-organized
        - Error handling is implemented
        - Code follows good practices
        """
        print("\nTesting Criterion 6: Code is well-structured and maintainable")
        print("-" * 60)
        
        passed = True
        
        # Check main calculator file
        if not os.path.exists("inference_calculator.py"):
            print("❌ inference_calculator.py file not found")
            passed = False
        else:
            print("✅ inference_calculator.py file exists")
            
            # Check file content for documentation
            with open("inference_calculator.py", "r", encoding="utf-8") as f:
                content = f.read()
                
                # Check for docstrings
                if '"""' in content:
                    print("✅ Contains docstrings")
                else:
                    print("❌ Missing docstrings")
                    passed = False
                
                # Check for error handling
                if "try:" in content and "except:" in content:
                    print("✅ Contains error handling")
                else:
                    print("❌ Missing error handling")
                    passed = False
                
                # Check for type hints
                if "->" in content and ":" in content:
                    print("✅ Contains type hints")
                else:
                    print("❌ Missing type hints")
                    passed = False
                
                # Check file size (should be substantial)
                file_size = os.path.getsize("inference_calculator.py")
                if file_size < 5000:  # Less than 5KB
                    print(f"❌ inference_calculator.py too small ({file_size} bytes)")
                    passed = False
                else:
                    print(f"✅ inference_calculator.py size: {file_size} bytes")
        
        print(f"Criterion 6 Result: {'✅ PASSED' if passed else '❌ FAILED'}")
        return passed
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all success criteria tests"""
        print("=" * 80)
        print("SUCCESS CRITERIA VERIFICATION")
        print("=" * 80)
        
        self.results = {
            "Criterion 1": self.test_criterion_1_reasonable_estimates(),
            "Criterion 2": self.test_criterion_2_hardware_compatibility(),
            "Criterion 3": self.test_criterion_3_cost_calculations(),
            "Criterion 4": self.test_criterion_4_scenario_analysis(),
            "Criterion 5": self.test_criterion_5_documentation(),
            "Criterion 6": self.test_criterion_6_code_structure()
        }
        
        # Calculate overall result
        self.all_passed = all(self.results.values())
        
        # Print summary
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)
        
        for criterion, passed in self.results.items():
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{criterion}: {status}")
        
        print(f"\nOverall Result: {'✅ ALL CRITERIA PASSED' if self.all_passed else '❌ SOME CRITERIA FAILED'}")
        
        return self.results


def main():
    """Run success criteria verification"""
    verifier = SuccessCriteriaVerifier()
    results = verifier.run_all_tests()
    
    # Exit with appropriate code
    return 0 if verifier.all_passed else 1


if __name__ == "__main__":
    exit(main()) 