#!/usr/bin/env python3

import asyncio
import os
import re
import json
import logging
import time
from urllib.parse import urlparse
from datetime import datetime
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 测试链接
TEST_URL = "https://v.douyin.com/4YCR59ZjYBk/"
SNAPANY_API_URL = "https://api.snapany.com/v1/extract"
SNAPANY_WEBSITE_URL = "https://snapany.com/zh/tiktok"

# 下载目录
OUTPUT_PATH = "D:\\视频"
os.makedirs(OUTPUT_PATH, exist_ok=True)

async def extract_video_from_snapany_playwright(url):
    """使用Playwright模拟浏览器访问SnapAny网站提取视频URL"""
    try:
        logger.info(f"使用Playwright提取视频: {url}")
        
        # 清理URL，确保只包含实际链接
        clean_url = url.strip()
        # 如果URL包含在文本中，尝试提取它
        url_match = re.search(r'https?://[^\s]+', clean_url)
        if url_match:
            clean_url = url_match.group(0)
            
        logger.info(f"提取的URL: {clean_url}")
        
        # 使用Playwright模拟浏览器
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
            )
            
            # 创建新页面
            page = await context.new_page()
            
            # 监听网络请求
            api_response_data = None
            
            async def handle_response(response):
                nonlocal api_response_data
                if response.url == SNAPANY_API_URL and response.status == 200:
                    try:
                        api_response_data = await response.json()
                        logger.info(f"捕获到API响应: {json.dumps(api_response_data, ensure_ascii=False)[:200]}...")
                    except:
                        logger.warning("无法解析API响应为JSON")
            
            # 添加响应监听器
            page.on("response", handle_response)
            
            try:
                # 访问SnapAny网站
                logger.info(f"访问SnapAny网站: {SNAPANY_WEBSITE_URL}")
                try:
                    # 增加超时时间，使用domcontentloaded等待策略而不是networkidle
                    await page.goto(SNAPANY_WEBSITE_URL, wait_until="domcontentloaded", timeout=60000)
                    logger.info("页面基本加载完成")
                    
                    # 等待页面完全加载
                    await asyncio.sleep(5)
                except Exception as e:
                    logger.error(f"页面加载失败: {str(e)}")
                    # 尝试不同的URL
                    alt_url = "https://snapany.com/zh/douyin"
                    logger.info(f"尝试访问备用URL: {alt_url}")
                    await page.goto(alt_url, wait_until="domcontentloaded", timeout=60000)
                    await asyncio.sleep(5)
                
                # 等待输入框加载
                logger.info("等待页面加载完成")
                await page.wait_for_selector('input[placeholder*="链接"]', state="visible", timeout=10000)
                
                # 输入视频链接
                logger.info(f"输入视频链接: {clean_url}")
                await page.fill('input[placeholder*="链接"]', clean_url)
                
                # 点击提取按钮
                logger.info("点击提取按钮")
                extract_button = await page.query_selector('button:has-text("提取")')
                if not extract_button:
                    # 尝试其他可能的按钮文本
                    extract_button = await page.query_selector('button:has-text("提取视频")')
                
                if not extract_button:
                    # 如果仍然找不到按钮，尝试通过类名或其他属性定位
                    extract_button = await page.query_selector('.extract-button, button.primary, button[type="submit"]')
                
                if not extract_button:
                    raise Exception("无法找到提取按钮")
                
                # 点击按钮
                await extract_button.click()
                
                # 等待API响应或视频元素出现
                logger.info("等待API响应或视频元素出现")
                timeout = 30  # 30秒超时
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    # 检查是否已捕获API响应
                    if api_response_data:
                        logger.info("已捕获API响应")
                        break
                    
                    # 检查页面上是否出现了视频元素
                    video_element = await page.query_selector('video')
                    if video_element:
                        logger.info("页面上检测到视频元素")
                        break
                    
                    # 等待一小段时间后再检查
                    await asyncio.sleep(0.5)
                
                # 如果没有捕获到API响应，尝试从页面元素中提取信息
                if not api_response_data:
                    logger.info("未捕获到API响应，尝试从页面元素提取信息")
                    
                    # 尝试从视频元素获取URL
                    video_element = await page.query_selector('video')
                    if video_element:
                        video_url = await video_element.get_attribute('src')
                        if video_url:
                            logger.info(f"从视频元素获取到URL: {video_url[:100]}...")
                            # 构造一个类似API响应的数据结构
                            api_response_data = {
                                "text": "从页面提取的视频",
                                "medias": [
                                    {
                                        "media_type": "video",
                                        "resource_url": video_url
                                    }
                                ]
                            }
                    
                    # 如果仍然没有数据，尝试查找下载按钮
                    if not api_response_data:
                        download_button = await page.query_selector('a[download], button:has-text("下载")')
                        if download_button:
                            download_url = await download_button.get_attribute('href')
                            if download_url:
                                logger.info(f"从下载按钮获取到URL: {download_url[:100]}...")
                                api_response_data = {
                                    "text": "从页面提取的视频",
                                    "medias": [
                                        {
                                            "media_type": "video",
                                            "resource_url": download_url
                                        }
                                    ]
                                }
                
                # 如果仍然没有数据，尝试从网络请求中获取
                if not api_response_data:
                    logger.info("尝试从网络请求中获取视频信息")
                    # 截图以便调试
                    await page.screenshot(path="debug_screenshot.png")
                    logger.info("已保存页面截图到debug_screenshot.png")
                    
                    raise Exception("无法从页面或API响应中获取视频信息")
                
                # 关闭浏览器
                await browser.close()
                
                return api_response_data
                
            except Exception as e:
                logger.error(f"Playwright操作失败: {str(e)}")
                # 截图以便调试
                try:
                    await page.screenshot(path="error_screenshot.png")
                    logger.info("已保存错误页面截图到error_screenshot.png")
                except:
                    pass
                
                # 关闭浏览器
                await browser.close()
                raise
    
    except Exception as e:
        logger.error(f"使用Playwright提取视频失败: {str(e)}")
        return {'error': str(e)}

async def download_file(url, file_path):
    """下载文件到指定路径"""
    import httpx
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                
                # 获取总大小
                total_size = int(response.headers.get("Content-Length", 0))
                
                # 创建并写入文件
                with open(file_path, "wb") as f:
                    downloaded = 0
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # 打印下载进度
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            if progress % 10 < 0.1:  # 每10%打印一次
                                logger.info(f"下载进度: {progress:.1f}% - {file_path}")
                
                logger.info(f"下载完成: {file_path}")
                return True
                
    except Exception as e:
        logger.error(f"下载失败: {str(e)}")
        return False

async def main():
    print(f"开始提取视频: {TEST_URL}")
    
    # 使用Playwright提取视频
    result = await extract_video_from_snapany_playwright(TEST_URL)
    
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
    asyncio.run(main()) 