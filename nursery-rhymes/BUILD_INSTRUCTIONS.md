# Nursery-Rhyme Shorts — pickup instructions for a new session

This folder lets a fresh Claude Code session continue the kids' nursery-rhyme
Shorts project without the original chat history.

## Context
- Backend: **Higgsfield** MCP, model **veo3_1** (Veo 3.1 fast), 9:16, 8s/clip, ~22 credits each.
- Locked style: bright glossy **3D Cocomelon** (huge sparkly eyes, squishy toy-like, candy colors).
- Music tip: front-load the song demand in the prompt ("A joyful children's nursery-rhyme SONG
  plays throughout with clear sung sing-along vocals... this audio is essential and must be present.").
- All rendered clip URLs are in `CLIP_LIBRARY.md`. Clips also live in the user's Higgsfield account.

## The 30-second short the user wants
4 clips × 8s ≈ 32s, ordered for the strongest hook:
1. Wheels on the Bus (animals)  2. Itsy Bitsy Spider  3. Five Little Ducks  4. Bingo

## How to build it (run in THIS session)
Requires ffmpeg + curl and the **claudeskills + CDN** environment (CDN host allowlisted).
```bash
bash nursery-rhymes/make_30s_short.sh   # -> nursery_30s_short.mp4
```
If ffmpeg is missing: `sudo apt-get update || true && sudo apt-get install -y ffmpeg`
Then send the resulting `nursery_30s_short.mp4` to the user with SendUserFile.

## Other tools here
- `stitch_compilation.sh <dir> <out>` — concatenate any folder of clips into one vertical video.
- `CLIP_LIBRARY.md` — every clip URL (14 from batch 1; batch 2/3 in the user's Higgsfield account).

## Remaining rhymes not yet generated (optional)
Are You Sleeping · Hey Diddle Diddle · ABC Song · Miss Polly Had a Dolly
(plus confirm batch-2: A-tisket, Farmer in the Dell, Hickory Dickory, Pat-a-Cake,
Johny Johny, Baa Baa Black Sheep, Ten in the Bed, Muffin Man)
