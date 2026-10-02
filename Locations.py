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
    "Goku DU - Saiyan Saga - Ch.1 - Raditz":              B3_LOC_BASE + 0x001,
    "Goku DU - Saiyan Saga - Ch.2 - Nappa":               B3_LOC_BASE + 0x002,
    "Goku DU - Saiyan Saga - Ch.3 - Vegeta":              B3_LOC_BASE + 0x003,
    "Goku DU - Frieza Saga - Ch.1 - Recoome":             B3_LOC_BASE + 0x004,
    "Goku DU - Frieza Saga - Ch.2 - Ginyu":               B3_LOC_BASE + 0x005,
    "Goku DU - Frieza Saga - Ch.3 - Frieza Final Form":   B3_LOC_BASE + 0x006,
    "Goku DU - Frieza Saga - Ch.4 - Frieza 100%":         B3_LOC_BASE + 0x007,
    "Goku DU - Cell Saga - Ch.1 - Perfect Cell":          B3_LOC_BASE + 0x008,
    "Goku DU - Buu Saga - Ch.1 - Majin Vegeta":           B3_LOC_BASE + 0x009,
    "Goku DU - Buu Saga - Ch.1 - Majin Buu":              B3_LOC_BASE + 0x00A,
    "Goku DU - Buu Saga - Ch.1 - Vegito vs Buuhan":       B3_LOC_BASE + 0x00B,
    "Goku DU - Buu Saga - Ch.1 - Super Buu (Inside Buu)": B3_LOC_BASE + 0x00C,
    "Goku DU - Buu Saga - Ch.1 - Kid Buu":                B3_LOC_BASE + 0x00D,

    # ── Kid Gohan DU ─────────────────────────────────────────────
    "Kid Gohan DU - Saiyan Saga - Ch.1 - Piccolo":         B3_LOC_BASE + 0x020,
    "Kid Gohan DU - Saiyan Saga - Ch.2 - Saibaman":        B3_LOC_BASE + 0x021,
    "Kid Gohan DU - Saiyan Saga - Ch.3 - Nappa":           B3_LOC_BASE + 0x022,
    "Kid Gohan DU - Frieza Saga - Ch.1 - Recoome":         B3_LOC_BASE + 0x023,
    "Kid Gohan DU - Frieza Saga - Ch.2 - Frieza 3rd Form": B3_LOC_BASE + 0x024,

    # ── Teen Gohan DU ────────────────────────────────────────────
    "Teen Gohan DU - Cell Saga - Ch.1 - Piccolo":            B3_LOC_BASE + 0x040,
    "Teen Gohan DU - Cell Saga - Ch.2 - Krillin":            B3_LOC_BASE + 0x041,
    "Teen Gohan DU - Cell Saga - Ch.2 - Goku":               B3_LOC_BASE + 0x042,
    "Teen Gohan DU - Cell Saga - Ch.2 - Perfect Cell":       B3_LOC_BASE + 0x043,
    "Teen Gohan DU - Cell Saga - Ch.2 - Super Perfect Cell": B3_LOC_BASE + 0x044,

    # ── Adult Gohan DU ───────────────────────────────────────────
    "Adult Gohan DU - Buu Saga - Ch.1 - Goten":     B3_LOC_BASE + 0x060,
    "Adult Gohan DU - Buu Saga - Ch.2 - Videl":     B3_LOC_BASE + 0x061,
    "Adult Gohan DU - Buu Saga - Ch.2 - Dabura":    B3_LOC_BASE + 0x062,
    "Adult Gohan DU - Buu Saga - Ch.3 - Majin Buu": B3_LOC_BASE + 0x063,
    "Adult Gohan DU - Buu Saga - Ch.3 - Super Buu": B3_LOC_BASE + 0x064,

    # ── Krillin DU ───────────────────────────────────────────────
    "Krillin DU - Saiyan Saga - Ch.2 - Nappa":                     B3_LOC_BASE + 0x080,
    "Krillin DU - Saiyan Saga - Ch.1 - Saibaman":                  B3_LOC_BASE + 0x081,
    "Krillin DU - Frieza Saga - Ch.1 - Recoome":                   B3_LOC_BASE + 0x082,
    "Krillin DU - Frieza Saga - Ch.2 - Ginyu as Goku":             B3_LOC_BASE + 0x083,
    "Krillin DU - Frieza Saga - Ch.3 - Frieza 2nd Form":           B3_LOC_BASE + 0x084,
    "Krillin DU - Frieza Saga - Ch.4 - Frieza Final Form":         B3_LOC_BASE + 0x085,
    "Krillin DU - Frieza Saga - Ch.4 - Frieza Final Form (Ginyu)": B3_LOC_BASE + 0x086,
    "Krillin DU - Cell Saga - Ch.1 - Perfect Cell":                B3_LOC_BASE + 0x087,

    # ── Piccolo DU ───────────────────────────────────────────────
    "Piccolo DU - Saiyan Saga - Ch.1 - Raditz (SBC)":        B3_LOC_BASE + 0x0A0,
    "Piccolo DU - Saiyan Saga - Ch.2 - Kid Gohan":           B3_LOC_BASE + 0x0A1,
    "Piccolo DU - Saiyan Saga - Ch.3 - Saibamen":            B3_LOC_BASE + 0x0A2,
    "Piccolo DU - Saiyan Saga - Ch.2 - Goku":                B3_LOC_BASE + 0x0A3,
    "Piccolo DU - Saiyan Saga - Ch.4 - Nappa":               B3_LOC_BASE + 0x0A4,
    "Piccolo DU - Saiyan Saga - Ch.3 - Vegeta":              B3_LOC_BASE + 0x0A5,
    "Piccolo DU - Saiyan Saga - Ch.1 - Raditz (Kame House)": B3_LOC_BASE + 0x0A6,
    "Piccolo DU - Frieza Saga - Ch.1 - Frieza 2nd Form":     B3_LOC_BASE + 0x0A7,
    "Piccolo DU - Frieza Saga - Ch.2 - Frieza 3rd Form":     B3_LOC_BASE + 0x0A8,
    "Piccolo DU - Frieza Saga - Ch.2 - Frieza Final Form":   B3_LOC_BASE + 0x0A9,
    "Piccolo DU - Frieza Saga - Ch.2 - Cooler":              B3_LOC_BASE + 0x0AA,
    "Piccolo DU - Frieza Saga - Ch.3 - Metal Cooler":        B3_LOC_BASE + 0x0AB,
    "Piccolo DU - Cell Saga - Ch.1 - Dr. Gero":              B3_LOC_BASE + 0x0AC,
    "Piccolo DU - Cell Saga - Ch.2 - Imperfect Cell":        B3_LOC_BASE + 0x0AD,
    "Piccolo DU - Cell Saga - Ch.2 - Imperfect Cell (Baba)": B3_LOC_BASE + 0x0AE,
    "Piccolo DU - Cell Saga - Ch.3 - Perfect Cell":          B3_LOC_BASE + 0x0AF,
    "Piccolo DU - Cell Saga - Ch.3 - Android 17":            B3_LOC_BASE + 0x0B0,
    "Piccolo DU - Buu Saga - Ch.1 - Dabura":                 B3_LOC_BASE + 0x0B1,
    "Piccolo DU - Buu Saga - Ch.1 - Super Buu":              B3_LOC_BASE + 0x0B2,
    "Piccolo DU - Buu Saga - Ch.2 - Broly":                  B3_LOC_BASE + 0x0B3,

    # ── Tien DU ──────────────────────────────────────────────────
    "Tien DU - Saiyan Saga - Ch.1 - Saibamen":                  B3_LOC_BASE + 0x0C0,
    "Tien DU - Saiyan Saga - Ch.2 - Nappa":                     B3_LOC_BASE + 0x0C1,
    "Tien DU - Cell Saga - Ch.1 - Semi-Perfect Cell":           B3_LOC_BASE + 0x0C2,
    "Tien DU - Cell Saga - Ch.2 - Cell Jr.":                    B3_LOC_BASE + 0x0C3,
    "Tien DU - Buu Saga - Ch.1 - Super Buu (Gotenks)":          B3_LOC_BASE + 0x0C4,
    "Tien DU - Buu Saga - Ch.1 - Super Buu (Gotenks/Chiaotzu)": B3_LOC_BASE + 0x0C5,
    "Tien DU - Buu Saga - Ch.2 - Yamcha":                       B3_LOC_BASE + 0x0C6,

    # ── Yamcha DU ────────────────────────────────────────────────
    "Yamcha DU - Saiyan Saga - Ch.1 - Saibamen": B3_LOC_BASE + 0x0E0,
    "Yamcha DU - Cell Saga - Ch.1 - Dr. Gero":   B3_LOC_BASE + 0x0E1,
    "Yamcha DU - Buu Saga - Ch.1 - Tien":        B3_LOC_BASE + 0x0E2,
    "Yamcha DU - Buu Saga - Ch.1 - Vegeta":      B3_LOC_BASE + 0x0E3,

    # ── Uub DU ───────────────────────────────────────────────────
    "Uub DU - Buu Saga - Ch.1 - Goku (WT)":     B3_LOC_BASE + 0x100,
    "Uub DU - Buu Saga - Ch.2 - Majin Buu":     B3_LOC_BASE + 0x101,
    "Uub DU - Buu Saga - Ch.2 - Vegeta & Goku": B3_LOC_BASE + 0x102,
    "Uub DU - Buu Saga - Ch.3 - Goku (Roshi)":  B3_LOC_BASE + 0x103,
    "Uub DU - Buu Saga - Ch.4 - Omega Shenron": B3_LOC_BASE + 0x104,

    # ── Broly DU ─────────────────────────────────────────────────
    "Broly DU - Buu Saga - Ch.1 - Videl":                B3_LOC_BASE + 0x120,
    "Broly DU - Buu Saga - Ch.1 - Kid Trunks":           B3_LOC_BASE + 0x121,
    "Broly DU - Buu Saga - Ch.1 - Goten":                B3_LOC_BASE + 0x122,
    "Broly DU - Buu Saga - Ch.1 - Gohan":                B3_LOC_BASE + 0x123,
    "Broly DU - Buu Saga - Ch.1 - Gohan (WT post-game)": B3_LOC_BASE + 0x124,
    "Broly DU - Buu Saga - Ch.1 - Gohan (Rematch)":      B3_LOC_BASE + 0x125,
    "Broly DU - Buu Saga - Ch.1 - Goku":                 B3_LOC_BASE + 0x126,
    # Vegeta DU
    "Vegeta DU - Saiyan Saga - Ch.1 - Goku":                                  B3_LOC_BASE + 0x140,
    "Vegeta DU - Saiyan Saga - Ch.2 - Kid Gohan":                             B3_LOC_BASE + 0x141,
    "Vegeta DU - Frieza Saga - Ch.1 - Recoome":                               B3_LOC_BASE + 0x142,
    "Vegeta DU - Frieza Saga - Ch.2 - Frieza 1st Form":                       B3_LOC_BASE + 0x143,
    "Vegeta DU - Frieza Saga - Ch.3 - Frieza Final Form":                     B3_LOC_BASE + 0x144,
    "Vegeta DU - Frieza Saga - Ch.3 - Cooler":                                B3_LOC_BASE + 0x145,
    "Vegeta DU - Cell Saga - Ch.1 - Android 17":                              B3_LOC_BASE + 0x146,
    "Vegeta DU - Cell Saga - Ch.1 - Android 18":                              B3_LOC_BASE + 0x147,
    "Vegeta DU - Cell Saga - Ch.2 - Semi-Perfect Cell":                       B3_LOC_BASE + 0x148,
    "Vegeta DU - Cell Saga - Ch.3 - Perfect Cell":                            B3_LOC_BASE + 0x149,
    "Vegeta DU - Buu Saga - Ch.1 - Goku (SS2)":                               B3_LOC_BASE + 0x14A,
    "Vegeta DU - Buu Saga - Ch.1 - Majin Buu":                                B3_LOC_BASE + 0x14B,
    "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Gohan Absorbed)":               B3_LOC_BASE + 0x14C,
    "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Gohan Absorbed) [Supreme Kai]": B3_LOC_BASE + 0x14D,
    "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Inside Buu)":                   B3_LOC_BASE + 0x14E,
    "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Inside Buu) [Supreme Kai]":     B3_LOC_BASE + 0x14F,
    "Vegeta DU - Buu Saga - Ch.2 - Kid Buu":                                  B3_LOC_BASE + 0x150,
    "Vegeta DU - Buu Saga - Ch.2 - Broly":                                    B3_LOC_BASE + 0x151,
    "Vegeta DU - Buu Saga - Ch.2 - Broly [Goku Friendship]":                  B3_LOC_BASE + 0x152,
    "Vegeta DU - Buu Saga - Ch.3 - Gotenks (SS)":                             B3_LOC_BASE + 0x153,
    "Vegeta DU - Buu Saga - Ch.3 - Goku (SS4)":                               B3_LOC_BASE + 0x154,
}

