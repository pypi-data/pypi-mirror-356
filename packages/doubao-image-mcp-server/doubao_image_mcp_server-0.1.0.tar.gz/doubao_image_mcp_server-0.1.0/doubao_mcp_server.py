#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包图像生成MCP服务器
基于FastMCP框架和火山方舟API实现图像生成功能
"""

import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Annotated

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent
from pydantic import Field

from doubao_image_gen import DoubaoImageGenerator

# 用于将调试信息输出到stderr的函数
def debug_print(*args, **kwargs):
    """将调试信息输出到stderr"""
    print(*args, file=sys.stderr, **kwargs)

# 设置日志系统
def setup_logging():
    """设置日志系统，将日志输出到文件和stderr"""
    # 创建log文件夹
    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 配置文件日志
    logging.basicConfig(
        level=logging.DEBUG,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / 'doubao_mcp_server.log', encoding='utf-8'),
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    return logging.getLogger(__name__)

# 初始化日志
logger = setup_logging()

# 初始化MCP服务器
mcp = FastMCP("豆包图像生成MCP服务")

# 从环境变量获取配置（模块级检查）
BASE_URL = os.getenv("BASE_URL", "").strip().strip('`') if os.getenv("BASE_URL") else None
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY", "").strip() if os.getenv("DOUBAO_API_KEY") else None
API_MODEL_ID = os.getenv("API_MODEL_ID", "").strip() if os.getenv("API_MODEL_ID") else None
IMAGE_SAVE_DIR = os.getenv("IMAGE_SAVE_DIR", "").strip() if os.getenv("IMAGE_SAVE_DIR") else None

# 模块级环境变量检查
required_env_vars = {
    "BASE_URL": BASE_URL,
    "DOUBAO_API_KEY": DOUBAO_API_KEY,
    "API_MODEL_ID": API_MODEL_ID,
    "IMAGE_SAVE_DIR": IMAGE_SAVE_DIR
}

for var_name, var_value in required_env_vars.items():
    if not var_value:
        error_msg = f"环境变量 {var_name} 未设置或为空，请检查 MCP JSON 配置中的 environment 字段"
        logger.error(error_msg)
        debug_print(f"错误: {error_msg}")
        sys.exit(1)

logger.info("所有必需的环境变量已成功加载")
debug_print("✓ 环境变量检查通过")

# 定义可用的图片分辨率
AVAILABLE_RESOLUTIONS = {
    "512x512": "512x512 (1:1 小正方形)",
    "768x768": "768x768 (1:1 正方形)",
    "1024x1024": "1024x1024 (1:1 大正方形)",
    "864x1152": "864x1152 (3:4 竖屏)",
    "1152x864": "1152x864 (4:3 横屏)",
    "1280x720": "1280x720 (16:9 宽屏)",
    "720x1280": "720x1280 (9:16 手机竖屏)",
    "832x1248": "832x1248 (2:3)",
    "1248x832": "1248x832 (3:2)",
    "1512x648": "1512x648 (21:9 超宽屏)",
    "2048x2048": "2048x2048 (1:1 超大正方形)"
}



# 初始化图像生成工具
image_generator = DoubaoImageGenerator(
    base_url=BASE_URL,
    api_key=DOUBAO_API_KEY,
    model_id=API_MODEL_ID,
    save_dir=IMAGE_SAVE_DIR
)

@mcp.resource("doubao://resolutions")
def get_available_resolutions() -> str:
    """获取可用的图片分辨率列表"""
    logger.info("获取可用分辨率列表")
    return format_options(AVAILABLE_RESOLUTIONS)

def format_options(options_dict: Dict[str, str]) -> str:
    """将选项字典格式化为字符串"""
    formatted_lines = []
    for key, description in options_dict.items():
        formatted_lines.append(f"• {key}: {description}")
    return "\n".join(formatted_lines)

# 格式化分辨率选项
available_resolutions_list = format_options(AVAILABLE_RESOLUTIONS)

def validate_ascii_only(text: str, field_name: str) -> None:
    """验证文本是否只包含ASCII字符"""
    if not text.isascii():
        raise ValueError(f"{field_name} 只能包含ASCII字符（英文字母、数字、标点符号）")

def validate_resolution(size: str) -> None:
    """验证分辨率是否有效"""
    if size not in AVAILABLE_RESOLUTIONS:
        available = ", ".join(AVAILABLE_RESOLUTIONS.keys())
        raise ValueError(f"无效的分辨率 '{size}'。可用分辨率: {available}")

@mcp.tool()
async def doubao_generate_image(
    prompt: Annotated[str, Field(description="用于生成图像的提示词，支持中英文描述")],
    size: Annotated[str, Field(description=f"生成图像的宽高像素，可选值:\n{available_resolutions_list}")] = "1024x1024",
    seed: Annotated[int, Field(description="随机数种子，用于控制模型生成内容的随机性，-1表示自动生成", ge=-1, le=2147483647)] = -1,
    guidance_scale: Annotated[float, Field(description="模型输出结果与prompt的一致程度，值越大越严格遵循提示词", ge=1.0, le=10.0)] = 8.0,
    watermark: Annotated[bool, Field(description="是否在生成的图片中添加水印")] = True,
    file_prefix: Annotated[Optional[str], Field(description="图片文件名前缀（仅限英文字母、数字、下划线），长度不超过20个字符")] = None
) -> List[TextContent]:
    """使用豆包API生成图像
    
    这个函数是MCP服务器的核心工具函数，用于调用豆包（火山方舟）API生成图像。
    函数会验证输入参数，调用底层的图像生成器，并返回格式化的结果信息。
    
    Args:
        prompt (str): 用于生成图像的提示词，支持中英文描述，不能为空
        size (str): 生成图像的宽高像素，必须是预定义的分辨率之一，默认"1024x1024"
        seed (int): 随机数种子，用于控制模型生成内容的随机性，-1表示自动生成，范围-1到2147483647
        guidance_scale (float): 模型输出结果与prompt的一致程度，值越大越严格遵循提示词，范围1.0到10.0
        watermark (bool): 是否在生成的图片中添加水印，默认True
        file_prefix (Optional[str]): 图片文件名前缀，仅限英文字母、数字、下划线和连字符，长度不超过20个字符
    
    Returns:
        List[TextContent]: 包含图像生成结果信息的文本内容列表，包括保存路径、分辨率、提示词等信息
    
    Raises:
        ValueError: 当输入参数不符合要求时抛出，如提示词为空、分辨率无效、文件前缀格式错误等
    """
    
    logger.info(f"开始生成图像，提示词: {prompt[:50]}...")
    debug_print(f"🎨 开始生成图像: {prompt[:50]}...")
    
    try:
        # 参数验证
        if not prompt.strip():
            raise ValueError("提示词不能为空")
        
        # 验证分辨率
        validate_resolution(size)
        
        # 验证文件前缀（如果提供）
        if file_prefix:
            validate_ascii_only(file_prefix, "文件前缀")
            # 验证文件前缀长度
            if len(file_prefix) > 20:
                raise ValueError("文件前缀长度不能超过20个字符")
            # 验证文件前缀格式
            if not file_prefix.replace('_', '').replace('-', '').isalnum():
                raise ValueError("文件前缀只能包含英文字母、数字、下划线和连字符")
        
        # 验证其他参数
        if not isinstance(seed, int) or seed < -1 or seed > 2147483647:
            raise ValueError("seed必须是-1到2147483647之间的整数")
        
        if not isinstance(guidance_scale, (int, float)) or guidance_scale < 1.0 or guidance_scale > 10.0:
            raise ValueError("guidance_scale必须是1.0到10.0之间的数值")
        
        if not isinstance(watermark, bool):
            raise ValueError("watermark必须是布尔值")
        
        logger.info(f"参数验证通过，开始调用图像生成API")
        
        # 调用图像生成处理
        result = await asyncio.create_task(
            image_generator.generate_image(
                prompt=prompt,
                size=size,
                seed=seed,
                guidance_scale=guidance_scale,
                watermark=watermark,
                file_prefix=file_prefix
            )
        )
        
        logger.info(f"图像生成成功，结果: {result}")
        debug_print(f"✅ 图像生成成功")
        
        # 处理返回结果
        if isinstance(result, dict) and "image_path" in result:
            image_path = result["image_path"]
            generation_info = result.get("generation_info", {})
            
            response_text = f"🎨 图像生成成功！\n\n"
            response_text += f"📁 保存路径: {image_path}\n"
            response_text += f"📐 分辨率: {size}\n"
            response_text += f"🎯 提示词: {prompt}\n"
            
            if generation_info:
                response_text += f"\n📊 生成信息:\n"
                for key, value in generation_info.items():
                    response_text += f"  • {key}: {value}\n"
            
            return [TextContent(type="text", text=response_text)]
        else:
            error_msg = "图像生成返回了意外的结果格式"
            logger.error(f"{error_msg}: {result}")
            return [TextContent(type="text", text=f"❌ {error_msg}")]
            
    except ValueError as e:
        error_msg = f"参数验证失败: {str(e)}"
        logger.error(error_msg)
        debug_print(f"❌ {error_msg}")
        return [TextContent(type="text", text=f"❌ {error_msg}")]
        
    except Exception as e:
        error_msg = f"图像生成过程中发生错误: {str(e)}"
        logger.error(error_msg, exc_info=True)
        debug_print(f"❌ {error_msg}")
        return [TextContent(type="text", text=f"❌ {error_msg}")]

@mcp.prompt()
def image_generation_prompt(
    prompt: str,
    size: str = "1024x1024",
    seed: int = -1,
    guidance_scale: float = 8.0,
    watermark: bool = True,
    file_prefix: str = ""
) -> str:
    """创建图片生成提示模板"""
    
    template = f"""
