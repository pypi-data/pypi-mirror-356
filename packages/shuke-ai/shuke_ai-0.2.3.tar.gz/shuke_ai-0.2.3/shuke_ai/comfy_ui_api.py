import requests
import json
import os
import time
from typing import Dict, List, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .utils.logger import logger
import urllib3
import ssl
from urllib3.poolmanager import PoolManager

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=context
        )

class ComfyUIAPI:
    def __init__(self, server_url: str):
        self.server_url = server_url.rstrip('/')
        logger.info(f"初始化ComfyUI API, 服务器地址: {self.server_url}")
        
        # 配置请求会话
        self.session = requests.Session()
        
        # 配置重试策略
        retries = Retry(
            total=5,  # 最大重试次数
            backoff_factor=0.5,  # 重试间隔
            status_forcelist=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        
        # 禁用SSL警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 配置SSL适配器
        adapter = TLSAdapter()
        self.session.mount('https://', adapter)
        self.session.verify = False
        
        # 禁用代理
        self.session.trust_env = False  # 不使用环境变量中的代理设置
        self.session.proxies = {
            'http': None,
            'https': None
        }
        
        logger.info("已配置SSL和网络策略")

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """发送请求并处理错误"""
        try:
            url = f"{self.server_url}/{endpoint.lstrip('/')}"
            logger.debug(f"发送{method}请求到: {url}")
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, 'text'):
                error_detail = e.response.text
                logger.error(f"API请求失败: {str(e)}, 详细信息: {error_detail}")
                raise Exception(f"API请求失败: {str(e)}, 详细信息: {error_detail}")
            logger.error(f"API请求失败: {str(e)}")
            raise Exception(f"API请求失败: {str(e)}")

    def upload_image(self, image_path: str) -> Dict:
        """上传图片到服务器"""
        try:
            logger.info(f"开始上传图片: {image_path}")
            if not os.path.exists(image_path):
                logger.error(f"图片不存在: {image_path}")
                raise Exception(f"图片不存在: {image_path}")
            
            files = {
                'image': (os.path.basename(image_path), open(image_path, 'rb'), 'application/octet-stream')
            }
            result = self._make_request('POST', '/upload/image', files=files)
            logger.info(f"图片上传成功: {result}")
            return result
        except Exception as e:
            logger.error(f"图片上传失败: {str(e)}")
            raise Exception(f"图片上传失败: {str(e)}")

    def upload_video(self, file_path: str, subfolder: str = "") -> Dict:
        """上传视频（通过图片上传端点）
        
        Args:
            file_path: 视频文件路径
            subfolder: 子文件夹名称
            
        Returns:
            上传结果
        """
        try:
            logger.info(f"开始上传视频: {file_path}")
            if not os.path.exists(file_path):
                logger.error(f"文件不存在: {file_path}")
                raise Exception(f"文件不存在: {file_path}")
                
            files = {
                'image': (os.path.basename(file_path), open(file_path, 'rb'), 'application/octet-stream')
            }
            
            result = self._make_request('POST', '/upload/image', files=files, data={'subfolder': subfolder})
            logger.info(f"视频上传成功: {result}")
            return result
            
        except Exception as e:
            logger.error(f"视频上传失败: {str(e)}")
            raise Exception(f"视频上传失败: {str(e)}")
    
    def get_history(self, prompt_id: str) -> Dict:
        """获取历史记录"""
        return self._make_request('GET', f'/history/{prompt_id}')

    def download_video(self, filename: str) -> bytes:
        """下载视频文件"""
        try:
            logger.info(f"开始下载视频: {filename}")
            response = self.session.get(f'{self.server_url}/view', params={'filename': filename})
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"视频下载失败: {str(e)}")
            raise Exception(f"视频下载失败: {str(e)}")

    def __del__(self):
        """清理资源"""
        self.session.close()
        logger.debug("已关闭API会话")