# Fights that need a second playthrough or an alternate route in the normal game.
# The map helper puts them on the map, so they are only locations with it on.
DU_BATTLE_LOCATIONS_MAP_HELPER = {
    "Goku DU - Saiyan Saga - Ch.1 - Tien (World Tournament)":          B3_LOC_BASE + 0x00E,
    "Goku DU - Frieza Saga - Ch.4 - Cooler":                           B3_LOC_BASE + 0x00F,
    "Goku DU - Frieza Saga - Ch.4 - Vegeta (Namek)":                   B3_LOC_BASE + 0x010,
    "Goku DU - Frieza Saga - Ch.5 - Metal Cooler":                     B3_LOC_BASE + 0x011,
    "Goku DU - Frieza Saga - Ch.5 - Cooler (Rematch)":                 B3_LOC_BASE + 0x012,
    "Goku DU - Frieza Saga - Ch.3 - Frieza Final Form (Cooler Route)": B3_LOC_BASE + 0x013,
    "Goku DU - Buu Saga - Ch.1 - Uub":                                 B3_LOC_BASE + 0x014,
    "Goku DU - Buu Saga - Ch.1 - Broly":                               B3_LOC_BASE + 0x015,
    "Goku DU - Buu Saga - Ch.2 - Gotenks (as Gogeta)":                 B3_LOC_BASE + 0x016,
    "Goku DU - Buu Saga - Ch.2 - Omega Shenron":                       B3_LOC_BASE + 0x017,
    "Goku DU - Buu Saga - Ch.1 - Vegito vs Buuhan (2nd Route)":        B3_LOC_BASE + 0x018,
    "Goku DU - Buu Saga - Ch.1 - Super Buu (Inside Buu) (2nd Route)":  B3_LOC_BASE + 0x019,
    "Goku DU - Buu Saga - Ch.2 - Gotenks (as Gogeta) (Ending)":        B3_LOC_BASE + 0x01A,
    "Kid Gohan DU - Saiyan Saga - Ch.1 - Goku":                        B3_LOC_BASE + 0x025,
    "Kid Gohan DU - Saiyan Saga - Ch.2 - Saibaman (2nd Route)":        B3_LOC_BASE + 0x026,
    "Kid Gohan DU - Frieza Saga - Ch.2 - Goku (Namek)":                B3_LOC_BASE + 0x027,
    "Kid Gohan DU - Frieza Saga - Ch.3 - Cooler":                      B3_LOC_BASE + 0x028,
    "Teen Gohan DU - Cell Saga - Ch.2 - Tien":                         B3_LOC_BASE + 0x045,
    "Teen Gohan DU - Cell Saga - Ch.2 - Yamcha":                       B3_LOC_BASE + 0x046,
    "Adult Gohan DU - Buu Saga - Ch.2 - Vegeta":                       B3_LOC_BASE + 0x065,
    "Adult Gohan DU - Buu Saga - Ch.2 - Piccolo":                      B3_LOC_BASE + 0x066,
    "Adult Gohan DU - Buu Saga - Ch.2 - Dabura (2nd Route)":           B3_LOC_BASE + 0x067,
    "Adult Gohan DU - Buu Saga - Ch.3 - Majin Vegeta":                 B3_LOC_BASE + 0x068,
    "Adult Gohan DU - Buu Saga - Ch.4 - Kid Buu":                      B3_LOC_BASE + 0x069,
    "Adult Gohan DU - Buu Saga - Ch.5 - Broly":                        B3_LOC_BASE + 0x06A,
    "Yamcha DU - Saiyan Saga - Ch.1 - Saibamen (2nd Route)":           B3_LOC_BASE + 0x0E4,
    "Vegeta DU - Buu Saga - Ch.1 - Adult Gohan":                       B3_LOC_BASE + 0x155,
    "Vegeta DU - Buu Saga - Ch.1 - Piccolo":                           B3_LOC_BASE + 0x156,
}