# 豆包图像生成请求

## 基本参数
- **提示词**: {prompt}
- **分辨率**: {size}
- **随机种子**: {seed if seed != -1 else '自动生成'}
- **引导强度**: {guidance_scale}
- **添加水印**: {'是' if watermark else '否'}
- **文件前缀**: {file_prefix if file_prefix else '使用时间戳'}

## 可用分辨率选项
{available_resolutions_list}

## 参数说明
- **prompt**: 图像描述文本，支持中英文，描述越详细效果越好
- **size**: 生成图像的宽高像素，从上述可用选项中选择
- **seed**: 随机数种子，-1表示自动生成，相同种子可复现结果
- **guidance_scale**: 1.0-10.0，值越大越严格遵循提示词
- **watermark**: 是否添加"AI生成"水印
- **file_prefix**: 图片文件名前缀，仅限英文字母数字下划线

## 使用示例
```
doubao_generate_image(
    prompt="一只可爱的橘猫坐在阳光明媚的窗台上",
    size="1024x1024",
    guidance_scale=8.0,
    watermark=False,
    file_prefix="cute_cat"
)
```
"""
    
    return template

def main():
    """主函数入口，启动MCP服务器"""
    logger.info("启动豆包图像生成MCP服务器")
    debug_print("🚀 启动豆包图像生成MCP服务器")
    
    # 显示配置信息（仅用于调试）
    debug_print(f"📋 配置信息:")
    debug_print(f"  • BASE_URL: {BASE_URL}")
    debug_print(f"  • API_MODEL_ID: {API_MODEL_ID}")
    debug_print(f"  • IMAGE_SAVE_DIR: {IMAGE_SAVE_DIR}")
    debug_print(f"  • DOUBAO_API_KEY: {'已设置' if DOUBAO_API_KEY else '未设置'}")
    
    # 启动MCP服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()