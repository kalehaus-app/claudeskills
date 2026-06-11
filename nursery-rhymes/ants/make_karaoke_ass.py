#!/usr/bin/env python3
"""Generate a karaoke-style .ass subtitle for the 10-clip Ants Go Marching video.

Each clip is 8s; clips play back-to-back, so verse N occupies [ (N-1)*8, N*8 ).
Within each clip we karaoke-highlight the two sung lines word-by-word with
estimated timing (the vocals are AI-generated, so this is a close estimate, not
frame-locked). Big, friendly, bottom-centered, with a bouncy highlight color.
"""

CLIP_LEN = 8.0  # seconds per clip

# (line1, line2) per verse
VERSES = [
    ("The ants go marching one by one, hoorah, hoorah!",   "The little one stops to suck his thumb!"),
    ("The ants go marching two by two, hoorah, hoorah!",   "The little one stops to tie his shoe!"),
    ("The ants go marching three by three, hoorah, hoorah!","The little one stops to climb a tree!"),
    ("The ants go marching four by four, hoorah, hoorah!",  "The little one stops to shut the door!"),
    ("The ants go marching five by five, hoorah, hoorah!",  "The little one stops to take a dive!"),
    ("The ants go marching six by six, hoorah, hoorah!",    "The little one stops to pick up sticks!"),
    ("The ants go marching seven by seven, hoorah, hoorah!","The little one stops to pray to heaven!"),
    ("The ants go marching eight by eight, hoorah, hoorah!","The little one stops to rollerskate!"),
    ("The ants go marching nine by nine, hoorah, hoorah!",  "The little one stops to check the time!"),
    ("The ants go marching ten by ten, hoorah, hoorah!",    "The little one stops to shout THE END!"),
]

# Timing within each 8s clip (seconds). Singing tends to start a touch in and
# leave room at the end for the "boom boom boom".
L1_START, L1_END = 0.5, 4.0
L2_START, L2_END = 4.0, 7.4


def fmt(t: float) -> str:
    h = int(t // 3600); t -= h * 3600
    m = int(t // 60);   t -= m * 60
    s = int(t)
    cs = int(round((t - s) * 100))
    if cs == 100:
        cs = 0; s += 1
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def karaoke_line(words, start, end):
    """Return an ASS karaoke fragment ({\\kNN}) distributing the window across
    words weighted by length (a rough proxy for syllables)."""
    total_cs = int(round((end - start) * 100))
    weights = [max(2, len(w)) for w in words]
    wsum = sum(weights)
    durs = [max(8, int(round(total_cs * w / wsum))) for w in weights]
    # fix rounding drift
    drift = total_cs - sum(durs)
    durs[-1] += drift
    return "".join(f"{{\\k{d}}}{w} " for d, w in zip(durs, words)).rstrip()


HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sing, Arial Rounded MT Bold, 76, &H00FFFFFF, &H0033E0FF, &H00202020, &H64000000, -1, 0, 0, 0, 100, 100, 0, 0, 1, 5, 3, 2, 80, 80, 70, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

# SecondaryColour is the pre-highlight (un-sung) color; PrimaryColour is the
# sung/highlighted color. With \k, text starts as Secondary and flips to
# Primary as it's "sung" — classic karaoke fill.


def main():
    lines = [HEADER]
    for i, (l1, l2) in enumerate(VERSES):
        base = i * CLIP_LEN
        # line 1 (upper)
        s1, e1 = base + L1_START, base + L1_END
        txt1 = "{\\an2\\pos(960,930)}" + karaoke_line(l1.split(), s1, e1)
        lines.append(f"Dialogue: 0,{fmt(s1)},{fmt(e1)},Sing,,0,0,0,,{txt1}")
        # line 2 (lower)
        s2, e2 = base + L2_START, base + L2_END
        txt2 = "{\\an2\\pos(960,1010)}" + karaoke_line(l2.split(), s2, e2)
        lines.append(f"Dialogue: 0,{fmt(s2)},{fmt(e2)},Sing,,0,0,0,,{txt2}")
    out = "\n".join(lines) + "\n"
    with open("karaoke.ass", "w") as f:
        f.write(out)
    print("wrote karaoke.ass")


if __name__ == "__main__":
    main()
