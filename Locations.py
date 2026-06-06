from BaseClasses import Location, Region
from .Items import B3_BASE_ID

B3_LOC_BASE = B3_BASE_ID + 0x10000

class B3Location(Location):
    game = "Dragon Ball Z Budokai 3"

# ─── DU Battle Locations ──────────────────────────────────────────────────────
# One location per fight in each DU campaign.
# Key: location name → AP ID
# Format: "<Character> DU - <Fight Name>"

DU_BATTLE_LOCATIONS = {
    # ── Goku DU ──────────────────────────────────────────────────
    "Goku DU - Raditz":                         B3_LOC_BASE + 0x001,
    "Goku DU - Nappa":                          B3_LOC_BASE + 0x002,
    "Goku DU - Vegeta":                         B3_LOC_BASE + 0x003,
    "Goku DU - Recoome":                        B3_LOC_BASE + 0x004,
    "Goku DU - Ginyu":                          B3_LOC_BASE + 0x005,
    "Goku DU - Frieza Final Form":              B3_LOC_BASE + 0x006,
    "Goku DU - Frieza 100%":                    B3_LOC_BASE + 0x007,
    "Goku DU - Perfect Cell":                   B3_LOC_BASE + 0x008,
    "Goku DU - Majin Vegeta":                   B3_LOC_BASE + 0x009,
    "Goku DU - Majin Buu":                      B3_LOC_BASE + 0x00A,
    "Goku DU - Vegito vs Buuhan":               B3_LOC_BASE + 0x00B,
    "Goku DU - Super Buu (Inside Buu)":         B3_LOC_BASE + 0x00C,
    "Goku DU - Kid Buu":                        B3_LOC_BASE + 0x00D,

    # ── Kid Gohan DU ─────────────────────────────────────────────
    "Kid Gohan DU - Piccolo":                   B3_LOC_BASE + 0x020,
    "Kid Gohan DU - Saibaman":                  B3_LOC_BASE + 0x021,
    "Kid Gohan DU - Nappa":                     B3_LOC_BASE + 0x022,
    "Kid Gohan DU - Recoome":                   B3_LOC_BASE + 0x023,
    "Kid Gohan DU - First Form Frieza":         B3_LOC_BASE + 0x024,

    # ── Teen Gohan DU ────────────────────────────────────────────
    "Teen Gohan DU - Piccolo":                  B3_LOC_BASE + 0x040,
    "Teen Gohan DU - Krillin":                  B3_LOC_BASE + 0x041,
    "Teen Gohan DU - Goku":                     B3_LOC_BASE + 0x042,
    "Teen Gohan DU - Perfect Cell":             B3_LOC_BASE + 0x043,
    "Teen Gohan DU - Super Perfect Cell":       B3_LOC_BASE + 0x044,

    # ── Adult Gohan DU ───────────────────────────────────────────
    "Adult Gohan DU - Goten":                   B3_LOC_BASE + 0x060,
    "Adult Gohan DU - Videl":                   B3_LOC_BASE + 0x061,
    "Adult Gohan DU - Dabura":                  B3_LOC_BASE + 0x062,
    "Adult Gohan DU - Majin Buu":               B3_LOC_BASE + 0x063,
    "Adult Gohan DU - Super Buu":               B3_LOC_BASE + 0x064,

    # ── Krillin DU ───────────────────────────────────────────────
    "Krillin DU - Nappa":                       B3_LOC_BASE + 0x080,
    "Krillin DU - Saibaman":                    B3_LOC_BASE + 0x081,
    "Krillin DU - Recoome":                     B3_LOC_BASE + 0x082,
    "Krillin DU - Ginyu as Goku":               B3_LOC_BASE + 0x083,
    "Krillin DU - Frieza Second Form":          B3_LOC_BASE + 0x084,
    "Krillin DU - Frieza Final Form":           B3_LOC_BASE + 0x085,
    "Krillin DU - Frieza Final Form (Ginyu)":   B3_LOC_BASE + 0x086,
    "Krillin DU - Perfect Cell":                B3_LOC_BASE + 0x087,

    # ── Piccolo DU ───────────────────────────────────────────────
    "Piccolo DU - Raditz (SBC)":                B3_LOC_BASE + 0x0A0,
    "Piccolo DU - Kid Gohan":                   B3_LOC_BASE + 0x0A1,
    "Piccolo DU - Saibamen":                    B3_LOC_BASE + 0x0A2,
    "Piccolo DU - Goku":                        B3_LOC_BASE + 0x0A3,
    "Piccolo DU - Nappa":                       B3_LOC_BASE + 0x0A4,
    "Piccolo DU - Vegeta":                      B3_LOC_BASE + 0x0A5,
    "Piccolo DU - Raditz (Kame House)":         B3_LOC_BASE + 0x0A6,
    "Piccolo DU - Frieza 2nd Form":             B3_LOC_BASE + 0x0A7,
    "Piccolo DU - Frieza 3rd Form":             B3_LOC_BASE + 0x0A8,
    "Piccolo DU - Frieza Final Form":           B3_LOC_BASE + 0x0A9,
    "Piccolo DU - Cooler":                      B3_LOC_BASE + 0x0AA,
    "Piccolo DU - Metal Cooler":                B3_LOC_BASE + 0x0AB,
    "Piccolo DU - Dr. Gero":                    B3_LOC_BASE + 0x0AC,
    "Piccolo DU - Cell 1st Form":               B3_LOC_BASE + 0x0AD,
    "Piccolo DU - Cell 1st Form (Baba)":        B3_LOC_BASE + 0x0AE,
    "Piccolo DU - Perfect Cell":                B3_LOC_BASE + 0x0AF,
    "Piccolo DU - Android 17":                  B3_LOC_BASE + 0x0B0,
    "Piccolo DU - Dabura":                      B3_LOC_BASE + 0x0B1,
    "Piccolo DU - Super Buu":                   B3_LOC_BASE + 0x0B2,
    "Piccolo DU - Broly":                       B3_LOC_BASE + 0x0B3,

    # ── Tien DU ──────────────────────────────────────────────────
    "Tien DU - Saibamen":                       B3_LOC_BASE + 0x0C0,
    "Tien DU - Nappa":                          B3_LOC_BASE + 0x0C1,
    "Tien DU - Cell 2nd Form":                  B3_LOC_BASE + 0x0C2,
    "Tien DU - Cell Jr.":                       B3_LOC_BASE + 0x0C3,
    "Tien DU - Super Buu (Gotenks)":            B3_LOC_BASE + 0x0C4,
    "Tien DU - Super Buu (Gotenks/Chiaotzu)":   B3_LOC_BASE + 0x0C5,
    "Tien DU - Yamcha":                         B3_LOC_BASE + 0x0C6,

    # ── Yamcha DU ────────────────────────────────────────────────
    "Yamcha DU - Saibamen":                     B3_LOC_BASE + 0x0E0,
    "Yamcha DU - Dr. Gero":                     B3_LOC_BASE + 0x0E1,
    "Yamcha DU - Tien":                         B3_LOC_BASE + 0x0E2,
    "Yamcha DU - Vegeta":                       B3_LOC_BASE + 0x0E3,

    # ── Uub DU ───────────────────────────────────────────────────
    "Uub DU - Goku (WT)":                       B3_LOC_BASE + 0x100,
    "Uub DU - Majin Buu":                       B3_LOC_BASE + 0x101,
    "Uub DU - Vegeta & Goku":                   B3_LOC_BASE + 0x102,
    "Uub DU - Goku (Roshi)":                    B3_LOC_BASE + 0x103,
    "Uub DU - Omega Shenron":                   B3_LOC_BASE + 0x104,

    # ── Broly DU ─────────────────────────────────────────────────
    "Broly DU - Videl":                         B3_LOC_BASE + 0x120,
    "Broly DU - Kid Trunks":                    B3_LOC_BASE + 0x121,
    "Broly DU - Goten":                         B3_LOC_BASE + 0x122,
    "Broly DU - Gohan":                         B3_LOC_BASE + 0x123,
    "Broly DU - Gohan (WT post-game)":          B3_LOC_BASE + 0x124,
    "Broly DU - Gohan (Rematch)":               B3_LOC_BASE + 0x125,
    "Broly DU - Goku":                          B3_LOC_BASE + 0x126,
    # Vegeta DU
    "Vegeta DU - Goku":                                          B3_LOC_BASE + 0x140,
    "Vegeta DU - Kid Gohan":                                     B3_LOC_BASE + 0x141,
    "Vegeta DU - Recoome":                                       B3_LOC_BASE + 0x142,
    "Vegeta DU - Frieza (1st Form)":                             B3_LOC_BASE + 0x143,
    "Vegeta DU - Frieza (Final Form)":                           B3_LOC_BASE + 0x144,
    "Vegeta DU - Cooler":                                        B3_LOC_BASE + 0x145,
    "Vegeta DU - Android 17":                                    B3_LOC_BASE + 0x146,
    "Vegeta DU - Android 18":                                    B3_LOC_BASE + 0x147,
    "Vegeta DU - Cell (17 Absorbed)":                            B3_LOC_BASE + 0x148,
    "Vegeta DU - Cell (Perfect)":                                B3_LOC_BASE + 0x149,
    "Vegeta DU - Goku (SS2)":                                    B3_LOC_BASE + 0x14A,
    "Vegeta DU - Majin Buu":                                     B3_LOC_BASE + 0x14B,
    "Vegeta DU - Super Buu (Gohan Absorbed)":                    B3_LOC_BASE + 0x14C,
    "Vegeta DU - Super Buu (Gohan Absorbed) [Supreme Kai]":      B3_LOC_BASE + 0x14D,
    "Vegeta DU - Super Buu (Inside Buu)":                        B3_LOC_BASE + 0x14E,
    "Vegeta DU - Super Buu (Inside Buu) [Supreme Kai]":          B3_LOC_BASE + 0x14F,
    "Vegeta DU - Kid Buu":                                       B3_LOC_BASE + 0x150,
    "Vegeta DU - Broly":                                         B3_LOC_BASE + 0x151,
    "Vegeta DU - Broly [Goku Friendship]":                       B3_LOC_BASE + 0x152,
    "Vegeta DU - Gotenks (SS)":                                  B3_LOC_BASE + 0x153,
    "Vegeta DU - Goku (SS4)":                                    B3_LOC_BASE + 0x154,
}

