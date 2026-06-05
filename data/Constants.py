# Dragon Ball Z Budokai 3 - Memory Address Constants
# NTSC-U, SLUS-20998, CRC C97EF0A4

GAME_ID = "SLUS-20998"
GAME_CRC = "c97ef0a4"

# ─── Cave ────────────────────────────────────────────────────────────────────
ADDR_CAVE          = 0x00600000   # cave code start
ADDR_DEBUG         = 0x00605000   # debug area (hit counter, mode, char, battle)
ADDR_SCRATCH       = 0x00606000   # register save area (t0,t1,t2,t3)
ADDR_INTERCEPT     = 0x001B32A8   # patched instruction
ADDR_RETURN        = 0x001B32AC   # jump-back target
CAVE_JUMP          = 0x08180000   # j 0x00600000
ORIG_INSTR         = 0x864206B0   # lh v0,0x6B0(s2)

# ─── Game State ──────────────────────────────────────────────────────────────
ADDR_SCREEN        = 0x0046A5B0   # 16-bit screen ID
ADDR_MODE          = 0x00543C20   # DU mode byte (0x01 = DU)
ADDR_DU_CHAR       = 0x00543C24   # current DU character selector
ADDR_ZENIE_RT      = 0x00543D28   # real-time Zenie (32-bit)
ADDR_ZENIE_DU      = 0x004C6F08   # DU Zenie (32-bit)

SCREEN_SHOP        = 0x0016

# ─── Battle ──────────────────────────────────────────────────────────────────
ADDR_P1_CHAR       = 0x0044B5C0
ADDR_P1_CHAR_T4    = 0x0044B5C4   # template/form field - clear on swap
ADDR_P1_CAPS       = 0x0044B5E4   # capsule block (16 bytes)
ADDR_P2_CHAR       = 0x0044B610
ADDR_P2_CHAR_T4    = 0x0044B614   # template/form field - clear on swap
ADDR_P2_CAPS       = 0x0044B634   # capsule block (16 bytes)
ADDR_STAGE_SELECT  = 0x0044B6F4
ADDR_BATTLE_MOD    = 0x0044B708   # 0x00020003 = HP drain

# ─── Shop ────────────────────────────────────────────────────────────────────
ADDR_SHOP_COUNT    = 0x0088DE2C   # number of items (0-11)
ADDR_SHOP_TABLE    = 0x0088DE3C   # item entries (20 bytes each)
ADDR_CAPS_OWN_BASE = 0x005510C7   # capsule ownership array

# ─── DU Character Bases ──────────────────────────────────────────────────────
# Each base + offsets below gives per-character DU state

DU_BASES = {
    "Goku":        {"du_id": 0x00, "base": 0x0049D260},
    "Kid Gohan":   {"du_id": 0x02, "base": 0x0049F680},
    "Teen Gohan":  {"du_id": 0x03, "base": 0x004A0890},
    "Adult Gohan": {"du_id": 0x04, "base": 0x004A1AA0},
    "Vegeta":      {"du_id": 0x07, "base": 0x004A50D0},
    "Krillin":     {"du_id": 0x0A, "base": 0x004A8700},
    "Piccolo":     {"du_id": 0x0B, "base": 0x004A9910},
    "Tien":        {"du_id": 0x0C, "base": 0x004AAB20},
    "Yamcha":      {"du_id": 0x0D, "base": 0x004ABD30},
    "Uub":         {"du_id": 0x11, "base": 0x004B0570},
    "Broly":       {"du_id": 0x22, "base": 0x004C3880},
}

# Per-character DU offsets
OFFSET_BATTLE      = 0x14   # battle state (0xFF = idle, 0x1518XXXX = in fight)
OFFSET_SAGA        = 0x1C   # saga (0x00=Saiyan, 0x01=Frieza, 0x02=Cell, 0x03=Buu, 0x04=GT, 0x05=Extra)
OFFSET_BATTLE_COMP = 0x44   # battle completion flag (0x07 → 0x01 on win)
OFFSET_DRAGONBALLS = 0x24   # Dragon Ball bitmask
OFFSET_LEVEL       = 0x27   # current level
OFFSET_EXP         = 0x40   # total EXP (32-bit)

# ─── Battle ID Table ─────────────────────────────────────────────────────────
# (char_name, saga_id, battle_low16) → location_name

