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
from mcp.server.fastmcp import FastMCP
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
        
        # 添加g-timestamp和g-footer头
        headers["g-timestamp"] = str(timestamp)
        headers["g-footer"] = "2cfa72328df209d07dcaee32a7ede261"  # 固定值，从请求中获取
        
        # 打印完整的请求头
        logger.info(f"完整请求头: {json.dumps(headers, ensure_ascii=False)}")
        
        # 只使用API方式获取视频信息
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # 发送API请求
            logger.info(f"发送API请求到: {SNAPANY_API_URL}")
            logger.info(f"请求数据: {{'link': '{clean_url}'}}")
            logger.info(f"请求头: {headers}")
            
            try:
                response = await client.post(
                    SNAPANY_API_URL,
                    json={"link": clean_url},
                    headers=headers,
                    timeout=TIMEOUT
                )
                response.raise_for_status()
                
                # 获取API响应
                api_response = response.json()
                
                # 检查响应是否有效
                if not api_response:
                    raise Exception("API返回空响应")
                
                # 记录API响应状态
                if 'code' in api_response:
                    logger.info(f"API响应状态码: {api_response['code']}")
                    
                    # 检查API响应是否成功
                    if api_response['code'] != 0 and 'msg' in api_response:
                        logger.warning(f"API返回错误: {api_response['msg']}")
                
                # 保存API响应以便调试
                try:
                    with open("api_response.json", "w", encoding="utf-8") as f:
                        json.dump(api_response, f, ensure_ascii=False, indent=2)
                    logger.info("已保存API响应到api_response.json")
                except Exception as e:
                    logger.error(f"保存API响应失败: {str(e)}")
                
                # 直接返回API响应，不进行网页抓取
                return api_response
                
            except httpx.HTTPStatusError as e:
                logger.error(f"API请求失败，HTTP状态码: {e.response.status_code}")
                try:
                    error_text = e.response.text
                    logger.error(f"响应内容: {error_text[:1000]}...")
                    
                    # 尝试解析错误响应
                    try:
                        error_json = e.response.json()
                        logger.error(f"错误响应JSON: {json.dumps(error_json, ensure_ascii=False)}")
                    except:
                        pass
                        
                    # 如果是400错误，尝试使用不同的请求格式
                    if e.response.status_code == 400:
                        logger.info("尝试使用不同的请求格式...")
                        # 尝试不同的请求体格式
                        alt_formats = [
                            {"link": clean_url},  # 标准格式
                            {"url": clean_url},   # 旧格式
                            {"video_url": clean_url}  # 可能的其他格式
                        ]
                        
                        for format_data in alt_formats:
                            try:
                                logger.info(f"尝试请求格式: {json.dumps(format_data, ensure_ascii=False)}")
                                alt_response = await client.post(
                                    SNAPANY_API_URL,
                                    json=format_data,
                                    headers=headers,
                                    timeout=TIMEOUT
                                )
                                alt_response.raise_for_status()
                                api_response = alt_response.json()
                                logger.info(f"使用格式 {list(format_data.keys())[0]} 成功获取响应")
                                return api_response
                            except Exception as format_error:
                                logger.warning(f"格式 {list(format_data.keys())[0]} 失败: {str(format_error)}")
                                continue
                        
                        # 如果所有格式都失败
                        logger.error("所有备用请求格式都失败")
                except Exception as inner_e:
                    logger.error(f"尝试替代请求格式失败: {str(inner_e)}")
                
                # 如果API方法也失败，返回错误信息
                return {'error': f"API请求失败，HTTP状态码: {e.response.status_code}"}
                
            except httpx.RequestError as e:
                logger.error(f"API请求网络错误: {str(e)}")
                return {'error': f"API请求网络错误: {str(e)}"}
                
            except json.JSONDecodeError as e:
                logger.error(f"API响应不是有效的JSON: {str(e)}")
                try:
                    logger.error(f"响应内容: {response.text[:1000]}...")
                except:
                    logger.error("无法获取响应内容")
                return {'error': f"API响应不是有效的JSON: {str(e)}"}
            
    except Exception as e:
        logger.error(f"Error extracting video from SnapAny: {str(e)}")
        return {'error': str(e)}


