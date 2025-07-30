from typing import Annotated, Optional, Literal, List, Any

from pydantic import BaseModel, Field

from chanjing.core import ChanjingHttpClient
from chanjing.schemas import ResponseData, SynthesisVideo, FontInfo


class PersonConfig(BaseModel):
    id: str = Field(description="形象列表返回的id")
    x: Optional[int] = Field(default=0, description="x位置")
    y: Optional[int] = Field(default=480, description="y位置")
    figure_type: Optional[Literal["whole_body"]] = Field(
        default=None,
        description="数字人类型。仅在使用公共数字人时需要传递该参数，值为'whole_body'",
    )
    width: Optional[int] = Field(default=1080, description="宽")
    height: Optional[int] = Field(default=1920, description="高")
    drive_mode: Optional[Literal["", "random"]] = Field(
        default="",
        description="驱动模式。支持正常顺序驱动，和随机帧动作驱动random。默认正常顺序驱动",
    )
    is_rgba_mode: Optional[bool] = Field(
        default=False,
        description="是否驱动四通道webm视频。注意事项：1.需要数字人是webm格式四通道视频定制的;2.2025年2月8号以及之后定制的数字人开始生效;3.该方式生成的数字人合成视频不含字幕以及背景",
    )
    backway: Optional[int] = Field(
        default=1, description="指定数字人驱动到素材末尾的播放顺序，1正放，2倒放"
    )


class TTSConfig(BaseModel):
    text: list[str] = Field(
        description="文本, 字符串数组，所有内容放到一个字符串上面。使用标点符号分割就行，不用分多个字符串"
    )
    speed: Annotated[float, Field(ge=0.5, le=2)] = Field(
        default=1.0, description="浮点数类型，请在0.5和2之间"
    )
    audio_man: Optional[str] = Field(
        default=None, description="数字人中列表audio_man_id数字人的音色"
    )


class BgConfig(BaseModel):
    src_url: str = Field(description="背景图片地址，仅支持 jpg,png格式")
    x: int = Field(default=0, description="x 坐标")
    y: int = Field(default=0, description="y 坐标")
    width: Annotated[int, Field(ge=1)] = Field(
        default=1080, description="图片宽度，必须大于等于 1"
    )
    height: Annotated[int, Field(ge=1)] = Field(
        default=1920, description="图片高度，必须大于等于 1"
    )


class SubtitleConfig(BaseModel):
    x: int = Field(default=31, description="x坐标，字体显示范围的起始x坐标，推荐31")
    y: int = Field(default=1521, description="y坐标，字体显示范围的起始y坐标，推荐1521")
    show: bool = Field(default=True, description="是否显示字幕")
    width: Annotated[int, Field(ge=1)] = Field(
        default=1080, description="字体显示范围的宽度，必须大于等于 1"
    )
    height: Annotated[int, Field(ge=1)] = Field(
        default=1920, description="字体显示范围的高度，必须大于等于 1"
    )
    font_size: Annotated[int, Field(ge=1)] = Field(
        default=64, description="字体大小，必须大于等于 1"
    )
    color: Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")] = Field(
        default="#000000", description="颜色，默认黑色"
    )
    font_id: Optional[str] = Field(default=None, description="字体 ID，可选")


class AudioConfig(BaseModel):
    tts: TTSConfig = Field(description="文字转语音配置")
    wav_url: Optional[str] = Field(
        default=None, description="mp3、m4a 或者 wav 视频文件，根据音频文件驱动数字人"
    )
    type: Literal["tts", "audio"] = Field(
        default="tts",
        description="生成声音类型，当前默认tts表示通过tts文本生成。audio表示通过音频文件生成",
    )
    volume: int = Field(default=100, description="音量，默认 100")
    language: str = Field(default="cn", description="语言类型，默认 'cn'")


class CreateVideoRequest(BaseModel):
    """创建合成视频请求模型

    属性:
        name: 合成视频名称
        url: 外网可下载播放的视频链接
        callback: 回调地址，任务结束后会向该地址发送POST请求

    """

    person: PersonConfig = Field(description="数字人形象配置")
    audio: AudioConfig = Field(description="声音配置")
    bg: Optional[BgConfig] = None
    subtitle_config: Optional[SubtitleConfig] = None
    bg_color: str = Field(
        default="#000000",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="背景颜色，十六进制颜色代码",
    )
    screen_width: Annotated[int, Field(ge=1)] = Field(
        default=1080, description="屏幕宽度默认 1080"
    )
    screen_height: Annotated[int, Field(ge=1)] = Field(
        default=1920, description="屏幕高度默认 1920"
    )
    callback: Optional[str] = Field(
        default=None, description="回调地址，任务结束后会向该地址发送POST请求"
    )


class ListVideoRequest(BaseModel):
    """合成视频列表请求模型

    属性:
        page: 当前页码
        page_size: 每页记录数
    """

    page: int
    page_size: int


class Video(object):
    def __init__(self, client: ChanjingHttpClient) -> None:
        """
        初始化合成视频管理类

        Args:
            client: 禅境HTTP客户端
        """
        self.client = client
        pass

    def create(self, request: CreateVideoRequest) -> str:
        """
        创建合成视频

        Args:
            request: 创建合成视频请求
        """
        response = self.client.request(
            "POST", "create_video", json=request.model_dump()
        )
        response.raise_for_status()
        return response.data

    def list(self, request: ListVideoRequest) -> ResponseData[SynthesisVideo]:
        """
        获取合成视频列表

        Args:
            request: 合成视频列表请求
        """
        response = self.client.request("POST", "video_list", json=request.model_dump())
        return ResponseData[SynthesisVideo](**response.data)

    def detail(self, id: str) -> SynthesisVideo:
        """
        合成视频详情

        Args:
            id: 合成视频ID
        """
        response = self.client.request("GET", "video", params={"id": id})
        return SynthesisVideo(**response.data)

    def font_list(self) -> List[FontInfo]:
        """
        获取字体列表
        """
        response = self.client.request("GET", "font_list")
        data: List[dict[str, Any]] = response.data
        return [FontInfo(**item) for item in data]
