# LLM Inference Calculator

A comprehensive calculator for estimating LLM inference costs, latency, and memory usage for different models and deployment scenarios.

## 🚀 Overview

The LLM Inference Calculator helps developers and organizations make informed decisions about LLM deployment strategies by providing accurate estimates for:

- **Latency**: Inference time per request
- **Memory Usage**: Hardware requirements for local deployment
- **Cost**: Per-request costs for both local and API deployments
- **Hardware Compatibility**: Automatic compatibility checking
- **Recommendations**: Smart suggestions for optimization

## 🎯 Supported Models

| Model | Deployment | Use Case |
|-------|------------|----------|
| **Mistral 7B** | Local (Ollama) | Development, testing, low-volume production |
| **LangChain 13B** | API | Medium-scale production workloads |
| **GPT-4** | API (OpenAI) | Enterprise applications requiring high quality |

## 📋 Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd W3D3-LLM-Inference-Calculator
   ```

2. **Verify Python installation**:
   ```bash
   python --version  # Should be 3.8 or higher
   ```

3. **Test the calculator**:
   ```bash
   python test_calculator.py
   ```

## 🚀 Quick Start

### Interactive CLI (Recommended for New Users)

For the best user experience, use the interactive CLI:

```bash
python interactive_cli.py
```

The interactive CLI provides:
- 🎯 **Guided Setup**: Step-by-step configuration with helpful explanations
- ✅ **Input Validation**: Automatic validation with clear error messages
- 📊 **Scenario Comparison**: Compare different configurations side-by-side
- 💡 **Smart Recommendations**: Context-aware optimization suggestions
- 📖 **Built-in Help**: Comprehensive help system and best practices
- 🎨 **User-Friendly Interface**: Professional formatting with emojis and clear menus

**Features:**
- **Quick Calculation**: Fast estimates with saved configurations
- **Configure Settings**: Detailed setup for all parameters
- **Compare Scenarios**: Side-by-side comparison of different setups
- **View Recommendations**: Best practices and optimization tips
- **Help & Information**: Comprehensive documentation

### Command Line Interface

```bash
# Basic usage
python inference_calculator.py --model 7B --tokens 1000 --hardware GPU_16GB --deployment local

# API deployment
python inference_calculator.py --model 13B --tokens 500 --deployment api

# Enterprise usage
python inference_calculator.py --model GPT-4 --tokens 2000 --deployment api
```

### Programmatic Usage

```python
from inference_calculator import LLMInferenceCalculator

# Initialize calculator
calculator = LLMInferenceCalculator()

# Calculate inference estimates
result = calculator.calculate(
    model_size="7B",
    tokens=1000,
    batch_size=1,
    hardware_type="GPU_16GB",
    deployment_mode="local"
)

# Access results
print(f"Latency: {result.latency_seconds:.2f} seconds")
print(f"Memory: {result.memory_usage_gb:.2f} GB")
print(f"Cost: ${result.cost_per_request_usd:.6f}")
print(f"Compatible: {result.hardware_compatible}")
```

## 🎬 Interactive CLI Demo

See the interactive CLI in action:

```bash
python demo_interactive_cli.py
```

This demo shows all the features without requiring user input, including:
- Application header and menu system
- Model selection interface
- Token input guidance
- Hardware selection options
- Deployment mode selection
- Calculation results display
- Scenario comparison
- Recommendations system
- Help and information

## 📊 Usage Examples

### Example 1: Local Development Setup

```python
# Check if your hardware can run Mistral 7B
result = calculator.calculate(
    model_size="7B",
    tokens=1000,
    hardware_type="GPU_8GB",  # Your current GPU
    deployment_mode="local"
)

if result.hardware_compatible:
    print("✅ Your hardware can run Mistral 7B!")
    print(f"Expected latency: {result.latency_seconds:.1f} seconds")
else:
    print("❌ Hardware incompatible")
    print("Recommendations:", result.recommendations)
```

### Example 2: Cost Comparison

```python
# Compare costs across different models
models = ["7B", "13B", "GPT-4"]
tokens = 1000

for model in models:
    if model == "7B":
        result = calculator.calculate(model, tokens, hardware_type="GPU_16GB", deployment_mode="local")
    else:
        result = calculator.calculate(model, tokens, deployment_mode="api")
    
    print(f"{model}: ${result.cost_per_request_usd:.6f}")
```

### Example 3: Batch Processing Analysis

```python
# Analyze batch processing impact
tokens = 500
batch_sizes = [1, 4, 8, 16]

for batch_size in batch_sizes:
    result = calculator.calculate(
        model_size="7B",
        tokens=tokens,
        batch_size=batch_size,
        hardware_type="GPU_24GB",
        deployment_mode="local"
    )
    
    print(f"Batch {batch_size}: {result.latency_seconds:.1f}s, {result.memory_usage_gb:.1f}GB")
