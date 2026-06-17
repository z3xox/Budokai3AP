# Dragon Ball Z Budokai 3 - Memory Address Constants
# NTSC-U, SLUS-20998, CRC C97EF0A4

GAME_ID  = "SLUS-20998"
GAME_CRC = "c97ef0a4"

# ─── Supported Versions ───────────────────────────────────────────────────────
# Version-specific addresses keyed by CRC (lowercase). The client loads the
# matching entry on connect and overrides the defaults below.
# Addresses not listed in a version entry fall back to the NTSC-U defaults.
VERSIONS = {
    "c97ef0a4": {  # NTSC-U, SLUS-20998
        "game_id":          "SLUS-20998",
        "addr_screen":      0x0046A5B0,
        # DeathLink (NTSC-U live-confirmed)
        "addr_p1_hp":       [0x0044CEC0, 0x0044CEC4, 0x0044CEC8,
                             0x0044CF00, 0x0044CF0C, 0x0044CF10],
        "addr_fight_end_hp": 0x0044CF00,
        "addr_mode":        0x00543C20,
        "addr_du_char":     0x00543C24,
        "addr_zenie_rt":    0x00543D28,
        "addr_zenie_du":    0x004C6F08,
        "addr_zenie_saved": 0x00495568,
        "addr_cave":        0x00600000,
        "addr_intercept":   0x001B32A8,
        "addr_return":      0x001B32AC,
        "cave_jump":        0x08180000,   # j 0x00600000
        "orig_instr":       0x864206B0,   # lh v0,0x6B0(s2)
        "du_char_capsules": {
            "Goku":        0x00495762,
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
        },
        "addr_p1_char":     0x0044B5C0,
        "addr_p1_char_t4":  0x0044B5C4,
        "addr_p1_caps":     0x0044B5E4,
        "addr_p2_char":     0x0044B610,
        "addr_p2_char_t4":  0x0044B614,
        "addr_p2_caps":     0x0044B634,
        "addr_stage_select":0x0044B6F4,
        "addr_music":       0x0044B6F6,   # stage_select + 0x02 (NTSC-U)
        "addr_battle_mod":  0x0044B708,
        "addr_intercept2":  0x001F2B54,
        "addr_return2":     0x001F2B5C,
        "orig_instr2":      0x3C010002,
        "addr_cave2":       0x00623000,
        "addr_lock_table":  0x00622000,
        "cave2_jump":       0x08188C00,   # j 0x00623000
        "shop_off_items":   0x98,
        "shop_off_count":   0x88,
        "shop_off_zenie":   None,   # NTSC-U: live shop Zenie display refresh not mapped
        "dragon_ball_addrs": {
            "Goku":       0x0049D284,
            "Kid Gohan":  0x0049F6A4,
            "Teen Gohan": 0x004A08B4,
            "Gohan":      0x004A1AC4,
            "Vegeta":     0x004A50F4,
            "Krillin":    0x004A8724,
            "Piccolo":    0x004A9934,
            "Tien":       0x004AAB44,
            "Yamcha":     0x004ABD54,
            "Uub":        0x004B0594,
            "Broly":      0x004C38A4,
        },
        "rt_caps_base":     0x005510EF,
        "du_rt_caps_base":  0x004C6F3B,
        "da_clear_base":    0x00495A16,
        "da_ticket_display":    0x0049579D,
        "da_ticket_ownership":  0x005512F1,
        "da_ticket_du_rt":      0x004C713D,
        "shop_ownership_base":  0x005510C7,
        "shop_purchase_base":   0x005510C7,   # NTSC-U: same as ownership, indexed by own_idx
        "shop_purchase_by_display": False,
        "addr_shop_count":  0x0088DCEC,
        "du_bases": {
            "Goku":       {"du_id": 0x00, "base": 0x0049D260},
            "Kid Gohan":  {"du_id": 0x02, "base": 0x0049F680},
            "Teen Gohan": {"du_id": 0x03, "base": 0x004A0890},
            "Adult Gohan":{"du_id": 0x04, "base": 0x004A1AA0},
            "Vegeta":     {"du_id": 0x07, "base": 0x004A50D0},
            "Krillin":    {"du_id": 0x0A, "base": 0x004A8700},
            "Piccolo":    {"du_id": 0x0B, "base": 0x004A9910},
            "Tien":       {"du_id": 0x0C, "base": 0x004AAB20},
            "Yamcha":     {"du_id": 0x0D, "base": 0x004ABD30},
            "Uub":        {"du_id": 0x11, "base": 0x004B0570},
            "Broly":      {"du_id": 0x22, "base": 0x004C3880},
        },
    },
    "2a4b60eb": {  # Black Label (PAL/other), CRC 2A4B60EB
        "game_id":          "SLES-XXXXX",  # update with real serial
        "addr_screen":      0x004B4B40,
        # DeathLink (BL): 0x00497B60 is the HP control — reads 0 on fight end
        # (win/loss) and re-initializes on restart, same role NTSC-U's 0x0044CF00
        # plays. Used as both the kill target and the fight-end marker. Win/loss
        # is discriminated via addr_screen (already mapped for BL).
        "addr_p1_hp":        [0x00497B60],
        "addr_fight_end_hp": 0x00497B60,
        "addr_mode":        0x0058F660,
        "addr_du_char":     0x0058F664,
        "addr_zenie_rt":    0x0058F718,    # confirmed: persistent RT Zenie
        "addr_zenie_du":    0x00511448,    # same address (DU_ZENIE was off-by-one)
        "addr_zenie_saved": 0x004DFAE8,    # saved/memory-card Zenie (updates on save)
        # Battle struct (confirmed via Goku vs Piccolo dump)
        "addr_p1_char":     0x00496220,
        "addr_p1_char_t4":  0x00496224,
        "addr_p1_caps":     0x00496244,
        "addr_p2_char":     0x00496270,
        "addr_p2_char_t4":  0x00496274,
        "addr_p2_caps":     0x00496294,
        "addr_stage_select":0x00496354,
        "addr_music":       0x00496356,   # stage_select + 0x02 (BL)
        "addr_battle_mod":  0x00496368,   # STAGE + 0x14 (same offset as NTSC-U)
        # Cave (confirmed: intercept at 0x001B119C, free mem at 0x00800000)
        "addr_cave":        0x00800000,
        "addr_debug":       0x00820000,
        "addr_scratch":     0x00821000,
        "addr_lock_table":  0x00822000,
        "addr_cave2":       0x00823000,
        "cave2_jump":       0x08208C00,   # j 0x00823000
        "shop_off_items":   0x90,
        "shop_off_count":   0x88,
        "shop_off_zenie":   0x28,   # live Zenie display field inside ess_shop.c struct
        "dragon_ball_addrs": {
            "Goku":       0x004E77C4,
            "Kid Gohan":  0x004E9BE4,
            "Teen Gohan": 0x004EADF4,
            "Gohan":      0x004EC004,
            "Vegeta":     0x004EF634,
            "Krillin":    0x004F2C64,
            "Piccolo":    0x004F3E74,
            "Tien":       0x004F5084,
            "Yamcha":     0x004F6294,
            "Uub":        0x004FAAD4,
            "Broly":      0x0050DDE4,
        },
        "addr_intercept":   0x001B119C,
        "addr_return":      0x001B11A0,
        "cave_jump":        0x08200000,    # j 0x00800000
        "orig_instr":       0x862307E2,    # lh v1,0x7E2(s0)
        "addr_intercept2":  0x001EFD70,   # lui at,0x0002 — before jal z_un_0026dc80 commits values
        "addr_return2":     0x001EFD74,   # daddu a0,s4,zero (let ori+jal run with our values)
        "orig_instr2":      0x3C010002,   # lui at,0x0002
        # Character lock display bytes (confirmed via manual testing)
        "du_char_capsules": {
            "Goku":        0x004DFCE2,
            "Kid Gohan":   0x004DFCE4,
            "Teen Gohan":  0x004DFCE5,
            "Adult Gohan": 0x004DFCE6,
            "Vegeta":      0x004DFCE9,
            "Krillin":     0x004DFCEC,
            "Piccolo":     0x004DFCED,
            "Tien":        0x004DFCEE,
            "Yamcha":      0x004DFCEF,
            "Uub":         0x004DFCF3,
            "Broly":       0x004DFD04,
        },
        "du_rt_caps_base":  0x0051147B,
        "rt_caps_base":     0x0051147B,
        "da_clear_base":    0x004DFF96,
        "da_ticket_display":    0x004DFD1D,   # GHE display table (main menu)
        "da_ticket_ownership":  0x0059CCA1,   # shop ownership table
        "da_ticket_du_rt":      0x0051167D,   # RT/DU-RT table (DU context)
        "shop_ownership_base":  0x00511453,   # RT_CAPS_BASE - 40 (same table, different offset)
        "shop_purchase_base":   0x0059CA9D,   # BL: quantity table, indexed by DISPLAY index
        "shop_purchase_by_display": True,
        "du_bases": {
            "Goku":       {"du_id": 0x00, "base": 0x004E77A0},
            "Kid Gohan":  {"du_id": 0x02, "base": 0x004E9BC0},
            "Teen Gohan": {"du_id": 0x03, "base": 0x004EADD0},
            "Adult Gohan":{"du_id": 0x04, "base": 0x004EBFE0},
            "Vegeta":     {"du_id": 0x07, "base": 0x004EF610},
            "Krillin":    {"du_id": 0x0A, "base": 0x004F2C40},
            "Piccolo":    {"du_id": 0x0B, "base": 0x004F3E50},
            "Tien":       {"du_id": 0x0C, "base": 0x004F5060},
            "Yamcha":     {"du_id": 0x0D, "base": 0x004F6270},
            "Uub":        {"du_id": 0x11, "base": 0x004FAAB0},
            "Broly":      {"du_id": 0x22, "base": 0x0050DDC0},
        },
    },
}

