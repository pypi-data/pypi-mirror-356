#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
豆包图像生成工具
基于火山方舟API实现图像生成功能
"""

import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import requests
from PIL import Image
from io import BytesIO
from volcenginesdkarkruntime import Ark

# 用于将调试信息输出到stderr的函数
def debug_print(*args, **kwargs):
    """将调试信息输出到stderr"""
    print(*args, file=sys.stderr, **kwargs)

# 设置日志系统
def setup_logging():
    """设置日志系统，将日志输出到文件"""
    # 创建log文件夹
    log_dir = Path("log")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 创建logger
    logger = logging.getLogger('doubao_image_gen')
    logger.setLevel(logging.DEBUG)
    
    # 避免重复添加handler
    if not logger.handlers:
        # 文件handler
        file_handler = logging.FileHandler(log_dir / 'doubao_image_gen.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)
        
        # stderr handler
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.INFO)
        stderr_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(stderr_handler)
    
    return logger

class DoubaoImageGenerator:
    """豆包图像生成工具类"""
    
    def __init__(self, base_url: str, api_key: str, model_id: str, save_dir: str):
        """初始化图像生成工具
        
        Args:
            base_url: 豆包API基础URL
            api_key: API密钥
            model_id: 模型ID
            save_dir: 图片保存目录
        """
        self.logger = setup_logging()
        
        # 设置全局变量
        self.base_url = base_url
        self.api_key = api_key
        self.model_id = model_id
        self.save_dir = save_dir
        
        self.logger.info(f"初始化豆包图像生成工具")
        self.logger.info(f"BASE_URL: {base_url}")
        self.logger.info(f"MODEL_ID: {model_id}")
        self.logger.info(f"SAVE_DIR: {save_dir}")
        
        # 初始化Ark客户端
        try:
            self.client = Ark(
                base_url=base_url,
                api_key=api_key
            )
            self.logger.info("Ark客户端初始化成功")
            debug_print("✓ Ark客户端初始化成功")
        except Exception as e:
            error_msg = f"Ark客户端初始化失败: {str(e)}"
            self.logger.error(error_msg)
            debug_print(f"❌ {error_msg}")
            raise
        
        # 创建图片保存目录
        try:
            self.save_path = Path(save_dir)
            self.save_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"图片保存目录已创建: {self.save_path.absolute()}")
            debug_print(f"✓ 图片保存目录: {self.save_path.absolute()}")
        except Exception as e:
            error_msg = f"创建图片保存目录失败: {str(e)}"
            self.logger.error(error_msg)
            debug_print(f"❌ {error_msg}")
            raise
    
    async def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        seed: int = -1,
        guidance_scale: float = 8.0,
        watermark: bool = True,
        file_prefix: Optional[str] = None
    ) -> Dict[str, Any]:
        """生成图像
        
        Args:
            prompt: 用于生成图像的提示词
            size: 生成图像的宽高像素
            seed: 随机数种子
            guidance_scale: 模型输出结果与prompt的一致程度
            watermark: 是否在生成的图片中添加水印
            file_prefix: 图片文件名前缀
            
        Returns:
            包含图片路径和生成信息的字典
        """
        
        self.logger.info(f"开始生成图像")
        self.logger.info(f"参数 - prompt: {prompt[:100]}...")
        self.logger.info(f"参数 - size: {size}, seed: {seed}, guidance_scale: {guidance_scale}")
        self.logger.info(f"参数 - watermark: {watermark}, file_prefix: {file_prefix}")
        
        debug_print(f"🎨 正在生成图像...")
        
        try:
            # 参数验证
            if not prompt.strip():
                raise ValueError("提示词不能为空")
            
            # 调用豆包API生成图片
            self.logger.info("调用豆包API生成图片")
            response = self.client.images.generate(
                model=self.model_id,
                prompt=prompt,
                size=size,
                seed=seed,
                guidance_scale=guidance_scale,
                watermark=watermark,
                response_format="url"  # 固定使用URL格式
            )
            
            self.logger.info("API调用成功，开始处理响应")
            debug_print("✓ API调用成功")
            
            # 检查响应
            if not response or not response.data:
                raise ValueError("API返回空响应")
            
            # 获取图片URL
            image_url = response.data[0].url
            self.logger.info(f"获取到图片URL: {image_url}")
            
            # 等待并下载图片
            self.logger.info("开始下载图片")
            debug_print("📥 正在下载图片...")
            
            # 添加重试机制的图片下载
            max_retries = 3
            retry_delay = 2
            
            for attempt in range(max_retries):
                try:
                    # 异步下载图片
                    image_data = await self._download_image_async(image_url)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"下载图片失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避
                    else:
                        raise
            
            self.logger.info("图片下载成功")
            debug_print("✓ 图片下载成功")
            
            # 生成文件名
            if file_prefix:
                filename = f"image_{file_prefix}_{int(time.time())}.jpg"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"image_{timestamp}.jpg"
            
            # 保存图片
            image_path = self.save_path / filename
            
            # 将图片数据保存到文件
            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            self.logger.info(f"图片已保存到: {image_path.absolute()}")
            debug_print(f"💾 图片已保存: {image_path.name}")
            
            # 收集生成信息
            generation_info = {
                "model": getattr(response, 'model', self.model_id),
                "created": getattr(response, 'created', int(time.time())),
                "seed": seed,
                "guidance_scale": guidance_scale,
                "watermark": watermark,
                "size": size,
                "original_url": image_url
            }
            
            result = {
                "image_path": str(image_path.absolute()),
                "filename": filename,
                "generation_info": generation_info
            }
            
            self.logger.info(f"图像生成完成: {result}")
            return result
            
        except Exception as e:
            error_msg = f"图像生成失败: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            debug_print(f"❌ {error_msg}")
            raise
    
    async def _download_image_async(self, url: str) -> bytes:
        """异步下载图片
        
        Args:
            url: 图片URL
            
        Returns:
            图片二进制数据
        """
        
        try:
            # 使用requests下载图片（在实际异步环境中可以考虑使用aiohttp）
            loop = asyncio.get_event_loop()
            
            def download_sync():
                response = requests.get(url, timeout=30)
                response.raise_for_status()
                return response.content
            
            # 在线程池中执行同步下载
            image_data = await loop.run_in_executor(None, download_sync)
            
            # 验证图片数据
            try:
                img = Image.open(BytesIO(image_data))
                img.verify()  # 验证图片完整性
                self.logger.info(f"图片验证成功，格式: {img.format}, 尺寸: {img.size}")
            except Exception as e:
                raise ValueError(f"下载的图片数据无效: {str(e)}")
            
            return image_data
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"下载图片失败: {str(e)}")
        except Exception as e:
            raise ValueError(f"处理图片数据失败: {str(e)}")

# 测试函数
async def test_image_generation():
    """测试图像生成功能"""
    
    print("🧪 开始测试豆包图像生成功能")
    
    # 测试参数（参照test_ark_image_generation.py中的固定值）
    test_params = {
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        #"api_key": "your_api_key_here",  # 需要替换为实际的API密钥
        "api_key": "5fa5c431-80a3-4ad1-97da-14d971368377",
        "model_id": "ep-20250528154802-c4np4",  # 需要替换为实际的模型ID
        "save_dir": "images"
    }
    
    test_prompt = "小人国奇幻场景，小人们误闯到了正常人类的厨房里，正在用人类的厨具做饭"
    
    try:
        # 创建图像生成器
        generator = DoubaoImageGenerator(
            base_url=test_params["base_url"],
            api_key=test_params["api_key"],
            model_id=test_params["model_id"],
            save_dir=test_params["save_dir"]
        )
        
        print(f"✓ 图像生成器初始化成功")
        
        # 生成图片
        result = await generator.generate_image(
            prompt=test_prompt,
            size="1024x1024",
            seed=-1,
            guidance_scale=10.0,
            watermark=False,
            file_prefix="test"
        )
        
        print(f"✅ 测试成功！")
        print(f"📁 图片路径: {result['image_path']}")
        print(f"📊 生成信息: {result['generation_info']}")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("豆包图像生成工具 - 独立测试模式")
    print("注意: 请确保设置了正确的API密钥和模型ID")
    
    # 运行测试
    asyncio.run(test_image_generation())