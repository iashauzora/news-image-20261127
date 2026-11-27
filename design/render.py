#!/usr/bin/env python3
"""Render the front page for the news-image-20261127 entry.

Draws a 1024x1024 newspaper front page with PIL and saves it as
entry.png in the repository root (one level above this script).

Every block of text is measured before it is drawn. Blocks are
stacked by their measured heights, so nothing overlaps, and the
whole page is laid out again at a slightly smaller scale whenever
the columns would run into the footer rule.
"""

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 56
GUTTER = 36
CONTENT_W = PAGE - 2 * MARGIN
COLUMN_W = (CONTENT_W - GUTTER) // 2
FOOTER_TOP = PAGE - 96

PAPER = (247, 242, 231)
INK = (30, 27, 24)
FADED = (94, 87, 77)
ACCENT = (158, 28, 28)

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF_BOLD = FONT_DIR / "dejavu" / "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR / "dejavu" / "DejaVuSerif.ttf"
SERIF_ITALIC = FONT_DIR / "dejavu" / "DejaVuSerif-Italic.ttf"
SANS_BOLD = FONT_DIR / "liberation" / "LiberationSans-Bold.ttf"

MASTHEAD = "THE WORLD IN A DAY"
DATE_LINE = "Friday 27 November 2026 · Six headlines, one front page"
FOOTER = (
    "Every headline backed by at least two reports dated "
    "27 November 2026 · Sources in design/sources.md"
)

LEAD = (
    "LEAD · CAIRO · EGYPT",
    "FUEL TANKER FIRE NEAR CAIRO KILLS 31",
    "Prosecutors arrest a man accused of sparking the blaze after a "
    "fuel truck overturned on a packed highway outside the capital.",
)

STORIES = [
    (
        "WASHINGTON · MOSCOW",
        "TRUMP URGES PUTIN TO END HOSTILITIES IN EUROPE",
        "He says he asked Moscow to wind down military action; "
        "NATO's Rutte echoes the warning.",
    ),
    (
        "PYONGYANG",
        "KIM JONG UN ORDERS WIDER NUCLEAR DEPLOYMENT",
        "Touring nuclear-material sites, Kim calls for more "
        "strategic weapons, KCNA reports.",
    ),
    (
        "LONDON",
        "UK TRAIN ATTACKER FOUND GUILTY OF ATTEMPTED MURDER",
        "A man who stabbed passengers on a train and elsewhere is "
        "convicted in Britain.",
    ),
    (
        "KYIV",
        "US APPROVES $622M TO KEEP UKRAINE'S F-16S FLYING",
        "Four European allies share the cost of the support deal "
        "for Kyiv's fighter fleet.",
    ),
    (
        "PARIS",
        "DEPARDIEU TO FACE TRIAL, HIS LAWYER SAYS",
        "The French actor will stand trial on a sexual assault "
        "charge, his attorney confirms.",
    ),
]


def font(path, size):
    """Load a TrueType font, falling back to the plain serif faces
    when a variant (such as the italic) is not installed."""
    size = max(8, int(round(size)))
    for candidate in (path, SERIF, SERIF_BOLD):
        try:
            return ImageFont.truetype(str(candidate), size)
        except OSError:
            continue
    raise OSError("no readable font for " + str(path))


def line_step(draw, fnt):
    """Vertical advance for one line of the given font."""
    box = draw.textbbox((0, 0), "Ag", font=fnt)
    return int((box[3] - box[1]) * 1.22) + 2


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap using measured text widths."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, lines, fnt, fill, step):
    for line in lines:
        w = draw.textlength(line, font=fnt)
        draw.text((cx - w / 2, y), line, font=fnt, fill=fill)
        y += step
    return y


def draw_story(draw, x, y, story, scale):
    """Draw one column story at (x, y); return the y below it."""
    label, headline, summary = story
    label_f = font(SANS_BOLD, 16 * scale)
    head_f = font(SERIF_BOLD, 27 * scale)
    sum_f = font(SERIF, 18.5 * scale)

    draw.text((x, y), label, font=label_f, fill=ACCENT)
    y += line_step(draw, label_f) + int(4 * scale)

    for line in wrap(draw, headline, head_f, COLUMN_W):
        draw.text((x, y), line, font=head_f, fill=INK)
        y += line_step(draw, head_f)
    y += int(4 * scale)

    for line in wrap(draw, summary, sum_f, COLUMN_W):
        draw.text((x, y), line, font=sum_f, fill=FADED)
        y += line_step(draw, sum_f)
    return y


def layout(scale):
    """Draw the whole page at the given scale; return (image, end_y)."""
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    cx = PAGE // 2

    y = 30
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=3)
    draw.line([(MARGIN, y + 6), (PAGE - MARGIN, y + 6)], fill=INK, width=1)
    y += 20

    mast_f = font(SERIF_BOLD, 62 * scale)
    y = draw_centered(draw, cx, y, [MASTHEAD], mast_f, INK,
                      line_step(draw, mast_f))
    y += int(4 * scale)
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=1)
    y += int(12 * scale)

    date_f = font(SERIF_ITALIC, 21 * scale)
    y = draw_centered(draw, cx, y, [DATE_LINE], date_f, FADED,
                      line_step(draw, date_f))
    y += int(10 * scale)
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=2)
    y += int(22 * scale)

    lead_label_f = font(SANS_BOLD, 19 * scale)
    y = draw_centered(draw, cx, y, [LEAD[0]], lead_label_f, ACCENT,
                      line_step(draw, lead_label_f))
    y += int(8 * scale)

    lead_head_f = font(SERIF_BOLD, 52 * scale)
    head_lines = wrap(draw, LEAD[1], lead_head_f, CONTENT_W)
    y = draw_centered(draw, cx, y, head_lines, lead_head_f, INK,
                      line_step(draw, lead_head_f))
    y += int(10 * scale)

    lead_sum_f = font(SERIF_ITALIC, 23 * scale)
    sum_lines = wrap(draw, LEAD[2], lead_sum_f, CONTENT_W - 80)
    y = draw_centered(draw, cx, y, sum_lines, lead_sum_f, FADED,
                      line_step(draw, lead_sum_f))
    y += int(20 * scale)
    draw.line([(MARGIN, y), (PAGE - MARGIN, y)], fill=INK, width=1)
    y += int(22 * scale)

    left_x = MARGIN
    right_x = MARGIN + COLUMN_W + GUTTER
    left_end = y
    for story in STORIES[:3]:
        left_end = draw_story(draw, left_x, left_end, story, scale)
        left_end += int(26 * scale)
    right_end = y
    for story in STORIES[3:]:
        right_end = draw_story(draw, right_x, right_end, story, scale)
        right_end += int(26 * scale)

    return img, max(left_end, right_end)


def draw_footer(draw):
    foot_f = font(SERIF, 16)
    draw.line([(MARGIN, FOOTER_TOP), (PAGE - MARGIN, FOOTER_TOP)],
              fill=INK, width=1)
    lines = wrap(draw, FOOTER, foot_f, CONTENT_W)
    draw_centered(draw, PAGE // 2, FOOTER_TOP + 14, lines, foot_f, FADED,
                  line_step(draw, foot_f))


def main():
    scale = 1.0
    while True:
        img, end_y = layout(scale)
        if end_y <= FOOTER_TOP - 10 or scale <= 0.6:
            break
        scale -= 0.04
    draw_footer(ImageDraw.Draw(img))

    out_path = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out_path, format="PNG")
    data = out_path.read_bytes()
    print("wrote", out_path)
    print("scale", round(scale, 2), "content ends at y", end_y)
    print("bytes", len(data))
    print("sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
