from typing import Optional
from pydantic import BaseModel
from chanjing.core import ChanjingHttpClient
from chanjing.schemas import Audio, ResponseData

class CreateCustomisedAudioRequest(BaseModel):
    """创建定制声音请求模型
    
    属性:
        name: 定制声音名称
        url: 外网可下载播放的声音链接
        callback: 回调地址，任务结束后会向该地址发送POST请求
      
    """
    name: str
    url: str
    callback: str
    model_type: Optional[str] = "cicada3.0"
 

class ListCustomisedAudioRequest(BaseModel):
    """定制声音列表请求模型
    
    属性:
        page: 当前页码
        page_size: 每页记录数
    """
    page : int
    page_size: int


class CustomisedAudio(object):
    def __init__(self,client:ChanjingHttpClient) -> None:
        """
        初始化定制声音管理类
        
        Args:
            client: 禅境HTTP客户端
        """
        self.client = client
        pass
    def create(self , request:CreateCustomisedAudioRequest)->str:
        """
        创建定制声音
        
        Args:
            request: 创建定制声音请求
        """
        response = self.client.request("POST", "create_customised_audio", json=request.model_dump())
        return response.data

    def list(self , request:ListCustomisedAudioRequest)->ResponseData[Audio]:
        """
        获取声音定制结果
        
        Args:
            request: 定制声音列表请求
        """
        response = self.client.request("POST", "list_customised_audio", json=request.model_dump())
        return ResponseData[Audio].model_validate(response.data)

    def detail(self , id:str)->Audio:
        """
        定制声音详情
        
        Args:
            id: 定制声音ID
        """
        response = self.client.request("GET", "customised_audio", params={"id": id})
        return Audio.model_validate(response.data)

  