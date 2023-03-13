from dataclasses import dataclass, field
from typing import Tuple, List, TypedDict, Any, Union, Dict

from .enums import (
    ChipType, LinearPitch, LoopModality, DelayBehavior, JumpTreatment, InputPortSet, OutputPortSet,
    InstrumentType, MacroCode, OpMacroCode, MacroType, MacroItem, GBHwCommand, WaveFX, ESFilterMode,
    SNESSusMode, GainMode, Note
)


# modules
@dataclass
class ChipInfo:
    """
    Data for a single chip defn.
    """
    type: ChipType
    #: shall be a simple dict, no enums needed
    flags: Dict[str, Any] = field(default_factory=dict)
    panning = 0.0
    surround = 0.0  # chip front/rear balance
    volume = 1.0


@dataclass
class ModuleMeta:
    """
    Module metadata.
    """
    name = ''
    name_jp = ''
    author = ''
    author_jp = ''
    album = ''
    album_jp = ''
    sys_name = 'Sega Genesis/Mega Drive'
    sys_name_jp = ''
    comment = ''
    version = 0
    tuning = 440.0


@dataclass
class TimingInfo:
    """
    Timing information for a single subsong.
    """
    arp_speed = 1
    clock_speed = 60.0
    highlight: Tuple[int, int] = (4, 16)
    speed: Tuple[int, int] = (0, 0)
    timebase = 1
    virtual_tempo: Tuple[int, int] = (150, 150)


@dataclass
class ChipList:
    """
    Information about chips used in the module.
    """
    list: List[ChipInfo] = field(default_factory=list)
    master_volume = 2.0


@dataclass(repr=False)
class ChannelDisplayInfo:
    """
    Relating to channel display in Pattern and Order windows.
    """
    name = ''
    abbreviation = ''
    collapsed = False
    shown = True

    def __repr__(self) -> str:
        return "ChannelDisplayInfo(name='%s', abbreviation='%s', collapsed=%s, shown=%s)" % (
            self.name,
            self.abbreviation,
            self.collapsed,
            self.shown
        )


@dataclass
class ModuleCompatFlags:
    """
    Module compatibility flags, a.k.a. "The Motherload"

    Default values correspond with fileOps.cpp in the furnace src.
    """

    # compat 1

    limit_slides: bool = False
    linear_pitch: LinearPitch = LinearPitch.FULL_LINEAR
    loop_modality: LoopModality = LoopModality.DO_NOTHING
    proper_noise_layout: bool = True
    wave_duty_is_volume: bool = False
    reset_macro_on_porta: bool = False
    legacy_volume_slides: bool = False
    compatible_arpeggio: bool = False
    note_off_resets_slides: bool = True
    target_resets_slides: bool = True
    arpeggio_inhibits_portamento: bool = False
    wack_algorithm_macro: bool = False
    broken_shortcut_slides: bool = False
    ignore_duplicates_slides: bool = False
    stop_portamento_on_note_off: bool = False
    continuous_vibrato: bool = False
    broken_dac_mode: bool = False
    one_tick_cut: bool = False
    instrument_change_allowed_in_porta: bool = True
    reset_note_base_on_arpeggio_stop: bool = True

    # compat 2 (>= dev70)

    broken_speed_selection: bool = False
    no_slides_on_first_tick: bool = False
    next_row_reset_arp_pos: bool = False
    ignore_jump_at_end: bool = False
    buggy_portamento_after_slide: bool = False
    gb_ins_affects_env: bool = True
    shared_extch_state: bool = True
    ignore_outside_dac_mode_change: bool = False
    e1e2_takes_priority: bool = False
    new_sega_pcm: bool = True
    weird_fnum_pitch_slides: bool = False
    sn_duty_resets_phase: bool = False
    linear_pitch_macro: bool = True
    pitch_slide_speed_in_linear: int = 4
    old_octave_boundary: bool = False
    disable_opn2_dac_volume_control: bool = False
    new_volume_scaling: bool = True
    volume_macro_lingers: bool = True
    broken_out_vol: bool = False
    e1e2_stop_on_same_note: bool = False
    broken_porta_after_arp: bool = False
    sn_no_low_periods: bool = False
    cut_delay_effect_policy: DelayBehavior = DelayBehavior.LAX
    jump_treatment: JumpTreatment = JumpTreatment.ALL_JUMPS
    auto_sys_name: bool = True
    disable_sample_macro: bool = False
    broken_out_vol_2: bool = False
    old_arp_strategy: bool = False

    # not-a-compat (>= dev135)

    auto_patchbay: bool = True

    # compat 3 (>= dev138)

    broken_porta_during_legato: bool = False


