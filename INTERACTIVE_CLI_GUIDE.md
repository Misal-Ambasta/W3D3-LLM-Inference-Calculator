# Interactive CLI User Guide

## 🎯 Getting Started

The Interactive CLI provides a user-friendly way to calculate LLM inference metrics without needing to remember command-line arguments or understand technical details.

### Starting the Interactive CLI

```bash
python interactive_cli.py
```

You'll see a welcome screen with the main menu:

```
============================================================
🤖 LLM Inference Calculator - Interactive Mode
============================================================
Calculate costs, latency, and memory usage for LLM inference
============================================================

📋 Main Menu:
1. 🚀 Quick Calculation
2. ⚙️  Configure Settings
3. 📊 Compare Scenarios
4. 💡 View Recommendations
5. 📖 Help & Information
6. 🚪 Exit
----------------------------------------
```

## 🚀 Quick Calculation

**Best for**: Getting fast estimates with minimal setup

1. Select **"1. 🚀 Quick Calculation"**
2. If you have a saved configuration, you can use it or create a new one
3. Follow the guided setup process
4. View your results immediately

**Example Flow**:
```
🚀 Quick Calculation Mode
Let's get your inference estimates quickly!
----------------------------------------
✅ Using saved configuration

📋 Current Configuration:
----------------------------------------
Model: 7B
Tokens: 1000
Batch Size: 1
Deployment: local
Hardware: GPU_16GB
----------------------------------------

Use saved configuration? (y/n): y
```

## ⚙️ Configure Settings

**Best for**: Detailed setup and customization

This option guides you through each setting step-by-step:

### 1. Model Selection
```
🤖 Select Model Size:
1. Mistral 7B (Local via Ollama)
2. LangChain 13B (API)
3. GPT-4 (OpenAI API)
----------------------------------------
Select model (1-3): 1
✅ Selected: 7B
```

### 2. Token Count
```
📝 Token Count:
Enter the total number of tokens (input + output)
Typical values:
  • Short response: 100-500 tokens
  • Medium response: 500-1000 tokens
  • Long response: 1000-2000 tokens
  • Document analysis: 2000+ tokens
----------------------------------------
Enter token count: 1000
✅ Tokens: 1000
```

### 3. Batch Size
```
📦 Batch Size:
Number of requests to process together
• 1: Single request (most common)
• 2-4: Small batch (good for efficiency)
• 5+: Large batch (may cause memory issues)
----------------------------------------
Enter batch size (default: 1): 
✅ Batch size: 1 (default)
```

### 4. Deployment Mode
```
🌐 Select Deployment Mode:
1. Local (Self-hosted - requires hardware)
2. API (Cloud-based - no hardware needed)
----------------------------------------
Select deployment mode (1-2): 1
✅ Selected: local
```

### 5. Hardware Selection (Local Only)
```
💻 Select Hardware (for local deployment):
1. CPU (Development/testing only - very slow)
2. GPU 4GB (Small models only)
3. GPU 8GB (Limited compatibility)
4. GPU 12GB (Good for 7B models)
5. GPU 16GB (Recommended minimum)
6. GPU 24GB (Excellent performance)
7. GPU 32GB (Best performance)
----------------------------------------
Select hardware (1-7): 5
✅ Selected: GPU_16GB
```

## 📊 Compare Scenarios

**Best for**: Understanding different deployment options

This feature automatically compares three common scenarios:

1. **Development (Mistral 7B Local)**: For individual developers
2. **Production API (LangChain 13B)**: For small to medium businesses
3. **Enterprise (GPT-4 API)**: For high-quality enterprise applications

**Sample Output**:
```
====================================
📊 SCENARIO COMPARISON (1000 tokens)
====================================
Scenario                         Latency (s)  Memory (GB)  Cost/Req ($)  Cost/1K ($)  
--------------------------------------------------------------------------------
Development (Mistral 7B Local)   28.57        17.52        0.000009      0.000009     
Production API (LangChain 13B)   24.00        N/A          0.000150      0.000150     
Enterprise (GPT-4 API)           21.00        N/A          0.017000      0.017000     
====================================

💡 Key Insights:
• Local deployment has lowest cost but requires hardware investment
• API deployment offers convenience but ongoing costs
• GPT-4 provides best quality but highest cost
• Consider your use case and budget when choosing
```

## 💡 View Recommendations

**Best for**: Learning best practices and optimization tips

Provides context-aware recommendations based on your configuration:

### For Development & Testing:
- Use Mistral 7B locally for cost-free development
- Minimum hardware: RTX 4080 (16GB VRAM)
- Consider quantization for memory efficiency

