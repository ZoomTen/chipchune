from chipchune.furnace.module import FurnaceModule, FurnacePattern
from chipchune.furnace.enums import ChipType
from chipchune.interchange.enums import InterNote
import chipchune.utils.conversion as convert
from typing import cast, List

inter_note_to_smps = {
    InterNote.__: "nRst",
    InterNote.Off: "nRst",
    InterNote.OffRel: "nRst",
    InterNote.Rel: "nRst",
    InterNote.C_: "nC",
    InterNote.Cs: "nCs",
    InterNote.D_: "nD",
    InterNote.Ds: "nEb",
    InterNote.E_: "nE",
    InterNote.F_: "nF",
    InterNote.Fs: "nFs",
    InterNote.G_: "nG",
    InterNote.Gs: "nAb",
    InterNote.A_: "nA",
    InterNote.As: "nBb",
    InterNote.B_: "nB",
}

def fur2smps(module: FurnaceModule, title: str) -> List[str]:
    if not (
        len(module.chips.list) > 1 and
        module.chips.list[0].type == ChipType.YM2612 and 
        module.chips.list[1].type == ChipType.SMS
    ):
        raise Exception("Not a (Furnace) Genesis module")
    
    lines: List[str] = []
    
    lines += [
        "%s_Header:" % title,

        # Sonic 3&K track
        "\tsmpsHeaderStartSong 3",

        "\tsmpsHeaderVoice S3_UVB",
        "\tsmpsHeaderChan 6, 3",
        
        # TODO
        "\tsmpsHeaderTempo 6, $38",
        "\tsmpsHeaderDAC %s_DAC, 0, $a" % title,
        "\tsmpsHeaderFM %s_FM0, 0, 0" % title,
        "\tsmpsHeaderFM %s_FM1, 0, 0" % title,
        "\tsmpsHeaderFM %s_FM2, 0, 0" % title,
        "\tsmpsHeaderFM %s_FM3, 0, 0" % title,
        "\tsmpsHeaderFM %s_FM4, 0, 0" % title,
        "\tsmpsHeaderPSG %s_PSG6, 0, 0, 0, sTone_0C" % title,
        "\tsmpsHeaderPSG %s_PSG7, 0, 0, 0, sTone_0C" % title,
        "\tsmpsHeaderPSG %s_PSG9, 0, 0, 0, sTone_0C" % title,
    ]
    
    for i in range(module.get_num_channels()):
        order = module.subsongs[0].order[i]
        if i == 8: # ignored
            pass
        else:
            lines += ["",""]
            if i < 5: # FM channels
                lines += ["%s_FM%d:" % (title, i)]
                lines += [
                    "\tsmpsCall %s_FM%d_%02x" % (
                        title, i, ord_num
                    )
                    for ord_num in order
                ]
            elif i == 5: # DAC
                lines += ["%s_DAC:" % (title)]
                lines += [
                    "\tsmpsCall %s_DAC_%02x" % (
                        title, ord_num
                    )
                    for ord_num in order
                ]
            else: # PSG channels
                lines += ["%s_PSG%d:" % (title, i)]
                lines += [
                    "\tsmpsCall %s_PSG%d_%02x" % (
                        title, i, ord_num
                    )
                    for ord_num in order
                ]
            lines += ["\tsmpsStop"]

            avail_patterns = filter(
                lambda x: (
                    x.channel == i and
                    x.subsong == 0
                ),
                module.patterns
            )
            for p in avail_patterns:
                lines += [""]
                if i < 5: # FM channels
                    lines += [
                        "%s_FM%d_%02x:" % (
                            title, i, p.index
                        )
                    ]
                elif i == 5: # DAC
                    lines += [
                        "%s_DAC_%02x:" % (
                            title, p.index
                        )
                    ]
                else: # PSG channels
                    lines += [
                        "%s_PSG%d_%02x:" % (
                            title, i, p.index
                        )
                    ]
                sequence = convert.pattern_to_sequence(p)
                cur_instrument = -1
                cur_volume = -1
                #print(p)
                for s in sequence:
                    if s.volume != cur_volume:
                        cur_volume = s.volume
                        lines += [
                            "\tsmpsSetVol %d" % (cur_volume - 10)
                        ]
                    if (
                        s.instrument != -1 and
                        s.instrument != cur_instrument
                    ):
                        cur_instrument = s.instrument
                        lines += [
                            "\tsmpsSetvoice %d" % cur_instrument
                        ]

                    note = inter_note_to_smps[s.note]
                    if note != "nRst":
                        note += str(s.octave)
                    
                    lines += [
                        #"\t;%s" % str(s),
                        "\tdc.b %s, %d" % (
                            note,
                            s.length
                        )
                    ]
                lines += ["\tsmpsReturn"]
    return lines

module = FurnaceModule("files/rocky_mountain.197.fur")
print("\n".join(fur2smps(module, "RockyMtn1")))

# pattern = module.get_pattern(3, 1, 0)

# for i in convert.pattern_to_sequence(pattern):
#     print(i)