@dataclass
class SubSong:
    """
    Information on a single subsong.
    """
    name: str = ''
    comment: str = ''
    speed_pattern: List[int] = field(default_factory=lambda: [6])
    grooves: List[List[int]] = field(default_factory=list)
    timing: TimingInfo = TimingInfo()
    pattern_length = 64
    order: Dict[int, List[int]] = field(default_factory=lambda: {
        0: [0], 1: [0], 2: [0], 3: [0], 4: [0],
        5: [0], 6: [0], 7: [0], 8: [0], 9: [0]
    })
    effect_columns: List[int] = field(default_factory=lambda: [
        1 for _ in range(
            ChipType.YM2612.channels + ChipType.SMS.channels
        )
    ])
    channel_display: List[ChannelDisplayInfo] = field(default_factory=lambda: [
        ChannelDisplayInfo() for _ in range(
            ChipType.YM2612.channels + ChipType.SMS.channels
        )
    ])


@dataclass
class FurnaceRow:
    note: Note
    octave: int
    instrument: int
    volume: int
    effects: List[Tuple[int, int]] = field(default_factory=list)

    def as_clipboard(self) -> str:
        """
        Renders the selected row in Furnace clipboard format (without header!)

        :return: Furnace clipboard data
        """
        note_maps = {
            Note.Cs: "C#",
            Note.D_: "D-",
            Note.Ds: "D#",
            Note.E_: "E-",
            Note.F_: "F-",
            Note.Fs: "F#",
            Note.G_: "G-",
            Note.Gs: "G#",
            Note.A_: "A-",
            Note.As: "A#",
            Note.B_: "B-",
            Note.C_: "C-",
        }
        if self.note == Note.OFF:
            note_str = "OFF"
        elif self.note == Note.OFF_REL:
            note_str = "==="
        elif self.note == Note.REL:
            note_str = "REL"
        elif self.note == Note.__:
            note_str = "..."
        else:
            note_str = "%s%d" % (note_maps[self.note], self.octave)

        vol = ".." if self.volume==0xffff else "%02X" % self.volume
        ins = ".." if self.instrument==0xffff else "%02X" % self.instrument

        rep_str = "%s%s%s"

        for fx in self.effects:
            cmd, val = fx
            cmd_str = ".." if cmd == 0xffff else "%02X" % cmd
            val_str = ".." if val == 0xffff else "%02X" % val
            rep_str += "%s%s" % (cmd_str, val_str)

        return rep_str % (
            note_str,
            ins, vol
        ) + "|"

    def __str__(self) -> str:
        if self.note == Note.OFF:
            note_str = "OFF"
        elif self.note == Note.OFF_REL:
            note_str = "==="
        elif self.note == Note.REL:
            note_str = "///"
        elif self.note == Note.__:
            note_str = "---"
        else:
            note_str = "%s%d" % (self.note, self.octave)

        vol = "--" if self.volume==0xffff else "%02x" % self.volume
        ins = "--" if self.instrument==0xffff else "%02x" % self.instrument

        rep_str = "row data: %s %s %s"

        for fx in self.effects:
            cmd, val = fx
            cmd_str = "--" if cmd == 0xffff else "%02x" % cmd
            val_str = "--" if val == 0xffff else "%02x" % val
            rep_str += " %s%s" % (cmd_str, val_str)

        return "<" + rep_str % (
            note_str,
            ins, vol
        ) + ">"


@dataclass
class FurnacePattern:
    channel: int = 0
    index: int = 0
    subsong: int = 0
    data: List[FurnaceRow] = field(default_factory=list)  # yeah...
    name: str = ""

    def as_clipboard(self) -> str:
        """
        Renders the selected pattern in Furnace clipboard format.

        :return: Furnace clipboard data
        """
        return "org.tildearrow.furnace - Pattern Data\n0\n" + "\n".join([x.as_clipboard() for x in self.data])

    def __str__(self) -> str:
        return "<Furnace pattern %s for ch.%02d of subsong %02d>" % (
            self.name if len(self.name) > 0 else "%02x" % self.index,
            self.channel,
            self.subsong
        )


