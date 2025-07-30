from numpy import ndarray

## 一个用numpy实现的8bit音乐生成器

### 功能特性

- MIDI 音符映射：通过枚举类将 MIDI 缺陷值与音名绑定。
- 多种波形支持：包括正弦波、方波、三角波、锯齿波和白噪声。
- 基本鼓组支持：Kick、Snare、Hi-hat 等常见打击乐器模拟。
- 通道生成器：支持旋律和鼓声分别生成独立通道。
- 后处理与播放：混音、音量控制、裁剪与播放功能。
- ️参数配置系统：灵活定义采样率、BPM 和时长等音频参数。

### 安装方式

```bash
pip install chippymu
```


### 示例用法

#### 播放一段旋律

```python
from chippymu.models import Note, WaveType, Melody
from chippymu.configs import BasicParams
from chippymu.channelgen import generate_wave
from chippymu.sound import post_processing, play

from numpy import ndarray

params = BasicParams(sample_rate=16000, bpm=90, length=4)

melody = Melody()
basic_melody: list[tuple[float, Note, float]] = [(0.0, Note.C1, 1.0), (2.0, Note.E1, 1.0), (3.0, Note.G1, 1.0)]
melody.apm(basic_melody, 0.0)

wave: ndarray = generate_wave(melody=melody, wave_type=WaveType.SINE, params=params)

channels: list[ndarray] = [wave,]
volumes: list[float] = [0.8,]
mixed: ndarray = post_processing(channels=channels, volumes=volumes, params=params)

play(data=mixed, params=params)
```

#### 播放一段鼓点

```python
from chippymu.models import DrumType
from chippymu.configs import BasicParams
from chippymu.channelgen import generate_drums
from chippymu.sound import post_processing, play

from numpy import ndarray

params = BasicParams(sample_rate=16000, bpm=90, length=4)

drums: list[tuple[float, DrumType, float]] = [(0.0, DrumType.KICK, 0.1), (1.0, DrumType.HIHAT, 0.2), (2.0, DrumType.SNARE, 0.2)]
drum_audio: ndarray = generate_drums(drums=drums, params=params)

channels: list[ndarray] = [drum_audio,]
volumes: list[float] = [0.8,]

mixed = post_processing(channels=channels, volumes=volumes)
play(data=mixed, params=params)
```

### 核心模块说明

1. `models` 模块：定义了 MIDI 音符映射、波形类型和鼓点类型。

    - WaveType：波形类型，包括 `SINE`、`SQUARE`、`SAWTOOTH` 和 `TRIANGLE`。
    - DrumType：鼓点类型，包括 `KICK`、`HIHAT`、`SNARE` 和 `PERC`。
    - Note：音符对象，包含音符的起始时间、持续时间、音高和音量等信息。

2. `configs` 模块：定义了参数配置，包括采样率、每分钟节拍数、总时长。

    - sample_rate：采样率，默认为 16000 Hz。
    - bpm：每分钟节拍数，默认为 90。
    - length：总时长(以拍数为单位)。

3. `utils` 模块：工具函数集合。

    - `note_to_freq`：将音符对象转换为频率。
    - `basic_wave_gen`：生成基本波形。
    - `basic_drum_gen`：生成基本鼓声。

4. `channelgen`模块：通道生成器。

    - `generate_wave`： 生成波形通道。
    - `generate_drum`： 生成鼓声通道。

5. `sound`模块：后处理与播放。

    - `post_processing`: 混音、裁剪、量化等。
    - `play`: 使用`sounddevice`播放音频。

### 更新记录

#### 0.3.0

- 将noice从波形移动至鼓声，保持一致的创建方式。
- 更新README.md以符合类型标注。

#### 0.3.1

- 修复了音符与midi音符的映射错误。

#### 0.3.2

- 修改了混音基准长度的计算方法。
- 将sound模块的函数改为不能传位置参数

#### 0.4.0

- 增加了Melody类，用于按开始位置拼接短音片段。
