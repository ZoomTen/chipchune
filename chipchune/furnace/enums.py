from chipchune._util import EnumShowNameOnly, EnumValueEquals
from typing import Tuple


class LinearPitch(EnumShowNameOnly, EnumValueEquals):
    """
    Options for :attr:`chipchune.furnace.data_types.ModuleCompatFlags.linear_pitch`.
    """

    NON_LINEAR = 0
    ONLY_PITCH_CHANGE = 1
    FULL_LINEAR = 2


class LoopModality(EnumShowNameOnly, EnumValueEquals):
    """
    Options for :attr:`chipchune.furnace.data_types.ModuleCompatFlags.loop_modality`.
    """

    HARD_RESET_CHANNELS = 0
    SOFT_RESET_CHANNELS = 1
    DO_NOTHING = 2


class DelayBehavior(EnumShowNameOnly, EnumValueEquals):
    """
    Options for :attr:`chipchune.furnace.data_types.ModuleCompatFlags.cut_delay_effect_policy`.
    """

    STRICT = 0
    BROKEN = 1
    LAX = 2


class JumpTreatment(EnumShowNameOnly, EnumValueEquals):
    """
    Options for :attr:`chipchune.furnace.data_types.ModuleCompatFlags.jump_treatment`.
    """

    ALL_JUMPS = 0
    FIRST_JUMP_ONLY = 1
    ROW_JUMP_PRIORITY = 2


class Note(EnumShowNameOnly):
    """
    All notes recognized by Furnace
    """

    __ = 0
    Cs = 1
    D_ = 2
    Ds = 3
    E_ = 4
    F_ = 5
    Fs = 6
    G_ = 7
    Gs = 8
    A_ = 9
    As = 10
    B_ = 11
    C_ = 12
    OFF = 100
    OFF_REL = 101
    REL = 102


class MacroItem(EnumShowNameOnly):
    """
    Special values used only in this parser, to allow data editing similar to that
    of Furnace itself.
    """

    LOOP = 0
    RELEASE = 1


class MacroCode(EnumShowNameOnly, EnumValueEquals):
    """
    Marks what aspect of an instrument does a macro change.
    """

    VOL = 0
    """
    Also:
    - C64 cutoff
    """

    ARP = 1
    """
    Not applicable to MSM6258 and MSM6295.
    """

    DUTY = 2
    """
    Also:
    - AY noise freq
    - POKEY audctl
    - Mikey duty/int
    - MSM5232 group ctrl
    - Beeper/Pokemon Mini pulse width
    - T6W28 noise type
    - Virtual Boy noise length
    - PC Engine/Namco/WonderSwan noise type
    - SNES noise freq
    - Namco 163 waveform pos.
    - ES5506 filter mode
    - MSM6258/MSM6295 freq. divider
    - ADPCMA global volume
    - QSound echo level
    """

    WAVE = 3
    """
    Also:
    - OPLL patch
    - OPZ/OPM lfo1 shape
    """

    PITCH = 4

    EX1 = 5
    """
    - OPZ/OPM am depth
    - C64 filter mode
    - SAA1099 envelope
    - X1-010 env. mode
    - Namco 163 wave length
    - FDS mod depth
    - TSU cutoff
    - ES5506 filter k1
    - MSM6258 clk divider
    - QSound echo feedback
    - SNES special
    - MSM5232 group attack
    - AY8930 duty? 
    """

    EX2 = 6
    """
    - C64 resonance
    - Namco 163 wave update
    - FDS mod speed
    - TSU resonance
    - ES5506 filter k2
    - QSound echo length
    - SNES gain
    - MSM5232 group decay
    - AY3/AY8930 envelope
    """

    EX3 = 7
    """
    - C64 special
    - AY/AY8930 autoenv num
    - X1-010 autoenv num
    - Namco 163 waveload wave
    - FDS mod position
    - TSU control
    - MSM5232 noise
    """

    ALG = 8
    """
    Also:
    - AY/AY8930 autoenv den
    - X1-010 autoenv den
    - Namco 163 waveload pos
    - ES5506 control
    """

    FB = 9
    """
    Also:
    - AY8930 noise & mask
    - Namco 163 waveload len
    - ES5506 outputs
    """

    FMS = 10
    """
    Also:
    - AY8930 noise | mask
    - Namco 163 waveload trigger
    """

    AMS = 11

    PAN_L = 12

    PAN_R = 13

    PHASE_RESET = 14

    EX4 = 15
    """
    - C64 test/gate
    - TSU phase reset timer
    - FM/OPM opmask
    """

    EX5 = 16
    """
    - OPZ am depth 2
    """

    EX6 = 17
    """
    - OPZ pm depth 2
    """

    EX7 = 18
    """
    - OPZ lfo2 speed
    """

    EX8 = 19
    """
    - OPZ lfo2 shape
    """

    STOP = 255
    """
    Marks end of macro reading.
    """


