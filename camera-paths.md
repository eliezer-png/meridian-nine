# Meridian Nine — camera path spec (procedural 2.5D)

Architecture A: one continuous forward take, six legs, no connectors. The camera never
reverses. With a virtual camera we control the path exactly, so the seam rule is enforced by
construction rather than by luck.

## The seam strategy: a light chain

We cannot make leg *i*'s last frame pixel-identical to leg *i+1*'s first frame — they are six
different photographs. So instead of matching *content*, we match *luminance and texture*, and
let the engine's crossfade land where the eye has nothing to hold on to.

Every leg ends by pushing into a region that is either **blown-out bright** (a lamp, a window,
a doorway) or **near-black**, and the next leg begins from its own region of the same value.
The camera appears to pass *through the light* into the next room. This is a real cinematic
device, not a workaround — it is how match-cuts on brightness have always worked.

The chain, in order:

| Seam | Leg out ends on | Leg in starts from | Value |
|---|---|---|---|
| 1 → 2 | inside the glowing doorway | the warm task-lamp glow, upper left | warm blowout |
| 2 → 3 | the bright window wall, right | the frosted windows, upper left | cool bright |
| 3 → 4 | specular bloom on the polished case | the window wall of the lab | cool bright |
| 4 → 5 | white blowout through the lab window | vitrine glow, upper left | warm bright |
| 5 → 6 | the dark far end of the boutique | near-black stone around the watch | near-black |

Note the arc: the film opens cold outside, moves through warm craft, cools into the lab, warms
into the boutique, then falls to black for the product. The seams are riding a deliberate
exposure curve, so they read as intent.

## Per-leg parameters

`target` is the normalized (x, y) the camera dollies toward — the vanishing point or the focal
object. `z` is how far it travels in depth units (1.0 ≈ the full estimated depth range; beyond
~0.55 the warp starts to tear on these images). `dur` is seconds at 24fps.

### Leg 1 — The Manufacture
- `target` (0.500, 0.605) — the lit doorway, dead centre at the end of the gravel path
- `z` 0.52, `dur` 8.0, ease: slow start, steady middle, no deceleration at the end
- Move: straight forward dolly down the path. The strongest parallax in the film — wet gravel
  sweeps past the bottom of frame while the treeline barely moves.
- Ends: frame filled by the doorway's warm light.

### Leg 2 — The Atelier
- `target` (0.330, 0.225) — the bench's vanishing point, up and to the left
- Secondary drift to (0.780, 0.300) in the final 1.5s — toward the window light
- `z` 0.42, `dur` 8.0
- Move: forward along the bench, then the late drift right. The near bench edge and the brass
  lamp in the foreground carry the parallax; the movement on the grey mat passes just below camera.
- Ends: the bright window wall.

### Leg 3 — Finishing
- `target` (0.600, 0.470) — the case in the lathe jig
- `z` 0.38, `dur` 7.0 — shorter and closer; this is a detail beat, not a corridor
- Move: low push-in toward the lathe with a slight left-to-right slide, so the tool tray in the
  foreground sweeps out of frame left.
- Ends: the specular highlight on the polished case blooms out.

### Leg 4 — Regulation
- `target` (0.420, 0.300) — down the row of chronometer machines
- `z` 0.50, `dur` 7.5
- Move: straight forward dolly down the room. Cool, even, unhurried — the machines pass in
  sequence like fence posts.
- Ends: drift left into the white window wall.

### Leg 5 — The Boutique
- `target` (0.545, 0.355) — the far end of the corridor, where the city window is
- `z` 0.48, `dur` 8.0
- Move: forward down the vitrine, biased slightly left so the lit watches slide past close to
  camera. The strongest sense of "walking through" in the film.
- Ends: into the dark far end — falls to near-black.

### Leg 6 — The Nine
- `target` (0.470, 0.500) — the watch
- `z` 0.22, `dur` 9.0 — the shortest travel, the longest time. Deliberately slow.
- Move: gentle push-in with a small lateral arc (±0.03 x) that reads as a partial orbit. Settles
  and stops in the final 1.5s so the copy and CTA land on a still frame.
- Starts: near-black, matching leg 5's ending.

## Honest limits of this technique

- **No reveals.** The roof never opens, walls never part, nothing transforms. Every leg is a
  camera move over a fixed photograph.
- **Bounded travel.** Past `z` ≈ 0.55 the depth warp tears at object edges — most visibly on
  the lamp arms in scene 2 and the chair backs in scene 5. The `z` values above are set under
  that ceiling on purpose.
- **No new occlusion.** The camera cannot move far enough sideways to see behind anything,
  which is why every move is dominated by forward travel.
- **Seams are dissolves, not continuations.** A viewer scrubbing slowly across a seam will
  read it as a cross-dissolve through light, not as an unbroken camera move. Seedance would
  have given a true continuation; this is the honest cost of the free path.

What it does buy: genuine depth parallax, exact camera control, frame-accurate determinism,
re-rendering in minutes instead of credits, and stills that stay as sharp as the source.
