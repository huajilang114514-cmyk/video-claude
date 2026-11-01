"""Stand-ins for the gitignored ai_history/images/* (only the 6 files the code opens unguarded).

The renderer guards the *card* photos with has_img(), but three things open files unconditionally:
  * ERAS  (ai_history_film.py:712)  -> 5 era backdrops, grayscale, blurred, 8-12 % opacity
  * diffusion_arrays (:1823)        -> turing_aged16.jpg, only when the Stable Diffusion node is on screen
Without these files the very first frame raises FileNotFoundError. They are replaced by dark,
low-contrast plates so the layers keep their structure and the film reads as "no photographs".
"""
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.normpath(os.path.join(HERE, "..", "ai_history", "images"))
os.makedirs(IMG, exist_ok=True)
ERAS = ["eniac.jpg", "symbolics_lisp_chm.jpg", "sun_e3000_cluster.jpg", "gpu_gtx1060_rear.jpg",
        "wmf_servers_2012.jpg"]
SEED = {"turing_aged16.jpg": 11}


def plate(path, seed, size=(1200, 900), base=(20, 18, 15)):
    """Dark, slightly noisy, top-lit plate: reads as texture at 10 % opacity, as an empty frame in a card."""
    rng = np.random.default_rng(seed)
    w, h = size
    h8, w8 = -(-h // 8), -(-w // 8)                      # ceil: the tile block may be trimmed below
    a = np.array(base, float)[None, None, :] + rng.normal(0, 4.0, (h8, w8, 1))
    a = np.repeat(np.repeat(a, 8, 0), 8, 1)[:h, :w]
    yy = np.linspace(0, 1, h)[:, None, None]
    a = a * (1.0 - 0.35 * yy)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path)


for i, name in enumerate(ERAS):
    plate(os.path.join(IMG, name), 100 + i)
for name, seed in SEED.items():
    plate(os.path.join(IMG, name), seed, size=(640, 800), base=(26, 24, 21))
print("placeholders:", len(ERAS) + len(SEED), "files in", IMG)
