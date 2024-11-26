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

## Performance Metrics for Different Scheduling Policies

| Scheduling Policy | Request Throughput (req/s) | Output Token Throughput (tok/s) | Mean End-to-End Latency (ms) | Mean TTFT (ms) | TP95 TTFT (ms) | TP99 TTFT (ms) | Mean ITL (ms) | TP95 ITL (ms) | TP99 ITL (ms) |
| ------------------|----------------------------|---------------------------------|------------------------------|----------------|----------------|----------------|---------------|---------------|---------------|
| LPM               | 4.2                        | 844.0                           | 267208.8                     | 255247.3       | 487127.6       | 511899.5       | 60.3          | 30.7          | 188.1         |
| Random            | 4.2                        | 843.0                           | 267239.5                     | 256162.9       | 568143.0       | 633107.3       | 56.0          | 30.9          | 190.9         |
| FCFS              | 4.2                        | 842.9                           | 266770.4                     | 254763.2       | 487114.0       | 508571.2       | 60.4          | 30.8          | 174.8         |
| DFS-Weight        | 4.1                        | 818.4                           | 282485.2                     | 271800.6       | 566219.4       | 569575.0       | 53.8          | 31.6          | 245.3         |
| LOF               | 4.2                        | 844.0                           | 267246.1                     | 255257.9       | 487189.1       | 508590.9       | 60.4          | 30.7          | 183.0         |
| FCFS w/o cache    | 4.3                        | 850.6                           | 264140.7                     | 254602.9       | 489061.3       | 510224.5       | 48.1          | 30.6          | 36.4          |
| Random w/o cache  | 4.3                        | 850.2                           | 264214.9                     | 254663.1       | 565340.6       | 628747.4       | 48.5          | 30.7          | 37.8          |

*Notes:*
1. "TTFT" stands for "Time to First Token". When the radix cache is disabled, the LPM and DFS-Weight policies perform equivalently to the Random policy.
2. "ITL" stands for "Inter-Token Latency".
3. The data collected in this figure are conducted on *Random-2000* dataset.
4. The maximum number of tokens (corresponding to the cache size) is set to 128K, and the request rate is fixed to 16.

<p align="center">
<img src="https://github.com/wangraying/sglang/blob/v0.3.5.post2-dev/docs/images/output-throughput-vs-schedule-policy.png?raw=true" alt="Output Throughput"/>
</p>

<p align="center">
<img src="https://github.com/wangraying/sglang/blob/v0.3.5.post2-dev/docs/images/p99-ttft-latency-vs-schedule-policy.png?raw=true" alt="P99 TTFT Latency"/>
</p>

<p align="center">
<img src="https://github.com/wangraying/sglang/blob/v0.3.5.post2-dev/docs/images/p99-itl-latency-vs-schedule-policy.png?raw=true" alt="P99 ITL Latency"/>
</p>