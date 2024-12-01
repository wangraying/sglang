# Benchmark Results

## Machine Setup

- **GPUs**: NVIDIA A100-SXM4-40GB
- **CPU Cores**: 96
- **CPU Memory**: 1.5 TB
- **Software**: SGLang v0.3.2.post2, PyTorch 2.4.0
- **CUDA Version**: 12.4

# Datasets Overview

The datasets for benchmarking are as follows, each with varying sizes and characteristics.

| Dataset Name           | Total Input Tokens | Total Output Tokens | Average System Prompt Length | Average Question Length |
|------------------------|--------------------|---------------------|------------------------------|-------------------------|
| Random-1000            | 3000000            | 300000              | -      | -   |
| Random-2000            | 6000000            | 600000              | -      | -   |
| Random-4000            | 12000000           | 1200000             | -      | -   |
| Random                 | 6020143            | 601639              | -      | -   |
| ShareGPT               | 6664740            | 5940589             | -      | -   |
| Generated-Shared-Prefix| 10948645           | 1048576             | 2137.7 | 535.3

- **Random-*n***: A dataset of 3000 sequences consisting of randomly generated tokens, each sequence maintaining a fixed input length of *n*.
- **Random**: A dataset of 3000 sequences consisting of randomly generated tokens, each sequence has a random input length, the random range ratio is 0.5.
- **ShareGPT**: A dataset of 30000 sequences derived from [ShareGPT dataset](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered).
- **Generated-Shared-Prefix**: A dataset of 4096 sequences organized in 128 groups, with sequences in each group starting with a common shared prefix.

## Varying Scheduling Policies

### Experiment Settings

- The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed at 16.
- Vary the schedule policies among LPM (Longest-Prefix-Match), FCFS (First-Come-First-Serve), DFS-Weight, Random, and LOF (Longest-Output-First).
- Default values are used for all other parameters, such as the prefilled chunk size is fixed to 8192 and mixed chunks are not enabled.

### Performance
<p style="text-align: center;">
<em>Table: Performance Metrics collected on Random-2000 dataset.</em>
</p>

| Scheduling Policy | Request Throughput (req/s) | Output Token Throughput (tok/s) | Mean End-to-End Latency (ms) | Mean TTFT (ms) | TP95 TTFT (ms) | TP99 TTFT (ms) | Mean ITL (ms) | TP95 ITL (ms) | TP99 ITL (ms) |
|-------------------|----------------------------|---------------------------------|------------------------------|----------------|----------------|----------------|---------------|---------------|---------------|
| LPM               | 4.2                        | 844.0                           | 267208.8                     | 255247.3       | 487127.6       | 511899.5       | 60.3          | 30.7          | 188.1         |
| Random            | 4.2                        | 843.0                           | 267239.5                     | 256162.9       | 568143.0       | 633107.3       | 56.0          | 30.9          | 190.9         |
| FCFS              | 4.2                        | 842.9                           | 266770.4                     | 254763.2       | 487114.0       | 508571.2       | 60.4          | 30.8          | 174.8         |
| DFS-Weight        | 4.1                        | 818.4                           | 282485.2                     | 271800.6       | 566219.4       | 569575.0       | 53.8          | 31.6          | 245.3         |
| LOF               | 4.2                        | 844.0                           | 267246.1                     | 255257.9       | 487189.1       | 508590.9       | 60.4          | 30.7          | 183.0         |

*Notes:*
1. "TTFT" stands for "Time to First Token".
2. "ITL" stands for "Inter-Token Latency".

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/output-throughput-vs-schedule-policy.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

**TTFT Latency:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-ttft-latency-vs-schedule-policy.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

For better visualization, normalize TTFT latency using the first value of each group.

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-ttft-latency-vs-schedule-policy-normalized.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

**ITL Latency:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-itl-latency-vs-schedule-policy.png" alt="P99 ITL Latency" style="width:80%; height:auto;"/>
</p>