class InputPatchBayEntry(TypedDict):
    """
    A patch that has an "input" connector.
    """
    set: InputPortSet
    port: int


class OutputPatchBayEntry(TypedDict):
    """
    A patch that has an "output" connector.
    """
    set: OutputPortSet
    port: int


@dataclass
class PatchBay:
    """
    A single patchbay connection.
    """
    source: OutputPatchBayEntry
    dest: InputPatchBayEntry


# instruments
@dataclass
class InsFeatureAbstract:
    _code: str = field(init=False)

    def __post_init__(self) -> None:
        if len(self._code) != 2:
            raise ValueError('No code defined for this instrument feature')

    # def serialize(self) -> bytes:
    #     raise Exception('Method serialize() has not been overridden...')


@dataclass
class InsFeatureName(InsFeatureAbstract, str):
    _code = 'NA'
    name: str = ''

    def __str__(self) -> str:
        return self.name


@dataclass
class InsMeta:
    version: int = 143
    type: InstrumentType = InstrumentType.FM_4OP


@dataclass
class InsFMOperator:
    am: bool = False
    ar: int = 0
    dr: int = 0
    mult: int = 0
    rr: int = 0
    sl: int = 0
    tl: int = 0
    dt2: int = 0
    rs: int = 0
    dt: int = 0
    d2r: int = 0
    ssg_env: int = 0
    dam: int = 0
    dvb: int = 0
    egt: bool = False
    ksl: int = 0
    sus: bool = False
    vib: bool = False
    ws: int = 0
    ksr: bool = False
    enable: bool = True
    kvs: int = 2


@dataclass
class InsFeatureFM(InsFeatureAbstract):
    _code = 'FM'
    alg: int = 0
    fb: int = 4
    fms: int = 0
    ams: int = 0
    fms2: int = 0
    ams2: int = 0
    ops: int = 2
    opll_preset: int = 0
    op_list: List[InsFMOperator] = field(default_factory=lambda: [
        InsFMOperator(
            tl=42, ar=31, dr=8,
            sl=15, rr=3, mult=5,
            dt=5
        ),
        InsFMOperator(
            tl=48, ar=31, dr=4,
            sl=11, rr=1, mult=1,
            dt=5
        ),
        InsFMOperator(
            tl=18, ar=31, dr=10,
            sl=15, rr=4, mult=1,
            dt=0
        ),
        InsFMOperator(
            tl=2, ar=31, dr=9,
            sl=15, rr=9, mult=1,
            dt=0
        ),
    ])


@dataclass
class SingleMacro:
    kind: Union[MacroCode, OpMacroCode] = MacroCode.VOL
    mode: int = 0
    type: MacroType = MacroType.SEQUENCE
    delay: int = 0
    speed: int = 1
    open: bool = False
    data: List[Union[int, MacroItem]] = field(default_factory=list)


@dataclass
class InsFeatureMacro(InsFeatureAbstract):
    _code = 'MA'
    macros: List[SingleMacro] = field(default_factory=lambda: [SingleMacro()])


@dataclass
class InsFeatureOpr1Macro(InsFeatureMacro):
    _code = 'O1'


@dataclass
class InsFeatureOpr2Macro(InsFeatureMacro):
    _code = 'O2'


@dataclass
class InsFeatureOpr3Macro(InsFeatureMacro):
    _code = 'O3'


@dataclass
class InsFeatureOpr4Macro(InsFeatureMacro):
    _code = 'O4'


@dataclass
class GBHwSeq:
    command: GBHwCommand
    data: List[int] = field(default_factory=lambda: [0, 0])


@dataclass
class InsFeatureGB(InsFeatureAbstract):
    _code = 'GB'
    env_vol: int = 15
    env_dir: int = 0
    env_len: int = 2
    sound_len: int = 0
    soft_env: bool = False
    always_init: bool = False
    hw_seq: List[GBHwSeq] = field(default_factory=list)


