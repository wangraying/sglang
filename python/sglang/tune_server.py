"""
Set tunable parameters for the server.

Usage:
python3 -m sglang.tune_server --url http://localhost:30000 --schedule-policy lpm --chunked-prefill-size 512 --enable-mixed-chunk --schedule-conservativeness 1.0
"""

import argparse
import requests

from sglang.srt.server_args import ServerArgs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, default="http://localhost:30000")
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
        "--schedule-conservativeness",
        type=float,
        default=ServerArgs.schedule_conservativeness,
        help="How conservative the schedule policy is. A larger value means more conservative scheduling. Use a larger value if you see requests being retracted frequently.",
    )
    args = parser.parse_args()

    response = requests.post(
        args.url + "/set_tunnable_params",
        json={
            "schedule_policy": args.schedule_policy,
            "chunked_prefill_size": args.chunked_prefill_size,
            "enable_mixed_chunk": args.enable_mixed_chunk,
            "schedule_conservativeness": args.schedule_conservativeness,
        },
    )

    assert response.status_code == 200
    print(response.content)
