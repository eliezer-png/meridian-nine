# Meridian Nine — brand bible

Single source of truth for every page. Nothing on the site may contradict this file, and no
page may invent a fact that isn't here. If a page needs a fact that is missing, add it here
first.

> Meridian Nine is a fictional brand created for this build. Every claim below is invented.

---

## 1. Positioning

An independent watchmaker in the Vallée de Joux that makes **nine watches a year**. Founded
2016; the first watch left the building in 2025 — nine years of development, which is where the
name comes from. One calibre, one case, three dials. There is no second model and no plan for
one.

**The single idea:** scarcity as a consequence, not a marketing device. Nine a year is what one
watchmaker can do properly, not a number chosen to create a waiting list.

## 2. Voice

Restrained, declarative, specific. The register of a technical document written by someone with
taste.

**Rules:**
- Short sentences. Full stops over commas.
- Numbers instead of adjectives. Not "exceptional accuracy" — "−2/+4 seconds a day, measured
  over fifteen days."
- Never: "luxury", "exquisite", "timeless", "craftsmanship", "journey", "curated", "bespoke",
  "iconic", "unparalleled", "passion".
- No exclamation marks. No rhetorical questions. No second-person hard sell.
- Admit limits plainly. "There are nine a year. Most years they are spoken for by March."
- Prices are stated. A brand that hides its prices is selling to a different customer.

**Sample cadence (use this as the target):**
> Two hundred and fourteen parts. One watchmaker assembles them, takes them apart, and
> assembles them again. Their mark goes on the bridge, under the balance, where only the next
> watchmaker will see it.

## 3. The collection

Three references. Same calibre, same case, same dimensions — the dial is the whole difference.

| | **Nine Bianco** | **Nine Notte** | **Nine Terra** |
|---|---|---|---|
| Dial | Bone-white guilloché, hand-turned | Grained near-black, matte | Deep teal, translucent lacquer over guilloché |
| Indices | Applied gold, polished | Applied gold, polished | Applied gold, polished |
| Hands | Blued steel | Blued steel | Blued steel |
| Case | 38.5mm steel, brushed with polished flanks | as Bianco | as Bianco, gold crown |
| Crystal | Domed sapphire, double AR | as Bianco | as Bianco |
| Water resistance | 30m | 30m | 30m |
| Strap | Black alligator, steel pin buckle | as Bianco | Teal alligator, gold pin buckle |
| Price | CHF 42,000 | CHF 44,000 | CHF 46,000 |
| Availability | Four a year | Three a year | Two a year |

Total: nine.

**Case (all references):** 38.5mm diameter, 9.1mm thick, 45mm lug to lug, 20mm lug width.
Cut from a single billet of 316L. Brushed top surfaces, polished flanks, one clean transition
line where they meet — the part you feel before you read it.

## 4. Calibre M9

Hand-wound. Designed and made in the building.

| | |
|---|---|
| Parts | 214 |
| Jewels | 27 |
| Frequency | 21,600 vph (3 Hz) |
| Power reserve | 72 hours |
| Balance | Free-sprung, four-arm, adjustable inertia weights |
| Hairspring | Flat, in-house, hand-adjusted terminal curve |
| Finishing | Hand-bevelled bridges, polished countersinks, circular-grained mainplate |
| Diameter | 30.4mm |
| Thickness | 4.2mm |

**Regulation:** every movement runs 15 days in five positions and two temperatures before it is
cased. The result is **−2/+4 seconds a day**. The actual measured rate of your specific watch is
printed on the certificate and stays on file.

**Assembly:** one watchmaker builds a movement from start to finish, disassembles it entirely,
and rebuilds it. Their mark is engraved on the underside of the balance bridge.

## 5. The manufacture

One building at the head of a valley in the Vallée de Joux. Stone and glass, built 2016.
Everything happens inside it: movement, case finishing, dials, regulation, service.

Eleven people. Four are watchmakers.

## 6. Ownership

- **Lifetime servicing, included.** Not a warranty period — for as long as the watch exists,
  including after it changes hands. Servicing is priced into the watch, not invoiced later.
- **Service interval:** every 7 years, or sooner if the rate drifts outside tolerance.
- **Turnaround:** 10–14 weeks. A loan watch is offered for any service over 6 weeks.
- **Certificate:** the measured rate, the assembling watchmaker's mark, the date it was cased.
- **Purchase:** by introduction at one of four boutiques, or by writing to the manufacture.
  Most years the nine are spoken for by March. There is no paid priority list.

## 7. Boutiques

| City | Address | |
|---|---|---|
| Geneva | 14 Rue du Rhône | +41 22 000 00 00 |
| Tokyo | 3-5-8 Ginza, Chūō-ku | +81 3 0000 0000 |
| New York | 27 East 64th Street | +1 212 000 0000 |
| Singapore | 2 Orchard Turn, #03-14 | +65 6000 0000 |

Manufacture: Route du Lac 9, 1347 Le Sentier, Switzerland.
General enquiries: `enquiries@meridiannine.example`

## 8. Design system

The visual identity comes from the photography and the film. The chrome stays quiet.

**Palette**

| Token | Hex | Use |
|---|---|---|
| `--ink` | `#0A0C0F` | page ground |
| `--ink-2` | `#12151A` | raised surfaces, cards |
| `--ink-3` | `#1B1F26` | borders, hairlines |
| `--bone` | `#EDEEF0` | primary text |
| `--bone-soft` | `#8A929C` | secondary text |
| `--gold` | `#C9A227` | accent: rules, active nav, primary button |
| `--teal` | `#1F6F6B` | secondary accent, Terra reference only |
| `--slate` | `#3E4A57` | tertiary, chart/spec strokes |

**Type**
- Display: **Cormorant Garamond**, 300/400. Headlines only. Generous size contrast — a page
  headline should be at least 4× body size.
- Body: **Inter**, 300/400/500. Body, labels, specs.
- Spec tables and numbers: Inter with `font-variant-numeric: tabular-nums`.
- Letter-spacing: eyebrows and small caps at `0.18em`. Display type at `-0.01em`.

**Rules**
- Dark ground everywhere. This is not a themeable site; it is one deliberate look.
- Whitespace is the main luxury signal. Sections breathe: `clamp(6rem, 12vh, 12rem)` vertical.
- One accent per view. Gold is the default; teal appears only on Terra.
- Hairlines, not boxes. `1px solid var(--ink-3)` rules to separate; avoid card borders.
- Images are large and uncropped where possible. Never a busy grid of small thumbnails.
- Motion: fades and small translations only, 400–700ms, `cubic-bezier(0.16,1,0.3,1)`.
  Everything respects `prefers-reduced-motion`.
- No shadows on the dark ground — separate with value, not with blur.

**Layout**
- Content column max 1200px; text measure max 68ch.
- Shared header: wordmark left, nav right, hairline under, transparent over the film on home.
- Shared footer: four columns — collection, manufacture, ownership, contact.

## 9. Pages

| Page | File | Job |
|---|---|---|
| Home | `index.html` | The scroll film. Ends on the CTA. |
| The Collection | `collection.html` | Three references, specs, prices. |
| Calibre M9 | `calibre.html` | The movement, in technical detail. |
| The Manufacture | `manufacture.html` | The building, the eleven people, the process. |
| Ownership | `ownership.html` | Servicing, certificate, what buying involves. |
| Boutiques | `boutiques.html` | Four addresses, the manufacture, enquiry form. |
