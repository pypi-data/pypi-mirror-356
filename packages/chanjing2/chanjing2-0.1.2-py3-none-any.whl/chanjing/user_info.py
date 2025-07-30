import chanjing.schemas
from chanjing.core import ChanjingHttpClient


class UserInfo(object):
    def __init__(self, client: ChanjingHttpClient) -> None:
        """
        初始化用户信息管理类

        Args:
            client: 禅境HTTP客户端
        """
        self.client = client
        pass

    def user_info(self) -> chanjing.schemas.UserInfo:
        """
        获取用户信息
        """
        response = self.client.request("GET", "user_info")
        return response.data

    def list_common_dp(self) -> chanjing.schemas.CommonPerson:
        """
        公共数字人
        """
        response = self.client.request("GET", "list_common_dp")
        return response.data
