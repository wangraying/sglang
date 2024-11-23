"""
Get Cache Stat

Usage:
python3 -m sglang.srt.mem_cache.cache_stat --url http://localhost:30000
"""

import requests

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get the status of the cache")
    parser.add_argument("--url", required=True, help="The URL of the cache server")
    args = parser.parse_args()

    response = requests.get(f"{args.url}/get_cache_stat")
    assert response.status_code == 200
    print(response.json())