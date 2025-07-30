from operator import ifloordiv
from typing import Optional
from pydantic import BaseModel
from chanjing.core import ChanjingHttpClient
from chanjing.schemas import Person, ResponseData


class CreateCustomisedPersonRequest(BaseModel):
    """创建定制数字人请求模型
    
    属性:
        name: 定制数字人名称
        material_video: 外网可下载播放的mp4视频文件
        callback: 回调地址，任务结束后会向该地址发送POST请求
        train_type: 训练类型，可选参数
    """
    name: str
    material_video: str
    callback: str
    train_type: Optional[str] = None

class ListCustomisedPersonRequest(BaseModel):
    """定制数字人列表请求模型
    
    属性:
        page: 当前页码
        page_size: 每页记录数
    """
    page : int
    page_size: int

class DeleteCustomisedPersonRequest(BaseModel):
    """删除定制数字人请求模型
    
    属性:
        id: 定制数字人ID
    """
    id  : str

class CustomisedPerson(object):
    def __init__(self,client:ChanjingHttpClient) -> None:
        """
        初始化定制数字人管理类
        
        Args:
            client: 禅境HTTP客户端
        """
        self.client = client
        pass
    def create(self , request:CreateCustomisedPersonRequest)->str:
        """
        创建定制数字人
        
        Args:
            request: 创建定制数字人请求
        """
        response = self.client.request("POST", "create_customised_person", json=request.model_dump())
        return response.data

    def list(self , request:ListCustomisedPersonRequest)-> ResponseData[Person]:
        """
        定制数字人列表
        
        Args:
            request: 定制数字人列表请求
        """
        response = self.client.request("POST", "list_customised_person", json=request.model_dump())
        return ResponseData[Person].model_validate(response.data)

    def detail(self , id:str)->Person:
        """
        定制数字人形象详情
        
        Args:
            id: 定制数字人ID
        """
        response = self.client.request("GET", "customised_person", params={"id": id})
        return Person.model_validate(response.data)

    def delete(self , request:DeleteCustomisedPersonRequest)->bool:
        """
        删除定制数字人
        
        Args:
            request: 删除定制数字人请求
        """
        response = self.client.request("POST", "delete_customised_person", json=request.model_dump())
        return not bool(response.data)