FIGHT_LOCATIONS = {
    # Goku DU
    ("Goku", 0x00, 0x01): "Goku DU - Raditz",
    ("Goku", 0x00, 0x03): "Goku DU - Nappa",
    ("Goku", 0x00, 0x05): "Goku DU - Vegeta",
    ("Goku", 0x01, 0x01): "Goku DU - Recoome",
    ("Goku", 0x01, 0x03): "Goku DU - Ginyu",
    ("Goku", 0x01, 0x05): "Goku DU - Frieza Final Form",
    ("Goku", 0x01, 0x10): "Goku DU - Frieza 100%",
    ("Goku", 0x02, 0x01): "Goku DU - Perfect Cell",
    ("Goku", 0x03, 0x01): "Goku DU - Majin Vegeta",
    ("Goku", 0x03, 0x04): "Goku DU - Majin Buu",
    ("Goku", 0x03, 0x06): "Goku DU - Vegito vs Buuhan",
    ("Goku", 0x03, 0x08): "Goku DU - Super Buu (Inside Buu)",
    ("Goku", 0x03, 0x0B): "Goku DU - Kid Buu",
    # Kid Gohan DU
    ("Kid Gohan", 0x00, 0x01): "Kid Gohan DU - Piccolo",
    ("Kid Gohan", 0x00, 0x18): "Kid Gohan DU - Saibaman",
    ("Kid Gohan", 0x00, 0x06): "Kid Gohan DU - Nappa",
    ("Kid Gohan", 0x01, 0x01): "Kid Gohan DU - Recoome",
    ("Kid Gohan", 0x01, 0x05): "Kid Gohan DU - First Form Frieza",
    # Teen Gohan DU
    ("Teen Gohan", 0x02, 0x01): "Teen Gohan DU - Piccolo",
    ("Teen Gohan", 0x02, 0x03): "Teen Gohan DU - Krillin",
    ("Teen Gohan", 0x02, 0x09): "Teen Gohan DU - Goku",
    ("Teen Gohan", 0x02, 0x0B): "Teen Gohan DU - Perfect Cell",
    ("Teen Gohan", 0x02, 0x0D): "Teen Gohan DU - Super Perfect Cell",
    # Adult Gohan DU
    ("Adult Gohan", 0x03, 0x01): "Adult Gohan DU - Goten",
    ("Adult Gohan", 0x03, 0x03): "Adult Gohan DU - Videl",
    ("Adult Gohan", 0x03, 0x0A): "Adult Gohan DU - Dabura",
    ("Adult Gohan", 0x03, 0x0D): "Adult Gohan DU - Majin Buu",
    ("Adult Gohan", 0x03, 0x11): "Adult Gohan DU - Super Buu",
    # Krillin DU
    ("Krillin", 0x00, 0x02): "Krillin DU - Nappa",
    ("Krillin", 0x00, 0x10): "Krillin DU - Saibaman",
    ("Krillin", 0x01, 0x01): "Krillin DU - Recoome",
    ("Krillin", 0x01, 0x03): "Krillin DU - Ginyu as Goku",
    ("Krillin", 0x01, 0x05): "Krillin DU - Frieza Second Form",
    ("Krillin", 0x01, 0x07): "Krillin DU - Frieza Final Form",
    ("Krillin", 0x01, 0x09): "Krillin DU - Frieza Final Form (Ginyu)",
    ("Krillin", 0x02, 0x01): "Krillin DU - Perfect Cell",
    # Piccolo DU
    ("Piccolo", 0x00, 0x01): "Piccolo DU - Raditz (SBC)",
    ("Piccolo", 0x00, 0x03): "Piccolo DU - Kid Gohan",
    ("Piccolo", 0x00, 0x04): "Piccolo DU - Saibamen",
    ("Piccolo", 0x00, 0x05): "Piccolo DU - Goku",
    ("Piccolo", 0x00, 0x08): "Piccolo DU - Nappa",
    ("Piccolo", 0x00, 0x0A): "Piccolo DU - Vegeta",
    ("Piccolo", 0x00, 0x0C): "Piccolo DU - Raditz (Kame House)",
    ("Piccolo", 0x01, 0x01): "Piccolo DU - Frieza 2nd Form",
    ("Piccolo", 0x01, 0x03): "Piccolo DU - Frieza 3rd Form",
    ("Piccolo", 0x01, 0x05): "Piccolo DU - Frieza Final Form",
    ("Piccolo", 0x01, 0x07): "Piccolo DU - Cooler",
    ("Piccolo", 0x01, 0x0B): "Piccolo DU - Metal Cooler",
    ("Piccolo", 0x02, 0x01): "Piccolo DU - Dr. Gero",
    ("Piccolo", 0x02, 0x04): "Piccolo DU - Cell 1st Form",
    ("Piccolo", 0x02, 0x05): "Piccolo DU - Cell 1st Form (Baba)",
    ("Piccolo", 0x02, 0x07): "Piccolo DU - Perfect Cell",
    ("Piccolo", 0x02, 0x09): "Piccolo DU - Android 17",
    ("Piccolo", 0x03, 0x01): "Piccolo DU - Dabura",
    ("Piccolo", 0x03, 0x03): "Piccolo DU - Super Buu",
    ("Piccolo", 0x03, 0x05): "Piccolo DU - Broly",
    # Tien DU
    ("Tien", 0x00, 0x08): "Tien DU - Saibamen",
    ("Tien", 0x00, 0x0C): "Tien DU - Nappa",
    ("Tien", 0x02, 0x01): "Tien DU - Cell 2nd Form",
    ("Tien", 0x02, 0x03): "Tien DU - Cell Jr.",
    ("Tien", 0x03, 0x02): "Tien DU - Super Buu (Gotenks)",
    ("Tien", 0x03, 0x03): "Tien DU - Super Buu (Gotenks/Chiaotzu)",
    ("Tien", 0x03, 0x07): "Tien DU - Yamcha",
    # Yamcha DU
    ("Yamcha", 0x00, 0x01): "Yamcha DU - Saibamen",
    ("Yamcha", 0x02, 0x01): "Yamcha DU - Dr. Gero",
    ("Yamcha", 0x03, 0x01): "Yamcha DU - Tien",
    ("Yamcha", 0x03, 0x03): "Yamcha DU - Vegeta",
    # Uub DU
    ("Uub", 0x04, 0x01): "Uub DU - Goku (WT)",
    ("Uub", 0x04, 0x03): "Uub DU - Majin Buu",
    ("Uub", 0x04, 0x06): "Uub DU - Vegeta & Goku",
    ("Uub", 0x04, 0x07): "Uub DU - Goku (Roshi)",
    ("Uub", 0x04, 0x09): "Uub DU - Omega Shenron",
    # Broly DU
    ("Broly", 0x05, 0x02): "Broly DU - Videl",
    ("Broly", 0x05, 0x05): "Broly DU - Kid Trunks",
    ("Broly", 0x05, 0x08): "Broly DU - Goten",
    ("Broly", 0x05, 0x0B): "Broly DU - Gohan",
    ("Broly", 0x05, 0x0C): "Broly DU - Gohan (WT post-game)",
    ("Broly", 0x05, 0x0F): "Broly DU - Gohan (Rematch)",
    ("Broly", 0x05, 0x12): "Broly DU - Goku",
}

