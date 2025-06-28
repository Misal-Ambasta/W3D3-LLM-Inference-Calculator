# LLM Inference Calculator

**Q: 1**

Build a calculator that estimates LLM inference costs, latency, and memory usage.

## Tasks

1. **Research**: Document LLM inference basics and compare 3 models (7B, 13B, GPT-4)
2. **Build Calculator**: Accept model size, tokens, hardware → output latency, memory, cost
3. **Analyze Scenarios**: Test 3 use cases and provide recommendations

## Inputs/Outputs

### Inputs
- `model_size`
- `tokens`
- `batch_size`
- `hardware_type`
- `deployment_mode`

### Outputs
- Latency
- Memory usage
- Cost per request
- Hardware compatibility

## Deliverables
- inference_calculator.py
- research_notes.md
- sceanrio_analysis.md
- README.md

## Reference
- https://llm-inference-calculator-rki02.kinsta.page/
- https://apxml.com/tools/vram-calculator
