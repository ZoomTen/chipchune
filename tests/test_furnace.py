from chipchune.furnace.module import FurnaceModule, PatchBay, InputPatchBayEntry, OutputPatchBayEntry
from chipchune.furnace.instrument import FurnaceInstrument
from chipchune.furnace.wavetable import FurnaceWavetable
from chipchune.furnace.data_types import InsFeatureFM, InsFeatureMacro, SingleMacro
from chipchune.furnace.enums import MacroCode
from typing import Union

import pytest

from chipchune.furnace.wavetable import FurnaceWavetable

# pytest --cov=chipchune

@pytest.fixture
def dev_70() -> FurnaceModule:
    return FurnaceModule('samples/furnace/skate_or_die.70.fur')


@pytest.fixture
def dev_143() -> FurnaceModule:
    return FurnaceModule('samples/furnace/skate_or_die.143.fur')


@pytest.fixture
def dev_181() -> FurnaceModule:
    return FurnaceModule('samples/furnace/skate_or_die.181.fur')


@pytest.fixture
def dev_140() -> FurnaceModule:
    return FurnaceModule('samples/furnace/map04.140.fur')


@pytest.fixture
def new_ins() -> FurnaceInstrument:
    return FurnaceInstrument('samples/furnace/opl1_brass.new.fui')


@pytest.fixture
def new_ins_2() -> FurnaceInstrument:
    return FurnaceInstrument('samples/furnace/bass.new.fui')


@pytest.fixture
def old_ins() -> FurnaceInstrument:
    return FurnaceInstrument('samples/furnace/opl1_brass.old.fui')


@pytest.fixture
def wav_181() -> FurnaceWavetable:
    return FurnaceWavetable('samples/furnace/skate_or_die.181.wave.1.fuw')


def test_meta(dev_70: FurnaceModule, dev_143: FurnaceModule) -> None:
    # verify correct metadata
    assert dev_70.meta.name == 'Skate or Die - Title Theme'
    assert dev_70.meta.author == "Rob Hubbard '87, cv:Zumi '22"
    assert dev_143.meta.album == ''
    assert dev_143.meta.sys_name == 'PC Engine/TurboGrafx-16 + AY-3-8910 + AY-3-8910'

    # verify integrity
    assert dev_70.meta.name == dev_143.meta.name
    assert dev_70.meta.author == dev_143.meta.author


def test_info(dev_70: FurnaceModule, dev_143: FurnaceModule) -> None:
    # verify info
    assert dev_70.meta.tuning == 440.0
    assert dev_70.subsongs[0].pattern_length == 64

    # verify integrity
    assert dev_70.meta.tuning == dev_143.meta.tuning
    assert dev_70.subsongs[0].pattern_length == dev_143.subsongs[0].pattern_length


def test_compat_flags(dev_70: FurnaceModule, dev_143: FurnaceModule) -> None:
    # make sure default compat flags match
    for k, v in dev_70.compat_flags.__dict__.items():
        assert v == dev_143.compat_flags.__dict__[k], 'compat_flags.%s does not match' % k


def test_old2new_chip_flag_convert(dev_70: FurnaceModule, dev_143: FurnaceModule) -> None:
    # make sure old chip flags are correctly converted to new ones
    for i in range(len(dev_70.chips.list)):
        for k, v in dev_70.chips.list[i].flags.items():
            if k in dev_143.chips.list[i].flags.keys():
                assert v == dev_143.chips.list[i].flags[k], 'chips.list[%d].flags["%s"] does not match' % (i, k)


@pytest.mark.skip
def test_patchbay(dev_143: FurnaceModule) -> None:
    pass


# panning and volume values are not tested due to negligible rounding errors


def test_timing(dev_70: FurnaceModule, dev_143: FurnaceModule) -> None:
    # verify dev70 info
    assert dev_70.subsongs[0].timing.clock_speed == 60.0
    assert dev_70.subsongs[0].timing.speed == (3, 3)
    assert dev_70.subsongs[0].timing.timebase == 1
    assert dev_70.subsongs[0].timing.highlight == (8, 32)

    # verify dev143 info
    assert dev_143.subsongs[0].speed_pattern == [3, 3]
    assert len(dev_143.subsongs[0].grooves) == 0
    assert dev_143.subsongs[0].timing.virtual_tempo == (150, 150)

    # verify integrity
    assert dev_70.subsongs[0].timing.clock_speed == dev_143.subsongs[0].timing.clock_speed
    assert dev_70.subsongs[0].timing.speed == dev_143.subsongs[0].timing.speed
    assert dev_70.subsongs[0].timing.timebase == dev_143.subsongs[0].timing.timebase
    assert dev_70.subsongs[0].timing.highlight == dev_143.subsongs[0].timing.highlight