```

## 🔧 API Reference

### LLMInferenceCalculator Class

#### Constructor
```python
calculator = LLMInferenceCalculator()
```

#### Main Method: `calculate()`

```python
def calculate(
    model_size: str,           # "7B", "13B", or "GPT-4"
    tokens: int,               # Number of tokens (input + output)
    batch_size: int = 1,       # Batch size (default: 1)
    hardware_type: str = "GPU_8GB",  # Hardware configuration
    deployment_mode: str = "local"    # "local" or "api"
) -> CalculationResult
```

**Parameters:**
- `model_size`: Model to analyze ("7B", "13B", "GPT-4")
- `tokens`: Total tokens for the request
- `batch_size`: Number of requests to process together
- `hardware_type`: Hardware configuration (see supported types below)
- `deployment_mode`: "local" for self-hosted, "api" for cloud API

**Returns:** `CalculationResult` object with:
- `latency_seconds`: Estimated inference time
- `memory_usage_gb`: Memory requirements (local only)
- `cost_per_request_usd`: Cost per request
- `hardware_compatible`: Whether hardware supports the model
- `recommendations`: List of optimization suggestions

### Supported Hardware Types

| Hardware | VRAM | Use Case |
|----------|------|----------|
| `CPU` | 0GB | Development/testing only |
| `GPU_4GB` | 4GB | Small models only |
| `GPU_8GB` | 8GB | Limited compatibility |
| `GPU_12GB` | 12GB | Good for 7B models |
| `GPU_16GB` | 16GB | Recommended minimum |
| `GPU_24GB` | 24GB | Excellent performance |
| `GPU_32GB` | 32GB | Best performance |

## 📈 Scenario Analysis

The project includes comprehensive scenario analysis for three real-world use cases:

### Scenario 1: Local Development (Mistral 7B)
- **Use Case**: Individual developer or small team
- **Hardware**: RTX 4080 (16GB) recommended
- **Cost**: ~$0.000006-0.000022 per request
- **Performance**: 20-67 seconds for 1000 tokens

### Scenario 2: Production API (LangChain 13B)
- **Use Case**: Small to medium business
- **Cost**: ~$0.000300 per 1000 tokens
- **Performance**: 24 seconds per 1000 tokens
- **Scalability**: Excellent

### Scenario 3: Enterprise API (GPT-4)
- **Use Case**: High-quality enterprise applications
- **Cost**: ~$0.017 per 1000 tokens
- **Performance**: 21 seconds per 1000 tokens
- **Quality**: Best-in-class

## 🧪 Testing

### Run All Tests
```bash
python test_calculator.py
```

### Test Interactive CLI
```bash
python test_interactive_cli.py
```

### Run Scenario Analysis
```bash
python scenario_testing.py
```

### Manual Testing
```bash
# Test different configurations
python inference_calculator.py --model 7B --tokens 1000 --hardware GPU_16GB --deployment local
python inference_calculator.py --model 13B --tokens 500 --deployment api
python inference_calculator.py --model GPT-4 --tokens 2000 --deployment api
```

## 📁 Project Structure

```
W3D3-LLM-Inference-Calculator/
├── inference_calculator.py    # Main calculator implementation
├── interactive_cli.py         # Interactive CLI interface
├── demo_interactive_cli.py    # Interactive CLI demo
├── test_interactive_cli.py    # Interactive CLI tests
├── test_calculator.py         # Basic functionality tests
├── scenario_testing.py        # Automated scenario testing
├── scenario_analysis.md       # Detailed scenario analysis
├── research_notes.md          # Technical research and formulas
├── problem_statement.md       # Original project requirements
└── README.md                  # This file
```

## 🔍 Calculation Details

### Memory Usage
```
Total Memory = Model Weights + KV Cache + Activation Memory + Safety Margin (20%)
```

### Latency
**Local Deployment:**
```
Latency = Compute Time + Memory Overhead (10%)
```

**API Deployment:**
```
Latency = Network Latency (2s) + Processing Time
```

### Cost
**Local Deployment:**
```
Cost = (Hardware Cost + Electricity Cost) × Time Used
```

**API Deployment:**
```
Cost = Input Tokens × Input Price + Output Tokens × Output Price
```

## 🎯 Best Practices

### For Local Deployment
1. **Hardware Selection**: Use GPU with 16GB+ VRAM for 7B models
2. **Quantization**: Consider INT8/INT4 for memory efficiency
3. **Batch Processing**: Process multiple requests together
4. **Context Management**: Limit context length when possible

### For API Deployment
1. **Request Batching**: Group related requests
2. **Caching**: Cache common responses
3. **Rate Limiting**: Implement proper backoff strategies
4. **Monitoring**: Track costs and performance metrics

### Cost Optimization
1. **Model Selection**: Use smaller models for simple tasks
2. **Token Management**: Optimize prompts to reduce token usage
3. **Hybrid Approach**: Combine local and API deployments

## 🚨 Limitations

1. **Estimates Only**: Results are approximations based on typical hardware
2. **Hardware Variation**: Actual performance may vary by specific hardware
3. **API Pricing**: Prices may change over time
4. **Network Conditions**: API latency depends on network quality
5. **Model Updates**: Performance characteristics may change with model updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone and setup
git clone <repository-url>
cd W3D3-LLM-Inference-Calculator

# Run tests
python test_calculator.py
python scenario_testing.py

# Check code quality
python -m py_compile inference_calculator.py
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Mistral AI** for the Mistral 7B model
- **LangChain** for the 13B API service
- **OpenAI** for the GPT-4 API
- **Ollama** for local model deployment framework

## 📞 Support

For questions, issues, or contributions:
1. Check the [scenario_analysis.md](scenario_analysis.md) for detailed analysis
2. Review the [research_notes.md](research_notes.md) for technical details
3. Open an issue on GitHub for bugs or feature requests

---

**Note**: This calculator provides estimates for planning purposes. Actual performance and costs may vary based on specific hardware, network conditions, and model configurations.