### For Production (Low-Medium Volume):
- Use LangChain 13B API for good balance of cost/quality
- Implement request caching to reduce costs
- Monitor usage and set rate limits

### For Enterprise (High Quality Required):
- Use GPT-4 API for best-in-class performance
- Implement proper error handling and retries
- Consider hybrid approach for cost optimization

### Cost Optimization Tips:
- Optimize prompts to reduce token usage
- Use smaller models for simple tasks
- Implement streaming for long outputs
- Batch requests when possible

### Performance Tips:
- Use appropriate hardware for local deployment
- Implement proper caching strategies
- Monitor latency and optimize bottlenecks
- Consider model quantization for efficiency

## 📖 Help & Information

**Best for**: Understanding the calculator and its capabilities

Provides comprehensive information about:

### About the Calculator:
- What the tool does and how it helps
- What metrics it calculates
- How to interpret results

### Supported Models:
- **Mistral 7B**: Local deployment via Ollama
- **LangChain 13B**: API-based deployment
- **GPT-4**: OpenAI API deployment

### Hardware Options:
- **CPU**: Development/testing only (very slow)
- **GPU 4GB-32GB**: Various performance levels
- Higher VRAM = better performance

### Deployment Modes:
- **Local**: Self-hosted (requires hardware)
- **API**: Cloud-based (no hardware needed)

### Usage Tips:
- Start with Quick Calculation for simple estimates
- Use Configure Settings for detailed setup
- Compare Scenarios to see different options
- Check Recommendations for optimization tips

## 📊 Understanding Results

When you perform a calculation, you'll see results like this:

```
============================================================
📊 CALCULATION RESULTS
============================================================
Model: 7B
Tokens: 1,000
Batch Size: 1
Deployment: local
Hardware: GPU_16GB

----------------------------------------
📈 Performance Metrics:
  ⏱️  Latency: 28.57 seconds
  💾 Memory Usage: 17.52 GB
  💰 Cost per Request: $0.000009
  📊 Cost per 1K tokens: $0.000009
  🔧 Hardware: ✅ Compatible

💡 Recommendations:
  1. Hardware compatible - good choice for 7B model
  2. Consider quantization for memory efficiency
============================================================
```

### What Each Metric Means:

- **Latency**: How long inference takes (lower is better)
- **Memory Usage**: How much VRAM is needed (local only)
- **Cost per Request**: Price for this specific request
- **Cost per 1K tokens**: Normalized cost for comparison
- **Hardware Compatibility**: Whether your hardware can run the model

## 🎯 Tips for Best Results

### 1. Start Simple
- Use Quick Calculation for your first estimates
- Start with common configurations (1000 tokens, batch size 1)

### 2. Understand Your Use Case
- **Development**: Use local deployment for cost-free testing
- **Production**: Consider API deployment for reliability
- **Enterprise**: Use GPT-4 for highest quality

### 3. Consider Hardware Constraints
- Check hardware compatibility before local deployment
- Higher VRAM = better performance and compatibility
- CPU is only for testing, not production

### 4. Optimize for Your Needs
- Use smaller models for simple tasks
- Optimize prompts to reduce token usage
- Consider batch processing for efficiency

### 5. Monitor and Adjust
- Track actual performance vs. estimates
- Adjust configurations based on real-world usage
- Consider hybrid approaches for cost optimization

## 🚨 Troubleshooting

### Common Issues:

**"Hardware incompatible"**
- Solution: Choose hardware with more VRAM or use API deployment

**"Very slow performance"**
- Solution: Use GPU instead of CPU, or consider API deployment

**"High costs"**
- Solution: Use smaller models, optimize prompts, or use local deployment

**"Memory issues"**
- Solution: Reduce batch size, use quantization, or choose hardware with more VRAM

### Getting Help:

1. Use the built-in Help & Information section
2. Check the recommendations for your specific configuration
3. Compare different scenarios to find the best option
4. Review the main README.md for technical details

## 🎉 Next Steps

After using the Interactive CLI:

1. **Save your configuration**: The CLI remembers your last setup
2. **Try different scenarios**: Use Compare Scenarios to explore options
3. **Check recommendations**: Review optimization tips for your use case
4. **Read the documentation**: Check README.md for technical details
5. **Run automated tests**: Use the test scripts to verify calculations

The Interactive CLI makes it easy to get started with LLM inference planning. Whether you're a beginner or an expert, it provides the guidance and information you need to make informed decisions about your LLM deployment strategy. 