class OpMacroCode(EnumShowNameOnly, EnumValueEquals):
    """
    Controls which FM parameter a macro should change.
    """

    AM = 0
    AR = 1
    DR = 2
    MULT = 3
    RR = 4
    SL = 5
    TL = 6
    DT2 = 7
    RS = 8
    DT = 9
    D2R = 10
    SSG_EG = 11
    DAM = 12
    DVB = 13
    EGT = 14
    KSL = 15
    SUS = 16
    VIB = 17
    WS = 18
    KSR = 19


class MacroType(EnumShowNameOnly):
    """
    Instrument macro type (version 120+).
    """

    SEQUENCE = 0
    ADSR = 1
    LFO = 2


class MacroSize(EnumShowNameOnly):
    """
    Type of value stored in the instrument file.
    """

    _value_: int
    num_bytes: int
    signed: bool

    UINT8: Tuple[int, int, bool] = (0, 1, False)
    INT8: Tuple[int, int, bool] = (1, 1, True)
    INT16: Tuple[int, int, bool] = (2, 2, True)
    INT32: Tuple[int, int, bool] = (3, 4, True)

    def __new__(cls, id: int, num_bytes: int, signed: bool):  # type: ignore[no-untyped-def]
        member = object.__new__(cls)
        member._value_ = id
        setattr(member, "num_bytes", num_bytes)
        setattr(member, "signed", signed)
        return member


class GBHwCommand(EnumShowNameOnly):
    """
    Game Boy hardware envelope commands.
    """

    ENVELOPE = 0
    SWEEP = 1
    WAIT = 2
    WAIT_REL = 3
    LOOP = 4
    LOOP_REL = 5


class SampleType(EnumShowNameOnly):
    """
    Sample types used in Furnace
    """

    ZX_DRUM = 0
    NES_DPCM = 1
    QSOUND_ADPCM = 4
    ADPCM_A = 5
    ADPCM_B = 6
    X68K_ADPCM = 7
    PCM_8 = 8
    SNES_BRR = 9
    VOX = 10
    PCM_16 = 16


class InstrumentType(EnumShowNameOnly):
    """
    Instrument types currently available as of version 144.
    """

    STANDARD = 0
    FM_4OP = 1
    GB = 2
    C64 = 3
    AMIGA = 4
    PCE = 5
    SSG = 6
    AY8930 = 7
    TIA = 8
    SAA1099 = 9
    VIC = 10
    PET = 11
    VRC6 = 12
    FM_OPLL = 13
    FM_OPL = 14
    FDS = 15
    VB = 16
    N163 = 17
    KONAMI_SCC = 18
    FM_OPZ = 19
    POKEY = 20
    PC_BEEPER = 21
    WONDERSWAN = 22
    LYNX = 23
    VERA = 24
    X1010 = 25
    VRC6_SAW = 26
    ES5506 = 27
    MULTIPCM = 28
    SNES = 29
    TSU = 30
    NAMCO_WSG = 31
    OPL_DRUMS = 32
    FM_OPM = 33
    NES = 34
    MSM6258 = 35
    MSM6295 = 36
    ADPCM_A = 37
    ADPCM_B = 38
    SEGAPCM = 39
    QSOUND = 40
    YMZ280B = 41
    RF5C68 = 42
    MSM5232 = 43
    T6W28 = 44
    K007232 = 45
    GA20 = 46
    POKEMON_MINI = 47
    SM8521 = 48
    PV1000 = 49


