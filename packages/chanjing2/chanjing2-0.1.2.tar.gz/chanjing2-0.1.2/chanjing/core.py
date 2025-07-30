import requests
import logging
from .schemas import APIResponse
from curlify2 import Curlify

class ChanjingHttpClient(object):

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        base_url: str = "https://www.chanjing.cc/api/open/v1",
    ) -> None:
        """
        初始化禅境HTTP客户端
        Args:
            app_id: API应用ID
            app_secret: API应用密钥
            base_url: API基础URL，默认为"https://www.chanjing.cc/api/open/v1"
        """
        self.base_url = base_url
        url = f"{self.base_url}/access_token"
        headers = {"Content-Type": "application/json", "charset ": "utf-8"}
        payload = {"app_id": app_id, "secret_key": app_secret}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            self.access_token = response.json()["data"]["access_token"]
        else:
            raise Exception(f"Failed to get access token: {response.text}")

        """
        初始化禅境HTTP客户端
        
        Args:
            access_token: API访问令牌
            base_url: API基础URL，默认为"https://www.chanjing.cc/api/open/v1"
        """

        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.logger = logging.getLogger("chanjing")

    def request(self, method: str, url: str, **kwargs) -> APIResponse:
        """
        发送HTTP请求到禅境API

        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            url: API端点路径（不包含基础URL）
            **kwargs: 传递给requests库的额外参数

        Returns:
            APIResponse: API响应对象

        Raises:
            ValueError: 当HTTP方法不支持或参数无效时
            ConnectionError: 当网络连接失败时
            TimeoutError: 当请求超时时
            Exception: 其他异常情况
        """
        method = method.upper()
        if method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            raise ValueError(f"不支持的HTTP方法: {method}")

        # 构建完整URL
        full_url = f"{self.base_url}/{url.lstrip('/')}"

        # 设置请求头
        headers = kwargs.pop("headers", {})
        headers.update(
            {
                "access_token": self.access_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
                "charset": "utf-8",
            }
        )

        # 记录请求信息（不包含敏感信息）
        safe_headers = {k: v for k, v in headers.items() if k.lower() != "access_token"}
        self.logger.debug(f"发送 {method} 请求到 {full_url}")
        self.logger.debug(f"请求头: {safe_headers}")
        # 发送请求
        response = self.session.request(
            method=method,
            url=full_url,
            headers=headers,
            timeout=30,  # 默认超时时间为30秒
            **kwargs,
        )
        curlify = Curlify(response.request)
        print(curlify.to_curl())
        # 检查HTTP状态码
        response.raise_for_status()
        response_data = response.json()
        # 将响应数据转换为APIResponse对象
        api_response = APIResponse.model_validate(response_data)
        return api_response
