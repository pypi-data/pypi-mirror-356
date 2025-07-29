import argparse
from .server import mcp, download_video

def main():
    """MCP视频下载工具: 从抖音、TikTok等平台下载无水印视频"""
    parser = argparse.ArgumentParser(
        description="从抖音、TikTok等平台下载无水印视频的MCP服务"
    )
    parser.parse_args()
    mcp.run()

if __name__ == "__main__":
    main() 