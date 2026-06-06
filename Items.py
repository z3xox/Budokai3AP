from BaseClasses import Item, ItemClassification

B3_BASE_ID = 0xDB3000

class B3Item(Item):
    game = "Dragon Ball Z Budokai 3"

# ─── Saga Unlock Items ───────────────────────────────────────────────────────
# These gate progression through Dragon Universe sagas.

SAGA_ITEMS = {
    "Frieza Saga Unlock":  B3_BASE_ID + 0x01,
    "Cell Saga Unlock":    B3_BASE_ID + 0x02,
    "Buu Saga Unlock":     B3_BASE_ID + 0x03,
}

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

# ─── Full item table ──────────────────────────────────────────────────────────

item_table = {}
item_table.update(SAGA_ITEMS)
item_table.update(CHARACTER_ITEMS)
item_table.update(CAPSULE_ITEMS)
item_table.update(TRAP_ITEMS)
item_table.update(SPECIAL_ITEMS)

def get_item_classification(name: str) -> ItemClassification:
    if name in SAGA_ITEMS:
        return ItemClassification.progression
    if name in CHARACTER_ITEMS:
        return ItemClassification.progression
    if name == "Dragon Arena Ticket":
        return ItemClassification.progression
    if name in SPECIAL_ITEMS:
        return ItemClassification.useful
    if name in TRAP_ITEMS:
        return ItemClassification.trap
    return ItemClassification.filler

def create_item(world, name: str) -> B3Item:
    return B3Item(name, get_item_classification(name), item_table[name], world.player)