# ─── Roster ──────────────────────────────────────────────────────────────────
# name → (char_id, breakthrough_capsule_index)

ROSTER = {
    "Goku":           (0x00, 0xCF),
    "Kid Goku":       (0x01, 0xD0),
    "Kid Gohan":      (0x02, 0xD1),
    "Teen Gohan":     (0x03, 0xD2),
    "Adult Gohan":    (0x04, 0xD3),
    "Great Saiyaman": (0x05, 0xD4),
    "Goten":          (0x06, 0xD5),
    "Vegeta":         (0x07, 0xD6),
    "Trunks":         (0x08, 0xD7),
    "Kid Trunks":     (0x09, 0xD8),
    "Krillin":        (0x0A, 0xD9),
    "Piccolo":        (0x0B, 0xDA),
    "Tien":           (0x0C, 0xDB),
    "Yamcha":         (0x0D, 0xDC),
    "Mr. Satan":      (0x0E, 0xDD),
    "Videl":          (0x0F, 0xDE),
    "Supreme Kai":    (0x10, 0xDF),
    "Uub":            (0x11, 0xE0),
    "Raditz":         (0x12, 0xE1),
    "Nappa":          (0x13, 0xE2),
    "Ginyu":          (0x14, 0xE3),
    "Recoome":        (0x15, 0xE4),
    "Frieza":         (0x1B, 0xE5),
    "Android 16":     (0x1C, 0xE6),
    "Android 17":     (0x1D, 0xE7),
    "Android 18":     (0x1E, 0xE8),
    "Dr. Gero":       (0x20, 0xE9),
    "Cell":           (0x21, 0xEA),
    "Majin Buu":      (0x22, 0xEB),
    "Super Buu":      (0x23, 0xEC),
    "Kid Buu":        (0x24, 0xED),
    "Dabura":         (0x25, 0xEE),
    "Cooler":         (0x26, 0xEF),
    "Bardock":        (0x27, 0xF0),
    "Broly":          (0x28, 0xF1),
    "Omega Shenron":  (0x29, 0xF2),
    "Saibaman":       (0x2A, 0xF3),
    "Cell Jr.":       (0x2B, 0xF4),
}

