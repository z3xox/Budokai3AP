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

CAPSULE_ITEMS = {
    "Capsule: Kamehameha":      B3_BASE_ID + 0x100,
    "Capsule: Galick Gun":      B3_BASE_ID + 0x101,
    "Capsule: Final Flash":     B3_BASE_ID + 0x102,
    "Capsule: Special Beam Cannon": B3_BASE_ID + 0x103,
    "Capsule: Kaioken":         B3_BASE_ID + 0x104,
    "Capsule: Super Saiyan":    B3_BASE_ID + 0x105,
    "Capsule: Spirit Bomb":     B3_BASE_ID + 0x106,
    "Capsule: Destructo Disc":  B3_BASE_ID + 0x107,
    "Capsule: Tri-Beam":        B3_BASE_ID + 0x108,
    "Capsule: Wolf Fang Fist":  B3_BASE_ID + 0x109,
    "Capsule: Senzu Bean":      B3_BASE_ID + 0x10A,
    "Capsule: Z-Sword":         B3_BASE_ID + 0x10B,
    "Zenie x500":               B3_BASE_ID + 0x110,
    "Zenie x1000":              B3_BASE_ID + 0x111,
    "Zenie x2000":              B3_BASE_ID + 0x112,
}

# ─── Trap Items ───────────────────────────────────────────────────────────────

TRAP_ITEMS = {
    "HP Drain Trap":  B3_BASE_ID + 0x200,
}

# ─── Full item table ──────────────────────────────────────────────────────────

item_table = {}
item_table.update(SAGA_ITEMS)
item_table.update(CHARACTER_ITEMS)
item_table.update(CAPSULE_ITEMS)
item_table.update(TRAP_ITEMS)

def get_item_classification(name: str) -> ItemClassification:
    if name in SAGA_ITEMS:
        return ItemClassification.progression
    if name in CHARACTER_ITEMS:
        return ItemClassification.progression
    if name in TRAP_ITEMS:
        return ItemClassification.trap
    return ItemClassification.filler

def create_item(world, name: str) -> B3Item:
    return B3Item(name, get_item_classification(name), item_table[name], world.player)
