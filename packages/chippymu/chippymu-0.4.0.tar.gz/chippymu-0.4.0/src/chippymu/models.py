"""
定义一些基础类型
"""

from enum import Enum


class WaveType(str, Enum):
    """
    几种波形
    """

    SINE = "sine"
    SQUARE = "square"
    TRIANGLE = "triangle"
    SAWTOOTH = "sawtooth"
    # 移至鼓
    # NOISE = "noise"


class DrumType(str, Enum):
    """
    几种鼓声
    """

    KICK = "kick"
    SNARE = "snare"
    HIHAT = "hihat"
    NOICE = "noice"


class Note(int, Enum):
    """
    音符
    """

    C0 = 48
    C0_SHARP = 49
    D0 = 50
    D0_SHARP = 51
    E0 = 52
    F0 = 53
    F0_SHARP = 54
    G0 = 55
    G0_SHARP = 56
    A0 = 57
    A0_SHARP = 58
    B0 = 59

    C1 = 60
    C1_SHARP = 61
    D1 = 62
    D1_SHARP = 63
    E1 = 64
    F1 = 65
    F1_SHARP = 66
    G1 = 67
    G1_SHARP = 68
    A1 = 69
    A1_SHARP = 70
    B1 = 71

    C2 = 72
    C2_SHARP = 73
    D2 = 74
    D2_SHARP = 75
    E2 = 76
    F2 = 77
    F2_SHARP = 78
    G2 = 79
    G2_SHARP = 80
    A2 = 81
    A2_SHARP = 82
    B2 = 83

    C3 = 84
    C3_SHARP = 85
    D3 = 86
    D3_SHARP = 87
    E3 = 88
    F3 = 89
    F3_SHARP = 90
    G3 = 91
    G3_SHARP = 92
    A3 = 93
    A3_SHARP = 94
    B3 = 95

    C4 = 96
    C4_SHARP = 97
    D4 = 98
    D4_SHARP = 99
    E4 = 100
    F4 = 101
    F4_SHARP = 102
    G4 = 103
    G4_SHARP = 104
    A4 = 105
    A4_SHARP = 106
    B4 = 107


class Melody(list):
    """
    音阶类，用于生成音阶和音阶操作
    """

    def __init__(
        self,
        *,
        basic_melody: list[tuple[float, int | Note | DrumType, float]] | None = None,
    ):
        """
        类初始化

        参数：
            - basic_melody: 基础音阶
        """
        init_melody: list[tuple[float, int | Note | DrumType, float]] = []
        if basic_melody is not None:
            init_melody = basic_melody

        super().__init__(init_melody)

    def apm(
        self, mel: list[tuple[float, int | Note | DrumType, float]], start_time: float
    ):
        """
        添加音阶

        参数：
            - mel: 音阶
            - start_time: 音阶开始时间
        """
        for time, note, dur in mel:
            self.append([time + start_time, note, dur])
        return self
