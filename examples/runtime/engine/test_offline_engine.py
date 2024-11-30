"""
Usage:
python3 test_offline_engine.py --model-path /models/meta-llama/Llama-3.1-8B-Instruct --schedule-policy fcfs --chunked-prefill-size 1024 --enable-mixed-chunk --schedule-conservativeness 1.0 --disable-radix-cache --dataset-path=/datasets/random/dumped_requests.json
"""
import argparse
import dataclasses
import json
import sglang as sgl
from sglang.srt.server_args import ServerArgs
from typing import List, Tuple


def load_requests(dataset_path: str) -> List[Tuple[str, int, int]]:
    with open(dataset_path) as f:
        dataset = json.load(f)
    return dataset


def main(args):

    # Create an LLM.
    server_args = ServerArgs(
        model_path=args.model_path,
        schedule_policy=args.schedule_policy,
        chunked_prefill_size=args.chunked_prefill_size,
        enable_mixed_chunk=args.enable_mixed_chunk,
        disable_radix_cache=args.disable_radix_cache,
        schedule_conservativeness=args.schedule_conservativeness,
        log_level=args.log_level,
    )
    llm = sgl.Engine(**dataclasses.asdict(server_args))

    input_requests = load_requests(args.dataset_path)
    prompts = [request[0] for request in input_requests[: args.num_prompts]]

    sampling_params = {
        "temperature": 0.0,
        "max_new_tokens": args.max_new_tokens,
        "ignore_eos": not args.disable_ignore_eos,
    }

    outputs = llm.generate(prompts, sampling_params)
    for prompt, output in zip(prompts, outputs):
        print("===============================")
        print(f"Prompt: {prompt}\nGenerated text: {output['text']}")


# The __main__ condition is necessary here because we use "spawn" to create subprocesses
# Spawn starts a fresh program every time, if there is no __main__, it will run into infinite loop to keep spawning processes from sgl.Engine
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-path",
        type=str,
        required=True,
        help="The path to the dataset.",
    )
    parser.add_argument(
        "--num-prompts",
        type=int,
        default=10,
        help="Number of prompts to process. Default is 10.",
    )
    # Add arguments to the request.
    parser.add_argument(
        "--disable-ignore-eos",
        action="store_true",
        help="Disable ignoring EOS.",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=200,
        help="The maximum number of tokens to generate.",
    )

    # Add arguments to the server.
    parser.add_argument(
        "--model-path",
        type=str,
        default="meta-llama/Meta-Llama-3.1-8B-Instruct",
        help="The path to the model.",
    )
    parser.add_argument(
        "--schedule-policy",
        type=str,
        default=ServerArgs.schedule_policy,
        choices=["lpm", "random", "fcfs", "dfs-weight", "lof"],
        help="The scheduling policy of the requests.",
    )
    parser.add_argument(
        "--chunked-prefill-size",
        type=int,
        default=ServerArgs.chunked_prefill_size,
        help="The maximum number of tokens in a chunk for the chunked prefill. Setting this to -1 means disabling chunked prefill",
    )
    parser.add_argument(
        "--enable-mixed-chunk",
        action="store_true",
        help="Enabling mixing prefill and decode in a batch when using chunked prefill.",
    )
    parser.add_argument(
        "--disable-radix-cache",
        action="store_true",
        help="Disable radix cache.",
    )
    parser.add_argument(
        "--schedule-conservativeness",
        type=float,
        default=ServerArgs.schedule_conservativeness,
        help="How conservative the schedule policy is. A larger value means more conservative scheduling. Use a larger value if you see requests being retracted frequently.",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="DEBUG",
        help="The logging level of all loggers.",
    )
    args = parser.parse_args()
    main(args)
