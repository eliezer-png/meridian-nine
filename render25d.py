#!/usr/bin/env python3
"""
Procedural 2.5D camera-flight renderer for the Meridian Nine scroll world.

Synthesises a forward dolly from a still by treating the scene as a single-vanishing-point
volume and warping each frame through a real pinhole magnification model:

    a point at depth Z, after the camera advances by d, magnifies by  m = Z / (Z - d)

Near pixels (small Z) magnify faster than far ones, which is parallax. Because a forward
dolly only ever magnifies, the inverse warp never opens a disocclusion hole — that is
precisely why this technique is safe for a forward-only chain and would tear if the camera
ever pulled back.

Depth is analytic, not estimated: these compositions are corridors and a path to a door, so
depth is a smooth function of radial distance from the vanishing point. No ML model required
(and none would fit on this machine).

Seams are handled by the exposure ramp described in camera-paths.md — each leg ends pushing
into a blown-out light or into black, and the next leg opens on that same value.
"""

import os
import subprocess
import sys

import numpy as np
from PIL import Image

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stills")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site", "assets", "vid")
WORK = "/tmp/m9frames"

FPS = 24
W, H = 1600, 900   # 2752px source => 1.72x zoom headroom before pixel density drops

# The camera advance is arbitrary in scale; the depth model is solved to fit it.
DOLLY = 0.10

# Per-leg camera paths. See camera-paths.md for the reasoning behind every number.
#   vp        vanishing point / dolly target, normalised (x, y)
#   mCenter   how much the TARGET grows by the end of the leg. This is the sense of
#             arrival — the doorway, the far end of the corridor, the watch.
#   mEdge     how much the NEAREST pixels grow. The gap between mEdge and mCenter IS
#             the parallax; if they were equal this would be a flat zoom.
#             Source is 2752px against a 1600px output, so up to ~1.72 holds 1:1.
#   dur       seconds
#   drift     optional (dx, dy) travel of the sampling centre — a small arc reads as
#             a partial orbit
#   settle    True = decelerate to a stop (final scene); False = hand off at speed
#   fadeIn    (r, g, b) value the leg opens from, or None
#   fadeOut   (r, g, b) value the leg ends on, or None
LEGS = [
    dict(n=1, vp=(0.500, 0.605), mCenter=1.50, mEdge=1.95, dur=8.0, drift=(0.0, 0.0),
         settle=False, fadeIn=None,            fadeOut=(255, 226, 170), skyLock=0.38),
    dict(n=2, vp=(0.330, 0.225), mCenter=1.35, mEdge=1.80, dur=8.0, drift=(0.085, 0.020),
         settle=False, fadeIn=(255, 226, 170), fadeOut=(226, 232, 238)),
    dict(n=3, vp=(0.600, 0.470), mCenter=1.40, mEdge=1.70, dur=7.0, drift=(0.020, 0.0),
         settle=False, fadeIn=(226, 232, 238), fadeOut=(238, 240, 243)),
    dict(n=4, vp=(0.420, 0.300), mCenter=1.40, mEdge=1.85, dur=7.5, drift=(-0.030, 0.0),
         settle=False, fadeIn=(238, 240, 243), fadeOut=(244, 246, 248)),
    dict(n=5, vp=(0.545, 0.355), mCenter=1.45, mEdge=1.90, dur=8.0, drift=(-0.020, 0.0),
         settle=False, fadeIn=(244, 246, 248), fadeOut=(6, 8, 11)),
    dict(n=6, vp=(0.470, 0.500), mCenter=1.18, mEdge=1.32, dur=9.0, drift=(0.030, 0.0),
         settle=True,  fadeIn=(6, 8, 11),      fadeOut=None),
]

# Fraction of a leg spent ramping to/from the seam value.
FADE_IN_FRAC = 0.09
FADE_OUT_FRAC = 0.10


def solve_depths(m_center, m_edge):
    """Given the magnification wanted at the target and at the nearest pixels, recover the
    two depths that produce them under m = Z / (Z - d). Two constraints, two unknowns."""
    z_far = DOLLY * m_center / (m_center - 1.0)
    z_near = DOLLY * m_edge / (m_edge - 1.0)
    return z_near, z_far


def depth_map(vpx, vpy, z_near, z_far, sky_lock=None):
    """Analytic depth: z_far at the vanishing point, z_near at the far corners.

    Radial distance from the vanishing point is the right proxy for these compositions —
    a corridor's floor, ceiling and side walls all recede toward the same point, so
    everything near that point is far away and everything at the frame edge is close.
    """
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xs - vpx * W) / W
    dy = (ys - vpy * H) / H
    r = np.sqrt(dx * dx + dy * dy)
    r /= r.max()
    # (1 - r) ** k shapes how quickly depth falls off away from the vanishing point.
    # k < 1 keeps more of the frame "far", which suits deep corridors.
    z = z_near + (z_far - z_near) * np.power(1.0 - r, 0.85)
    if sky_lock is not None:
        # Everything above the horizon is effectively at infinity, so it must not magnify.
        # A radial model would otherwise treat the top corners as near and swell the
        # mountains as the camera advances. Soft band to avoid a visible seam at the line.
        yn = ys / H
        band = np.clip((sky_lock - yn) / 0.10, 0.0, 1.0)
        z = z * (1 - band) + z_far * band
    return z.astype(np.float32)


