from BaseClasses import Item, ItemClassification

B3_BASE_ID = 0xDB3000

class B3Item(Item):
    game = "Dragon Ball Z Budokai 3"

# ─── DU Character Unlock Items ───────────────────────────────────────────────
# Unlocks a character's Dragon Universe campaign.

CHARACTER_ITEMS = {
    "Goku DU":        B3_BASE_ID + 0x10,
    "Kid Gohan DU":   B3_BASE_ID + 0x11,
    "Teen Gohan DU":  B3_BASE_ID + 0x12,
    "Adult Gohan DU": B3_BASE_ID + 0x13,
    "Vegeta DU":      B3_BASE_ID + 0x14,
    "Krillin DU":     B3_BASE_ID + 0x15,
    "Piccolo DU":     B3_BASE_ID + 0x16,
    "Tien DU":        B3_BASE_ID + 0x17,
    "Yamcha DU":      B3_BASE_ID + 0x18,
    "Uub DU":         B3_BASE_ID + 0x19,
    "Broly DU":       B3_BASE_ID + 0x1A,
}

# ─── Capsule Items ────────────────────────────────────────────────────────────
# Random capsules the AP server can send to the player's shop.

from .data.Constants import SKILL_CAPSULES

CAPSULE_ITEMS = {
    f"Skill: {name}": B3_BASE_ID + 0x100 + i
    for i, name in enumerate(SKILL_CAPSULES.keys())
}
CAPSULE_ITEMS.update({
    "Zenie x500":   B3_BASE_ID + 0x110 + 0xA0,
    "Zenie x1000":  B3_BASE_ID + 0x111 + 0xA0,
    "Zenie x2000":  B3_BASE_ID + 0x112 + 0xA0,
})

# ─── Trap Items ───────────────────────────────────────────────────────────────

TRAP_ITEMS = {
    "HP Drain Trap":  B3_BASE_ID + 0x200,
}

# ─── Special Items ────────────────────────────────────────────────────────────

SPECIAL_ITEMS = {
    "Shop Restock":  B3_BASE_ID + 0x300,
    "Dragon Arena Ticket":   B3_BASE_ID + 0x301,
    "Dragon Arena Rank Up":  B3_BASE_ID + 0x302,
}

# ─── Dark Star Dragon Ball (McGuffin goal item) ──────────────────────────────
# A single named progression item placed in the pool `dark_star_balls_total`
# times; collect `dark_star_balls_required` to satisfy the McGuffin goal.
DARK_STAR_BALL_ITEM = "Dark Star Dragon Ball"
MCGUFFIN_ITEMS = {
    DARK_STAR_BALL_ITEM: B3_BASE_ID + 0x310,
}

# ─── Item capsules (filler variety) ──────────────────────────────────────────
# Equipment/consumable capsules granted exactly like skills (write 1 to DU-RT +
# RT). Used to replace monotonous Zenie filler with flavorful capsule unlocks.
# Named "Capsule: <name>" to distinguish from skills and shop locations.
#
# IMPORTANT: capsules used as SHOP CHECKS (SHOP_CAPSULE_POOL) are EXCLUDED. The
# shop fires its check by detecting a capsule's ownership flag increasing, so
# granting one of those capsules as an AP item would falsely trigger the shop
# check. Excluding them removes that conflict entirely.
from .data.Constants import ITEM_CAPSULES as _ITEM_CAPSULES
from .data.Constants import SHOP_CAPSULE_POOL as _SHOP_CAPSULE_POOL
_SHOP_CAPSULE_NAMES = {entry[2] for entry in _SHOP_CAPSULE_POOL}
ITEM_CAPSULE_ITEMS = {
    f"Capsule: {name}": B3_BASE_ID + 0x400 + i
    for i, name in enumerate(_ITEM_CAPSULES.keys())
    if name not in _SHOP_CAPSULE_NAMES
}

# ─── Full item table ──────────────────────────────────────────────────────────

item_table = {}
item_table.update(CHARACTER_ITEMS)
item_table.update(CAPSULE_ITEMS)
item_table.update(TRAP_ITEMS)
item_table.update(SPECIAL_ITEMS)
item_table.update(MCGUFFIN_ITEMS)
item_table.update(ITEM_CAPSULE_ITEMS)

def get_item_classification(name: str) -> ItemClassification:
    if name in CHARACTER_ITEMS:
        return ItemClassification.progression
    # These gate access to locations, so they MUST be progression (otherwise
    # the generator can't sphere them and gated locations break).
    if name in ("Dragon Arena Ticket", "Dragon Arena Rank Up", "Shop Restock"):
        return ItemClassification.progression
    if name in MCGUFFIN_ITEMS:
        return ItemClassification.progression
    if name in ITEM_CAPSULE_ITEMS:
        return ItemClassification.filler
    if name in SPECIAL_ITEMS:
        return ItemClassification.useful
    if name in TRAP_ITEMS:
        return ItemClassification.trap
    return ItemClassification.filler

def create_item(world, name: str) -> B3Item:
    return B3Item(name, get_item_classification(name), item_table[name], world.player)