# ─── Cave ─────────────────────────────────────────────────────────────────────
ADDR_CAVE          = 0x00600000   # cave code start
ADDR_DEBUG         = 0x00620000   # debug area (hit counter, mode, char, battle)
ADDR_SCRATCH       = 0x00621000   # register save area (t0,t1,t2,t3)
ADDR_INTERCEPT     = 0x001B32A8   # patched instruction
ADDR_RETURN        = 0x001B32AC   # jump-back target
CAVE_JUMP          = 0x08180000   # j 0x00600000
ORIG_INSTR         = 0x864206B0   # lh v0,0x6B0(s2)

# ─── Game State ──────────────────────────────────────────────────────────────
ADDR_SCREEN        = 0x0046A5B0   # 16-bit screen ID
ADDR_MODE          = 0x00543C20   # DU mode byte (0x01 = DU)
# Skill capsule table bases (overridden per-version). SKILL_CAPSULES holds
# NTSC-U absolute addresses; apply_skill_locks translates them to the active
# version using these bases.
RT_CAPS_BASE       = 0x005510EF
DU_RT_CAPS_BASE    = 0x004C6F3B
NTSC_RT_CAPS_BASE    = 0x005510EF  # fixed reference for offset translation
NTSC_DU_RT_CAPS_BASE = 0x004C6F3B  # fixed reference for offset translation
ADDR_DU_CHAR       = 0x00543C24   # current DU character selector
ADDR_ZENIE_RT      = 0x00543D28   # real-time Zenie (32-bit)
ADDR_ZENIE_DU      = 0x004C6F08   # DU Zenie (32-bit)
ADDR_ZENIE_SAVED   = 0x00495568   # memory-card / saved total (updates on save)

SCREEN_SHOP        = 0x0016