class ChipType(EnumShowNameOnly):
    """
    Furnace chip database, either planned or implemented.
    Contains console name, chip ID and number of channels.
    """

    _value_: int
    channels: int

    YMU759 = (0x01, 17)
    GENESIS = (0x02, 10)  # YM2612 + SN76489
    SMS = (0x03, 4)  # SN76489
    GB = (0x04, 4)  # LR53902
    PCE = (0x05, 6)  # HuC6280
    NES = (0x06, 5)  # RP2A03
    C64_8580 = (0x07, 4)  # SID r8580
    SEGA_ARCADE = (0x08, 13)  # YM2151 + SegaPCM
    NEO_GEO_CD = (0x09, 13)

    GENESIS_EX = (0x42, 13)  # YM2612 + SN76489
    SMS_JP = (0x43, 13)  # SN76489 + YM2413
    NES_VRC7 = (0x46, 11)  # RP2A03 + YM2413
    C64_6581 = (0x47, 3)  # SID r6581
    NEO_GEO_CD_EX = (0x49, 16)

    AY38910 = (0x80, 3)
    AMIGA = (0x81, 4)  # Paula
    YM2151 = (0x82, 8)  # YM2151
    YM2612 = (0x83, 6)  # YM2612
    TIA = (0x84, 2)
    VIC20 = (0x85, 4)
    PET = (0x86, 1)
    SNES = (0x87, 8)  # SPC700
    VRC6 = (0x88, 3)
    OPLL = (0x89, 9)  # YM2413
    FDS = (0x8A, 1)
    MMC5 = (0x8B, 3)
    N163 = (0x8C, 8)
    OPN = (0x8D, 6)  # YM2203
    PC98 = (0x8E, 16)  # YM2608
    OPL = (0x8F, 9)  # YM3526

    OPL2 = (0x90, 9)  # YM3812
    OPL3 = (0x91, 18)  # YMF262
    MULTIPCM = (0x92, 24)
    PC_SPEAKER = (0x93, 1)  # Intel 8253
    POKEY = (0x94, 4)
    RF5C68 = (0x95, 8)
    WONDERSWAN = (0x96, 4)
    SAA1099 = (0x97, 6)
    OPZ = (0x98, 8)
    POKEMON_MINI = (0x99, 1)
    AY8930 = (0x9A, 3)
    SEGAPCM = (0x9B, 16)
    VIRTUAL_BOY = (0x9C, 6)
    VRC7 = (0x9D, 6)
    YM2610B = (0x9E, 16)
    ZX_BEEPER = (0x9F, 6)  # tildearrow's engine

    YM2612_EX = (0xA0, 9)
    SCC = (0xA1, 5)
    OPL_DRUMS = (0xA2, 11)
    OPL2_DRUMS = (0xA3, 11)
    OPL3_DRUMS = (0xA4, 20)
    NEO_GEO = (0xA5, 14)
    NEO_GEO_EX = (0xA6, 17)
    OPLL_DRUMS = (0xA7, 11)
    LYNX = (0xA8, 4)
    SEGAPCM_DMF = (0xA9, 5)
    MSM6295 = (0xAA, 4)
    MSM6258 = (0xAB, 1)
    COMMANDER_X16 = (0xAC, 17)  # VERA
    BUBBLE_SYSTEM_WSG = (0xAD, 2)
    OPL4 = (0xAE, 42)
    OPL4_DRUMS = (0xAF, 44)

    SETA = (0xB0, 16)  # Allumer X1-010
    ES5506 = (0xB1, 32)
    Y8950 = (0xB2, 10)
    Y8950_DRUMS = (0xB3, 12)
    SCC_PLUS = (0xB4, 5)
    TSU = (0xB5, 8)
    YM2203_EX = (0xB6, 9)
    YM2608_EX = (0xB7, 19)
    YMZ280B = (0xB8, 8)
    NAMCO = (0xB9, 3)  # Namco WSG
    N15XX = (0xBA, 8)  # Namco 15xx
    CUS30 = (0xBB, 8)  # Namco CUS30
    MSM5232 = (0xBC, 8)
    YM2612_PLUS_EX = (0xBD, 11)
    YM2612_PLUS = (0xBE, 7)
    T6W28 = (0xBF, 4)

    PCM_DAC = (0xC0, 1)
    YM2612_CSM = (0xC1, 10)
    NEO_GEO_CSM = (0xC2, 18)  # YM2610 CSM
    YM2203_CSM = (0xC3, 10)
    YM2608_CSM = (0xC4, 20)
    YM2610B_CSM = (0xC5, 20)
    K007232 = (0xC6, 2)
    GA20 = (0xC7, 4)
    SM8521 = (0xC8, 3)
    M114S = (0xC9, 16)
    ZX_BEEPER_QUADTONE = (0xCA, 5)  # Natt Akuma's engine
    PV_1000 = (0xCB, 3)  # NEC D65010G031
    K053260 = (0xCC, 4)
    TED = (0xCD, 2)
    NAMCO_C140 = (0xCE, 24)
    NAMCO_C219 = (0xCF, 16)

    NAMCO_C352 = (0xD0, 32)
    ESFM = (0xD1, 18)
    ES5503 = (0xD2, 32)
    POWERNOISE = (0xD4, 4)
    DAVE = (0xD5, 6)
    NDS = (0xD6, 16)
    GBA = (0xD7, 2)
    GBA_MINMOD = (0xD8, 16)
    BIFURCATOR = (0xD9, 4)
    YM2610B_EX = (0xDE, 19)

    QSOUND = (0xE0, 19)

    SID2 = (0xF0, 3)  # SID2
    FIVEE01 = (0xF1, 5)  # 5E01
    PONG = (0xFC, 1)
    DUMMY = (0xFD, 1)
    RESERVED_1 = (0xFE, 1)
    RESERVED_2 = (0xFF, 1)

    def __new__(cls, id: int, channels: int):  # type: ignore[no-untyped-def]
        member = object.__new__(cls)
        member._value_ = id
        setattr(member, "channels", channels)
        return member

    def __repr__(self) -> str:
        # repr abuse
        # about as stupid as "mapping for the renderer"...
        return "%s (0x%02x), %d channel%s" % (
            self.name,
            self._value_,
            self.channels,
            "s" if self.channels != 1 else "",
        )