def test_dev140_module(dev_140: FurnaceModule) -> None:
    assert dev_140.meta.name == 'MAP04 "Between Levels"'
    assert dev_140.meta.author == "Bobby Prince '94, cv: Zumi '23"
    assert dev_140.meta.album == 'Doom II'
    assert dev_140.meta.sys_name == 'tildearrow Sound Unit'
    assert dev_140.compat_flags.auto_sys_name is True
    assert dev_140.meta.tuning == 444.0


def test_new_ins_name(new_ins: FurnaceInstrument) -> None:
    assert new_ins.get_name() == 'Brass Lead'


def test_new_ins_has_fm(new_ins: FurnaceInstrument) -> None:
    # check for existence of fm
    fm = None
    for i in new_ins.features:
        if isinstance(i, InsFeatureFM):
            fm = i
    assert isinstance(fm, InsFeatureFM)
    assert fm.fb == 7
    assert fm.alg == 0
    assert fm.ops == 2


def test_new_ins_has_macro(new_ins_2: FurnaceInstrument) -> None:
    assert new_ins_2.get_name() == 'bass'
    mac = None
    vol = None
    res = None
    for i in new_ins_2.features:
        if isinstance(i, InsFeatureMacro):
            mac = i
    assert isinstance(mac, InsFeatureMacro)
    for j in mac.macros:
        if j.kind == MacroCode.VOL:
            vol = j
        elif j.kind == MacroCode.EX1:
            res = j
    assert vol is not None
    assert vol.data == [
        1254, 921, 819, 729, 652, 576, 537, 486
    ]
    assert res.data == [
        1
    ]


def test_if_old_instr_the_same(dev_70: FurnaceModule, dev_143: FurnaceModule) -> None:
    assert len(dev_70.instruments) == len(dev_143.instruments)
    inslens = len(dev_70.instruments)

    # get macro from A
    for e in range(inslens):
        a = dev_70.instruments[e]
        b = dev_143.instruments[e]
        assert a.get_name() == b.get_name()
        assert a.meta.type == b.meta.type
        try:
            for i in a.features:
                if type(i) is InsFeatureMacro:
                    a_vol = next(filter(
                        lambda x: x.kind == MacroCode.VOL, i.macros
                    ))
                    a_arp = next(filter(
                        lambda x: x.kind == MacroCode.ARP, i.macros
                    ))
                    a_duty = next(filter(
                        lambda x: x.kind == MacroCode.DUTY, i.macros
                    ))
                    a_wave = next(filter(
                        lambda x: x.kind == MacroCode.WAVE, i.macros
                    ))

            for i in b.features:
                if type(i) is InsFeatureMacro:
                    b_vol = next(filter(
                        lambda x: x.kind == MacroCode.VOL, i.macros
                    ))
                    b_arp = next(filter(
                        lambda x: x.kind == MacroCode.ARP, i.macros
                    ))
                    b_duty = next(filter(
                        lambda x: x.kind == MacroCode.DUTY, i.macros
                    ))
                    b_wave = next(filter(
                        lambda x: x.kind == MacroCode.WAVE, i.macros
                    ))

            assert a_vol == b_vol
            assert a_arp == b_arp
            assert a_duty == b_duty
            assert a_wave == b_wave
        except StopIteration:
            continue


def test_old_new_pettern_match(dev_143: FurnaceModule, dev_181: FurnaceModule) -> None:
    # make sure old & new patterns match
    assert dev_143.patterns == dev_181.patterns


def test_wavetables(dev_181: FurnaceModule, wav_181: FurnaceWavetable) -> None:
    # verify wavetables
    assert len(dev_181.wavetables) == 7
    assert dev_181.wavetables[1].data == wav_181.data

    assert wav_181.meta.width == 32
    assert wav_181.meta.height == 32
    assert wav_181.data == [7, 19, 31, 25, 23, 21, 19, 16, 7, 1, 0, 0, 16, 14, 25, 24,
                            23, 21, 20, 20, 17, 31, 6, 9, 11, 13, 16, 19, 20, 22, 25, 30]
