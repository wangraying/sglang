import dataclasses
import sglang as sgl
from sglang.srt.server_args import ServerArgs


def main():
    # Sample prompts.
    prompts = [
        "Hello, my name is",
        "The president of the United States is",
        "The capital of France is",
        "The future of AI is",
        # "I love you",
        # "Beijing is the capital of",
        "The capital of China is",
        "Welcome to New"
    ]
    # Create a sampling params object.
    sampling_params = {"temperature": 0.8, "top_p": 0.95, "max_new_tokens": 5}

    # Create an LLM.
    server_args = ServerArgs(
        model_path="meta-llama/Meta-Llama-3.1-8B-Instruct",
        schedule_policy="fcfs",
        chunked_prefill_size=4,
        enable_mixed_chunk=True,
        disable_radix_cache=True,
    )
    llm = sgl.Engine(**dataclasses.asdict(server_args))

    outputs = llm.generate(prompts, sampling_params)
    # Print the outputs.
    for prompt, output in zip(prompts, outputs):
        print("===============================")
        print(f"Prompt: {prompt}\nGenerated text: {output['text']}")


# The __main__ condition is necessary here because we use "spawn" to create subprocesses
# Spawn starts a fresh program every time, if there is no __main__, it will run into infinite loop to keep spawning processes from sgl.Engine
if __name__ == "__main__":
    main()
