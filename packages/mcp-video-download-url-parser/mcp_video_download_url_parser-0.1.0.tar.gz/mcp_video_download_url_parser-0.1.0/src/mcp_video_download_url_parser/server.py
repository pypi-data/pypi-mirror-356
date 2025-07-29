#!/usr/bin/env python3

import logging
import httpx
import os
import re
import asyncio
import aiofiles
import json
from urllib.parse import urlparse
from datetime import datetime
from fastmcp import FastMCP
import time
from playwright.async_api import async_playwright

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 初始化MCP服务器
mcp = FastMCP("video-url-parser")

# 全局配置
DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH", "./downloads")
MAX_RETRIES = 3
TIMEOUT = 30
SNAPANY_API_URL = "https://api.snapany.com/v1/extract"
SNAPANY_WEBSITE_URL = "https://snapany.com/zh/tiktok"

# 确保下载目录存在
os.makedirs(DOWNLOAD_PATH, exist_ok=True)


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
                await page.goto(SNAPANY_WEBSITE_URL, wait_until="networkidle")
                
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
                    # 获取所有请求
                    requests = await page.context.storage_state()
                    
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


async def extract_video_from_snapany(url):
    """使用SnapAny API解析视频URL"""
    try:
        # 首先尝试使用Playwright方法
        logger.info("尝试使用Playwright方法提取视频")
        result = await extract_video_from_snapany_playwright(url)
        
        # 如果Playwright方法成功，直接返回结果
        if result and 'error' not in result:
            logger.info("Playwright方法成功提取视频")
            return result
        
        # 如果Playwright方法失败，记录错误并尝试使用API方法
        logger.warning(f"Playwright方法失败: {result.get('error', '未知错误')}")
        logger.info("尝试使用API方法提取视频")
        
        # 清理URL，确保只包含实际链接
        clean_url = url.strip()
        # 如果URL包含在文本中，尝试提取它
        url_match = re.search(r'https?://[^\s]+', clean_url)
        if url_match:
            clean_url = url_match.group(0)
            
        logger.info(f"提取的URL: {clean_url}")
        
        # 根据URL确定平台类型
        platform = identify_platform(clean_url)
        logger.info(f"检测到平台: {platform}")
        
        # 设置正确的请求头，完全匹配实际请求
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
            "Accept": "*/*",
            "Accept-Language": "zh",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "Origin": "https://snapany.com",
            "Referer": "https://snapany.com/",
            "Sec-Ch-Ua": '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Priority": "u=1, i"
        }
        
        # 生成时间戳和footer (如果需要)
        timestamp = int(time.time() * 1000)
        
        # 准备请求体
        data = {
            "url": clean_url,
            "lang": "zh",
            "platform": platform
        }
        
        # 发送请求
        logger.info(f"发送API请求: {json.dumps(data, ensure_ascii=False)}")
        timeout = httpx.Timeout(TIMEOUT)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                SNAPANY_API_URL,
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                logger.error(f"API请求失败: 状态码 {response.status_code}")
                return {'error': f'API请求失败，状态码: {response.status_code}'}
            
            # 解析响应
            try:
                response_data = response.json()
                logger.info(f"API响应: {json.dumps(response_data, ensure_ascii=False)[:200]}...")
                return response_data
            except Exception as e:
                logger.error(f"解析API响应失败: {str(e)}")
                return {'error': f'解析API响应失败: {str(e)}'}
    
    except Exception as e:
        logger.error(f"API方法提取视频失败: {str(e)}")
        return {'error': str(e)}


def identify_platform(url):
    """根据URL识别平台类型"""
    domain = urlparse(url).netloc.lower()
    
    if 'douyin' in domain or 'tiktok' in domain:
        return 'tiktok'
    elif 'bilibili' in domain:
        return 'bilibili'
    elif 'youtube' in domain or 'youtu.be' in domain:
        return 'youtube'
    elif 'instagram' in domain:
        return 'instagram'
    elif 'weibo' in domain:
        return 'weibo'
    elif 'twitter' in domain or 'x.com' in domain:
        return 'twitter'
    elif 'facebook' in domain:
        return 'facebook'
    else:
        return 'unknown'


