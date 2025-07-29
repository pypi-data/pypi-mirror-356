#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Replicate Vision服务
用于与Replicate API交互，支持图像生成和图像分析
"""

import os
import time
import uuid
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
import asyncio
import aiohttp
import replicate # 导入 replicate 库
from PIL import Image
from io import BytesIO

# 调整 BaseService 的导入路径以匹配您的项目结构
from isa_model.inference.services.base_service import BaseService
from isa_model.inference.providers.base_provider import BaseProvider
from isa_model.inference.base import ModelType

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReplicateVisionService(BaseService):
    """
    Replicate Vision服务，用于处理图像生成和分析。
    经过调整，使用原生异步调用并优化了文件处理。
    """
    
    def __init__(self, provider: BaseProvider, model_name: str):
        """
        初始化Replicate Vision服务
        """
        super().__init__(provider, model_name)
        # 从 provider 或环境变量获取 API token
        self.api_token = self.provider.config.get("api_token", os.environ.get("REPLICATE_API_TOKEN"))
        self.model_type = ModelType.VISION
        
        # 可选的默认配置
        self.guidance_scale = self.provider.config.get("guidance_scale", 7.5)
        self.num_inference_steps = self.provider.config.get("num_inference_steps", 30)
        
        # 生成的图像存储目录
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # ★ 调整点: 为 replicate 库设置 API token
        if self.api_token:
            # replicate 库会自动从环境变量读取，我们确保它被设置
            os.environ["REPLICATE_API_TOKEN"] = self.api_token
        else:
            logger.warning("Replicate API token 未找到。服务可能无法正常工作。")

    async def _prepare_input_files(self, input_data: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Any]]:
        """
        ★ 新增辅助函数: 准备输入数据，将本地文件路径转换为文件对象。
        这使得服务能统一处理本地文件和URL。
        """
        prepared_input = input_data.copy()
        files_to_close = []
        for key, value in prepared_input.items():
            # 如果值是字符串，且看起来像一个存在的本地文件路径
            if isinstance(value, str) and not value.startswith(('http://', 'https://')) and os.path.exists(value):
                logger.info(f"检测到本地文件路径 '{value}'，准备打开文件。")
                try:
                    file_handle = open(value, "rb")
                    prepared_input[key] = file_handle
                    files_to_close.append(file_handle)
                except Exception as e:
                    logger.error(f"打开文件失败 '{value}': {e}")
                    raise
        return prepared_input, files_to_close

    async def generate_image(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用Replicate模型生成图像 (已优化为原生异步)
        """
        prepared_input, files_to_close = await self._prepare_input_files(input_data)
        try:
            # 设置默认参数
            if "guidance_scale" not in prepared_input:
                prepared_input["guidance_scale"] = self.guidance_scale
            if "num_inference_steps" not in prepared_input:
                prepared_input["num_inference_steps"] = self.num_inference_steps
            
            logger.info(f"开始使用模型 {self.model_name} 生成图像 (原生异步)")
            
            # ★ 调整点: 使用原生异步的 replicate.async_run
            output = await replicate.async_run(self.model_name, input=prepared_input)
            
            # 将结果转换为标准格式 (此部分逻辑无需改变)
            if isinstance(output, list):
                urls = output
            else:
                urls = [output]

            result = {
                "urls": urls,
                "metadata": {
                    "model": self.model_name,
                    "input": input_data # 返回原始输入以供参考
                }
            }
            logger.info(f"图像生成完成: {result['urls']}")
            return result
        except Exception as e:
            logger.error(f"图像生成失败: {e}")
            raise
        finally:
            # ★ 新增: 确保所有打开的文件都被关闭
            for f in files_to_close:
                f.close()
    
    async def analyze_image(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """
        分析图像 (已优化为原生异步)
        """
        input_data = {"image": image_path, "prompt": prompt}
        prepared_input, files_to_close = await self._prepare_input_files(input_data)
        try:
            logger.info(f"开始使用模型 {self.model_name} 分析图像 (原生异步)")
            # ★ 调整点: 使用原生异步的 replicate.async_run
            output = await replicate.async_run(self.model_name, input=prepared_input)
            
            result = {
                "text": "".join(output) if isinstance(output, list) else output,
                "metadata": {
                    "model": self.model_name,
                    "input": input_data
                }
            }
            logger.info(f"图像分析完成")
            return result
        except Exception as e:
            logger.error(f"图像分析失败: {e}")
            raise
        finally:
            # ★ 新增: 确保所有打开的文件都被关闭
            for f in files_to_close:
                f.close()
    
    async def generate_and_save(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成图像并保存到本地 (此方法无需修改)"""
        result = await self.generate_image(input_data)
        saved_paths = []
        for i, url in enumerate(result["urls"]):
            timestamp = int(time.time())
            file_name = f"{self.output_dir}/{timestamp}_{uuid.uuid4().hex[:8]}_{i+1}.png"
            try:
                # Convert FileOutput object to string if necessary
                url_str = str(url) if hasattr(url, "__str__") else url
                await self._download_image(url_str, file_name)
                saved_paths.append(file_name)
                logger.info(f"图像已保存至: {file_name}")
            except Exception as e:
                logger.error(f"保存图像失败: {e}")
        result["saved_paths"] = saved_paths
        return result
    
    async def _download_image(self, url: str, save_path: str) -> None:
        """异步下载图像并保存 (此方法无需修改)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    content = await response.read()
                    with Image.open(BytesIO(content)) as img:
                        img.save(save_path)
        except Exception as e:
            logger.error(f"下载图像时出错: {url}, {e}")
            raise

    # `load` 和 `unload` 方法在Replicate API场景下通常是轻量级的
    async def load(self) -> None:
        if not self.api_token:
            raise ValueError("缺少Replicate API令牌，请设置REPLICATE_API_TOKEN环境变量或在provider配置中提供")
        logger.info(f"Replicate Vision服务已准备就绪，使用模型: {self.model_name}")

    async def unload(self) -> None:
        logger.info(f"卸载Replicate Vision服务: {self.model_name}")