def identify_platform(url):
    """识别URL所属的平台"""
    domain = urlparse(url).netloc.lower()
    
    if any(d in domain for d in ['douyin.com', 'iesdouyin.com']):
        return 'tiktok'
    elif 'tiktok.com' in domain:
        return 'tiktok'
    elif 'bilibili.com' in domain:
        return 'bilibili'
    elif 'youtube.com' in domain or 'youtu.be' in domain:
        return 'youtube'
    elif 'facebook.com' in domain or 'fb.com' in domain:
        return 'facebook'
    elif 'pinterest.com' in domain:
        return 'pinterest'
    elif 'instagram.com' in domain:
        return 'instagram'
    elif 'twitter.com' in domain or 'x.com' in domain:
        return 'twitter'
    else:
        return 'tiktok'  # 默认使用抖音/TikTok解析器


async def download_file(url, file_path):
    """下载文件到指定路径"""
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT) as client:
                async with client.stream("GET", url) as response:
                    response.raise_for_status()
                    
                    # 获取总大小
                    total_size = int(response.headers.get("Content-Length", 0))
                    
                    # 创建并写入文件
                    async with aiofiles.open(file_path, "wb") as f:
                        downloaded = 0
                        async for chunk in response.aiter_bytes(chunk_size=8192):
                            await f.write(chunk)
                            downloaded += len(chunk)
                            
                            # 打印下载进度
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                if progress % 10 < 0.1:  # 每10%打印一次
                                    logger.info(f"下载进度: {progress:.1f}% - {file_path}")
                    
                    logger.info(f"下载完成: {file_path}")
                    return True
                    
        except httpx.HTTPError as e:
            logger.warning(f"下载尝试 {attempt+1}/{MAX_RETRIES} 失败: {str(e)}")
            await asyncio.sleep(2 ** attempt)  # 指数退避
    
    logger.error(f"下载失败，已达最大重试次数: {url}")
    return False


def sanitize_filename(name):
    """清理文件名，移除不安全字符"""
    # 移除文件名中不允许的字符
    invalid_chars = r'[\\/*?:"<>|]'
    return re.sub(invalid_chars, '_', name)