class InputPortSet(EnumShowNameOnly):
    """
    Devices which contain an "input" port.
    """

    SYSTEM = 0
    NULL = 0xFFF


class OutputPortSet(EnumShowNameOnly):
    """
    Devices which contain an "output" port.
    """

    CHIP_1 = 0
    CHIP_2 = 1
    CHIP_3 = 2
    CHIP_4 = 3
    CHIP_5 = 4
    CHIP_6 = 5
    CHIP_7 = 6
    CHIP_8 = 7
    CHIP_9 = 8
    CHIP_10 = 9
    CHIP_11 = 10
    CHIP_12 = 11
    CHIP_13 = 12
    CHIP_14 = 13
    CHIP_15 = 14
    CHIP_16 = 15
    CHIP_17 = 16
    CHIP_18 = 17
    CHIP_19 = 18
    CHIP_20 = 19
    CHIP_21 = 20
    CHIP_22 = 21
    CHIP_23 = 22
    CHIP_24 = 23
    CHIP_25 = 24
    CHIP_26 = 25
    CHIP_27 = 26
    CHIP_28 = 27
    CHIP_29 = 28
    CHIP_30 = 29
    CHIP_31 = 30
    CHIP_32 = 31
    PREVIEW = 0xFFD
    METRONOME = 0xFFE
    NULL = 0xFFF


class WaveFX(EnumShowNameOnly):
    """
    Used in :attr:`chipchune.furnace.data_types.InsFeatureWaveSynth.effect`.
    """

    NONE = 0

    # single waveform
    INVERT = 1
    ADD = 2
    SUBTRACT = 3
    AVERAGE = 4
    PHASE = 5
    CHORUS = 6

    # double waveform
    NONE_DUAL = 128
    WIPE = 129
    FADE = 130
    PING_PONG = 131
    OVERLAY = 132
    NEGATIVE_OVERLAY = 133
    SLIDE = 134
    MIX = 135
    PHASE_MOD = 136


class ESFilterMode(EnumShowNameOnly):
    """
    Used in :attr:`chipchune.furnace.data_types.InsFeatureES5506.filter_mode`.
    """

    HPK2_HPK2 = 0
    HPK2_LPK1 = 1
    LPK2_LPK2 = 2
    LPK2_LPK1 = 3


class GainMode(EnumShowNameOnly):
    """
    Used in :attr:`chipchune.furnace.data_types.InsFeatureSNES.gain_mode`.
    """

    DIRECT = 0
    DEC_LINEAR = 4
    DEC_LOG = 5
    INC_LINEAR = 6
    INC_INVLOG = 7


class SNESSusMode(EnumShowNameOnly):
    """
    Used in :attr:`chipchune.furnace.data_types.InsFeatureSNES.sus`.
    """

    DIRECT = 0
    SUS_WITH_DEC = 1
    SUS_WITH_EXP = 2
    SUS_WITH_REL = 3


class _FurInsImportType(EnumShowNameOnly, EnumValueEquals):
    """
    Also only used in this parser to differentiate between different types of instrument formats.
    """

    # Old format
    FORMAT_0_FILE = 0
    FORMAT_0_EMBED = 1

    # Dev127 format
    FORMAT_1_FILE = 2
    FORMAT_1_EMBED = 3


class _FurWavetableImportType(EnumShowNameOnly, EnumValueEquals):
    """
    Also only used in this parser to differentiate between different types of wavetable formats.
    """

    FILE = 0
    EMBED = 1