async def download_file(url, file_path):
    """下载文件到指定路径"""
    try:
        logger.info(f"开始下载文件: {url} -> {file_path}")
        
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 使用httpx下载文件
        timeout = httpx.Timeout(60.0)  # 增加下载超时时间
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("GET", url) as response:
                response.raise_for_status()
                
                async with aiofiles.open(file_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        await f.write(chunk)
        
        logger.info(f"文件下载完成: {file_path}")
        return True
    except Exception as e:
        logger.error(f"文件下载失败: {str(e)}")
        return False


def sanitize_filename(name):
    """清理文件名，移除不合法字符"""
    # 替换不允许在文件名中使用的字符
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    name = re.sub(r'\s+', " ", name).strip()  # 替换多余空白字符
    return name[:100]  # 限制文件名长度


@mcp.tool()
async def download_video(url: str, output_path: str = None) -> dict:
    """
    从抖音、TikTok等平台下载无水印视频
    
    Args:
        url: 视频URL或包含视频URL的文本
        output_path: 视频保存路径（默认为./downloads）
    
    Returns:
        包含下载结果信息的字典
    """
    try:
        logger.info(f"接收到下载请求: {url}")
        
        # 设置输出路径
        if output_path:
            # 确保路径存在
            os.makedirs(output_path, exist_ok=True)
        else:
            output_path = DOWNLOAD_PATH
        
        logger.info(f"设置输出路径: {output_path}")
        
        # 从URL中提取视频信息
        api_response = await extract_video_from_snapany(url)
        
        if 'error' in api_response:
            return {
                'success': False,
                'error': api_response['error'],
                'message': '解析视频失败'
            }
        
        logger.info(f"解析视频成功，准备下载")
        
        # 检查响应格式并提取视频URL和标题
        video_url = None
        video_title = None
        
        # 尝试提取标题
        if 'text' in api_response:
            video_title = api_response['text']
            logger.info(f"从响应中提取标题: {video_title}")
        
        # 遍历不同的响应格式尝试提取视频URL
        if 'medias' in api_response and len(api_response['medias']) > 0:
            # 格式1: 直接在medias数组中
            for media in api_response['medias']:
                if media.get('media_type') == 'video' and 'resource_url' in media:
                    video_url = media['resource_url']
                    logger.info(f"从medias数组中提取视频URL: {video_url[:100]}...")
                    break
        
        if not video_url and 'data' in api_response:
            # 格式2: 在data对象内
            if isinstance(api_response['data'], dict):
                # 尝试搜索嵌套对象中的视频URL
                video_url = search_video_url(api_response['data'])
                if video_url:
                    logger.info(f"从data对象中提取视频URL: {video_url[:100]}...")
                
                # 如果没有找到标题，尝试从data中提取
                if not video_title:
                    video_title = search_title(api_response['data'])
                    if video_title:
                        logger.info(f"从data对象中提取标题: {video_title}")
        
        if not video_url:
            # 如果仍然没有找到，直接搜索整个响应对象
            video_url = search_video_url(api_response)
            if video_url:
                logger.info(f"从整个响应中提取视频URL: {video_url[:100]}...")
        
        if not video_title:
            # 如果仍然没有找到标题，尝试从整个响应中提取
            video_title = search_title(api_response)
            if video_title:
                logger.info(f"从整个响应中提取标题: {video_title}")
            else:
                # 使用当前时间作为默认标题
                video_title = f"视频_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                logger.info(f"未找到标题，使用默认标题: {video_title}")
        
        if not video_url:
            return {
                'success': False,
                'error': '无法从响应中提取视频URL',
                'api_response': api_response
            }
        
        # 清理标题并构建文件名
        clean_title = sanitize_filename(video_title)
        file_name = f"{clean_title}.mp4"
        file_path = os.path.join(output_path, file_name)
        
        # 下载视频
        download_success = await download_file(video_url, file_path)
        
        if download_success:
            return {
                'success': True,
                'message': '视频下载成功',
                'file_path': file_path,
                'title': video_title,
                'url': video_url
            }
        else:
            return {
                'success': False,
                'error': '下载视频文件失败',
                'video_url': video_url
            }
            
        def search_video_url(obj, path=""):
            """递归搜索对象中的视频URL"""
            if isinstance(obj, dict):
                # 检查常见的视频URL字段
                for key in ['url', 'video_url', 'download_url', 'play_url', 'resource_url']:
                    if key in obj and isinstance(obj[key], str) and ('http' in obj[key] and ('.mp4' in obj[key] or '/video/' in obj[key])):
                        return obj[key]
                
                # 递归搜索嵌套对象
                for k, v in obj.items():
                    result = search_video_url(v, f"{path}.{k}" if path else k)
                    if result:
                        return result
            
            elif isinstance(obj, list):
                # 递归搜索列表
                for i, item in enumerate(obj):
                    result = search_video_url(item, f"{path}[{i}]")
                    if result:
                        return result
            
            return None
            
        def search_title(obj, path=""):
            """递归搜索对象中的标题"""
            if isinstance(obj, dict):
                # 检查常见的标题字段
                for key in ['title', 'desc', 'description', 'text', 'name', 'caption']:
                    if key in obj and isinstance(obj[key], str) and len(obj[key]) > 0:
                        return obj[key]
                
                # 递归搜索嵌套对象
                for k, v in obj.items():
                    result = search_title(v, f"{path}.{k}" if path else k)
                    if result:
                        return result
            
            elif isinstance(obj, list):
                # 递归搜索列表
                for i, item in enumerate(obj):
                    result = search_title(item, f"{path}[{i}]")
                    if result:
                        return result
            
            return None
                
    except Exception as e:
        logger.error(f"下载视频异常: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'message': '下载视频过程中发生异常'
        } 