# ─── Interactsanity Locations ─────────────────────────────────────────────────
# Talk scenes and item pickups on the Dragon Universe map (Interactsanity option).
from .data.MapLocations import INTERACT_LOCATION_OFFSETS

INTERACT_LOCATIONS = {
    name: B3_LOC_BASE + offset for name, offset in INTERACT_LOCATION_OFFSETS.items()
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

# Dragon Balls: 7 per DU character. Wishes: 1 per character.
_DU_CHARS = ["Goku", "Kid Gohan", "Teen Gohan", "Gohan", "Vegeta", "Krillin",
             "Piccolo", "Tien", "Yamcha", "Uub", "Broly"]
DRAGON_BALL_LOCATIONS = {
    f"Dragon Ball: {ch} #{b+1}": B3_LOC_BASE + 0x900 + ci * 8 + b
    for ci, ch in enumerate(_DU_CHARS)
    for b in range(7)
}
WISH_LOCATIONS = {
    f"Wish: {ch}": B3_LOC_BASE + 0xA00 + ci
    for ci, ch in enumerate(_DU_CHARS)
}

location_table = {}
location_table.update(DU_BATTLE_LOCATIONS)
location_table.update(DU_BATTLE_LOCATIONS_MAP_HELPER)
location_table.update(INTERACT_LOCATIONS)
location_table.update(SHOP_LOCATIONS)
location_table.update(DU_COMPLETION_LOCATIONS)
location_table.update(DRAGON_ARENA_LOCATIONS)
location_table.update(DRAGON_BALL_LOCATIONS)
location_table.update(WISH_LOCATIONS)

def get_location_names():
    return {name: loc_id for name, loc_id in location_table.items()}
