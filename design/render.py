#!/usr/bin/env python3
"""Render the news-image-20261127 front page: 1024x1024 PNG. v2 layout."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (18, 18, 18)
ACCENT = (146, 24, 24)
GREY = (84, 80, 72)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

def centered(text, y, fnt, fill=INK):
    w_ = d.textlength(text, font=fnt)
    d.text(((W - w_) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 8

def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

def block(x, y, max_w, text, fnt, leading, fill=INK, center=False):
    for ln in wrap(text, fnt, max_w):
        if center:
            d.text((x + (max_w - d.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
        else:
            d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

M = 56

# --- masthead -------------------------------------------------------------
d.rectangle([M, 30, W - M, 34], fill=INK)
centered("THE WORLD IN A DAY", 46, font(SERIF_B, 62))
y = 122
centered("Friday 27 November 2026  ·  Six headlines, one front page", y, font(SANS, 26), GREY)
y += 40
d.rectangle([M, y, W - M, y + 3], fill=INK)
d.rectangle([M, y + 7, W - M, y + 9], fill=INK)
y += 26

# --- lead story -----------------------------------------------------------
centered("C A I R O   ·   E G Y P T", y, font(SANS_B, 23), ACCENT)
y += 38
y = block(M, y, W - 2 * M, "FUEL TANKER FIRE NEAR CAIRO KILLS 31",
          font(SERIF_B, 55), 64, INK, center=True)
y += 4
y = block(M + 70, y, W - 2 * M - 140,
          "Prosecutors arrest a man accused of sparking the blaze after a "
          "fuel truck overturned on a packed highway outside the capital.",
          font(SERIF, 24), 32, GREY)
y += 18
d.rectangle([M, y, W - M, y + 2], fill=INK)
y += 24

# --- secondary stories ----------------------------------------------------
stories = [
    ("WASHINGTON · MOSCOW", "TRUMP URGES PUTIN TO END HOSTILITIES IN EUROPE",
     "He says he asked Moscow to wind down military action; NATO's Rutte echoes the warning."),
    ("PYONGYANG", "KIM JONG UN ORDERS WIDER NUCLEAR DEPLOYMENT",
     "Touring nuclear-material sites, Kim calls for more strategic weapons, KCNA reports."),
    ("LONDON", "UK TRAIN ATTACKER FOUND GUILTY OF ATTEMPTED MURDER",
     "A man who stabbed passengers on a train and elsewhere is convicted in Britain."),
    ("KYIV", "US APPROVES $622M TO KEEP UKRAINE'S F-16S FLYING",
     "Four European allies share the cost of the support deal for Kyiv's fighter fleet."),
    ("PARIS", "DEPARDIEU TO FACE TRIAL, HIS LAWYER SAYS",
     "The French actor will stand trial on a sexual assault charge, his attorney confirms."),
]

def story(x, y, max_w, label, head, dek):
    d.text((x, y), label, font=font(SANS_B, 19), fill=ACCENT)
    y += 27
    y = block(x, y, max_w, head, font(SERIF_B, 24), 29)
    y += 3
    y = block(x, y, max_w, dek, font(SANS, 19), 23, GREY)
    return y

col_w = (W - 2 * M - 36) // 2
left_y = story(M, y, col_w, *stories[0])
left_y = story(M, left_y + 16, col_w, *stories[1])
right_y = story(M + col_w + 36, y, col_w, *stories[2])
right_y = story(M + col_w + 36, right_y + 16, col_w, *stories[3])
y = max(left_y, right_y) + 14
d.rectangle([M, y, W - M, y + 1], fill=GREY)
y += 16
y = story(M, y, W - 2 * M, *stories[4])

# --- footer ---------------------------------------------------------------
d.rectangle([M, H - 58, W - M, H - 56], fill=INK)
centered("Every headline backed by at least two reports dated 27 November 2026 · Sources in design/sources.md",
         H - 46, font(SANS, 17), GREY)
print("last content y:", y)
img.save("entry.png", optimize=True)
print("saved")
