#!/usr/bin/env python3
# Copyright (c) 2026 Innodisk Corp.
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Generate the default Open Graph card for the iQ Studio docs site.

Composition (per .agent-artifacts/seo-checklist.md §3):
  - 1200 x 630 PNG, white background.
  - iq-studio-logo.png on the left, centered vertically.
  - "iQ Studio Documentation" in Barlow Condensed (or DejaVu fallback)
    right of the logo.
  - Red #ec1b23 horizontal rule under the title.
  - "Innodisk Dragonwing AI Platform" subtitle in muted gray.

Output: docs/fig/og-default.png

Usage (from repo root):
    python3 tools/generate_og_image.py

Dependencies: Pillow (pinned in requirements.txt).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow not installed. Run `pip install -r requirements.txt`.",
          file=sys.stderr)
    sys.exit(1)


# Paths -------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = REPO_ROOT / "docs" / "fig" / "iq-studio-logo.png"
OUTPUT_PATH = REPO_ROOT / "docs" / "fig" / "og-default.png"

# Design tokens (brand-guide.md) -----------------------------------------
W, H = 1200, 630
BG = (255, 255, 255)              # white
INK = (22, 39, 46)                # #16272e -- Innodisk preferred ink
MUTED = (149, 149, 149)           # #959595
BRAND_RED = (236, 27, 35)         # #ec1b23

# Layout tokens
PADDING = 64
LOGO_SIZE = 360
GAP_LOGO_TEXT = 56
RULE_THICKNESS = 6
RULE_WIDTH = 280


# Font discovery ---------------------------------------------------------
def find_font(candidates: list[str], size: int) -> ImageFont.ImageFont:
    """Try a list of font filenames; return the first that loads.

    Falls back to PIL's default bitmap font if none match.
    """
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    print(f"  WARNING: no preferred font found for size={size}, using PIL default.",
          file=sys.stderr)
    return ImageFont.load_default()


# Candidate lists (Barlow Condensed first; fall back to DejaVu/Liberation
# which ship with most Linux distros, including this build environment).
TITLE_FONT_CANDIDATES = [
    # Barlow Condensed if installed via brand-guide.md §5.2
    "BarlowCondensed-Bold.ttf",
    "BarlowCondensed-SemiBold.ttf",
    "Barlow_Condensed/BarlowCondensed-Bold.ttf",
    "/usr/share/fonts/truetype/barlow-condensed/BarlowCondensed-Bold.ttf",
    # Inter as the body-font fallback per brand-guide.md §5.1
    "Inter-Bold.ttf",
    "/usr/share/fonts/truetype/inter/Inter-Bold.ttf",
    # System fallbacks
    "DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

SUBTITLE_FONT_CANDIDATES = [
    "Inter-Regular.ttf",
    "/usr/share/fonts/truetype/inter/Inter-Regular.ttf",
    "DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def main() -> int:
    if not LOGO_PATH.exists():
        print(f"ERROR: source logo not found at {LOGO_PATH}", file=sys.stderr)
        return 1

    print(f"Generating {OUTPUT_PATH.relative_to(REPO_ROOT)} ({W}x{H})...")

    # Canvas
    card = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(card)

    # Logo (left, vertically centered)
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo.thumbnail((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
    lw, lh = logo.size
    logo_x = PADDING
    logo_y = (H - lh) // 2
    card.paste(logo, (logo_x, logo_y), logo)

    # Text column origin
    text_x = logo_x + lw + GAP_LOGO_TEXT
    text_block_width = W - text_x - PADDING

    title_font = find_font(TITLE_FONT_CANDIDATES, size=72)
    subtitle_font = find_font(SUBTITLE_FONT_CANDIDATES, size=30)

    # Title text -- two lines to balance the right column.
    title_lines = ["iQ Studio", "Documentation"]
    line_heights = []
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_heights.append(bbox[3] - bbox[1])
    title_total_h = sum(line_heights) + 16  # small interline gap

    # Subtitle
    subtitle = "Innodisk Dragonwing AI Platform"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    sub_h = sub_bbox[3] - sub_bbox[1]

    # Compose vertically: title block, then rule, then subtitle.
    rule_gap_above = 28
    rule_gap_below = 28
    block_h = title_total_h + rule_gap_above + RULE_THICKNESS + rule_gap_below + sub_h
    cursor_y = (H - block_h) // 2

    # Draw title lines
    for line, lh_px in zip(title_lines, line_heights):
        draw.text((text_x, cursor_y), line, font=title_font, fill=INK)
        cursor_y += lh_px + 16
    cursor_y -= 16  # remove trailing gap
    cursor_y += rule_gap_above

    # Brand-red rule
    draw.rectangle(
        [text_x, cursor_y, text_x + RULE_WIDTH, cursor_y + RULE_THICKNESS],
        fill=BRAND_RED,
    )
    cursor_y += RULE_THICKNESS + rule_gap_below

    # Subtitle
    draw.text((text_x, cursor_y), subtitle, font=subtitle_font, fill=MUTED)

    # Small footprint: "innodisk.com" in the bottom-right corner.
    footer = "innodisk.com"
    footer_font = find_font(SUBTITLE_FONT_CANDIDATES, size=22)
    fbbox = draw.textbbox((0, 0), footer, font=footer_font)
    fw = fbbox[2] - fbbox[0]
    fh = fbbox[3] - fbbox[1]
    draw.text(
        (W - PADDING - fw, H - PADDING - fh),
        footer,
        font=footer_font,
        fill=MUTED,
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    card.save(OUTPUT_PATH, format="PNG", optimize=True)
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    print(f"  wrote {OUTPUT_PATH} ({size_kb:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
