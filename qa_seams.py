#!/usr/bin/env python3
"""Seam QA for the Meridian Nine camera chain.

The chain matches luminance rather than content at each seam (six different photographs
cannot hand off identical pixels), so the check is: does leg i's LAST frame land on the
same value and flatness as leg i+1's FIRST frame? A seam fails if the two differ enough
in mean colour that the crossfade would read as a colour shift, or if either side is
still busy with detail when it should have settled onto a flat value.
"""

import os
import subprocess
import sys

import numpy as np
from PIL import Image

VID = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site", "assets", "vid")
TMP = "/tmp/m9qa"

# Mean-channel difference above this reads as a visible colour shift across the dissolve.
DELTA_FAIL = 12.0
DELTA_WARN = 6.0
# Per-channel std above this means the frame still has structure where it should be flat.
FLAT_WARN = 26.0


def grab(clip: str, last: bool) -> np.ndarray:
    os.makedirs(TMP, exist_ok=True)
    tag = "last" if last else "first"
    out = os.path.join(TMP, "%s_%s.png" % (os.path.basename(clip)[:-4], tag))
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if last:
        cmd += ["-sseof", "-0.08", "-i", clip]
    else:
        cmd += ["-ss", "0", "-i", clip]
    cmd += ["-frames:v", "1", out]
    subprocess.run(cmd, check=True)
    return np.asarray(Image.open(out).convert("RGB"), dtype=np.float32)


def main() -> int:
    legs = [os.path.join(VID, "leg%d.mp4" % i) for i in range(1, 7)]
    missing = [l for l in legs if not os.path.exists(l)]
    if missing:
        print("missing clips: %s" % ", ".join(os.path.basename(m) for m in missing))
        return 2

    worst = "ok"
    print("%-9s %-22s %-22s %8s  %s" % ("seam", "leg out (mean rgb)", "leg in (mean rgb)", "delta", "verdict"))
    for i in range(5):
        a = grab(legs[i], last=True)
        b = grab(legs[i + 1], last=False)
        ma, mb = a.reshape(-1, 3).mean(0), b.reshape(-1, 3).mean(0)
        delta = float(np.abs(ma - mb).max())
        flat = max(float(a.reshape(-1, 3).std(0).max()), float(b.reshape(-1, 3).std(0).max()))

        if delta > DELTA_FAIL:
            verdict, worst = "FAIL colour shift", "fail"
        elif delta > DELTA_WARN or flat > FLAT_WARN:
            verdict = "warn"
            worst = "warn" if worst == "ok" else worst
        else:
            verdict = "ok"
        if flat > FLAT_WARN:
            verdict += " (still detailed, std %.0f)" % flat

        print("%-9s %-22s %-22s %8.1f  %s" % (
            "%d->%d" % (i + 1, i + 2),
            "(%3.0f,%3.0f,%3.0f)" % tuple(ma),
            "(%3.0f,%3.0f,%3.0f)" % tuple(mb),
            delta, verdict))

    print("\noverall: %s" % worst)
    return 0 if worst != "fail" else 1


if __name__ == "__main__":
    sys.exit(main())
