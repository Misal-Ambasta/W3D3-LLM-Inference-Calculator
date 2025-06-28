# LLM Inference Calculator - Research Notes

## Phase 1: LLM Inference Fundamentals

### 1. Transformer Architecture Basics

**Core Components:**
- **Self-Attention Mechanism**: O(n²) complexity where n is sequence length
- **Feed-Forward Networks**: Linear transformations with activation functions
- **Layer Normalization**: Stabilizes training and inference
- **Residual Connections**: Helps with gradient flow

**Computational Complexity:**
- **Attention**: O(n² × d) where d is embedding dimension
- **Feed-Forward**: O(n × d²)
- **Total per layer**: O(n² × d + n × d²)

### 2. Memory Requirements

**Model Weights:**
- **FP32 (32-bit float)**: 4 bytes per parameter
- **FP16 (16-bit float)**: 2 bytes per parameter
- **INT8 (8-bit integer)**: 1 byte per parameter
- **INT4 (4-bit integer)**: 0.5 bytes per parameter

**KV Cache Memory:**
- **Formula**: 2 × layers × heads × head_dim × sequence_length × batch_size × bytes_per_token
- **Typical values**: 2-4GB for 7B models with 2048 context length

**Total Memory = Model Weights + KV Cache + Activation Memory**

### 3. Latency Factors

**Compute Bound:**
- **FLOPS**: Floating point operations per second
- **GPU Compute**: Tensor cores, CUDA cores
- **CPU Compute**: Single-threaded vs multi-threaded

**Memory Bound:**
- **Memory Bandwidth**: GB/s transfer rate
- **VRAM Size**: GPU memory capacity
- **RAM Speed**: System memory bandwidth

**Network Bound (API):**
- **Latency**: Round-trip time to API server
- **Throughput**: Requests per second
- **Rate Limiting**: API provider constraints

## Phase 2: Target Model Specifications

### 1. Mistral 7B (Local via Ollama)

**Architecture:**
- **Parameters**: 7.3 billion
- **Layers**: 32
- **Heads**: 32
- **Head Dimension**: 128
- **Context Length**: 8,192 tokens
- **Vocabulary**: 32,000 tokens

**Memory Requirements:**
- **FP16**: ~14.6 GB
- **INT8**: ~7.3 GB
- **INT4**: ~3.65 GB
- **KV Cache**: ~2-4 GB (depending on sequence length)

**Performance (Ollama):**
- **CPU**: 1-5 tokens/second
- **GPU (8GB)**: 10-20 tokens/second
- **GPU (16GB+)**: 20-40 tokens/second

**Hardware Compatibility:**
- **Minimum**: 8GB RAM (CPU only)
- **Recommended**: 16GB+ RAM with GPU
- **Optimal**: 24GB+ VRAM for full precision

### 2. LangChain 13B API

**Architecture:**
- **Parameters**: ~13 billion (exact specs vary by provider)
- **Context Length**: 4,096-8,192 tokens
- **API Endpoint**: Cloud-based

**Pricing (Estimated):**
- **Input tokens**: $0.0001-0.0005 per 1K tokens
- **Output tokens**: $0.0002-0.001 per 1K tokens
- **Base cost**: $0.01-0.05 per request

**Performance:**
- **Latency**: 1-5 seconds per request
- **Throughput**: 10-100 requests per minute
- **Availability**: 99.9% uptime

### 3. GPT-4 (OpenAI API)

**Architecture:**
- **Parameters**: ~1.76 trillion (estimated)
- **Context Length**: 8,192 tokens (GPT-4), 128K tokens (GPT-4 Turbo)
- **API Endpoint**: OpenAI cloud infrastructure

**Pricing (Current as of 2024):**
- **GPT-4 (8K context)**:
  - Input: $0.03 per 1K tokens
  - Output: $0.06 per 1K tokens
- **GPT-4 Turbo (128K context)**:
  - Input: $0.01 per 1K tokens
  - Output: $0.03 per 1K tokens

**Performance:**
- **Latency**: 2-10 seconds per request
- **Throughput**: 3-10 requests per minute (rate limited)
- **Availability**: 99.9% uptime

## Phase 3: Hardware Considerations

### CPU vs GPU Performance

**CPU Inference:**
- **Pros**: No VRAM requirements, universal compatibility
- **Cons**: 10-50x slower than GPU, limited by single-thread performance
- **Best for**: Small models (<3B), development/testing

**GPU Inference:**
- **Pros**: Parallel processing, specialized tensor operations
- **Cons**: VRAM requirements, cost
- **Best for**: Production inference, larger models

### VRAM Requirements by Model Size

| Model Size | FP16 (GB) | INT8 (GB) | INT4 (GB) |
|------------|-----------|-----------|-----------|
| 3B         | 6         | 3         | 1.5       |
| 7B         | 14        | 7         | 3.5       |
| 13B        | 26        | 13        | 6.5       |
| 30B        | 60        | 30        | 15        |
| 70B        | 140       | 70        | 35        |

### Cloud Instance Pricing

**AWS EC2 (Monthly):**
- **g4dn.xlarge**: $0.526/hour = ~$380/month (16GB VRAM)
- **g5.xlarge**: $1.006/hour = ~$725/month (24GB VRAM)
- **p3.2xlarge**: $3.06/hour = ~$2,200/month (16GB VRAM)

**Google Cloud:**
- **n1-standard-4 + T4**: ~$200/month (16GB VRAM)
- **n1-standard-8 + V100**: ~$1,200/month (16GB VRAM)

## Phase 4: Calculation Formulas

### Memory Usage Calculation

```
Model Memory = Parameters × Bytes per Parameter
KV Cache = 2 × Layers × Heads × Head Dim × Seq Length × Batch Size × Bytes per Token
Total Memory = Model Memory + KV Cache + Safety Margin (20%)
```

### Latency Calculation

**Local Deployment:**
```
Compute Time = (FLOPS required) / (Hardware FLOPS)
Memory Time = (Memory Access) / (Memory Bandwidth)
Total Latency = Compute Time + Memory Time + Overhead
```

**API Deployment:**
```
Network Latency = Round-trip time to API server
Processing Time = Server-side inference time
Total Latency = Network Latency + Processing Time
```

### Cost Calculation

**Local Deployment:**
```
Hardware Cost = (Hardware Price / Lifetime) × Time Used
Electricity Cost = Power Consumption × Electricity Rate × Time Used
Total Cost = Hardware Cost + Electricity Cost
```

**API Deployment:**
```
Input Cost = Input Tokens × Input Price per Token
Output Cost = Output Tokens × Output Price per Token
Total Cost = Input Cost + Output Cost
```

## Research Sources

1. **Mistral AI Documentation**: https://mistral.ai/
2. **Ollama Performance Benchmarks**: https://ollama.ai/
3. **OpenAI Pricing**: https://openai.com/pricing
4. **LangChain Documentation**: https://python.langchain.com/
5. **Transformer Architecture**: "Attention Is All You Need" paper
6. **Hardware Benchmarks**: Various GPU and CPU benchmarks

## Assumptions and Limitations

1. **Performance estimates** are approximate and vary by hardware
2. **Pricing** is current as of research date but subject to change
3. **Memory requirements** include safety margins for stability
4. **Latency calculations** assume optimal conditions
5. **Cost calculations** exclude setup and maintenance costs

## Next Steps

1. Implement these formulas in the calculator
2. Add hardware compatibility checking
3. Create scenario testing framework
4. Validate calculations against real-world benchmarks 