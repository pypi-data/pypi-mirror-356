from pydantic import BaseModel, Field
from typing import List, Optional, Generic, TypeVar

from chanjing.exceptions import ChanjingException

T = TypeVar("T")


class Figure(BaseModel):
    """人物形象数据模型"""

    pic_path: str
    type: str
    cover: str
    width: int
    height: int
    preview_video_url: str


class CommonPerson(BaseModel):
    """公共数字人信息数据模型"""

    id: str
    name: str
    figures: List[Figure]
    gender: str
    width: int
    height: int
    audio_name: str
    audio_man_id: str
    audio_preview: str


class Person(BaseModel):
    """数字人形象信息数据模型"""

    id: Optional[str] = Field(default=None, description="数字人形象id")
    name: Optional[str] = Field(default=None, description="数字人名称")
    type: Optional[str] = Field(default="person", description="类型，默认person")
    pic_url: Optional[str] = Field(default=None, description="预览封面图")
    preview_url: Optional[str] = Field(default=None, description="预览地址")
    width: Optional[int] = Field(default=None, description="形象宽度")
    height: Optional[int] = Field(default=None, description="形象高度")
    audio_man_id: Optional[str] = Field(default=None, description="数字人的声音音色id")
    status: Optional[int] = Field(
        default=None, description="当前状态: 1制作中，2成功，4失败"
    )
    err_reason: Optional[str] = Field(default=None, description="失败后显示错误原因")
    is_open: Optional[int] = Field(default=None, description="是否可用，1可用，0不可用")
    reason: Optional[str] = Field(default=None, description="失败原因")
    progress: Optional[int] = Field(default=None, description="进度百分比，0-100")


class PageInfo(BaseModel):
    """分页信息数据模型"""

    page: int
    size: int
    total_count: int
    total_page: int


class ResponseData(BaseModel, Generic[T]):
    """响应数据模型"""

    list: List[T]
    page_info: Optional[PageInfo]


class APIResponse(BaseModel, Generic[T]):
    """API响应模型"""

    trace_id: str
    code: int
    msg: str
    data: Optional[T] = None

    def raise_for_status(self):
        if self.code == 50000:
            raise ChanjingException(self.msg, str(self.code))


class Audio(BaseModel):
    """声音"""

    id: Optional[str] = Field(default=None, description="声音id")
    name: Optional[str] = Field(default=None, description="声音名称")
    progress: Optional[int] = Field(default=None, description="进度百分比，0-100")
    audio_path: Optional[str] = Field(
        default=None, description="训练音频片段（从原音频中截取的有效片段用于训练）"
    )
    err_msg: Optional[str] = Field(default=None, description="失败后显示错误原因")


class SynthesisVideo(BaseModel):
    """合成视频信息"""

    id: str = Field(description="合成视频id")
    status: Optional[int] = Field(
        default=None,
        description="视频合成状态：10-生成中；30-成功；4X-参数异常；5X-服务异常",
    )
    progress: Optional[int] = Field(default=None, description="进度百分比，0-100")
    msg: Optional[str] = Field(default=None, description="错误信息")
    video_url: Optional[str] = Field(default=None, description="视频地址")
    create_time: Optional[int] = Field(default=None, description="创建时间")
    subtitle_data_url: Optional[str] = Field(default=None, description="字幕数据地址")
    preview_url: Optional[str] = Field(default=None, description="预览地址")
    duration: Optional[int] = Field(default=None, description="视频时长")


class FontInfo(BaseModel):
    """字体信息"""

    id: str = Field(description="字体id")
    name: str = Field(description="字体名称")
    preview: str = Field(description="字体预览地址")
    ttf_path: str = Field(description="字体路径")


class UserInfo(BaseModel):
    """用户信息"""

    name: str
    id: str
    custom_person_nums: int
    custom_person_limit: int
    video_create_seconds: int
    video_create_limit: int
