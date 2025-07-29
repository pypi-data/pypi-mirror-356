#!/usr/bin/env python3

import asyncio
import os
import sys
import json
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
            
            # Get the user profile URL from command line or prompt the user
            if len(sys.argv) > 1:
                user_url = sys.argv[1]
            else:
                user_url = input("Enter user profile URL (or press Enter to use example): ")
                if not user_url:
                    user_url = "https://www.douyin.com/user/example"  # Replace with an actual example URL
            
            # Get max videos count to fetch
            try:
                max_videos = int(input("Enter maximum videos to fetch (default 10): ") or 10)
            except ValueError:
                max_videos = 10
                print("Invalid input, using default value of 10")
            
            print(f"\nFetching videos for user: {user_url}")
            print(f"Maximum videos to fetch: {max_videos}")
            
            # Get user's video list
            print("\n=== Getting User Videos ===")
            result = await session.call_tool(
                "get_user_videos",
                arguments={
                    "user_url": user_url,
                    "max_videos": max_videos
                }
            )
            
            # Handle error
            if 'error' in result:
                print(f"Error: {result['error']}")
                return
            
            # Print user info
            if 'user_info' in result and result['user_info']:
                user_info = result['user_info']
                print("\n=== User Information ===")
                print(f"Nickname: {user_info.get('nickname', 'Unknown')}")
                print(f"Signature: {user_info.get('signature', 'None')}")
                print(f"UID: {user_info.get('uid', 'Unknown')}")
                print(f"Following count: {user_info.get('following_count', 0)}")
                print(f"Follower count: {user_info.get('follower_count', 0)}")
            
            # Print videos
            if 'videos' in result and result['videos']:
                videos = result['videos']
                print(f"\n=== Videos ({len(videos)}) ===")
                
                for i, video in enumerate(videos, 1):
                    print(f"\nVideo {i}:")
                    print(f"Description: {video.get('desc', 'No description')}")
                    
                    # Get statistics
                    stats = video.get('statistics', {})
                    print(f"Likes: {stats.get('digg_count', 0)}")
                    print(f"Comments: {stats.get('comment_count', 0)}")
                    print(f"Shares: {stats.get('share_count', 0)}")
                    
                    # Get video URLs
                    print("Video URL: " + video.get('share_url', 'Unknown'))
                
                # Check if more videos are available
                if result.get('has_more', False):
                    print(f"\n✓ More videos are available, max_cursor: {result.get('max_cursor', 0)}")
            else:
                print("\nNo videos found!")


if __name__ == "__main__":
    # Run the async function
    asyncio.run(run()) 