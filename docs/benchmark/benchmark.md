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
|------------------------|--------------------|-------------------|------------------------------|-------------------------|
| Random-1000            | 3,000,000            | 300,000           | -      | -   |
| Random-2000            | 6,000,000            | 600,000           | -      | -   |
| Random-4000            | 12,000,000           | 1,200,000         | -      | -   |
| Random                 | 6,020,143            | 601,639           | -      | -   |
| ShareGPT               | 6,664,740            | 5,940,589         | -      | -   |
| Generated-Shared-Prefix| 10,948,645           | 1,048,576         | 2137.7 | 535.3

- **Random-*n***: A dataset of 3000 sequences consisting of randomly generated tokens, each sequence maintaining a fixed input length of *n*.
- **Random**: A dataset of 3000 sequences consisting of randomly generated tokens, each sequence has a random input length, the random range ratio is 0.5.
- **ShareGPT**: A dataset of 30000 sequences derived from [ShareGPT dataset](https://huggingface.co/datasets/anon8231489123/ShareGPT_Vicuna_unfiltered).
- **Generated-Shared-Prefix**: A dataset of 4096 sequences organized in 128 groups, with sequences in each group starting with a common shared prefix.

## Varying Scheduling Policies

### Experiment Settings

- The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed at 16.
- Vary the schedule policies among LPM (Longest-Prefix-Match), FCFS (First-Come-First-Serve), DFS-Weight, Random, and LOF (Longest-Output-First).
- Default values are used for all other parameters, such as the prefilled chunk size is fixed to 8192 and mixed-running is not enabled.

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

1. Random policy performs worse across all datasets, in terms of output throughput and TTFT. It is especially worse on
Generated-Shared-Prefix dataset, since it fails to exploit the characteristic of sharing common prefix among
consecutive requests in each sequence group, but it still needs to maintain the prefix structure in the radix tree.
2. FCFS and LPM policies outperform the others across all the datasets, in terms of output throughput and TTFT.
3. LOF policy performs poorly in terms of TTFT on datasets with random length, i.e. Random. This is expected since LOF
policy offers no guarantee on TTFT.
4. By comparing the results of Random-*n* datasets, we could observe a trend of increasing TTFT but decreasing ITL as
the number of tokens increases, when considering FCFS, LOF and LPM.
5. For ShareGPT dataset, the performance metrics of different schedule policies don't differ much.

## Enabling and Disabling Radix Cache

### Experiment Settings

- The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed at 16.
- When the radix cache is disabled, LPM and DFS-Weight policies are equivalent to FCFS policy. Therefore, we only compare FCFS, LOF and Random policies in this experiment.
- Default values are used for all other parameters, such as the prefilled chunk size is fixed to 8192 and mixed-running is not enabled.

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

1. For Generated-Shared-Prefix dataset, enabling radix cache can significantly improve output throughput and decrease
TTFT latency. For other datasets, this performance improvement may not be as obvious. This is expected since enabling
radix cache allows for sharing common prefixes among requests. For Generated-Shared-Prefix dataset, consecutive
requests within each sequence group share a long common system prompt, and this will greatly decrease computation
when radix cache is enabled.
2. Enabling radix cache could also lead to a higher ITL, we attribute it to the overhead of maintaining the prefix
structure in the radix tree. (Peculiar datapoint on dataset Random-4000, with random policy)
3. Similar trends are observed when using chunked prefills with mixed-running enabled. We omit the details for brevity.
4. We conclude that for datasets that has a characteristic of sharing common prefix among requests, radix cache is
preferable to boost performance, otherwise, a simple key-value based chunk cache, i.e. the implentation when radix cache
is disabled, is sufficient to achieve good performance.

## Varying Varying Cache Sizes

### Experiment Settings

- The request rate is fixed at 16.
- The prefilled chunk size is set to 512, with mixed-running enabled.
- Vary the cache sizes among 32K, 64K, and 128K.
- Default values are used for all other parameters, and LPM policy is used for scheduling.

### Performance

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/output-throughput-vs-cache-size.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

**Mean End-to-End Latency (Normalized):**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/mean-e2e-latency-vs-cache-size-normalized.png" alt="Mean End-to-End Latency" style="width:80%; height:auto;"/>
</p>

### Observations

Since the size of the radix cache is determined by the `max_num_tokens` parameter of the server, increasing the cache size means increasing batch size, which almost always leads to a higher throughput and reduced end-to-end latency. However, for the Random-1000 and ShareGPT datasets, these performance gains saturate after the cache size exceeds 64K.

## Varying Prefilled Chunk Sizes

### Experiment Settings

- The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed at 16.
- Vary the prefilled chunk sizes among 256, 512, 1024, 2048 and 4096, with mixed-running enabled.
- Performance is compared with the radix cache both enabled and disabled. When running with radix cache disabled, a [patch](https://github.com/sgl-project/sglang/pull/2290) is applied to the original branch.
- Default values are used for all other parameters, and FCFS policy is used for scheduling.

### Performance

**Output Throughput:**
<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-output-throughput-vs-chunk-size.png" alt="Output Throughput" style="width:80%; height:auto;"/>
</p>

**TTFT Latency (Normalized):**

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-p99-ttft-vs-chunk-size-normalized.png" alt="P99 TTFT Latency" style="width:80%; height:auto;"/>
</p>

**ITL Latency:**

<p align="center">
<img src="https://raw.githubusercontent.com/wangraying/sglang/refs/heads/v0.3.5.post2-dev/docs/images/fcfs-p99-itl-vs-chunk-size.png" alt="P99 ITL Latency" style="width:80%; height:auto;"/>
</p>

### Observations
