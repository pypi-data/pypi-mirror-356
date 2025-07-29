"""
Example usage of EmbeddingServiceAsyncClient.

This example demonstrates how to use the async client to check the health of the embedding service,
request embeddings, and handle all possible errors.

Run this script with:
    python -m asyncio embed_client/example_async_usage.py --base-url http://localhost --port 8001

You can also set EMBED_CLIENT_BASE_URL and EMBED_CLIENT_PORT environment variables.
"""

import asyncio
import sys
import os
from embed_client.async_client import EmbeddingServiceAsyncClient

def get_params():
    base_url = None
    port = None
    for i, arg in enumerate(sys.argv):
        if arg in ("--base-url", "-b") and i + 1 < len(sys.argv):
            base_url = sys.argv[i + 1]
        if arg in ("--port", "-p") and i + 1 < len(sys.argv):
            port = sys.argv[i + 1]
    if not base_url:
        base_url = os.environ.get("EMBED_CLIENT_BASE_URL")
    if not port:
        port = os.environ.get("EMBED_CLIENT_PORT")
    if not base_url or not port:
        print("Error: base_url and port must be provided via --base-url/--port arguments or EMBED_CLIENT_BASE_URL/EMBED_CLIENT_PORT environment variables.")
        sys.exit(1)
        return None, None
    return base_url, int(port)

async def main():
    base_url, port = get_params()
    async with EmbeddingServiceAsyncClient(base_url=base_url, port=port) as client:
        # Check health
        health = await client.health()
        print("Service health:", health)

        # Request embeddings for a list of texts
        texts = ["hello world", "test embedding"]
        result = await client.cmd("embed", params={"texts": texts})
        
        if "error" in result:
            print(f"Error occurred: {result['error']}")
            if "lang" in result:
                print(f"Language: {result['lang']}")
            if "text" in result:
                print(f"Text: {result['text']}")
        else:
            vectors = result["result"]
            print(f"Embeddings for {len(texts)} texts:")
            for i, vec in enumerate(vectors):
                print(f"  Text: {texts[i]!r}\n  Vector: {vec[:5]}... (total {len(vec)} dims)")

        # Example: error handling for invalid command
        result = await client.cmd("health")
        print("Health check result:", result)

        # Example: error handling for empty command
        # result = await client.cmd("")
        # if "error" in result:
        #     print(f"Error for empty command: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main()) 