#!/usr/bin/env python3
"""Karaoke .ass for the 8-clip Poo Poo song. Each clip is 8s, back-to-back.
Word-highlight timing is estimated (AI-generated vocals)."""

CLIP_LEN = 8.0

# (line1, line2) per clip, in final video order
CLIPS = [
    ("What's brown and smelly,", "comes from your belly, out into the loo?"),
    ("Can be big or small, hard or soft,", "and different colours too."),
    ("Poo poo, poo poo, poo poo in the loo loo!", "Poo poo, poo poo, everyone needs to poo!"),
    ("From little bugs to birds above,", "and big animals too."),
    ("Like elephants and tall giraffes,", "cows and kangaroos!"),
    ("Poo poo, poo poo, poo poo in the loo loo!", "Poo poo, poo poo, everyone needs to poo!"),
    ("What goes in must come out, you can't deny the facts.", "Everyone poos, poo poo smells, it's made of this and that."),
    ("Poo poo, poo poo, poo poo in the loo loo!", "Everyone needs to poo!"),
]

L1_START, L1_END = 0.5, 4.0
L2_START, L2_END = 4.0, 7.4


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


HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sing, Arial Rounded MT Bold, 72, &H00FFFFFF, &H0033E0FF, &H00202020, &H64000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 5, 3, 2, 80, 80, 70, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def main():
    out = [HEADER]
    for i, (l1, l2) in enumerate(CLIPS):
        base = i * CLIP_LEN
        s1, e1 = base + L1_START, base + L1_END
        s2, e2 = base + L2_START, base + L2_END
        t1 = "{\\an2\\pos(960,930)}" + karaoke_line(l1.split(), s1, e1)
        t2 = "{\\an2\\pos(960,1010)}" + karaoke_line(l2.split(), s2, e2)
        out.append(f"Dialogue: 0,{fmt(s1)},{fmt(e1)},Sing,,0,0,0,,{t1}")
        out.append(f"Dialogue: 0,{fmt(s2)},{fmt(e2)},Sing,,0,0,0,,{t2}")
    with open("karaoke.ass", "w") as f:
        f.write("\n".join(out) + "\n")
    print("wrote karaoke.ass")


if __name__ == "__main__":
    main()
