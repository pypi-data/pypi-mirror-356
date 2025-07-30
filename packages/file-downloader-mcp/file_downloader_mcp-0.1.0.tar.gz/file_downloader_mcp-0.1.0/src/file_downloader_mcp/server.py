#!/usr/bin/env python3
"""
File Downloader MCP Server

A simple MCP server that provides file downloading functionality.
"""

import asyncio
import os
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("File Downloader")


@mcp.tool()
async def download_file(
    url: str,
    save_path: Optional[str] = None,
    filename: Optional[str] = None
) -> str:
    """
    从URL下载文件到指定目录

    Args:
        url: 要下载的文件URL
        save_path: 保存目录路径（可选，默认为当前目录下的downloads文件夹）
        filename: 自定义文件名（可选，默认从URL提取）

    Returns:
        下载结果信息
    """
    try:
        # 验证URL
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"❌ 错误：无效的URL格式: {url}"

        # 设置默认保存路径
        if save_path is None:
            save_path = "./downloads"

        # 创建保存目录
        save_dir = Path(save_path)
        save_dir.mkdir(parents=True, exist_ok=True)

        # 确定文件名
        if filename is None:
            # 从URL提取文件名
            url_path = parsed_url.path
            if url_path and url_path != '/':
                filename = Path(url_path).name
            else:
                filename = "downloaded_file"

        # 如果文件名没有扩展名，尝试从Content-Type推断
        file_path = save_dir / filename

        # 开始下载
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 先发送HEAD请求获取文件信息
            try:
                head_response = await client.head(url)
                content_length = head_response.headers.get('content-length')
                content_type = head_response.headers.get('content-type', '')

                # 如果文件名没有扩展名，尝试从Content-Type添加
                if '.' not in filename and content_type:
                    if 'image/jpeg' in content_type:
                        filename += '.jpg'
                    elif 'image/png' in content_type:
                        filename += '.png'
                    elif 'image/gif' in content_type:
                        filename += '.gif'
                    elif 'text/html' in content_type:
                        filename += '.html'
                    elif 'application/pdf' in content_type:
                        filename += '.pdf'
                    elif 'application/zip' in content_type:
                        filename += '.zip'

                    file_path = save_dir / filename

            except httpx.RequestError:
                # 如果HEAD请求失败，继续使用GET请求
                content_length = None

            # 发送GET请求下载文件
            async with client.stream('GET', url) as response:
                response.raise_for_status()

                # 检查文件是否已存在
                if file_path.exists():
                    base_name = file_path.stem
                    suffix = file_path.suffix
                    counter = 1
                    while file_path.exists():
                        new_name = f"{base_name}_{counter}{suffix}"
                        file_path = save_dir / new_name
                        counter += 1

                # 写入文件
                total_size = 0
                with open(file_path, 'wb') as f:
                    async for chunk in response.aiter_bytes(chunk_size=8192):
                        f.write(chunk)
                        total_size += len(chunk)

                # 格式化文件大小
                if total_size < 1024:
                    size_str = f"{total_size} B"
                elif total_size < 1024 * 1024:
                    size_str = f"{total_size / 1024:.1f} KB"
                else:
                    size_str = f"{total_size / (1024 * 1024):.1f} MB"

                return f"""✅ 文件下载成功！
📁 保存路径: {file_path.absolute()}
📊 文件大小: {size_str}
🌐 源URL: {url}
📝 文件名: {file_path.name}"""

    except httpx.HTTPStatusError as e:
        return f"❌ HTTP错误 {e.response.status_code}: {e.response.reason_phrase}"
    except httpx.RequestError as e:
        return f"❌ 网络请求错误: {str(e)}"
    except PermissionError:
        return f"❌ 权限错误：无法写入目录 {save_path}"
    except Exception as e:
        return f"❌ 下载失败: {str(e)}"


def main():
    """主函数：启动MCP服务器"""
    import sys
    print("🚀 启动文件下载MCP服务器...", file=sys.stderr)
    print("📡 等待MCP客户端连接...", file=sys.stderr)
    try:
        mcp.run()
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
