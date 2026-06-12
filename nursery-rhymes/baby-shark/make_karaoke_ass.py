#!/usr/bin/env python3
"""Vertical (9:16) karaoke .ass for the 4-clip Baby Shark Short. Each clip 8s."""

CLIP_LEN = 8.0

CLIPS = [
    ("Baby shark,", "doo doo doo doo doo doo!"),
    ("Mama shark,", "doo doo doo doo doo doo!"),
    ("Papa shark,", "doo doo doo doo doo doo!"),
    ("Bye bye sharks,", "doo doo doo doo doo doo!"),
]

L1_START, L1_END = 0.4, 3.8
L2_START, L2_END = 3.8, 7.6


def fmt(t):
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60);   t -= m * 60
    s = int(t); cs = int(round((t - s) * 100))
    if cs == 100:
        cs = 0; s += 1
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def karaoke_line(words, start, end):
    total = int(round((end - start) * 100))
    weights = [max(2, len(w)) for w in words]
    wsum = sum(weights)
    durs = [max(8, int(round(total * w / wsum))) for w in weights]
    durs[-1] += total - sum(durs)
    return "".join(f"{{\\k{d}}}{w} " for d, w in zip(durs, words)).rstrip()


# Vertical canvas 1080x1920; big bold captions in the lower third (above the
# YouTube Shorts UI overlap zone).
HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sing, Arial Rounded MT Bold, 76, &H00FFFFFF, &H0033E0FF, &H00202020, &H64000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 6, 4, 2, 60, 60, 70, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def main():
    out = [HEADER]
    for i, (l1, l2) in enumerate(CLIPS):
        base = i * CLIP_LEN
        s1, e1 = base + L1_START, base + L1_END
        s2, e2 = base + L2_START, base + L2_END
        t1 = "{\\an2\\pos(540,1480)}" + karaoke_line(l1.split(), s1, e1)
        t2 = "{\\an2\\pos(540,1580)}" + karaoke_line(l2.split(), s2, e2)
        out.append(f"Dialogue: 0,{fmt(s1)},{fmt(e1)},Sing,,0,0,0,,{t1}")
        out.append(f"Dialogue: 0,{fmt(s2)},{fmt(e2)},Sing,,0,0,0,,{t2}")
    with open("karaoke.ass", "w") as f:
        f.write("\n".join(out) + "\n")
    print("wrote karaoke.ass")


if __name__ == "__main__":
    main()
