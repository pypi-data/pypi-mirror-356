# Chanjing SDK

一个用于与禅境API交互的Python客户端库。

## 功能特点

- 提供数字人定制功能
- 支持声音定制
- 视频合成与管理
- 公共数字人资源访问
- 参数验证
- 错误处理

## 安装

使用pip安装：

```bash
pip install chanjing
```

## 使用方法

### 基础配置

```python
from chanjing import ChanjingHttpClient

# 初始化客户端
client = ChanjingHttpClient(
    app_id="your_app_id",
    app_secret="your_app_secret"
)
```

### 1. 定制数字人

```python
from chanjing.customised.person import CreateCustomisedPersonRequest, CustomisedPerson

# 创建定制数字人
person_request = CreateCustomisedPersonRequest(
    name="数字人名称",
    material_video="https://example.com/video.mp4",  # 训练视频URL
    callback="https://your-callback-url.com",        # 回调地址
    train_type=None                                  # 可选的训练类型
)
person_id = client.customised.person.create(person_request)

# 获取定制数字人列表
list_request = ListCustomisedPersonRequest(page=1, page_size=10)
person_list = client.customised.person.list(list_request)

# 删除定制数字人
delete_request = DeleteCustomisedPersonRequest(id=person_id)
client.customised.person.delete(delete_request)
```

### 2. 定制声音

```python
from chanjing.customised.audio import CreateCustomisedAudioRequest, CustomisedAudio

# 创建定制声音
audio_request = CreateCustomisedAudioRequest(
    name="声音名称",
    url="https://example.com/audio.wav",           # 音频文件URL
    callback="https://your-callback-url.com"       # 回调地址
)
audio_id = client.customised.audio.create(audio_request)

# 获取定制声音列表
list_request = ListCustomisedAudioRequest(page=1, page_size=10)
audio_list = client.customised.audio.list(list_request)
```

### 3. 视频合成

```python
from chanjing.synthesis import (
    Video, CreateVideoRequest, PersonConfig, 
    AudioConfig, TTSConfig, BgConfig, SubtitleConfig
)

# 配置数字人
person_config = PersonConfig(
    id="digital_person_id",     # 数字人ID
    x=0,                        # x坐标位置
    y=0,                        # y坐标位置
    width=1080,                 # 宽度
    height=1920,                # 高度
    figure_type=None,           # 可选，whole_body仅用于公共数字人
    drive_mode=None,            # 可选，支持正常顺序和随机帧动作
    is_rgba_mode=False,         # 是否使用RGBA模式
    backway=1                   # 1正放，2倒放
)

# 配置TTS
tts_config = TTSConfig(
    text=["您好，这是测试文本"],  # 文本内容
    speed=1.0,                  # 语速(0.5-2.0)
    audio_man="voice_id"        # 音色ID
)

# 配置音频
audio_config = AudioConfig(
    tts=tts_config,
    wav_url=None,              # 可选，外部音频文件URL
    type="tts",                # "tts"或"audio"
    volume=100,                # 音量
    language="cn"              # 语言
)

# 创建视频
video_request = CreateVideoRequest(
    person=person_config,
    audio=audio_config,
    bg_color="#000000",        # 背景颜色
    screen_width=1080,         # 视频宽度
    screen_height=1920,        # 视频高度
    callback="https://your-callback-url.com"  # 可选的回调地址
)
video_id = client.video.create(video_request)

# 获取视频列表
list_request = ListVideoRequest(page=1, page_size=10)
video_list = client.video.list(list_request)
```
更详细的示例请参考 `examples/http_client_example.py`。


## 开发环境设置

1. 克隆仓库
2. 创建并激活虚拟环境
3. 安装开发依赖


```bash
git clone https://github.com/yourusername/dify_sdk.git
cd dify_sdk
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"
```


### 发布到PyPI

本项目使用Hatch作为构建和发布工具。以下是发布到PyPI的步骤：

#### 1. 安装Hatch

```bash
pip install hatch
# 或使用uv
uv pip install hatch
```

#### 2. 配置PyPI凭证

有两种方式配置PyPI凭证：

**方式一：使用API令牌（推荐）**

1. 在[PyPI官网](https://pypi.org/manage/account/)注册并登录账号
2. 在账号设置中创建API令牌
3. 创建`~/.pypirc`文件：

```
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**方式二：使用环境变量**

```bash
# Windows (PowerShell)
$env:HATCH_INDEX_USER="__token__"
$env:HATCH_INDEX_AUTH="pypi-AgEIcHlwaS5vcmcCJDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Linux/Mac
export HATCH_INDEX_USER=__token__
export HATCH_INDEX_AUTH=pypi-AgEIcHlwaS5vcmcCJDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3. 构建分发包

```bash
hatch build
```

这将在`dist/`目录下创建源代码分发包（.tar.gz）和轮子分发包（.whl）。

#### 4. 发布到PyPI

```bash
hatch publish
```

如果您想先在测试环境（TestPyPI）上发布：

```bash
hatch publish -r test
```

#### 5. 验证发布

发布成功后，您可以通过pip安装您的包来验证：

```bash
pip install chanjing
```

## 许可证

MIT

## 项目结构

```
chanjing/
├── __init__.py
├── core.py              # 核心客户端实现
├── schemas.py          # 数据模型定义
├── synthesis.py        # 视频合成相关
├── user_info.py        # 用户信息管理
└── customised/         # 定制功能模块
    ├── person.py      # 定制数字人
    └── audio.py       # 定制声音
```