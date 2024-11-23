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