### Observations

In this experiment, we have the following observations:
1. Random policy almost always performs the worst across all datasets, in terms of output throughput and TTFT.
2. FCFS and LPM outperform the others across all the datasets, in terms of output throughput and TTFT.
3. LOF policy performs poorly in terms of TTFT on datasets with random output length, i.e. ShareGPT and Random, which aligns with our intuition that LOF policy has no guarantee on TTFT.
4. By comparing the results of Random-*n* datasets, we could observe a trend of increasing TTFT but decresing ITL for longer sequences, when considering FCFS, LOF and LPM.

## Enabling and Disabling Radix Cache

### Experiment Settings

- The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed at 16.
- When the radix cache is disabled, the LPM and DFS-Weight policies are equivalent to the FCFS policy. Therefore, we only compare the FCFS, LOF and Random policies in this experiment.
- Default values are used for all other parameters, such as the prefilled chunk size is fixed to 8192 and mixed chunks are not enabled.

### Performance

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/output-throughput-w-wo-cache.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

**TTFT Latency (Normalized):**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-ttft-w-wo-cache-normalized.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

**ITL Latency:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-itl-w-wo-cache.png" alt="P99 ITL Latency" style="width:80%; height:auto;"/>
</p>

### Observations

In this experiment, we have the following observations:

1. For generated-shared-prefix dataset, enabling radix cache can significantly improve output throughput and decrease TTFT latency,
at the cost of increasing ITL latency, due to cache operations.
2. For other datasets, enabling cache may not result in obvious performance gains.
Usually, it could lead to more overhead, resulting in a slightly higher TTFT and reduced output throughput.
The only exception is the random-4000 dataset, which could see a small 1% improvement in some cases.

## Varying Varying Cache Sizes

### Experiment Settings

- The request rate is fixed at 16.
- The prefilled chunk size is set to 512, with mixed chunks enabled.
- Vary the cache size among 32K, 64K, and 128K.
- Default values are used for all other parameters, and the LPM policy is used as the scheduling policy.

### Performance

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/output-throughput-vs-cache-size.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

**TTFT Latency (Normalized):**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-ttft-vs-cache-size-normalized.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

**ITL Latency:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/p99-itl-vs-cache-size.png" alt="P99 ITL Latency" style="width:80%; height:auto;"/>
</p>

### Observations

Since the size of the radix cache is controlled by the `max_num_tokens` parameter of the server, increasing the cache size leads to a larger batch size. We observed higher output throughput, reduced TTFT, and ITL across all datasets as the cache size increases. However, for the Random-1000 and ShareGPT datasets, which have shorter context lenghs, the improvement saturates when the cache size is larger than 64K.

## Varying Prefilled Chunk Sizes

### Experiment Settings

- The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed at 16.
- Vary the prefilled chunk sizes among 256, 512, 1024 and 2048, with mixed chunks enabled.
- Use default values for others.

### LPM Policy

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/lpm-output-throughpt-vs-chunk-size.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

*Note*:
1. datapoints of `chunked_prefill_size,enable_mixed_chunk=(8192,False)`, which is the default setting, are added for better comparison.

**TTFT Latency:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/lpm-p99-ttft-vs-chunk-size.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

For better visualization, normalize TTFT latency using the first value of each group.

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/lpm-p99-ttft-vs-chunk-size-normalized.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

**ITL Latency:**

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/lpm-p99-itl-vs-chunk-size.png" alt="P99 ITL Latency" style="width:80%; height:auto;"/>
</p>

### FCFS Policy

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-output-throughpt-vs-chunk-size.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

**TTFT Latency:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-p99-ttft-vs-chunk-size.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

For better visualization, normalize TTFT latency using the first value of each group.

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-p99-ttft-vs-chunk-size-normalized.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

**ITL Latency:**

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-p99-itl-vs-chunk-size.png" alt="P99 ITL Latency" style="width:80%; height:auto;"/>
</p>