# ─── Capsule Shop Index Map ───────────────────────────────────────────────────
# AP item name → shop display/receive index (capsule_address - 0x4C6F39)

CAPSULE_SHOP_IDS = {
    "Capsule: Kamehameha":          0x07,
    "Capsule: Galick Gun":          0x26,
    "Capsule: Final Flash":         0x2E,
    "Capsule: Special Beam Cannon": 0x30,
    "Capsule: Kaioken":             0x01,
    "Capsule: Super Saiyan":        0x5A,
    "Capsule: Spirit Bomb":         0x0C,
    "Capsule: Destructo Disc":      0x0A,
    "Capsule: Tri-Beam":            0x0B,
    "Capsule: Wolf Fang Fist":      0x0D,
    "Capsule: Senzu Bean":          0x48,
}

# ─── Saga Unlock Saga IDs ─────────────────────────────────────────────────────
SAGA_UNLOCK_IDS = {
    "Frieza Saga Unlock": 0x01,
    "Cell Saga Unlock":   0x02,
    "Buu Saga Unlock":    0x03,
}

# ─── Stages ──────────────────────────────────────────────────────────────────
STAGES = {
    "World Tournament":         0x00,
    "Hyperbolic Time Chamber":  0x01,
    "Archipelago":              0x02,
    "Urban Area":               0x03,
    "Mountains":                0x04,
    "Plains":                   0x05,
    "Grandpa Gohan's House":    0x06,
    "Planet Namek":             0x07,
    "Cell Ring":                0x08,
    "Supreme Kai's World":      0x09,
    "Inside Buu":               0x0A,
    "Archipelago Ruins":        0x0B,
    "Urban Area Ruins":         0x0C,
    "Earth Ruins":              0x0D,
    "Dying Namek":              0x0E,
    "Red Ribbon Base":          0x10,
}

# ─── Screen IDs ───────────────────────────────────────────────────────────────
SCREEN_SHOP        = 0x0016
SCREEN_WORLD_MAP   = 0x0108
SCREEN_DU_BATTLE   = 0x0109
SCREEN_RESULTS_WIN = 0x010A
SCREEN_SHENRON     = 0x010B
SCREEN_DU_CREDITS  = 0x010C

# ─── DU Character Select Capsule Addresses ───────────────────────────────────
# Write 0x01 to show character, 0x00 to hide in DU character select
DU_CHAR_CAPSULES = {
    "Goku":        0x00495762,  # always unlocked
    "Kid Gohan":   0x00495764,
    "Teen Gohan":  0x00495765,
    "Adult Gohan": 0x00495766,
    "Vegeta":      0x00495769,
    "Krillin":     0x0049576C,
    "Piccolo":     0x0049576D,
    "Tien":        0x0049576E,
    "Yamcha":      0x0049576F,
    "Uub":         0x00495773,
    "Broly":       0x00495784,
}

SCREEN_DU_TITLE   = 0x0106
SCREEN_DU_CHARSEL = 0x0107