# ─── Battle ──────────────────────────────────────────────────────────────────
ADDR_P1_CHAR       = 0x0044B5C0
ADDR_P1_CHAR_T4    = 0x0044B5C4   # template/form field - clear on swap
ADDR_P1_CAPS       = 0x0044B5E4   # capsule block (16 bytes)
ADDR_P2_CHAR       = 0x0044B610
ADDR_P2_CHAR_T4    = 0x0044B614   # template/form field - clear on swap
ADDR_P2_CAPS       = 0x0044B634   # capsule block (16 bytes)
ADDR_STAGE_SELECT  = 0x0044B6F4
ADDR_MUSIC         = 0x0044B6F6   # stage_select + 0x02; single byte, range 0-22
ADDR_BATTLE_MOD    = 0x0044B708   # 0x00020003 = HP drain

# ─── DeathLink (version-aware; NTSC-U live-confirmed) ────────────────────────
# Incoming kill: pin the live HP float copies to a TINY NONZERO float so the AI
# keeps attacking and lands the finishing blow (writing true 0 makes the AI
# passive). 0x3B9ACA00 == float ~0.0047. These ADDRESSES are region-specific and
# get patched per-version from VERSIONS (addr_p1_hp / addr_fight_end_hp). The
# values below are the NTSC-U defaults / fallback.
ADDR_P1_HP = [0x0044CEC0, 0x0044CEC4, 0x0044CEC8,
              0x0044CF00, 0x0044CF0C, 0x0044CF10]
HP_KILL_VALUE = 0x3B9ACA00        # float ~0.0047 — region-INDEPENDENT (float bits)
# Outgoing death: 0x0044CF00 (a HP copy) is CLEARED to 0 when the fight ENDS
# (both win and loss). Discriminate via screen: a WIN moves screen to
# SCREEN_RESULTS_WIN (0x010A); a LOSS stays in SCREEN_DU_BATTLE (0x0109).
ADDR_FIGHT_END_HP = 0x0044CF00     # nonzero -> 0 on fight end (NTSC-U default)



# Music randomization: valid in-battle track IDs (single byte at ADDR_MUSIC).
MUSIC_TRACKS = list(range(0, 23))   # 0..22 inclusive

# ─── Shop ────────────────────────────────────────────────────────────────────
ADDR_SHOP_COUNT    = 0x0088DCEC   # fallback (first-boot location); struct is dynamic
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
    # Vegeta DU
    ("Vegeta", 0x05, 0x01): "Vegeta DU - Goku",
    ("Vegeta", 0x05, 0x03): "Vegeta DU - Kid Gohan",
    ("Vegeta", 0x01, 0x01): "Vegeta DU - Recoome",
    ("Vegeta", 0x01, 0x03): "Vegeta DU - Frieza (1st Form)",
    ("Vegeta", 0x01, 0x05): "Vegeta DU - Frieza (Final Form)",
    ("Vegeta", 0x01, 0x07): "Vegeta DU - Cooler",
    ("Vegeta", 0x02, 0x01): "Vegeta DU - Android 17",
    ("Vegeta", 0x02, 0x03): "Vegeta DU - Android 18",
    ("Vegeta", 0x02, 0x05): "Vegeta DU - Cell (17 Absorbed)",
    ("Vegeta", 0x02, 0x07): "Vegeta DU - Cell (Perfect)",
    ("Vegeta", 0x03, 0x01): "Vegeta DU - Goku (SS2)",
    ("Vegeta", 0x03, 0x07): "Vegeta DU - Majin Buu",
    ("Vegeta", 0x03, 0x0A): "Vegeta DU - Super Buu (Gohan Absorbed)",
    ("Vegeta", 0x03, 0x0B): "Vegeta DU - Super Buu (Gohan Absorbed) [Supreme Kai]",
    ("Vegeta", 0x03, 0x0E): "Vegeta DU - Super Buu (Inside Buu)",
    ("Vegeta", 0x03, 0x0F): "Vegeta DU - Super Buu (Inside Buu) [Supreme Kai]",
    ("Vegeta", 0x03, 0x11): "Vegeta DU - Kid Buu",
    ("Vegeta", 0x03, 0x14): "Vegeta DU - Broly",
    ("Vegeta", 0x03, 0x15): "Vegeta DU - Broly [Goku Friendship]",
    ("Vegeta", 0x03, 0x17): "Vegeta DU - Gotenks (SS)",
    ("Vegeta", 0x03, 0x19): "Vegeta DU - Goku (SS4)",
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
ADDR_CAVE2          = 0x00623000  # cave2 code (safe, after lock table)
ADDR_LOCK_TABLE     = 0x00622000  # 11 bytes: 0=locked, 1=unlocked per character
ADDR_LOCK_SCRATCH   = 0x00622080  # register save area for cave2
ADDR_INTERCEPT2     = 0x001F2B54  # original: lui at,0x0002
ADDR_RETURN2        = 0x001F2B5C  # jump back target (skip delay slot)
ORIG_INSTR2         = 0x3C010002  # lui at,0x0002
CAVE2_JUMP          = 0x08188C00  # j 0x00623000

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
    0x02, 0x00, 0x01, 0x3C,
    0x62, 0x00, 0x0A, 0x3C,
    0x80, 0x20, 0x4A, 0x35,
    0x00, 0x00, 0x48, 0xAD,
    0x04, 0x00, 0x49, 0xAD,
    0x62, 0x00, 0x08, 0x3C,
    0x00, 0x20, 0x08, 0x35,
    0x00, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x62, 0x57, 0x29, 0xA0,
    0x01, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x64, 0x57, 0x29, 0xA0,
    0x02, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x65, 0x57, 0x29, 0xA0,
    0x03, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x66, 0x57, 0x29, 0xA0,
    0x04, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x69, 0x57, 0x29, 0xA0,
    0x05, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x6C, 0x57, 0x29, 0xA0,
    0x06, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x6D, 0x57, 0x29, 0xA0,
    0x07, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x6E, 0x57, 0x29, 0xA0,
    0x08, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x6F, 0x57, 0x29, 0xA0,
    0x09, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x73, 0x57, 0x29, 0xA0,
    0x0A, 0x00, 0x09, 0x91,
    0x49, 0x00, 0x01, 0x3C,
    0x84, 0x57, 0x29, 0xA0,
    0x00, 0x00, 0x48, 0x8D,
    0x04, 0x00, 0x49, 0x8D,
    0x02, 0x00, 0x01, 0x3C,
    0xD7, 0xCA, 0x07, 0x08,
    0x00, 0x00, 0x00, 0x00,
])

