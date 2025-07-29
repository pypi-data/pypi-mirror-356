#!/usr/bin/env python3

import httpx
import asyncio
import json
import time
import os
import re
from urllib.parse import urlparse
from datetime import datetime

# 目标URL
URL = "https://api.snapany.com/v1/extract"

# 测试链接
TEST_URL = "https://v.douyin.com/4YCR59ZjYBk/"

# 下载目录
DOWNLOAD_PATH = "D:\\视频"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def download_file(url, filename):
    """下载文件到指定路径"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                filepath = os.path.join(DOWNLOAD_PATH, filename)
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"文件已保存到: {filepath}")
                return filepath
            else:
                print(f"下载失败，状态码: {response.status_code}")
                return None
    except Exception as e:
        print(f"下载文件时出错: {e}")
        return None

async def extract_video_url():
    """提取视频URL"""
    try:
        # 生成时间戳
        timestamp = int(time.time() * 1000)
        
        # 请求头，完全模拟浏览器
        headers = {
            "authority": "api.snapany.com",
            "method": "POST",
            "path": "/v1/extract",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh",
            "content-type": "application/json",
            "g-footer": "2cfa72328df209d07dcaee32a7ede261",  # 固定值
            "g-timestamp": str(timestamp),
            "origin": "https://snapany.com",
            "priority": "u=1, i",
            "referer": "https://snapany.com/zh/tiktok/",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
        }
        
        # 请求体
        data = {
            "link": TEST_URL
        }
        
        print(f"发送请求: {URL}")
        print(f"请求头: {json.dumps(headers, indent=2)}")
        print(f"请求体: {json.dumps(data, indent=2)}")
        
        # 发送请求
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, json=data, headers=headers)
            
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                # 提取视频URL和标题
                if "medias" in result and len(result["medias"]) > 0:
                    for media in result["medias"]:
                        if media.get("media_type") == "video" and "resource_url" in media:
                            video_url = media["resource_url"]
                            title = result.get("text", "未知标题")
                            
                            # 清理标题，用于文件名
                            clean_title = re.sub(r'[\\/*?:"<>|]', "_", title)
                            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                            filename = f"{clean_title}_{timestamp}.mp4"
                            
                            print(f"找到视频: {video_url}")
                            print(f"视频标题: {title}")
                            print(f"开始下载...")
                            
                            # 下载视频
                            await download_file(video_url, filename)
                            return
                    
                    print("未找到视频URL")
                else:
                    print("响应中没有媒体信息")
            else:
                print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"提取视频URL时出错: {e}")

async def main():
    await extract_video_url()

if __name__ == "__main__":
    asyncio.run(main()) 