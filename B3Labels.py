"""
B3Labels — draws text into the images the game shows as names.

The game has no text strings for names: each one is a small image with a
palette. The client redraws some of them (the map's hover label, the shop's
capsule names) so they can say what Archipelago item is behind them. Pure
Python: the client ships no image library, so the letters come from
data/LabelFont*.py, with smooth edges.

A drawn image uses 16 palette entries, as a ramp:
    0        clear
    1 - 5    the dark outline, fading out
    6 - 15   from outline to the text colour (the letters' soft edges)
"""
import math
from .data import LabelFont, LabelFontSmall, LabelFontTiny

FONTS = (LabelFont, LabelFontSmall, LabelFontTiny)     # tried in this order, largest first
OUTLINE = 2                                            # pixels of dark outline around the text
PADDING = 4                                            # kept clear at each side
EDGE_LEVELS, INK_LEVELS = 5, 10
PALETTE_SIZE = 1 + EDGE_LEVELS + INK_LEVELS

# Text colours (r, g, b), by what the label is about. The item colours follow
# Archipelago's own.
EDGE_COLOR = (16, 8, 0)
INK_COLORS = {
    "place":       (255, 165, 40),     # orange, like the game's own map labels
    "plain":       (255, 255, 255),
    "progression": (175, 153, 239),    # plum
    "useful":      (109, 139, 232),    # slate blue
    "trap":        (250, 128, 114),    # salmon
    "filler":      (0, 238, 238),      # cyan
}

# how strongly a letter pixel darkens its surroundings, by distance
_SPREAD = [(dx, dy, 1.0 if d <= 1.5 else 0.6 if d <= 2.3 else 0.25)
           for dx in range(-OUTLINE - 1, OUTLINE + 2) for dy in range(-OUTLINE - 1, OUTLINE + 2)
           for d in [math.hypot(dx, dy)] if 0 < d <= OUTLINE + 0.9]


def palette(ink, edge=EDGE_COLOR) -> list:
    """The 16 palette words (r | g<<8 | b<<16 | a<<24; alpha 0x80 = opaque)."""
    def word(rgb, alpha):
        return rgb[0] | rgb[1] << 8 | rgb[2] << 16 | alpha << 24
    words = [0]
    words += [word(edge, 0x80 * n // EDGE_LEVELS) for n in range(1, EDGE_LEVELS + 1)]
    for n in range(1, INK_LEVELS + 1):
        mix = tuple((edge[i] * (INK_LEVELS - n) + ink[i] * n) // INK_LEVELS for i in range(3))
        words.append(word(mix, 0x80))
    return words


def text_width(text: str, font) -> int:
    fallback = font.GLYPHS["?"]
    return sum(font.GLYPHS.get(ch, fallback)[0] for ch in text)


def fit(text: str, suffix: str, width: int, height: int):
    """(text, font) that fits the image. `suffix` (the player's name) is kept
    whole; `text` is cut short with '..' if even the smallest font is too wide."""
    room = width - 2 * (PADDING + OUTLINE)
    fonts = [f for f in FONTS if f.FONT_HEIGHT + 2 * OUTLINE <= height] or [FONTS[-1]]
    for font in fonts:
        if text_width(text + suffix, font) <= room:
            return text + suffix, font
    font = fonts[-1]
    while len(text) > 1 and text_width(text + ".." + suffix, font) > room:
        text = text[:-1]
    return text.rstrip() + ".." + suffix, font


def render(text: str, font, width: int, height: int, align: str = "right") -> list:
    """Palette indices (see the module docstring), row by row.

    align "right": the text ends at the right edge. The map anchors a label by
    its right edge on the scroll behind it, so a name grows to the left, as the
    game's own labels do. "left" is for lists."""
    fallback = font.GLYPHS["?"]
    x = PADDING + OUTLINE
    if align == "right":
        x = max(x, width - PADDING - OUTLINE - text_width(text, font))
    top = max(OUTLINE, (height - font.FONT_HEIGHT) // 2)
    ink = [0] * (width * height)           # how much of each pixel the letters cover, 0-15
    for ch in text:
        glyph_width, rows = font.GLYPHS.get(ch, fallback)
        for y, row in enumerate(rows):
            if top + y >= height:
                break
            for i, digit in enumerate(row):
                if digit != "0" and x + i < width:
                    ink[(top + y) * width + x + i] = int(digit, 16)
        x += glyph_width
    edge = [0.0] * (width * height)
    for at, cover in enumerate(ink):
        if cover:
            cx, cy = at % width, at // width
            for dx, dy, strength in _SPREAD:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    value = cover * strength
                    if value > edge[ny * width + nx]:
                        edge[ny * width + nx] = value
    px = [0] * (width * height)
    for at in range(width * height):
        if ink[at]:
            px[at] = EDGE_LEVELS + max(1, (ink[at] * INK_LEVELS + 7) // 15)
        elif edge[at]:
            px[at] = max(1, min(EDGE_LEVELS, round(edge[at] * EDGE_LEVELS / 15)))
    return px


def pack_4bit(px: list, size: int) -> list:
    """Indices -> the 32-bit words of a 16-colour image (`size` bytes; two
    pixels per byte, the first in the low half)."""
    data = bytearray(size)
    for i in range(0, min(len(px), 2 * size) - 1, 2):
        data[i // 2] = px[i] | (px[i + 1] << 4)
    return [int.from_bytes(data[i:i + 4], "little") for i in range(0, size - size % 4, 4)]


def pack_8bit(px: list, size: int) -> list:
    """Indices -> the 32-bit words of a 256-colour image (one pixel per byte)."""
    data = bytes(px[:size]).ljust(size, bytes(1))
    return [int.from_bytes(data[i:i + 4], "little") for i in range(0, size - size % 4, 4)]


def palette_slot_8bit(index: int) -> int:
    """Where colour `index` sits in a 256-colour palette as the game stores it
    (blocks of eight entries are swapped in pairs)."""
    return (index & 0xE0) | ((index & 0x10) >> 1) | ((index & 0x08) << 1) | (index & 0x07)