# ─── Shop System (confirmed) ─────────────────────────────────────────────────
ADDR_SHOP_STRUCT_BASE = 0x0088DCFC  # item structs, 20 bytes each
SHOP_STRUCT_SIZE      = 0x14         # 20 bytes per entry (confirmed: disp,recv,price,flags,extra)
SHOP_DISPLAY_BASE     = 0x495599     # display_index = def_addr - this
SHOP_OWNERSHIP_BASE   = 0x005510C7   # ownership: base + own_index
SHOP_PURCHASE_BASE        = 0x005510C7   # purchase-detection table (per version)
SHOP_PURCHASE_BY_DISPLAY  = False        # BL indexes by display, NTSC-U by own_idx
SHOP_PRICE            = 1500
SHOP_MAX_SLOTS        = 10

# Shop entry struct offsets
SHOP_OFF_DISPLAY  = 0x00   # display name index
SHOP_OFF_RECEIVED = 0x04   # capsule received index
SHOP_OFF_PRICE    = 0x08   # price (32-bit)
SHOP_OFF_FLAGS    = 0x0C   # flags (0x02)

# The shop struct is allocated dynamically and relocates after other menus
# load. It is anchored by the module string 'ess_shop.c'. Relative to the
# string address: count at +0x88, item list at +0x98 (stride 0x14).
SHOP_SIG0 = 0x5F737365   # 'ess_'
SHOP_SIG1 = 0x706F6873   # 'shop'
SHOP_OFF_COUNT_FROM_SIG = 0x88
SHOP_OFF_ITEMS_FROM_SIG = 0x98
SHOP_OFF_ZENIE_FROM_SIG = None   # live shop Zenie display (BL only)
# Scan window where the shop struct lives
SHOP_SCAN_START = 0x00880000
SHOP_SCAN_END   = 0x008E0000  # covers 0x00880000-0x008DFFFF including BL region

# Shop capsule pool: (display_index, ownership_index, name)
# Up to 50 capsules. Shop shows 10 at a time, restock items unlock more.
SHOP_CAPSULE_POOL = [
    (0x119, 0x13F, "Z-Sword"),
    (0x11A, 0x140, "Juice!"),
    (0x11B, 0x141, "Daimao's Power"),
    (0x11C, 0x142, "Fruits of Training"),
    (0x11D, 0x143, "Videl's Kiss"),
    (0x11E, 0x144, "Kibito's Backing"),
    (0x11F, 0x145, "Battle Testament"),
    (0x120, 0x146, "Power Amplification System"),
    (0x121, 0x147, "Warrior Genetics"),
    (0x126, 0x14C, "Power of Friends"),
    (0x128, 0x14E, "Strength Serum"),
    (0x129, 0x14F, "King's Lineage"),
    (0x12A, 0x150, "Cheering"),
    (0x16E, 0x194, "Potential"),
    (0x16F, 0x195, "Universal Power"),
    (0x170, 0x196, "Miracle Power"),
    (0x171, 0x197, "Ultimate Power"),
    (0x174, 0x19A, "Saiyans' Awakening"),
    (0x17A, 0x1A0, "Rage!"),
    (0x17D, 0x1A3, "Spirit!"),
    (0x180, 0x1A6, "Serious!"),
    (0x183, 0x1A9, "Power Near the Limit"),
    (0x186, 0x1AC, "Pride of the Strongest"),
    (0x18A, 0x1B0, "Piccolo's Regeneration"),
    (0x18C, 0x1B2, "Dende's Recovery"),
    (0x18E, 0x1B4, "Medical Machine"),
    (0x190, 0x1B6, "Saiyan Spirit"),
    (0x191, 0x1B7, "Going All-out!!"),
    (0x19E, 0x1C4, "Ki Control"),
    (0x19F, 0x1C5, "Warrior's Career"),
    (0x1A4, 0x1CA, "Meditation"),
    (0x1A6, 0x1CC, "Angel's Halo"),
    (0x1BA, 0x1E0, "Grandpa Gohan's Teachings"),
    (0x1BB, 0x1E1, "Goku's Teachings"),
    (0x1BC, 0x1E2, "Turtle Shell"),
    (0x1BD, 0x1E3, "Concentration"),
    (0x1BE, 0x1E4, "Sparking!"),
    (0x1BF, 0x1E5, "Sparking!!"),
    (0x1C0, 0x1E6, "Sparking!!!"),
    (0x1C5, 0x1EB, "WE GOTTA POWER!"),
    (0x14C, 0x172, "Special Coating"),
    (0x14E, 0x174, "Nanomachine"),
    (0x143, 0x169, "Champion's Belt"),
    (0x145, 0x16B, "Black Belt Vest"),
    (0x147, 0x16D, "Great Saiyaman's Wardrobe"),
    (0x16B, 0x191, "Mixed Blood Power"),
    (0x16C, 0x192, "Moon Light"),
    (0x172, 0x198, "King's Confidence"),
    (0x189, 0x1AF, "Dabura Cookie"),
    (0x197, 0x1BD, "Babidi's Mind Control"),
]

