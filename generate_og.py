#!/usr/bin/env python3
"""
QA Explained — OG Image Template Generator
--------------------------------------------
Reproduces the site's default OG image style (dark background, subtle grid,
warm top-right glow, ring logo, orange eyebrow label, bold serif title,
rule, author row, domain) and swaps in per-article content.

Usage: edit the CONFIG block at the bottom (or import `render_og`) and run.
Output: 1200x630 PNG, matching og:image / twitter:image dimensions.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630

# ---- Palette (sampled from the site's existing OG image) -----------------
BG_BASE      = (13, 13, 16)      # near-black base
BG_GLOW      = (46, 32, 20)      # warm ember glow, top-right
GRID_LINE    = (255, 255, 255)   # low-alpha overlay
ORANGE       = (227, 159, 78)    # accent / eyebrow / domain
WHITE        = (240, 238, 234)   # title
MUTED        = (188, 186, 182)   # secondary text (author name)
RULE_COLOR   = (58, 56, 54)

# macOS system fonts — Georgia for serif, Courier New for mono
_FONTS = "/System/Library/Fonts/Supplemental"
FONT_DIR_SERIF  = f"{_FONTS}/Georgia Bold.ttf"
FONT_DIR_MONO   = f"{_FONTS}/Courier New Bold.ttf"
FONT_DIR_MONO_R = f"{_FONTS}/Courier New.ttf"

# Avatar is cropped from the site's default OG image (Elena's photo is embedded there)
_HERE = os.path.dirname(os.path.abspath(__file__))
AVATAR_SOURCE   = os.path.join(_HERE, "assets/img/og-image.png")
AVATAR_CROP_BOX = (70, 495, 150, 575)  # pre-located circle crop in the reference image


def _font(path, size):
    try:
        f = ImageFont.truetype(path, size)
        try:
            f.set_variation_by_name('Bold')
        except Exception:
            pass
        return f
    except Exception:
        return ImageFont.load_default()


def draw_background(draw, img):
    for y in range(H):
        draw.line([(0, y), (W, y)], fill=BG_BASE)

    glow = Image.new("L", (W, H), 0)
    gdraw = ImageDraw.Draw(glow)
    cx, cy, r = W - 120, 40, 620
    for i in range(r, 0, -4):
        alpha = int(70 * (1 - i / r) ** 2)
        gdraw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=alpha)
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    warm_layer = Image.new("RGB", (W, H), BG_GLOW)
    img.paste(warm_layer, (0, 0), glow)

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = 60
    for x in range(0, W + step, step):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, H + step, step):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)
    img.alpha_composite(grid) if img.mode == "RGBA" else img.paste(
        Image.alpha_composite(img.convert("RGBA"), grid).convert("RGB"), (0, 0)
    )


def draw_ring_logo(img, x, y, d=34):
    draw = ImageDraw.Draw(img)
    draw.ellipse([x, y, x + d, y + d], outline=ORANGE, width=5)
    dot_r = int(d * 0.15)
    dcx, dcy = x + int(d * 0.78), y + int(d * 0.78)
    draw.ellipse([dcx - dot_r, dcy - dot_r, dcx + dot_r, dcy + dot_r], fill=(245, 243, 240))


def wrap_title(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def render_og(
    title,
    eyebrow,
    author="Elena Kulgavaya",
    domain="qaexplained.com",
    out_path="og-image.png",
    site_name="QA Explained",
):
    base = Image.new("RGB", (W, H), BG_BASE)
    draw_background(ImageDraw.Draw(base), base)
    img = base.convert("RGB")
    draw = ImageDraw.Draw(img)

    margin_x = 76

    # logo row
    draw_ring_logo(img, margin_x, 74, d=36)
    logo_font = _font(FONT_DIR_SERIF, 26)
    draw = ImageDraw.Draw(img)
    draw.text((margin_x + 52, 78), site_name, font=logo_font, fill=WHITE)

    # eyebrow
    eyebrow_font = _font(FONT_DIR_MONO, 17)
    ey = 188
    x = margin_x
    for ch in eyebrow.upper():
        draw.text((x, ey), ch, font=eyebrow_font, fill=ORANGE)
        x += draw.textlength(ch, font=eyebrow_font) + 6

    # title — auto-shrink to fit 3 lines
    max_w = 1050
    size = 58
    while size >= 38:
        title_font = _font(FONT_DIR_SERIF, size)
        try:
            title_font.set_variation_by_name('Bold')
        except Exception:
            pass
        lines = wrap_title(draw, title, title_font, max_w)
        if len(lines) <= 3:
            break
        size -= 4
    line_h = int(size * 1.17)

    TITLE_TOP = 232
    RULE_Y    = 468
    AUTHOR_Y  = 505

    ty = TITLE_TOP
    for line in lines[:3]:
        draw.text((margin_x, ty), line, font=title_font, fill=WHITE)
        ty += line_h

    # rule
    rule_y = max(ty + 18, RULE_Y)
    draw.line([(margin_x, rule_y), (W - margin_x, rule_y)], fill=RULE_COLOR, width=2)

    # author row
    ax, ay, ad = margin_x, max(rule_y + 34, AUTHOR_Y), 60
    try:
        avatar = Image.open(AVATAR_SOURCE).convert("RGB").crop(AVATAR_CROP_BOX).resize((ad, ad))
        mask = Image.new("L", (ad, ad), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, ad, ad], fill=255)
        img.paste(avatar, (ax, ay), mask)
    except Exception:
        pass

    name_font = _font(FONT_DIR_SERIF, 27)
    draw.text((ax + ad + 20, ay + ad // 2 - 18), author, font=name_font, fill=MUTED)

    domain_font = _font(FONT_DIR_MONO_R, 20)
    dw = draw.textlength(domain, font=domain_font)
    draw.text((W - margin_x - dw, ay + ad // 2 - 12), domain, font=domain_font, fill=ORANGE)

    img.save(out_path)
    print(f"saved → {out_path}")
    return out_path


if __name__ == "__main__":
    posts = [
        ("From E2E to Contract Tests: A Practical Migration Path.", "Testing · Strategy · 18 min read",
         "from-e2e-to-contract-tests-practical-migration-path"),
    ]

    out_dir = os.path.join(_HERE, "assets/img/posts")
    for title, eyebrow, slug in posts:
        render_og(
            title=title,
            eyebrow=eyebrow,
            out_path=os.path.join(out_dir, f"{slug}-og.png"),
        )
