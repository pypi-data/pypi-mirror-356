#!/usr/bin/env python3

import asyncio
import os
import sys
from main import extract_video_from_snapany_playwright, download_file

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
        video_url = None
        title = "未命名视频"
        
        if 'medias' in result and isinstance(result['medias'], list):
            for media in result['medias']:
                if media.get('media_type') == 'video' and 'resource_url' in media:
                    video_url = media['resource_url']
                    print(f"视频URL: {video_url[:100]}...")
                    break
        
        # 检查标题
        if 'text' in result:
            title = result['text']
            print(f"视频标题: {title}")
        
        # 下载视频
        if video_url:
            import re
            from datetime import datetime
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{title}_{timestamp}.mp4"
            # 清理文件名，移除不安全字符
            filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
            file_path = os.path.join(OUTPUT_PATH, filename)
            
            print(f"开始下载视频到: {file_path}")
            success = await download_file(video_url, file_path)
            
            if success:
                print(f"视频下载成功: {file_path}")
            else:
                print("视频下载失败")
        else:
            print("未找到视频URL")
    else:
        print(f"视频提取失败: {result.get('error', '未知错误')}")

if __name__ == "__main__":
    # 如果有命令行参数，使用第一个参数作为URL
    if len(sys.argv) > 1:
        TEST_URL = sys.argv[1]
    
    asyncio.run(main()) 