# ─── Skill Capsules (grantable AP rewards) ───────────────────────────────────
# Each skill: (DU_RT_address, RT_address). Writing 1 to both grants the skill
# in both Dragon Universe and regular battle. RT = DU_RT + 0x8A1B4.
SKILL_CAPSULES = {
    "Breakthrough (Goku)":            (0x4C7008, 0x5511BC),
    "Breakthrough (Kid Gohan)":       (0x4C700A, 0x5511BE),
    "Breakthrough (Teen Gohan)":      (0x4C700B, 0x5511BF),
    "Breakthrough (Gohan)":           (0x4C700C, 0x5511C0),
    "Breakthrough (Vegeta)":          (0x4C700F, 0x5511C3),
    "Breakthrough (Krillin)":         (0x4C7012, 0x5511C6),
    "Breakthrough (Piccolo)":         (0x4C7013, 0x5511C7),
    "Breakthrough (Tien)":            (0x4C7014, 0x5511C8),
    "Breakthrough (Yamcha)":          (0x4C7015, 0x5511C9),
    "Breakthrough (Uub)":             (0x4C7019, 0x5511CD),
    "Breakthrough (Broly)":           (0x4C702A, 0x5511DE),
    "Kaioken (Goku)":                 (0x4C6F3A, 0x5510EE),
    "Super Saiyan (Goku)":            (0x4C6F3B, 0x5510EF),
    "Super Saiyan 2 (Goku)":          (0x4C6F3C, 0x5510F0),
    "Super Saiyan 3 (Goku)":          (0x4C6F3D, 0x5510F1),
    "Super Saiyan 4 (Goku)":          (0x4C6F3E, 0x5510F2),
    "Super Saiyan (Teen Gohan)":      (0x4C6F4B, 0x5510FF),
    "Super Saiyan 2 (Teen Gohan)":    (0x4C6F4C, 0x551100),
    "Super Saiyan (Gohan)":           (0x4C6F50, 0x551104),
    "Super Saiyan 2 (Gohan)":         (0x4C6F51, 0x551105),
    "Super Saiyan (Vegeta)":          (0x4C6F5C, 0x551110),
    "Super Saiyan 2 (Vegeta)":        (0x4C6F5D, 0x551111),
    "Super Saiyan 4 (Vegeta)":        (0x4C6F5E, 0x551112),
    "Legendary Super Saiyan (Broly)": (0x4C6FC5, 0x551179),
    "Blaster Shell (Broly)":          (0x4C6FC6, 0x55117A),
    "Soaring Dragon Strike (Gohan)":  (0x4C6F54, 0x551108),
    "Elder Kai Unlock Ability (Gohan)": (0x4C6F52, 0x551106),
    "Fusion Gogeta (Goku)":           (0x4C6FE0, 0x551194),
    "Fusion Gogeta (Vegeta)":         (0x4C6FE4, 0x551198),
    "Fusion SSJ4 Gogeta (Goku)":      (0x4C6FE8, 0x55119C),
    "Fusion SSJ4 Gogeta (Vegeta)":    (0x4C6FEE, 0x5511A2),
    "Potara Vegito (Goku)":           (0x4C6FF4, 0x5511A8),
    "Potara Vegito (Vegeta)":         (0x4C6FF9, 0x5511AD),
    "Kamehameha (Goku)":              (0x4C6F3F, 0x5510F3),
    "Kamehameha (Teen Gohan)":        (0x4C6F4D, 0x551101),
    "Kamehameha (Gohan)":             (0x4C6F53, 0x551107),
    "Kamehameha (Krillin)":           (0x4C6F6F, 0x551123),
    "Kamehameha (Yamcha)":            (0x4C6F7B, 0x55112F),
    "Spirit Bomb (Goku)":             (0x4C6F43, 0x5510F7),
    "Final Flash (Vegeta)":           (0x4C6F63, 0x551117),
    "Destructive Wave (Piccolo)":     (0x4C6F74, 0x551128),
    "Wolf Fang Fist (Yamcha)":        (0x4C6F7C, 0x551130),
    "Ki Blast Cannon (Tien)":         (0x4C6F79, 0x55112D),
    "Final Impact (Vegeta)":          (0x4C6F61, 0x551115),
    "Masenko (Kid Gohan)":            (0x4C6F4A, 0x5510FE),
    "Gigantic Meteor (Broly)":        (0x4C6FC8, 0x55117C),
    "Ki Cannon (Uub)":                (0x4C6F88, 0x55113C),
    "Unlock Potential (Kid Gohan)":   (0x4C6F49, 0x5510FD),
    "Unlock Potential (Krillin)":     (0x4C6F6E, 0x551122),
    "Spirit Ball Attack (Yamcha)":    (0x4C6F7D, 0x551131),
    "Special Beam Cannon (Piccolo)":  (0x4C6F76, 0x55112A),
    "Hellzone Grenade (Piccolo)":     (0x4C6F77, 0x55112B),
    "Sync With Nail (Piccolo)":       (0x4C6F72, 0x551126),
    "Fuse With Kami (Piccolo)":       (0x4C6F73, 0x551127),
    "Super Kamehameha (Gohan)":       (0x4C6F55, 0x551109),
    "Big Bang Attack (Vegeta)":       (0x4C6F64, 0x551118),
    "Galick Gun (Vegeta)":            (0x4C6F5F, 0x551113),
}

# ─── Dragon Arena ────────────────────────────────────────────────────────────
SCREEN_DA_ENTRANCE = 0x0617
SCREEN_DA_CHARSEL  = 0x0618  # fight/opponent select list
SCREEN_DA_BATTLE   = 0x0619
SCREEN_DA_RESULTS  = 0x061A
SCREEN_DA_SAVE     = 0x061B

# Dragon Arena Ticket (3 tables, like character/skill unlocks)
DA_TICKET_DISPLAY   = 0x0049579D  # GHE display
DA_TICKET_OWNERSHIP = 0x005512F1  # Real-Time ownership
DA_TICKET_DU_RT     = 0x004C713D  # DU Real-Time

# Opponent list count — clamp to gate how many arena fights are visible
ADDR_DA_OPP_COUNT = 0x0089080C   # 32-bit; = 0x84 (132) at Lv.1-30 default

# Arena clear flags: 1 byte per fight, 0x01 when cleared. Win detection.
ADDR_DA_CLEAR_BASE = 0x00495A16  # Goku Lv.1
DA_FIGHT_COUNT     = 380          # total arena fights (0x495A16 .. 0x495B91)

