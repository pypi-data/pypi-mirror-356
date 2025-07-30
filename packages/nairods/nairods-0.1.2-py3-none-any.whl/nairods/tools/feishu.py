# 文件名：feishu.py
# 作者：nairoads
# 日期：2024-06-18 15:22:37
# 描述：飞书开放平台API工具类，支持消息与图片发送

import requests
import json
from typing import Optional, Dict, Any
from requests_toolbelt import MultipartEncoder
from .loggertool import log

class FeishuTool:
    """飞书开放平台API工具类"""
    
    def __init__(self, webhook: Optional[str] = None, app_id: Optional[str] = None, app_secret: Optional[str] = None):
        """
        初始化飞书工具类
        :param webhook: 机器人webhook地址
        :param app_id: 应用ID
        :param app_secret: 应用密钥
        """
        self.webhook = f"https://open.feishu.cn/open-apis/bot/v2/hook/{webhook}" if webhook else None
        self.app_id = app_id
        self.app_secret = app_secret
        self.token: Optional[str] = None
        self.base_url = "https://open.feishu.cn/open-apis"
        
    def _get_access_token(self) -> str:
        """
        获取access_token
        :return: access_token字符串
        """
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.token = data["tenant_access_token"]
            return self.token
        except Exception as e:
            log.error(f"获取access_token失败: {str(e)}")
            raise

    def send_text_message(self, content: str, at_user: Optional[str] = None) -> Dict[str, Any]:
        """
        发送文本消息
        :param content: 消息内容
        :param at_user: 要@的用户ID，不传则不@
        :return: API响应数据
        """
        if not self.webhook:
            raise ValueError("Webhook未初始化")
            
        text_content = content
        if at_user:
            text_content += f"<at user_id=\"{at_user}\">test</at>"
            
        payload = {
            "msg_type": "text",
            "content": {
                "text": text_content
            }
        }
        try:
            response = requests.post(
                self.webhook,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            log.error(f"发送文本消息失败: {str(e)}")
            raise

    def upload_image(self, image_path: str) -> Dict[str, Any]:
        """
        上传图片并发送
        :param image_path: 图片本地路径
        :return: API响应数据
        """
        if not self.token:
            self._get_access_token()
            
        url = f"{self.base_url}/im/v1/images"
        with open(image_path, 'rb') as img_file:
            form = {
                'image_type': 'message',
                'image': img_file
            }
            multi_form = MultipartEncoder(form)
            try:
                response = requests.post(
                    url,
                    headers={
                        'Authorization': f'Bearer {self.token}',
                        'Content-Type': multi_form.content_type
                    },
                    data=multi_form
                )
                response.raise_for_status()
                image_key = response.json()['data']['image_key']
                payload = {
                    "msg_type": "image",
                    "content": {"image_key": image_key}
                }
                response = requests.post(
                    self.webhook,
                    headers={'Authorization': f'Bearer {self.token}'},
                    data=json.dumps(payload)
                )
                return response.json()
            except Exception as e:
                log.error(f"上传图片失败: {str(e)}")
                raise 