# ─── Shop Locations ───────────────────────────────────────────────────────────
# 10 shop slots, AP controls the stock.

from .data.Constants import SHOP_CAPSULE_POOL

SHOP_LOCATIONS = {
    f"Shop: {SHOP_CAPSULE_POOL[i][2]}": B3_LOC_BASE + 0x500 + i
    for i in range(len(SHOP_CAPSULE_POOL))
}


# ─── DU Completion Locations ─────────────────────────────────────────────────
# One location per completed Dragon Universe campaign.

DU_COMPLETION_LOCATIONS = {
    "Complete Goku DU":        B3_LOC_BASE + 0x600,
    "Complete Kid Gohan DU":   B3_LOC_BASE + 0x601,
    "Complete Teen Gohan DU":  B3_LOC_BASE + 0x602,
    "Complete Adult Gohan DU": B3_LOC_BASE + 0x603,
    "Complete Vegeta DU":      B3_LOC_BASE + 0x604,
    "Complete Krillin DU":     B3_LOC_BASE + 0x605,
    "Complete Piccolo DU":     B3_LOC_BASE + 0x606,
    "Complete Tien DU":        B3_LOC_BASE + 0x607,
    "Complete Yamcha DU":      B3_LOC_BASE + 0x608,
    "Complete Uub DU":         B3_LOC_BASE + 0x609,
    "Complete Broly DU":       B3_LOC_BASE + 0x60A,
}

DU_COMPLETION_BY_CHAR_ID = {
    0x00: "Complete Goku DU",
    0x02: "Complete Kid Gohan DU",
    0x03: "Complete Teen Gohan DU",
    0x04: "Complete Adult Gohan DU",
    0x07: "Complete Vegeta DU",
    0x0A: "Complete Krillin DU",
    0x0B: "Complete Piccolo DU",
    0x0C: "Complete Tien DU",
    0x0D: "Complete Yamcha DU",
    0x11: "Complete Uub DU",
    0x22: "Complete Broly DU",
}

# ─── Full location table ──────────────────────────────────────────────────────

DRAGON_ARENA_LOCATIONS = {
    f"Dragon Arena Fight {i+1}": B3_LOC_BASE + 0x700 + i
    for i in range(380)
}

location_table = {}
location_table.update(DU_BATTLE_LOCATIONS)
location_table.update(SHOP_LOCATIONS)
location_table.update(DU_COMPLETION_LOCATIONS)
location_table.update(DRAGON_ARENA_LOCATIONS)

def get_location_names():
    return {name: loc_id for name, loc_id in location_table.items()}
