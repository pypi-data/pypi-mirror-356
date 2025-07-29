#!/usr/bin/env python3

import asyncio
import os
from main import extract_video_from_snapany_playwright

# 测试链接
TEST_URL = "https://v.douyin.com/4YCR59ZjYBk/"

# 下载目录
OUTPUT_PATH = "D:\\视频"
os.makedirs(OUTPUT_PATH, exist_ok=True)

async def main():
    print(f"开始提取视频: {TEST_URL}")
    
    # 使用Playwright提取视频
    result = await extract_video_from_snapany_playwright(TEST_URL)
    
    print(f"提取结果: {result}")
    
    if result and 'error' not in result:
        print("视频提取成功!")
        
        # 检查是否有媒体数据
        if 'medias' in result and isinstance(result['medias'], list):
            for media in result['medias']:
                if media.get('media_type') == 'video' and 'resource_url' in media:
                    print(f"视频URL: {media['resource_url'][:100]}...")
        
        # 检查标题
        if 'text' in result:
            print(f"视频标题: {result['text']}")
    else:
        print(f"视频提取失败: {result.get('error', '未知错误')}")

if __name__ == "__main__":
    asyncio.run(main()) 