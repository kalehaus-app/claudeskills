#!/usr/bin/env python3
"""Karaoke .ass for the 14-clip Finger Family video. Each clip is 8s, clips
play back-to-back. Greet/action clips have two sung lines; intro/finale one.
Word-highlight timing is estimated (AI-generated vocals)."""

CLIP_LEN = 8.0

# Each entry: (line1, line2 or None)
CLIPS = [
    ("Finger family, finger family,", "sing along with me!"),
    ("Daddy finger, daddy finger, where are you?", "Here I am, here I am! How do you do?"),
    ("Daddy finger, daddy finger, what do you do?", "Exercise, exercise, that's what I do!"),
    ("Mommy finger, mommy finger, where are you?", "Here I am, here I am! How do you do?"),
    ("Mommy finger, mommy finger, what do you do?", "Lots of work, lots of work, that's what I do!"),
    ("Brother finger, brother finger, where are you?", "Here I am, here I am! How do you do?"),
    ("Brother finger, brother finger, what do you do?", "Dinosaur, dinosaur, that's what I do!"),
    ("Grandpa finger, grandpa finger, where are you?", "Here I am, here I am! How do you do?"),
    ("Grandpa finger, grandpa finger, what do you do?", "Fixing things, fixing things, that's what I do!"),
    ("Grandma finger, grandma finger, where are you?", "Here I am, here I am! How do you do?"),
    ("Grandma finger, grandma finger, what do you do?", "Baking cakes, baking cakes, that's what I do!"),
    ("Sister finger, sister finger, where are you?", "Here I am, here I am! How do you do?"),
    ("Sister finger, sister finger, what do you do?", "Muddy puddles, muddy puddles, that's what I do!"),
    ("We are the finger family!", "We love you!"),
]

L1_START, L1_END = 0.5, 4.0
L2_START, L2_END = 4.0, 7.4
# single-line clips: span the whole sung window
SINGLE_START, SINGLE_END = 0.6, 7.2


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
Style: Sing, Arial Rounded MT Bold, 74, &H00FFFFFF, &H0033E0FF, &H00202020, &H64000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 5, 3, 2, 80, 80, 70, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def main():
    out = [HEADER]
    for i, (l1, l2) in enumerate(CLIPS):
        base = i * CLIP_LEN
        if l2 is None:
            s, e = base + SINGLE_START, base + SINGLE_END
            txt = "{\\an2\\pos(960,1000)}" + karaoke_line(l1.split(), s, e)
            out.append(f"Dialogue: 0,{fmt(s)},{fmt(e)},Sing,,0,0,0,,{txt}")
        else:
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
