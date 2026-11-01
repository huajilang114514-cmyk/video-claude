"""Rebuild ai_history/bgm/bgm_v3.beats.csv (gitignored: the song is not in the repo).

The beat map was originally produced by manim/sfx/analyze_bgm.py from bgm_v3.wav. Without the song we
reconstruct the *grid* it produced. The song is constant-tempo: the 56 hard-coded node times in
ai_history_film.py:B(..) are all downbeats, and a least-squares fit of t = t0 + k*T over them gives

    t0 = 1.37978 s, T = 0.966021 s (62.11 BPM), RMSE 7.8 ms = 0.23 frame @30 fps

so the grid below reproduces every node / window / closing line to within a quarter frame.
Only used because there is no audio in this render.
"""
import csv
import os

T0, BEAT, CYCLE = 1.37978, 0.966021, 294.558   # phase, seconds per beat, song length
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "ai_history", "bgm"))
os.makedirs(OUT, exist_ok=True)

rows, k = [], 0
while True:
    t = T0 + k * BEAT
    if t > CYCLE:
        break
    rows.append((t, k // 4 + 1, k % 4 + 1))
    k += 1
path = os.path.join(OUT, "bgm_v3.beats.csv")
with open(path, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["t", "bar", "beat_in_bar", "strength", "loud_db"])
    for i, (t, bar, pos) in enumerate(rows):
        w.writerow([f"{t:.3f}", bar, pos, "1.000", "0.0"])
print(f"wrote {path}: {len(rows)} beats over {CYCLE}s, downbeat every 4 beats from {T0:.3f}s")