# ─── Character Lock Cave ──────────────────────────────────────────────────────
ADDR_CAVE2          = 0x005FED9C  # cave2 code; confirmed empty area before randomizer cave
ADDR_LOCK_TABLE     = 0x00607000  # 11 bytes: 0=locked, 1=unlocked per character
ADDR_LOCK_SCRATCH   = 0x00607080  # register save area for cave2
ADDR_INTERCEPT2     = 0x001F2B54  # original: lui at,0x0002
ADDR_RETURN2        = 0x001F2B5C  # jump back target (skip delay slot)
ORIG_INSTR2         = 0x3C010002  # lui at,0x0002
CAVE2_JUMP          = 0x0817FB67  # j 0x005FED9C

# Order matches ADDR_LOCK_TABLE indices
LOCK_TABLE_CHARS = [
    ("Goku",        0x00495762),
    ("Kid Gohan",   0x00495764),
    ("Teen Gohan",  0x00495765),
    ("Adult Gohan", 0x00495766),
    ("Vegeta",      0x00495769),
    ("Krillin",     0x0049576C),
    ("Piccolo",     0x0049576D),
    ("Tien",        0x0049576E),
    ("Yamcha",      0x0049576F),
    ("Uub",         0x00495773),
    ("Broly",       0x00495784),
]

CAVE2_CODE_FULL = bytes([
    0x02, 0x00, 0x01, 0x3C,  # lui at,0x0002       ; original instruction
    0x60, 0x00, 0x0A, 0x3C,  # lui t2,0x0060
    0x80, 0x70, 0x4A, 0x35,  # ori t2,t2,0x7080    ; t2 = 0x00607080 (scratch)
    0x00, 0x00, 0x08, 0xAD,  # sw t0,0(t2)          ; save t0
    0x04, 0x00, 0x09, 0xAD,  # sw t1,4(t2)          ; save t1
    0x60, 0x00, 0x08, 0x3C,  # lui t0,0x0060
    0x00, 0x70, 0x08, 0x35,  # ori t0,t0,0x7000    ; t0 = lock table
    0x00, 0x00, 0x09, 0x91,  # lbu t1,0(t0)         ; [0] Goku
    0x49, 0x00, 0x01, 0x3C,  # lui at,0x0049
    0x62, 0x57, 0x29, 0xA0,  # sb t1,0x5762(at)     ; write Goku
    0x01, 0x00, 0x09, 0x91,  # lbu t1,1(t0)         ; [1] Kid Gohan
    0x49, 0x00, 0x01, 0x3C,  # lui at,0x0049
    0x64, 0x57, 0x29, 0xA0,  # sb t1,0x5764(at)
    0x02, 0x00, 0x09, 0x91,  # lbu t1,2(t0)         ; [2] Teen Gohan
    0x49, 0x00, 0x01, 0x3C,
    0x65, 0x57, 0x29, 0xA0,
    0x03, 0x00, 0x09, 0x91,  # lbu t1,3(t0)         ; [3] Adult Gohan
    0x49, 0x00, 0x01, 0x3C,
    0x66, 0x57, 0x29, 0xA0,
    0x04, 0x00, 0x09, 0x91,  # lbu t1,4(t0)         ; [4] Vegeta
    0x49, 0x00, 0x01, 0x3C,
    0x69, 0x57, 0x29, 0xA0,
    0x05, 0x00, 0x09, 0x91,  # lbu t1,5(t0)         ; [5] Krillin
    0x49, 0x00, 0x01, 0x3C,
    0x6C, 0x57, 0x29, 0xA0,
    0x06, 0x00, 0x09, 0x91,  # lbu t1,6(t0)         ; [6] Piccolo
    0x49, 0x00, 0x01, 0x3C,
    0x6D, 0x57, 0x29, 0xA0,
    0x07, 0x00, 0x09, 0x91,  # lbu t1,7(t0)         ; [7] Tien
    0x49, 0x00, 0x01, 0x3C,
    0x6E, 0x57, 0x29, 0xA0,
    0x08, 0x00, 0x09, 0x91,  # lbu t1,8(t0)         ; [8] Yamcha
    0x49, 0x00, 0x01, 0x3C,
    0x6F, 0x57, 0x29, 0xA0,
    0x09, 0x00, 0x09, 0x91,  # lbu t1,9(t0)         ; [9] Uub
    0x49, 0x00, 0x01, 0x3C,
    0x73, 0x57, 0x29, 0xA0,
    0x0A, 0x00, 0x09, 0x91,  # lbu t1,10(t0)        ; [10] Broly
    0x49, 0x00, 0x01, 0x3C,
    0x84, 0x57, 0x29, 0xA0,
    0x00, 0x00, 0x08, 0x8D,  # lw t0,0(t2)          ; restore t0
    0x04, 0x00, 0x09, 0x8D,  # lw t1,4(t2)          ; restore t1
    0x02, 0x00, 0x01, 0x3C,  # lui at,0x0002       ; restore original at for 0x001F2B5C ori
    0xD7, 0xCA, 0x07, 0x08,  # j 0x001F2B5C         ; jump back (delay slot at 0x1F2B58 already ran)
    0x00, 0x00, 0x00, 0x00,  # nop
])