def ease(t, settle):
    """Leg timing. Legs that hand off must still be moving at t=1, so they accelerate
    into the seam; only the final leg decelerates to rest."""
    if settle:
        return t * t * (3.0 - 2.0 * t)
    return 0.35 * t + 0.65 * t * t


def sample_bilinear(src, sx, sy):
    """Bilinear sample of an HxWx3 float array at float coordinates."""
    sh, sw = src.shape[:2]
    sx = np.clip(sx, 0, sw - 1.001)
    sy = np.clip(sy, 0, sh - 1.001)
    x0 = sx.astype(np.int32)
    y0 = sy.astype(np.int32)
    x1 = x0 + 1
    y1 = y0 + 1
    fx = (sx - x0)[..., None]
    fy = (sy - y0)[..., None]
    a = src[y0, x0]
    b = src[y0, x1]
    c = src[y1, x0]
    d = src[y1, x1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def render_leg(leg, preview_only=False):
    n = leg["n"]
    src_img = Image.open(os.path.join(SRC, "still_%d.png" % n)).convert("RGB")
    sw, sh = src_img.size
    src = np.asarray(src_img, dtype=np.float32)

    vpx, vpy = leg["vp"]
    z_near, z_far = solve_depths(leg["mCenter"], leg["mEdge"])
    z = depth_map(vpx, vpy, z_near, z_far, leg.get("skyLock"))
    D = DOLLY

    frames = int(round(leg["dur"] * FPS))
    outdir = os.path.join(WORK, "leg%d" % n)
    os.makedirs(outdir, exist_ok=True)

    # Output pixel grid, in normalised source coordinates.
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    px = xs / W
    py = ys / H

    idx = [0, frames // 2, frames - 1] if preview_only else range(frames)

    for i in idx:
        t = i / float(frames - 1)
        e = ease(t, leg["settle"])
        d = D * e

        # Sampling centre drifts over the leg (the partial-orbit feel).
        cx = vpx + leg["drift"][0] * e
        cy = vpy + leg["drift"][1] * e

        # Inverse warp. We know the magnification at the SOURCE pixel, not the output
        # pixel, so solve s = c + (p - c)/m(Z(s)) by fixed-point iteration. Z is smooth,
        # so three passes converge well below a pixel.
        sxn, syn = px.copy(), py.copy()
        for _ in range(3):
            zi = sample_bilinear(z[..., None], sxn * W, syn * H)[..., 0]
            m = zi / np.maximum(zi - d, 1e-3)
            sxn = cx + (px - cx) / m
            syn = cy + (py - cy) / m

        frame = sample_bilinear(src, sxn * sw, syn * sh)

        # Seam exposure ramp — the light chain from camera-paths.md.
        if leg["fadeIn"] is not None:
            k = FADE_IN_FRAC
            if t < k:
                w = 1.0 - (t / k)
                w = w * w
                frame = frame * (1 - w) + np.array(leg["fadeIn"], dtype=np.float32) * w
        if leg["fadeOut"] is not None:
            k = FADE_OUT_FRAC
            if t > 1.0 - k:
                w = (t - (1.0 - k)) / k
                w = w * w
                frame = frame * (1 - w) + np.array(leg["fadeOut"], dtype=np.float32) * w

        Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)).save(
            os.path.join(outdir, "f%05d.png" % i), compress_level=1
        )

    return outdir, frames


def encode(n, outdir, mobile=False):
    os.makedirs(OUT, exist_ok=True)
    if mobile:
        # Native portrait: crop the 16:9 frame to 9:16 around the focal centre, then 720 wide.
        dst = os.path.join(OUT, "leg%d-m.mp4" % n)
        vf = "crop=ih*9/16:ih,scale=720:-2,unsharp=5:5:0.6:5:5:0.0"
        gop = "4"
        crf = "23"
    else:
        dst = os.path.join(OUT, "leg%d.mp4" % n)
        vf = "unsharp=5:5:0.8:5:5:0.0"
        gop = "8"
        crf = "20"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS), "-i", os.path.join(outdir, "f%05d.png"),
        "-an", "-vf", vf,
        "-c:v", "libx264", "-preset", "slow", "-crf", crf, "-pix_fmt", "yuv420p",
        "-g", gop, "-keyint_min", gop, "-sc_threshold", "0",
        "-movflags", "+faststart", dst,
    ]
    subprocess.run(cmd, check=True)
    return dst


if __name__ == "__main__":
    which = sys.argv[1:] or [str(l["n"]) for l in LEGS]
    preview = "--preview" in which
    which = [w for w in which if w.isdigit()]
    for leg in LEGS:
        if str(leg["n"]) not in which:
            continue
        outdir, frames = render_leg(leg, preview_only=preview)
        print("leg %d: %d frames -> %s" % (leg["n"], frames, outdir))
        if not preview:
            print("  ", encode(leg["n"], outdir))
            print("  ", encode(leg["n"], outdir, mobile=True))