@mcp.tool()
async def download_video(url: str, output_path: str = None) -> dict:
    """下载视频到指定路径

    Args:
        url: 要下载的视频URL，支持抖音/TikTok/哔哩哔哩等平台
        output_path: 保存视频的路径，默认为./downloads文件夹

    Returns:
        下载结果信息
    """
    global DOWNLOAD_PATH
    try:
        logger.info(f"准备下载视频: {url}")
        
        # 使用指定的输出路径或默认路径
        actual_output_path = output_path if output_path else DOWNLOAD_PATH
        os.makedirs(actual_output_path, exist_ok=True)
        
        # 设置全局下载路径（用于extract_video_from_snapany函数）
        DOWNLOAD_PATH = actual_output_path
        
        # 解析视频
        logger.info(f"正在解析视频URL: {url}")
        video_data = await extract_video_from_snapany(url)
        
        if 'error' in video_data:
            return {
                'success': False,
                'message': f"视频解析失败: {video_data['error']}",
                'error': video_data['error']
            }
            
        # 获取视频下载链接和标题
        import json
        logger.info(f"解析视频数据: {json.dumps(video_data, ensure_ascii=False)[:200]}...")
        
        # 初始化变量
        video_url = None
        title = ""
        
        # 保存完整的API响应以便详细分析
        try:
            with open("full_api_response.json", "w", encoding="utf-8") as f:
                json.dump(video_data, f, ensure_ascii=False, indent=2)
            logger.info("已保存完整API响应到full_api_response.json")
        except Exception as e:
            logger.error(f"保存完整API响应失败: {str(e)}")
        
        # 尝试多种可能的响应格式
        # 新的API响应格式: 包含text和medias字段
        if 'text' in video_data and 'medias' in video_data and isinstance(video_data['medias'], list):
            logger.info("检测到新的API响应格式，包含text和medias字段")
            
            # 获取标题
            title = video_data['text']
            logger.info(f"从text字段获取到标题: {title}")
            
            # 查找视频类型的媒体
            for media in video_data['medias']:
                if isinstance(media, dict) and media.get('media_type') == 'video' and 'resource_url' in media:
                    video_url = media['resource_url']
                    logger.info(f"从medias[].resource_url获取到视频URL: {video_url[:100] if video_url else 'None'}...")
                    break
        
        # 情况1: 直接在顶层包含videoUrl和title
        elif 'videoUrl' in video_data:
            video_url = video_data['videoUrl']
            title = video_data.get('title', '')
            logger.info(f"从顶层获取到视频URL: {video_url[:100] if video_url else 'None'}...")
        
        # 情况2: 数据在data字段中
        elif 'data' in video_data and video_data['data']:
            data = video_data['data']
            logger.info(f"data字段内容: {json.dumps(data, ensure_ascii=False)[:200]}...")
            
            # 尝试获取无水印视频链接
            if 'video' in data:
                if isinstance(data['video'], dict) and 'url' in data['video']:
                    video_url = data['video']['url']
                    logger.info(f"从data.video.url获取到视频URL: {video_url[:100] if video_url else 'None'}...")
                elif isinstance(data['video'], str):
                    video_url = data['video']
                    logger.info(f"从data.video获取到视频URL: {video_url[:100] if video_url else 'None'}...")
            
            # 如果没有找到视频链接，尝试其他可能的字段
            if not video_url:
                for field in ['videoUrl', 'url', 'download_url', 'downloadUrl']:
                    if field in data and data[field]:
                        video_url = data[field]
                        logger.info(f"从data.{field}获取到视频URL: {video_url[:100] if video_url else 'None'}...")
                        break
                
            # 获取标题
            for field in ['title', 'desc', 'description', 'text']:
                if field in data and data[field]:
                    title = data[field]
                    logger.info(f"从data.{field}获取到标题: {title}")
                    break
        
        # 情况3: 数据在其他嵌套结构中
        elif 'result' in video_data:
            result = video_data['result']
            logger.info(f"result字段内容: {json.dumps(result, ensure_ascii=False)[:200] if isinstance(result, dict) else str(result)[:200]}...")
            
            if isinstance(result, dict):
                # 尝试从result中获取视频链接
                if 'videoUrl' in result:
                    video_url = result['videoUrl']
                    logger.info(f"从result.videoUrl获取到视频URL: {video_url[:100] if video_url else 'None'}...")
                elif 'video' in result:
                    if isinstance(result['video'], dict) and 'url' in result['video']:
                        video_url = result['video']['url']
                        logger.info(f"从result.video.url获取到视频URL: {video_url[:100] if video_url else 'None'}...")
                    elif isinstance(result['video'], str):
                        video_url = result['video']
                        logger.info(f"从result.video获取到视频URL: {video_url[:100] if video_url else 'None'}...")
                
                # 获取标题
                for field in ['title', 'desc', 'description', 'text']:
                    if field in result and result[field]:
                        title = result[field]
                        logger.info(f"从result.{field}获取到标题: {title}")
                        break
        
        # 如果上述方法都没找到视频链接，尝试递归搜索JSON中的所有可能字段
        if not video_url:
            logger.info("尝试递归搜索视频链接...")
            
            def search_video_url(obj, path=""):
                """递归搜索包含视频URL的字段"""
                if isinstance(obj, dict):
                    # 检查常见的视频URL字段名
                    for key in ['video', 'videoUrl', 'url', 'download_url', 'downloadUrl', 'playAddr', 'play_addr', 'resource_url']:
                        if key in obj:
                            value = obj[key]
                            if isinstance(value, str) and ('http' in value.lower()):
                                logger.info(f"在路径 {path}.{key} 找到可能的视频URL: {value[:100]}...")
                                return value
                            elif isinstance(value, dict) and 'url' in value:
                                url = value['url']
                                if isinstance(url, str) and ('http' in url.lower()):
                                    logger.info(f"在路径 {path}.{key}.url 找到可能的视频URL: {url[:100]}...")
                                    return url
                    
                    # 递归搜索所有字段
                    for key, value in obj.items():
                        result = search_video_url(value, f"{path}.{key}" if path else key)
                        if result:
                            return result
                            
                elif isinstance(obj, list):
                    # 搜索列表中的所有元素
                    for i, item in enumerate(obj):
                        result = search_video_url(item, f"{path}[{i}]")
                        if result:
                            return result
                
                return None
            
            # 从整个响应中搜索视频URL
            found_url = search_video_url(video_data)
            if found_url:
                video_url = found_url
                logger.info(f"通过递归搜索找到视频URL: {video_url[:100]}...")
        
        # 如果没有找到标题，尝试递归搜索
        if not title:
            logger.info("尝试递归搜索视频标题...")
            
            def search_title(obj, path=""):
                """递归搜索包含标题的字段"""
                if isinstance(obj, dict):
                    # 检查常见的标题字段名
                    for key in ['title', 'desc', 'description', 'text', 'content']:
                        if key in obj and obj[key] and isinstance(obj[key], str):
                            logger.info(f"在路径 {path}.{key} 找到可能的标题: {obj[key]}")
                            return obj[key]
                    
                    # 递归搜索所有字段
                    for key, value in obj.items():
                        result = search_title(value, f"{path}.{key}" if path else key)
                        if result:
                            return result
                            
                elif isinstance(obj, list):
                    # 搜索列表中的所有元素
                    for i, item in enumerate(obj):
                        result = search_title(item, f"{path}[{i}]")
                        if result:
                            return result
                
                return None
            
            # 从整个响应中搜索标题
            found_title = search_title(video_data)
            if found_title:
                title = found_title
                logger.info(f"通过递归搜索找到标题: {title}")
        
        # 如果仍然没有找到标题，使用当前时间作为文件名
        if not title:
            title = f"video_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            logger.info(f"使用默认标题: {title}")
        else:
            logger.info(f"最终获取到的标题: {title}")
        
        # 如果没有找到视频链接
        if not video_url:
            logger.error("无法从响应中获取视频URL")
            return {
                'success': False,
                'message': "无法从API响应中获取视频URL",
                'data': video_data
            }
        
        # 确保视频URL不是硬编码的
        # 检查是否是抖音视频URL
        if "365yg.com" in video_url or "douyin" in video_url:
            logger.info(f"检测到抖音视频链接: {video_url[:50]}...")
        else:
            logger.warning(f"视频链接可能不是抖音链接，请检查: {video_url[:50]}...")
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = sanitize_filename(f"{title}_{timestamp}.mp4")
        file_path = os.path.join(actual_output_path, filename)
        
        # 下载视频
        logger.info(f"开始下载视频到: {file_path}")
        success = await download_file(video_url, file_path)
        
        if success:
            return {
                'success': True,
                'message': f"视频下载成功: {file_path}",
                'file_path': file_path,
                'title': title,
                'video_url': video_url  # 返回视频URL以便调试
            }
        else:
            return {
                'success': False,
                'message': "视频下载失败",
                'video_url': video_url  # 返回视频URL以便调试
            }
            
    except Exception as e:
        logger.error(f"下载视频时出错: {str(e)}")
        return {'success': False, 'error': str(e), 'message': f"下载视频时出错: {str(e)}"}


if __name__ == "__main__":
    mcp.run(transport='stdio')