# Full cave2 code
CAVE2_CODE = bytes([
    0x02, 0x00, 0x01, 0x3C,  # lui at,0x0002       ; original instruction
    0x60, 0x00, 0x0A, 0x3C,  # lui t2,0x0060
    0x80, 0x70, 0x4A, 0x35,  # ori t2,t2,0x7080    ; t2 = scratch
    0x00, 0x00, 0x08, 0xAD,  # sw t0,0(t2)
    0x04, 0x00, 0x09, 0xAD,  # sw t1,4(t2)
    0x60, 0x00, 0x08, 0x3C,  # lui t0,0x0060
    0x00, 0x70, 0x08, 0x35,  # ori t0,t0,0x7000    ; lock table
    0x00, 0x00, 0x09, 0x91,  # lbu t1,0(t0)        ; Goku
    0x49, 0x00, 0x01, 0x3C,  # lui at,0x0049
    0x62, 0x57, 0x29, 0xA0,  # sb t1,0x5762(at)
    0x01, 0x00, 0x09, 0x91,  # lbu t1,1(t0)        ; Kid Gohan
    0x49, 0x00, 0x01, 0x3C,
    0x64, 0x57, 0x29, 0xA0,
    0x02, 0x00, 0x09, 0x91,  # lbu t1,2(t0)        ; Teen Gohan
    0x49, 0x00, 0x01, 0x3C,
    0x65, 0x57, 0x29, 0xA0,
    0x03, 0x00, 0x09, 0x91,  # lbu t1,3(t0)        ; Adult Gohan
    0x49, 0x00, 0x01, 0x3C,
    0x66, 0x57, 0x29, 0xA0,
    0x04, 0x00, 0x09, 0x91,  # lbu t1,4(t0)        ; Vegeta
    0x49, 0x00, 0x01, 0x3C,
    0x69, 0x57, 0x29, 0xA0,
    0x05, 0x00, 0x09, 0x91,  # lbu t1,5(t0)        ; Krillin
    0x49, 0x00, 0x01, 0x3C,
    0x6C, 0x57, 0x29, 0xA0,
    0x06, 0x00, 0x09, 0x91,  # lbu t1,6(t0)        ; Piccolo
    0x49, 0x00, 0x01, 0x3C,
    0x6D, 0x57, 0x29, 0xA0,
    0x07, 0x00, 0x09, 0x91,  # lbu t1,7(t0)        ; Tien
    0x49, 0x00, 0x01, 0x3C,
    0x6E, 0x57, 0x29, 0xA0,
    0x08, 0x00, 0x09, 0x91,  # lbu t1,8(t0)        ; Yamcha
    0x49, 0x00, 0x01, 0x3C,
    0x6F, 0x57, 0x29, 0xA0,
    0x09, 0x00, 0x09, 0x91,  # lbu t1,9(t0)        ; Uub
    0x49, 0x00, 0x01, 0x3C,
    0x73, 0x57, 0x29, 0xA0,
    0x0A, 0x00, 0x09, 0x91,  # lbu t1,10(t0)       ; Broly
    0x49, 0x00, 0x01, 0x3C,
    0x84, 0x57, 0x29, 0xA0,
    0x00, 0x00, 0x08, 0x8D,  # lw t0,0(t2)         ; restore t0
    0x04, 0x00, 0x09, 0x8D,  # lw t1,4(t2)         ; restore t1
    0x02, 0x00, 0x01, 0x3C,  # lui at,0x0002       ; restore original at for 0x001F2B5C ori
    0xD7, 0xCA, 0x07, 0x08,  # j 0x001F2B5C        ; jump back (delay slot at 0x1F2B58 already ran)
    0x00, 0x00, 0x00, 0x00,  # nop
])