# ─── Dragon Balls & Wishes ───────────────────────────────────────────────────
# One byte per character; bits 0-6 = the 7 Dragon Balls (bit0 = One-Star).
DRAGON_BALL_ADDRS = {
    "Goku":       0x0049D284,
    "Kid Gohan":  0x0049F6A4,
    "Teen Gohan": 0x004A08B4,
    "Gohan":      0x004A1AC4,
    "Vegeta":     0x004A50F4,
    "Krillin":    0x004A8724,
    "Piccolo":    0x004A9934,
    "Tien":       0x004AAB44,
    "Yamcha":     0x004ABD54,
    "Uub":        0x004B0594,
    "Broly":      0x004C38A4,
}

SCREEN_SHENRON = 0x010B  # Summoning Shenron screen (wish made)

# ─── Starting Transformations & Fusions ──────────────────────────────────────
# Spawn state = char ID (P1 0x0044B5C0 / P2 0x0044B610) + form field
# (P1 0x0044B5C4 / P2 0x0044B614), BOTH written at battle setup (cave timing).
# Form 0 = base. Indices are per-character. Mapped via DU scripted fights.
TRANSFORMATIONS = {
    # name: (char_id, {form_index: "form name"})
    "Goku":       (0x00, {1: "Kaioken", 2: "SSJ1", 3: "SSJ2", 4: "SSJ3", 5: "SSJ4"}),
    "Kid Gohan":  (0x02, {1: "Unlock Potential"}),
    "Teen Gohan": (0x03, {1: "SSJ1", 2: "SSJ2"}),
    "Gohan":      (0x04, {1: "SSJ1", 2: "SSJ2", 3: "Elder Kai Potential"}),
    "Goten":      (0x06, {1: "SSJ1"}),
    "Vegeta":     (0x07, {1: "SSJ1", 2: "SSJ2", 3: "SSJ4", 4: "Majin Vegeta"}),
    "Trunks":     (0x08, {1: "SSJ1", 2: "SSJ2"}),
    "Kid Trunks": (0x09, {1: "SSJ1"}),
    "Krillin":    (0x0A, {1: "Unlock Potential"}),
    "Piccolo":    (0x0B, {1: "Fused"}),
    "Hercule":    (0x0E, {1: "High Tension"}),
    "Frieza":     (0x1B, {1: "2nd Form", 2: "3rd Form", 3: "Final Form", 4: "100% Full Power", 5: "Mecha Frieza"}),
    "Cell":       (0x21, {1: "Semi-Perfect", 2: "Perfect", 3: "Super Perfect"}),
    "Dabura":     (0x25, {1: "Demonic Will"}),
    "Cooler":     (0x26, {1: "Final Form", 2: "Metal Cooler"}),
    "Broly":      (0x28, {1: "Legendary Super Saiyan"}),
    # Saibaman removed: its only "transformation" was a self-destruct
    # (1: "Self-Destructing"), which would make a randomized fighter blow itself
    # up. Excluded so the transformation randomizer never applies it.
}

# Fusion / special fighters (char ID + form field). These are distinct fighters.
FUSIONS = {
    "Gotenks":      (0x40, {3: "Gotenks", 4: "SSJ Gotenks", 5: "SSJ3 Gotenks"}),
    "Gogeta":       (0x44, {3: "SSJ Gogeta"}),
    "SSJ4 Gogeta":  (0x46, {4: "SSJ4 Gogeta"}),
    "Vegito":       (0x48, {2: "Vegito", 3: "Super Vegito"}),
    "Kibito Kai":   (0x4C, {2: "Kibito Kai"}),
}