@dataclass
class GenericADSR:
    a: int = 0
    d: int = 0
    s: int = 0
    r: int = 0


@dataclass
class InsFeatureC64(InsFeatureAbstract):
    _code = '64'
    tri_on: bool = False
    saw_on: bool = True
    pulse_on: bool = False
    noise_on: bool = False
    envelope: GenericADSR = GenericADSR(a=0, d=8, s=0, r=0)
    duty: int = 2048
    ring_mod: int = 0
    osc_sync: int = 0
    to_filter: bool = False
    vol_is_cutoff: bool = False
    init_filter: bool = False
    duty_is_abs: bool = False
    filter_is_abs: bool = False
    no_test: bool = False
    res: int = 0
    cut: int = 0
    hp: bool = False
    lp: bool = False
    bp: bool = False
    ch3_off: bool = False


@dataclass
class SampleMap:
    freq: int = 0
    sample_index: int = 0


@dataclass
class InsFeatureAmiga(InsFeatureAbstract):  # Sample data
    _code = 'SM'
    init_sample: int = 0
    use_note_map: bool = False
    use_sample: bool = False
    use_wave: bool = False
    wave_len: int = 31
    sample_map: List[SampleMap] = field(default_factory=lambda: [SampleMap() for _ in range(120)])


@dataclass
class InsFeatureX1010(InsFeatureAbstract):
    _code = 'X1'
    bank_slot: int = 0


@dataclass
class InsFeatureN163(InsFeatureAbstract):
    _code = 'N1'
    wave: int = -1
    wave_pos: int = 0
    wave_len: int = 32
    wave_mode: int = 3


@dataclass
class InsFeatureFDS(InsFeatureAbstract):  # Virtual Boy
    _code = 'FD'
    mod_speed: int = 0
    mod_depth: int = 0
    init_table_with_first_wave: bool = False  # compat
    mod_table: List[int] = field(default_factory=lambda: [0 for i in range(32)])


@dataclass
class InsFeatureMultiPCM(InsFeatureAbstract):
    _code = 'MP'
    ar: int = 15
    d1r: int = 15
    dl: int = 0
    d2r: int = 0
    rr: int = 15
    rc: int = 15
    lfo: int = 0
    vib: int = 0
    am: int = 0


@dataclass
class InsFeatureWaveSynth(InsFeatureAbstract):
    _code = 'WS'
    wave_indices: List[int] = field(default_factory=lambda: [0, 0])
    rate_divider: int = 1
    effect: WaveFX = WaveFX.NONE
    enabled: bool = False
    global_effect: bool = False
    speed: int = 0
    params: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    one_shot: bool = False  # not read?


@dataclass
class InsFeatureSoundUnit(InsFeatureAbstract):
    _code = 'SU'
    switch_roles: bool = False


@dataclass
class InsFeatureES5506(InsFeatureAbstract):
    _code = 'ES'
    filter_mode: ESFilterMode = ESFilterMode.LPK2_LPK1
    k1: int = 0xffff
    k2: int = 0xffff
    env_count: int = 0
    left_volume_ramp: int = 0
    right_volume_ramp: int = 0
    k1_ramp: int = 0
    k2_ramp: int = 0
    k1_slow: int = 0
    k2_slow: int = 0


@dataclass
class InsFeatureSNES(InsFeatureAbstract):
    _code = 'SN'
    use_env: bool = True
    sus: SNESSusMode = SNESSusMode.DIRECT
    gain_mode: GainMode = GainMode.DIRECT
    gain: int = 127
    d2: int = 0
    envelope: GenericADSR = GenericADSR(a=15, d=7, s=7, r=0)


@dataclass
class InsFeatureOPLDrums(InsFeatureAbstract):
    _code = 'LD'
    fixed_drums: bool = False
    kick_freq: int = 1312
    snare_hat_freq: int = 1360
    tom_top_freq: int = 448


@dataclass
class InsFeaturePointerAbstract(InsFeatureAbstract):
    _code = 'LL'
    pointers: Dict[int, int] = field(default_factory=dict)


@dataclass
class InsFeatureSampleList(InsFeaturePointerAbstract):
    _code = 'SL'


@dataclass
class InsFeatureWaveList(InsFeaturePointerAbstract):
    _code = 'WL'
