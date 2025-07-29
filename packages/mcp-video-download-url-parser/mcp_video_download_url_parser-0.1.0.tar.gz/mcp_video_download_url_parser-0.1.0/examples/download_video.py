#!/usr/bin/env python3

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define server parameters
server_params = StdioServerParameters(
    command="uv",
    args=["run", "--directory", os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py"],
    env={"API_BASE_URL": "http://localhost:8000"}  # You can change this to your API URL
)


async def run():
    # Start the server as a subprocess and get stdio read/write functions
    async with stdio_client(server_params) as (read, write):
        # Create a client session to communicate with the server
        async with ClientSession(read, write) as session:
            # Initialize the connection with the server
            await session.initialize()
            
            # Get the video URL from command line or prompt the user
            if len(sys.argv) > 1:
                url = sys.argv[1]
            else:
                url = input("Enter video URL (or press Enter to use example): ")
                if not url:
                    url = "https://v.douyin.com/example/"  # Replace with an actual example URL
            
            # Get the output path
            output_path = input("Enter save path (or press Enter to use default path): ")
            if not output_path:
                # Use the downloads folder in the current directory
                output_path = os.path.join(os.getcwd(), "downloads")
                os.makedirs(output_path, exist_ok=True)
                print(f"Will use default path: {output_path}")
            
            # Whether to download with watermark
            watermark_input = input("Download with watermark? (y/n, default is n): ").lower()
            with_watermark = watermark_input == 'y'
            
            print(f"\nStarting video download: {url}")
            print(f"Save path: {output_path}")
            print(f"With watermark: {'Yes' if with_watermark else 'No'}")
            
            # Parse the video first to get information
            print("\n=== Parsing Video ===")
            video_info = await session.call_tool(
                "parser_url",
                arguments={"url": url}
            )
            print(f"Type: {video_info.get('type', 'unknown')}")
            if 'desc' in video_info:
                print(f"Description: {video_info['desc']}")
            if 'author' in video_info and isinstance(video_info['author'], dict):
                print(f"Author: {video_info['author'].get('nickname', 'unknown')}")
            
            # Now download the video
            print("\n=== Downloading Video ===")
            result = await session.call_tool(
                "download_video",
                arguments={
                    "url": url,
                    "output_path": output_path,
                    "with_watermark": with_watermark
                }
            )
            
            # Print the result
            if result.get('status') == 'success':
                print(f"\n✓ Video successfully downloaded to: {result.get('file_path', 'unknown path')}")
            else:
                print(f"\n✗ Download failed: {result.get('error', 'unknown error')}")
            
            print("\n=== Video Information ===")
            if 'video_info' in result:
                info = result['video_info']
                print(f"Platform: {info.get('platform', 'unknown')}")
                
                # Print statistics if available
                stats = info.get('statistics', {})
                if stats:
                    print(f"Likes: {stats.get('digg_count', 0)}")
                    print(f"Comments: {stats.get('comment_count', 0)}")
                    print(f"Shares: {stats.get('share_count', 0)}")
                
                # Show available download links
                print("\nDownload Links:")
                if info.get('video_url'):
                    print(f"No watermark: {info.get('video_url')}")
                if info.get('watermark_url'):
                    print(f"With watermark: {info.get('watermark_url')}")
                if info.get('music_url'):
                    print(f"Music: {info.get('music_url')}")


if __name__ == "__main__":
    # Run the async function
    asyncio.run(run()) 