# ── Item capsules (equipment/consumables) for filler variety ──────────────────
# (du_rt, rt) NTSC-U addresses; granted exactly like skills (write 1 to both).
# Used to replace Zenie filler with flavorful capsule unlocks.
ITEM_CAPSULES = {
    "Tempura Bowl": (0x4C702F, 0x5511E3),
    "Tonkatsu (Fried Pork) Bowl": (0x4C7030, 0x5511E4),
    "Chicken & Egg Bowl": (0x4C7031, 0x5511E5),
    "Grilled Juice": (0x4C7032, 0x5511E6),
    "Well Chilled Juice": (0x4C7033, 0x5511E7),
    "Extremely Chilled Juice": (0x4C7034, 0x5511E8),
    "1/3 Senzu Bean": (0x4C7035, 0x5511E9),
    "1/2 Senzu Bean": (0x4C7036, 0x5511EA),
    "Senzu Bean": (0x4C7037, 0x5511EB),
    "King-Kai's Water": (0x4C7038, 0x5511EC),
    "Supreme Kai's Water": (0x4C7039, 0x5511ED),
    "Grand Supreme Kai's Water": (0x4C703A, 0x5511EE),
    "Super Holy Water Drop": (0x4C703B, 0x5511EF),
    "Super Holy Water Bottle": (0x4C703C, 0x5511F0),
    "Super Holy Water": (0x4C703D, 0x5511F1),
    "Hercule Drink": (0x4C703E, 0x5511F2),
    "Hercule Drink DX": (0x4C703F, 0x5511F3),
    "Hercule Drink SP": (0x4C7040, 0x5511F4),
    "Super Kami Water Drop": (0x4C7041, 0x5511F5),
    "Super Kami Water Bottle": (0x4C7042, 0x5511F6),
    "Super Kami Water": (0x4C7043, 0x5511F7),
    "Portable Shield (Prototype)": (0x4C7044, 0x5511F8),
    "Portable Shield (Improved)": (0x4C7045, 0x5511F9),
    "Portable Shield (Production)": (0x4C7046, 0x5511FA),
    "Portable Barrier System": (0x4C7047, 0x5511FB),
    "Gero Style Defense System": (0x4C7048, 0x5511FC),
    "Gero Style Barrier System": (0x4C7049, 0x5511FD),
    "Bibidi's Pot": (0x4C704A, 0x5511FE),
    "Vaccine": (0x4C704B, 0x5511FF),
    "Senzu Root": (0x4C704C, 0x551200),
    "Senzu Leaf": (0x4C704D, 0x551201),
    "Senzu Seedling": (0x4C704E, 0x551202),
    "Centipede Eel Soup": (0x4C704F, 0x551203),
    "Chicken-fried 7-Seasoned Toad": (0x4C7050, 0x551204),
    "Paozusaurus Tail": (0x4C7051, 0x551205),
    "Z-Sword": (0x4C7052, 0x551206),
    "Juice!": (0x4C7053, 0x551207),
    "Daimao's Power": (0x4C7054, 0x551208),
    "Fruits of Training": (0x4C7055, 0x551209),
    "Videl's Kiss": (0x4C7056, 0x55120A),
    "Kibito's Backing": (0x4C7057, 0x55120B),
    "Battle Testament": (0x4C7058, 0x55120C),
    "Power Amplification System": (0x4C7059, 0x55120D),
    "Warrior Genetics": (0x4C705A, 0x55120E),
    "Demon Realm Flames": (0x4C705B, 0x55120F),
    "Kakarot's Crying": (0x4C705C, 0x551210),
    "Ginyu Special Forces": (0x4C705D, 0x551211),
    "Cooler's Armored Squad": (0x4C705E, 0x551212),
    "Power of Friends": (0x4C705F, 0x551213),
    "Appetites of Man": (0x4C7060, 0x551214),
    "Strength Serum": (0x4C7061, 0x551215),
    "King's Lineage": (0x4C7062, 0x551216),
    "Cheering": (0x4C7063, 0x551217),
    "General Vest": (0x4C7064, 0x551218),
    "Training Vest": (0x4C7065, 0x551219),
    "Sturdy Vest": (0x4C7066, 0x55121A),
    "Mysterious Vest": (0x4C7067, 0x55121B),
    "Vest from Grandpa Gohan": (0x4C7068, 0x55121C),
    "Vest with hole for tail": (0x4C7069, 0x55121D),
    "Turtle School Vest": (0x4C706A, 0x55121E),
    "Kami's Vest": (0x4C706B, 0x55121F),
    "Normal Tribe Uniform": (0x4C706C, 0x551220),
    "Evil Training Uniform": (0x4C706D, 0x551221),
    "Evil Sturdy Uniform": (0x4C706E, 0x551222),
    "Evil Mystery Uniform": (0x4C706F, 0x551223),
    "Normal Fiber Jacket": (0x4C7070, 0x551224),
    "Quality Fiber Jacket": (0x4C7071, 0x551225),
    "Sturdy Fiber Jacket": (0x4C7072, 0x551226),
    "Mystery Fiber Jacket": (0x4C7073, 0x551227),
    "Kami's Outfit": (0x4C7074, 0x551228),
    "King-Kai's Outfit": (0x4C7075, 0x551229),
    "Grand Kai's Outfit": (0x4C7076, 0x55122A),
    "Supreme Kai's Outfit": (0x4C7077, 0x55122B),
    "Old Training Vest": (0x4C7078, 0x55122C),
    "Wedding Vest": (0x4C7079, 0x55122D),
    "World Champion Vest": (0x4C707A, 0x55122E),
    "High-tech Vest": (0x4C707B, 0x55122F),
    "Champion Belt": (0x4C707C, 0x551230),
    "T-shirt": (0x4C707D, 0x551231),
    "Black Belt Vest": (0x4C707E, 0x551232),
    "Sparring Outfit": (0x4C707F, 0x551233),
    "Great Saiyaman's Wardrobe": (0x4C7080, 0x551234),
    "Old Style Armor": (0x4C7081, 0x551235),
    "Rit Armor": (0x4C7082, 0x551236),
    "New Style Armor": (0x4C7083, 0x551237),
    "Bulma's Armor": (0x4C7084, 0x551238),
    "Special Coating": (0x4C7085, 0x551239),
    "Improved Special Coating": (0x4C7086, 0x55123A),
    "Nanomachine": (0x4C7087, 0x55123B),
    "Improved Nanomachine": (0x4C7088, 0x55123C),
    "Life Extract for 10": (0x4C7089, 0x55123D),
    "Life Extract for 100": (0x4C708A, 0x55123E),
    "Life Extract for 1000": (0x4C708B, 0x55123F),
    "Life Extract for 10000": (0x4C708C, 0x551240),
    "Demon Realm Guard": (0x4C708D, 0x551241),
    "Mage Guard": (0x4C708E, 0x551242),
    "Babidi's Guard": (0x4C708F, 0x551243),
    "Bibidi's Guard": (0x4C7090, 0x551244),
    "Normal Belt": (0x4C7091, 0x551245),
    "Training Belt": (0x4C7092, 0x551246),
    "Warrior Belt": (0x4C7093, 0x551247),
    "Majin Belt": (0x4C7094, 0x551248),
    "Lower-class Saiyan Guard": (0x4C7095, 0x551249),
    "Kanassan-made Guard": (0x4C7096, 0x55124A),
    "Battle Jacket (Prototype)": (0x4C7097, 0x55124B),
    "Patched-up Battle Jacket": (0x4C7098, 0x55124C),
    "Strongman's Body Wrap": (0x4C7099, 0x55124D),
    "King's Body Wrap": (0x4C709A, 0x55124E),
    "God of Destruction Body Wrap": (0x4C709B, 0x55124F),
    "Legendary Body Wrap": (0x4C709C, 0x551250),
    "Shenron's Hide": (0x4C709D, 0x551251),
    "Porunga's Hide": (0x4C709E, 0x551252),
    "Shadow Dragons' Hide": (0x4C709F, 0x551253),
    "2X Enriched Serum": (0x4C70A0, 0x551254),
    "16X Enriched Serum": (0x4C70A1, 0x551255),
    "64X Enriched Serum": (0x4C70A2, 0x551256),
    "128X Enriched Serum": (0x4C70A3, 0x551257),
    "Mixed Blood Power": (0x4C70A4, 0x551258),
    "Moon Light": (0x4C70A5, 0x551259),
    "Full Moon's Glow": (0x4C70A6, 0x55125A),
    "Potential": (0x4C70A7, 0x55125B),
    "Universal Power": (0x4C70A8, 0x55125C),
    "Miracle Power": (0x4C70A9, 0x55125D),
    "Ultimate Power": (0x4C70AA, 0x55125E),
    "King's Confidence": (0x4C70AB, 0x55125F),
    "Mode-switching Systems": (0x4C70AC, 0x551260),
    "Saiyans' Awakening": (0x4C70AD, 0x551261),
    "Warrior Race's Awakening": (0x4C70AE, 0x551262),
    "Nature of Evil": (0x4C70AF, 0x551263),
    "Hatred of Kakarot": (0x4C70B0, 0x551264),
    "Black Dragonball": (0x4C70B1, 0x551265),
    "Toxic Chocolate": (0x4C70B2, 0x551266),
    "Rage!": (0x4C70B3, 0x551267),
    "Rage!!": (0x4C70B4, 0x551268),
    "Rage!!!": (0x4C70B5, 0x551269),
    "Spirit!": (0x4C70B6, 0x55126A),
    "Spirit!!": (0x4C70B7, 0x55126B),
    "Spirit!!!": (0x4C70B8, 0x55126C),
    "Serious!": (0x4C70B9, 0x55126D),
    "Serious!!": (0x4C70BA, 0x55126E),
    "Serious!!!": (0x4C70BB, 0x55126F),
    "Power Near the Limit": (0x4C70BC, 0x551270),
    "Desperate Resolution": (0x4C70BD, 0x551271),
    "Desperate Power": (0x4C70BE, 0x551272),
    "Pride of the Strongest": (0x4C70BF, 0x551273),
    "Last Ounce of Strength": (0x4C70C0, 0x551274),
    "Pressure on the Champ": (0x4C70C1, 0x551275),
    "Dabura Cookie": (0x4C70C2, 0x551276),
    "Piccolo's Regeneration": (0x4C70C3, 0x551277),
    "Majin Buu's Regeneration": (0x4C70C4, 0x551278),
    "Dende's Recovery": (0x4C70C5, 0x551279),
    "Kibito's Revival Power": (0x4C70C6, 0x55127A),
    "Medical Machine": (0x4C70C7, 0x55127B),
    "Automatic Restoration": (0x4C70C8, 0x55127C),
    "Saiyan Spirit": (0x4C70C9, 0x55127D),
    "Going All-out!": (0x4C70CA, 0x55127E),
    "Ginyu Force Badge": (0x4C70CB, 0x55127F),
    "Hercule's False Courage": (0x4C70CC, 0x551280),
    "Rush!!!": (0x4C70CD, 0x551281),
    "Frieza's Space Ship": (0x4C70CE, 0x551282),
    "Cooler's Space Ship": (0x4C70CF, 0x551283),
    "Babidi's Mind Control": (0x4C70D0, 0x551284),
    "Overtension": (0x4C70D1, 0x551285),
    "Gero's Deflection R&D": (0x4C70D2, 0x551286),
    "Gero's Deflect-Back R&D": (0x4C70D3, 0x551287),
    "Gero's Energy R&D": (0x4C70D4, 0x551288),
    "Viral Heart Disease": (0x4C70D5, 0x551289),
    "Babidi's Scope": (0x4C70D6, 0x55128A),
    "Ki Control": (0x4C70D7, 0x55128B),
    "Warrior's Career": (0x4C70D8, 0x55128C),
    "Power Save System": (0x4C70D9, 0x55128D),
    "Breathing Room of the Strongest": (0x4C70DA, 0x55128E),
    "Paragus' Admonishment": (0x4C70DB, 0x55128F),
    "Evil Grin": (0x4C70DC, 0x551290),
    "Meditation": (0x4C70DD, 0x551291),
    "Yakon": (0x4C70DE, 0x551292),
    "Angel's Halo": (0x4C70DF, 0x551293),
    "Human Candy": (0x4C70E0, 0x551294),
    "Marron's Wish": (0x4C70E1, 0x551295),
    "Chiaotzu's Wish": (0x4C70E2, 0x551296),
    "Puar's Wish": (0x4C70E3, 0x551297),
    "Chi-Chi's Wish": (0x4C70E4, 0x551298),
    "Dende's Wish": (0x4C70E5, 0x551299),
    "Bulma's Wish": (0x4C70E6, 0x55129A),
    "World's Expectations": (0x4C70E7, 0x55129B),
    "Loyalty to Frieza": (0x4C70E8, 0x55129C),
    "Universal Ambition": (0x4C70E9, 0x55129D),
    "Pride of the Clan": (0x4C70EA, 0x55129E),
    "Androids' Goals": (0x4C70EB, 0x55129F),
    "Essence of the Mighty": (0x4C70EC, 0x5512A0),
    "Loyalty to Babidi": (0x4C70ED, 0x5512A1),
    "Kibito's Wish": (0x4C70EE, 0x5512A2),
    "King-Kai's Wish": (0x4C70EF, 0x5512A3),
    "Thirst for Earth's Destruction": (0x4C70F0, 0x5512A4),
    "Thoughts of Friends": (0x4C70F1, 0x5512A5),
    "God of Destruction's Arrogance": (0x4C70F2, 0x5512A6),
    "Grandpa Gohan's Teachings": (0x4C70F3, 0x5512A7),
    "Goku's Teachings": (0x4C70F4, 0x5512A8),
    "Turtle Shell": (0x4C70F5, 0x5512A9),
    "Concentration": (0x4C70F6, 0x5512AA),
    "Sparking!": (0x4C70F7, 0x5512AB),
    "Sparking!!": (0x4C70F8, 0x5512AC),
    "Sparking!!!": (0x4C70F9, 0x5512AD),
    "Sparking!!!!": (0x4C70FA, 0x5512AE),
    "Sparking!!!!!": (0x4C70FB, 0x5512AF),
    "Sparking!!!!!!": (0x4C70FC, 0x5512B0),
    "Sparking!!!!!!!": (0x4C70FD, 0x5512B1),
    "WE GOTTA POWER!": (0x4C70FE, 0x5512B2),
    "WE GOTTA POWER!!": (0x4C70FF, 0x5512B3),
    "WE GOTTA POWER!!!": (0x4C7100, 0x5512B4),
    "WE GOTTA POWER!!!!": (0x4C7101, 0x5512B5),
}
