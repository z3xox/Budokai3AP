"""
B3Interface — PCSX2/PINE memory interface for Budokai 3.
Handles all game memory reads/writes and cave management.
"""
import os
import socket
import struct
import random
from platform import system
from typing import Optional
from logging import Logger

from .data.Constants import (
    GAME_ID, GAME_CRC, VERSIONS, DU_BASES, FIGHT_LOCATIONS, ROSTER, STAGES, CAPSULE_SHOP_IDS,
    ADDR_CAVE, ADDR_DEBUG, ADDR_SCRATCH, ADDR_INTERCEPT, ADDR_RETURN,
    CAVE_JUMP, ORIG_INSTR,
    ADDR_SCREEN, ADDR_MODE, ADDR_DU_CHAR, ADDR_ZENIE_RT,
    ADDR_ZENIE_DU, ADDR_ZENIE_SAVED,
    ADDR_P1_CHAR, ADDR_P1_CHAR_T4, ADDR_P1_CAPS,
    ADDR_P2_CHAR, ADDR_P2_CHAR_T4, ADDR_P2_CAPS,
    ADDR_STAGE_SELECT, ADDR_BATTLE_MOD, ADDR_MUSIC,
    ADDR_P1_HP, HP_KILL_VALUE, ADDR_FIGHT_END_HP,
    ADDR_SHOP_STRUCT_BASE, SHOP_STRUCT_SIZE, SHOP_DISPLAY_BASE,
    SHOP_OWNERSHIP_BASE, SHOP_PRICE, SHOP_MAX_SLOTS, ADDR_SHOP_COUNT,
    SHOP_SIG0, SHOP_SIG1, SHOP_OFF_COUNT_FROM_SIG, SHOP_OFF_ITEMS_FROM_SIG,
    SHOP_OFF_ZENIE_FROM_SIG,
    SHOP_SCAN_START, SHOP_SCAN_END,
    SHOP_OFF_DISPLAY, SHOP_OFF_RECEIVED, SHOP_OFF_PRICE, SHOP_OFF_FLAGS,
    SHOP_CAPSULE_POOL,
    SKILL_CAPSULES, ITEM_CAPSULES,
    RT_CAPS_BASE, DU_RT_CAPS_BASE,
    NTSC_RT_CAPS_BASE, NTSC_DU_RT_CAPS_BASE,
    SHOP_PURCHASE_BASE, SHOP_PURCHASE_BY_DISPLAY,
    SCREEN_DA_CHARSEL, SCREEN_DA_BATTLE, SCREEN_DA_RESULTS,
    DA_TICKET_DISPLAY, DA_TICKET_OWNERSHIP, DA_TICKET_DU_RT,
    ADDR_DA_OPP_COUNT, ADDR_DA_CLEAR_BASE, DA_FIGHT_COUNT,
    DRAGON_BALL_ADDRS, SCREEN_SHENRON,
    OFFSET_BATTLE, OFFSET_SAGA, OFFSET_BATTLE_COMP,
    SCREEN_SHOP, SCREEN_WORLD_MAP, SCREEN_DU_BATTLE,
    SCREEN_RESULTS_WIN, SCREEN_SHENRON,
    SCREEN_DU_TITLE, SCREEN_DU_CHARSEL,
    DU_CHAR_CAPSULES, LOCK_TABLE_CHARS,
    ADDR_CAVE2, ADDR_LOCK_TABLE, ADDR_INTERCEPT2, ADDR_RETURN2,
    ORIG_INSTR2, CAVE2_JUMP, CAVE2_CODE,
)


# ─── PINE CLIENT ─────────────────────────────────────────────────────────────

class Pine:
    def __init__(self, slot=28011):
        self._slot = slot
        self._sock: Optional[socket.socket] = None

    def connect(self) -> bool:
        try:
            if system() == "Windows":
                self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._sock.settimeout(5.0)
                self._sock.connect(("127.0.0.1", self._slot))
            elif system() == "Darwin":
                self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._sock.settimeout(5.0)
                self._sock.connect(os.environ.get("TMPDIR", "/tmp") + "/pcsx2.sock")
            else:
                self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._sock.settimeout(5.0)
                self._sock.connect(os.environ.get("XDG_RUNTIME_DIR", "/tmp") + "/pcsx2.sock")
            return True
        except Exception:
            self._sock = None
            return False

    def disconnect(self):
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None

    def is_connected(self) -> bool:
        return self._sock is not None

    def _send(self, req: bytes) -> bytes:
        self._sock.sendall(req)
        result = b""
        end = 4
        while len(result) < end:
            try:
                chunk = self._sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            result += chunk
            if end == 4 and len(result) >= 4:
                end = int.from_bytes(result[:4], "little")
                if end < 5 or end > 65536:
                    break  # sanity check
        return result

    def _req(self, cmd: int, addr: int, extra: bytes = b"") -> bytes:
        size = 9 + len(extra)
        return (size.to_bytes(4, "little") +
                cmd.to_bytes(1, "little") +
                addr.to_bytes(4, "little") +
                extra)

    def read8(self, addr: int) -> int:
        return int.from_bytes(self._send(self._req(0, addr))[-1:], "little")

    def read16(self, addr: int) -> int:
        return int.from_bytes(self._send(self._req(1, addr))[-2:], "little")

    def read32(self, addr: int) -> int:
        return int.from_bytes(self._send(self._req(2, addr))[-4:], "little")

    def write8(self, addr: int, val: int):
        self._send(self._req(4, addr, (val & 0xFF).to_bytes(1, "little")))

    def write16(self, addr: int, val: int):
        self._send(self._req(5, addr, (val & 0xFFFF).to_bytes(2, "little")))

    def write32(self, addr: int, val: int):
        self._send(self._req(6, addr, (val & 0xFFFFFFFF).to_bytes(4, "little")))

    def write_bytes(self, addr: int, data: bytes):
        for i in range(0, len(data), 4):
            chunk = data[i:i+4]
            if len(chunk) < 4:
                chunk += b"\x00" * (4 - len(chunk))
            self.write32(addr + i, int.from_bytes(chunk, "little"))

    def get_game_id(self) -> str:
        msg = (5).to_bytes(4, "little") + (0x0C).to_bytes(1, "little")
        resp = self._send(msg)
        return resp[9:-1].decode("ascii", errors="ignore").strip()

    def get_game_crc(self) -> str:
        msg = (5).to_bytes(4, "little") + (0x0D).to_bytes(1, "little")
        resp = self._send(msg)
        return resp[9:-1].decode("ascii", errors="ignore").strip()


# ─── MIPS ASSEMBLER ──────────────────────────────────────────────────────────

R = {
    "zero":0,"at":1,"v0":2,"v1":3,"a0":4,"a1":5,"a2":6,"a3":7,
    "t0":8,"t1":9,"t2":10,"t3":11,"t4":12,"t5":13,"t6":14,"t7":15,
    "s0":16,"s1":17,"s2":18,"s3":19,"s4":20,"s5":21,"s6":22,"s7":23,
    "t8":24,"t9":25,"k0":26,"k1":27,"gp":28,"sp":29,"fp":30,"ra":31,
}

def u16(x): return x & 0xFFFF

def _lui(rt, imm):     return 0x3C000000|(R[rt]<<16)|u16(imm)
def _ori(rt,rs,imm):   return 0x34000000|(R[rs]<<21)|(R[rt]<<16)|u16(imm)
def _lbu(rt,off,base): return 0x90000000|(R[base]<<21)|(R[rt]<<16)|u16(off)
def _lw(rt,off,base):  return 0x8C000000|(R[base]<<21)|(R[rt]<<16)|u16(off)
def _sw(rt,off,base):  return 0xAC000000|(R[base]<<21)|(R[rt]<<16)|u16(off)
def _sb(rt,off,base):  return 0xA0000000|(R[base]<<21)|(R[rt]<<16)|u16(off)
def _lh(rt,off,base):  return 0x84000000|(R[base]<<21)|(R[rt]<<16)|u16(off)
def _bne(rs,rt,off):   return 0x14000000|(R[rs]<<21)|(R[rt]<<16)|u16(off)
def _beq(rs,rt,off):   return 0x10000000|(R[rs]<<21)|(R[rt]<<16)|u16(off)
def _j(addr):          return 0x08000000|((addr>>2)&0x03FFFFFF)
def _nop():            return 0

class Asm:
    def __init__(self):
        self.items = []
        self.labels = {}
        self.branches = []

    def pc(self): return len(self.items)

    def label(self, name): self.labels[name] = self.pc()

    def emit(self, word): self.items.append(word & 0xFFFFFFFF)

    def bne(self, rs, rt, label):
        idx = self.pc(); self.emit(0)
        self.branches.append((idx, "bne", rs, rt, label))

    def beq(self, rs, rt, label):
        idx = self.pc(); self.emit(0)
        self.branches.append((idx, "beq", rs, rt, label))

    def load_imm(self, rt, value):
        value &= 0xFFFFFFFF
        hi = (value >> 16) & 0xFFFF
        lo = value & 0xFFFF
        if hi:
            self.emit(_lui(rt, hi))
            if lo:
                self.emit(_ori(rt, rt, lo))
        else:
            self.emit(_ori(rt, "zero", lo))

    def load_addr(self, rt, addr): self.load_imm(rt, addr)

    def write_word(self, addr, value):
        self.load_addr("t0", addr)
        self.load_imm("t1", value)
        self.emit(_sw("t1", 0, "t0"))

    def write_byte(self, addr, value):
        """Write a single byte (e.g. music track) to an absolute address."""
        self.load_addr("t0", addr)
        self.load_imm("t1", value & 0xFF)
        self.emit(_sb("t1", 0, "t0"))

    def finalize(self) -> bytes:
        for idx, op, rs, rt, label in self.branches:
            if label not in self.labels:
                raise ValueError(f"Unknown label: {label}")
            off = self.labels[label] - (idx + 1)
            if not -32768 <= off <= 32767:
                raise ValueError(f"Branch out of range to {label} (off={off})")
            self.items[idx] = (_bne(rs, rt, off) if op == "bne"
                               else _beq(rs, rt, off))
        return b"".join(struct.pack("<I", w) for w in self.items)


# ─── CAVE BUILDER ─────────────────────────────────────────────────────────────

def cap_word(bt_id: int) -> int:
    """Pack Breakthrough capsule ID into 16-byte capsule block word."""
    return ((bt_id & 0xFFFF) << 16) | 0x0007


def build_cave2() -> bytes:
    """
    Build cave2 code dynamically from the current version's addresses.
    This replaces the hardcoded CAVE2_CODE bytes so it works for any version.
    """
    import struct as _struct

    def _lui(rt, imm):   return _struct.pack("<I",(0x0F<<26)|(0<<21)|(rt<<16)|(imm&0xFFFF))
    def _ori(rt,rs,imm): return _struct.pack("<I",(0x0D<<26)|(rs<<21)|(rt<<16)|(imm&0xFFFF))
    def _sw(rt,off,base):return _struct.pack("<I",(0x2B<<26)|(base<<21)|(rt<<16)|(off&0xFFFF))
    def _lw(rt,off,base):return _struct.pack("<I",(0x23<<26)|(base<<21)|(rt<<16)|(off&0xFFFF))
    def _lbu(rt,off,base):return _struct.pack("<I",(0x24<<26)|(base<<21)|(rt<<16)|(off&0xFFFF))
    def _sb(rt,off,base): return _struct.pack("<I",(0x28<<26)|(base<<21)|(rt<<16)|(off&0xFFFF))
    def _j(addr):        return _struct.pack("<I",(0x02<<26)|((addr>>2)&0x3FFFFFF))
    def _nop():          return _struct.pack("<I",0)
    def load_addr_code(reg, addr):
        hi = (addr >> 16) & 0xFFFF
        lo = addr & 0xFFFF
        code = _lui(reg, hi)
        if lo:
            code += _ori(reg, reg, lo)
        return code

    # Register numbers
    AT, T0, T1, T2 = 1, 8, 9, 10

    # Get addresses from current module-level constants
    scratch_save = ADDR_SCRATCH + 0x80   # use a safe offset within scratch
    lock_table   = ADDR_LOCK_TABLE
    return_addr  = ADDR_RETURN2
    chars = DU_CHAR_CAPSULES  # {name: display_byte_addr}
    char_order = ["Goku","Kid Gohan","Teen Gohan","Adult Gohan","Vegeta",
                  "Krillin","Piccolo","Tien","Yamcha","Uub","Broly"]

    code = b""
    # Original instruction
    code += _struct.pack("<I", ORIG_INSTR2)

    # Save t0, t1
    code += load_addr_code(T2, scratch_save)
    code += _sw(T0, 0, T2)
    code += _sw(T1, 4, T2)

    # Load lock table base into t0
    code += load_addr_code(T0, lock_table)

    # For each character: lbu t1, index(t0) + sb t1, display_byte
    for i, name in enumerate(char_order):
        disp_addr = chars.get(name)
        if disp_addr is None:
            continue
        code += _lbu(T1, i, T0)
        # lui+sb: if lo >= 0x8000, sign extension makes offset negative.
        # Compensate by incrementing hi by 1.
        hi = (disp_addr >> 16) & 0xFFFF
        lo = disp_addr & 0xFFFF
        if lo >= 0x8000:
            hi = (hi + 1) & 0xFFFF
        code += _lui(AT, hi)
        code += _sb(T1, lo, AT)

    # Restore t0, t1
    code += load_addr_code(T2, scratch_save)
    code += _lw(T0, 0, T2)
    code += _lw(T1, 4, T2)

    # Re-execute the original instruction to restore the 'at' register to the
    # state the game expects at return_addr. Our lock writes clobber 'at' (via
    # lui at,0x004E), so without this the game's subsequent ori at,at,... +
    # use of 'at' would compute a wrong address and corrupt the save commit.
    code += _struct.pack("<I", ORIG_INSTR2)

    # Jump back
    code += _j(return_addr)
    code += _nop()

    return code


def build_cave(matchups: dict, randomize_stages: bool = True,
               music_in_cave: bool = False) -> bytes:
    for key, data in matchups.items():
        assert "p1" in data and "p2" in data, f"Missing p1/p2 in {key}"
        assert "char" in data["p1"] and "bt" in data["p1"], f"Missing char/bt in p1 for {key}"
        assert "char" in data["p2"] and "bt" in data["p2"], f"Missing char/bt in p2 for {key}"
        assert data["p1"]["bt"] is not None, f"None bt in p1 for {key}"
        assert data["p2"]["bt"] is not None, f"None bt in p2 for {key}"

    """
    Build the MIPS cave that intercepts fight loading and applies randomized matchups.

    matchups: { (char_name, saga_id, battle_id): {"p1": {...}, "p2": {...},
                                                   "stage_id": int,
                                                   "drain": bool} }
    """
    a = Asm()

    # Original overwritten instruction
    a.emit(ORIG_INSTR)

    # Save temp registers to scratch area
    a.load_addr("at", ADDR_SCRATCH)
    a.emit(_sw("t0", 0,  "at"))
    a.emit(_sw("t1", 4,  "at"))
    a.emit(_sw("t2", 8,  "at"))
    a.emit(_sw("t3", 12, "at"))

    # Guard: DU mode == 1
    a.load_addr("t0", ADDR_MODE)
    a.emit(_lbu("t0", 0, "t0"))
    a.load_imm("t1", 1)
    a.bne("t0", "t1", "return")
    a.emit(_nop())

    # Load DU character selector into t3
    a.load_addr("t3", ADDR_DU_CHAR)
    a.emit(_lbu("t3", 0, "t3"))

    # For each DU character that has mapped fights
    du_chars_in_matchups = set(k[0] for k in matchups)

    for char_name in du_chars_in_matchups:
        if char_name not in DU_BASES:
            continue
        du_id = DU_BASES[char_name]["du_id"]
        base  = DU_BASES[char_name]["base"]
        safe_name = char_name.replace(" ", "_").replace(".", "")
        next_char_label = f"next_char_{safe_name}"

        # Check if current DU char matches
        a.load_imm("t1", du_id)
        a.bne("t3", "t1", next_char_label)
        a.emit(_nop())

        # Load saga byte into t2 and battle state low byte into t0
        a.load_addr("t2", base + OFFSET_SAGA)
        a.emit(_lbu("t2", 0, "t2"))

        a.load_addr("t0", base + OFFSET_BATTLE)
        a.emit(_lbu("t0", 0, "t0"))   # low byte of battle state = fight ID

        # Check each fight for this character
        char_fights = {k: v for k, v in matchups.items() if k[0] == char_name}

        for (cn, saga_id, battle_id), data in sorted(char_fights.items()):
            safe_key = f"{safe_name}_{saga_id:02X}_{battle_id:02X}"
            target_label = f"target_{safe_key}"
            next_label   = f"next_{safe_key}"

            a.load_imm("t1", saga_id)
            a.bne("t2", "t1", next_label)
            a.emit(_nop())

            a.load_imm("t1", battle_id)
            a.beq("t0", "t1", target_label)
            a.emit(_nop())

            a.label(next_label)

        a.label(next_char_label)

    # No match — jump to return
    a.beq("zero", "zero", "return")
    a.emit(_nop())

    # Emit per-fight write blocks
    for (char_name, saga_id, battle_id), data in sorted(matchups.items()):
        safe_name = char_name.replace(" ", "_").replace(".", "")
        safe_key  = f"{safe_name}_{saga_id:02X}_{battle_id:02X}"
        a.label(f"target_{safe_key}")

        p1 = data["p1"]
        p2 = data["p2"]

        # Stage
        if randomize_stages:
            a.write_word(ADDR_STAGE_SELECT, data["stage_id"])

        # Music (NTSC-U only: the cave1 intercept timing works here, same as the
        # stage write. On BL the cave fires too early/gets overwritten, so music
        # is written via polling in the client instead — see _service_music).
        if music_in_cave and data.get("music") is not None:
            a.write_byte(ADDR_MUSIC, data["music"])

        # Drain trap
        if data.get("drain"):
            a.write_word(ADDR_BATTLE_MOD, 0x00020003)

        # P1 character + form (transformation) + Breakthrough block
        if data.get("write_p1", True):
            a.write_word(ADDR_P1_CHAR,   p1["char"])
            a.write_word(ADDR_P1_CHAR_T4, p1.get("form", 0) & 0xFFFFFFFF)
            a.write_word(ADDR_P1_CAPS + 0x00, cap_word(p1["bt"]))
            a.write_word(ADDR_P1_CAPS + 0x04, 0xFFFFFFFF)
            a.write_word(ADDR_P1_CAPS + 0x08, 0xFFFFFFFF)
            a.write_word(ADDR_P1_CAPS + 0x0C, 0xFFFFFFFF)

        # P2 character + form (transformation) + Breakthrough block
        if data.get("write_p2", True):
            a.write_word(ADDR_P2_CHAR,   p2["char"])
            a.write_word(ADDR_P2_CHAR_T4, p2.get("form", 0) & 0xFFFFFFFF)
            a.write_word(ADDR_P2_CAPS + 0x00, cap_word(p2["bt"]))
            a.write_word(ADDR_P2_CAPS + 0x04, 0xFFFFFFFF)
            a.write_word(ADDR_P2_CAPS + 0x08, 0xFFFFFFFF)
            a.write_word(ADDR_P2_CAPS + 0x0C, 0xFFFFFFFF)

        a.beq("zero", "zero", "return")
        a.emit(_nop())

    # Return: restore regs + jump back
    a.label("return")
    a.load_addr("at", ADDR_SCRATCH)
    a.emit(_lw("t0", 0,  "at"))
    a.emit(_lw("t1", 4,  "at"))
    a.emit(_lw("t2", 8,  "at"))
    a.emit(_lw("t3", 12, "at"))
    a.emit(_j(ADDR_RETURN))
    a.emit(_nop())

    return a.finalize()


# ─── B3 INTERFACE ─────────────────────────────────────────────────────────────

class B3Interface:
    def __init__(self, logger: Logger):
        self.pine = Pine()
        self.logger = logger
        self._game_id: Optional[str] = None
        self._cave_installed = False
        self._da_count_cache = None  # cached arena count address (per session)
        self._shop_sig_cache = None  # cached ess_shop.c anchor (per load)
        self._cave_supported = True  # False for versions without cave addresses
        self._deathlink_supported = False  # set True at connect if HP addrs mapped
        self._version = VERSIONS.get(GAME_CRC, {})
        self._installed_cave_code = None
        self._prev_screen = -1
        self._prev_battle_states: dict = {}   # char_name → last battle state
        self._prev_ownership: Optional[bytes] = None
        self._shop_open = False

    # ── Connection ────────────────────────────────────────────────────────────

    def connect(self) -> bool:
        if not self.pine.connect():
            return False
        try:
            crc = self.pine.get_game_crc()
            gid = self.pine.get_game_id()
            self.logger.info(f"[B3] Game: {gid!r} CRC: {crc!r}")
            if not crc:
                self.logger.warning("[B3] CRC empty - game may still be loading")
                return False
            ver = VERSIONS.get(crc.lower())
            if ver is None:
                self.logger.warning(f"[B3] Unsupported game CRC: {crc!r}")
                return False
            self._game_id = gid or ver.get("game_id", GAME_ID)
            self._version = ver
            self._crc = crc.lower()
            self._load_version_addrs(ver)
            self.logger.info(f"[B3] Connected - DBZ Budokai 3 ({crc.upper()})")
            return True
        except Exception as e:
            self.logger.warning(f"[B3] Connect error: {e}")
            return False

    def _load_version_addrs(self, ver: dict):
        """Override module-level address constants with version-specific values."""
        import sys
        mod = sys.modules[__name__]
        mapping = {
            "addr_p1_char":         "ADDR_P1_CHAR",
            "addr_p1_char_t4":      "ADDR_P1_CHAR_T4",
            "addr_p1_caps":         "ADDR_P1_CAPS",
            "addr_p2_char":         "ADDR_P2_CHAR",
            "addr_p2_char_t4":      "ADDR_P2_CHAR_T4",
            "addr_p2_caps":         "ADDR_P2_CAPS",
            "addr_stage_select":    "ADDR_STAGE_SELECT",
            "addr_music":           "ADDR_MUSIC",
            "addr_battle_mod":      "ADDR_BATTLE_MOD",
            "addr_screen":          "ADDR_SCREEN",
            "addr_mode":            "ADDR_MODE",
            "addr_du_char":         "ADDR_DU_CHAR",
            "addr_zenie_rt":        "ADDR_ZENIE_RT",
            "addr_zenie_du":        "ADDR_ZENIE_DU",
            "addr_zenie_saved":     "ADDR_ZENIE_SAVED",
            "addr_cave":            "ADDR_CAVE",
            "addr_debug":           "ADDR_DEBUG",
            "addr_scratch":         "ADDR_SCRATCH",
            "addr_intercept":       "ADDR_INTERCEPT",
            "addr_return":          "ADDR_RETURN",
            "cave_jump":            "CAVE_JUMP",
            "orig_instr":           "ORIG_INSTR",
            "addr_intercept2":      "ADDR_INTERCEPT2",
            "addr_return2":         "ADDR_RETURN2",
            "orig_instr2":          "ORIG_INSTR2",
            "addr_cave2":           "ADDR_CAVE2",
            "cave2_jump":           "CAVE2_JUMP",
            "shop_off_items":       "SHOP_OFF_ITEMS_FROM_SIG",
            "shop_off_count":       "SHOP_OFF_COUNT_FROM_SIG",
            "shop_off_zenie":       "SHOP_OFF_ZENIE_FROM_SIG",
            "dragon_ball_addrs":    "DRAGON_BALL_ADDRS",
            "shop_purchase_base":       "SHOP_PURCHASE_BASE",
            "shop_purchase_by_display": "SHOP_PURCHASE_BY_DISPLAY",
            "addr_lock_table":      "ADDR_LOCK_TABLE",
            "rt_caps_base":         "RT_CAPS_BASE",
            "du_rt_caps_base":      "DU_RT_CAPS_BASE",
            "da_clear_base":        "ADDR_DA_CLEAR_BASE",
            "da_ticket_display":    "DA_TICKET_DISPLAY",
            "da_ticket_ownership":  "DA_TICKET_OWNERSHIP",
            "da_ticket_du_rt":      "DA_TICKET_DU_RT",
            "shop_ownership_base":  "SHOP_OWNERSHIP_BASE",
            "du_char_capsules":     "DU_CHAR_CAPSULES",
            "du_bases":             "DU_BASES",
            "addr_p1_hp":           "ADDR_P1_HP",
            "addr_fight_end_hp":     "ADDR_FIGHT_END_HP",
        }
        for ver_key, const_name in mapping.items():
            if ver_key in ver and ver[ver_key] is not None:
                setattr(mod, const_name, ver[ver_key])
                self.logger.debug(f"[B3] {const_name} = {ver[ver_key]!r}")
        # Disable features that have None addresses (e.g. cave for unsupported version)
        if ver.get("addr_intercept") is None:
            self._cave_supported = False
            self.logger.info("[B3] Fight cave not supported for this version — randomization disabled")
        else:
            self._cave_supported = True
        # DeathLink requires the version's HP addresses. If absent/None, disable.
        if ver.get("addr_p1_hp") is None or ver.get("addr_fight_end_hp") is None:
            self._deathlink_supported = False
            self.logger.info("[B3] DeathLink not supported for this version (HP addresses not mapped).")
        else:
            self._deathlink_supported = True

    def disconnect(self):
        self.pine.disconnect()
        self._game_id = None
        self._cave_installed = False
        self._crc = ""

    def is_connected(self) -> bool:
        return self.pine.is_connected() and self._game_id is not None

    def music_cave_supported(self) -> bool:
        """NTSC-U (CRC c97ef0a4) writes battle music inside the cave1 intercept
        (works there). On BL (CRC 2a4b60eb) the intercept fires too early / gets
        overwritten, so music must be written via polling instead. Detection is
        by CRC, since both versions can report the same game_id string."""
        return getattr(self, "_crc", "") == "c97ef0a4"

    # ── Cave management ───────────────────────────────────────────────────────

    def cave_installed(self) -> bool:
        try:
            # Verify the jump is intact
            if self.pine.read32(ADDR_INTERCEPT) != CAVE_JUMP:
                return False
            # Verify the cave code is intact (check first + last words)
            code = getattr(self, "_installed_cave_code", None)
            if code is None or len(code) < 4:
                # No stored code — fall back to checking first instruction
                return self.pine.read32(ADDR_CAVE) == ORIG_INSTR
            first_expected = int.from_bytes(code[0:4], "little")
            last_expected  = int.from_bytes(code[-4:], "little")
            if self.pine.read32(ADDR_CAVE) != first_expected:
                return False
            if self.pine.read32(ADDR_CAVE + len(code) - 4) != last_expected:
                return False
            return True
        except Exception:
            return False

    def install_cave(self, cave_code: bytes):
        if not self._cave_supported:
            self.logger.info("[B3] Cave install skipped — not supported for this version")
            return
        if len(cave_code) > 0x10000:
            self.logger.error(f"[B3] Cave too large: {len(cave_code)} bytes!")
            return
        # Verify cave doesn't overlap scratch area
        cave_end = ADDR_CAVE + len(cave_code)
        if cave_end > ADDR_SCRATCH:
            self.logger.error(f"[B3] Cave overlaps scratch area! End=0x{cave_end:08X}")
            return
        self._installed_cave_code = cave_code  # store for integrity check
        self.pine.write_bytes(ADDR_CAVE, cave_code)
        self.pine.write32(ADDR_INTERCEPT, CAVE_JUMP)
        self._cave_installed = self.cave_installed()
        if self._cave_installed:
            self.logger.info(f"[B3] Cave installed ({len(cave_code)} bytes, end=0x{cave_end:08X})")
        else:
            self.logger.error("[B3] Cave installation failed!")

    def restore_original(self):
        self.pine.write32(ADDR_INTERCEPT, ORIG_INSTR)
        self._cave_installed = False
        self.logger.info("[B3] Cave removed, original instruction restored")

    # ── Game state reads ──────────────────────────────────────────────────────

    def get_screen(self) -> int:
        return self.pine.read16(ADDR_SCREEN)

    # ── DeathLink ─────────────────────────────────────────────────────────────
    def kill_player(self) -> bool:
        """Incoming DeathLink: pin Player 1's HP float copies to a TINY NONZERO
        value so the AI keeps attacking and lands the finishing blow (writing
        true 0 makes the AI passive and never finishes the kill). Returns True if
        any write went through. Meant to be called every poll until the fight
        registers its end (ADDR_FIGHT_END_HP -> 0)."""
        ok = False
        for addr in ADDR_P1_HP:
            try:
                self.pine.write32(addr, HP_KILL_VALUE)
                ok = True
            except Exception:
                pass
        return ok

    def fight_end_hp(self) -> int:
        """Read the HP copy that clears to 0 when a fight ENDS (win or loss)."""
        try:
            return self.pine.read32(ADDR_FIGHT_END_HP)
        except Exception:
            return -1

    def in_du_battle(self) -> bool:
        """True while on the Dragon Universe battle screen (fight is live; the
        retry/lose popup is an overlay that keeps this screen)."""
        try:
            return self.pine.read16(ADDR_SCREEN) == SCREEN_DU_BATTLE
        except Exception:
            return False

    def on_results_win(self) -> bool:
        """True on the win results screen (used to discriminate win from loss)."""
        try:
            return self.pine.read16(ADDR_SCREEN) == SCREEN_RESULTS_WIN
        except Exception:
            return False


    def get_mode(self) -> int:
        return self.pine.read8(ADDR_MODE)

    def get_du_char(self) -> int:
        return self.pine.read8(ADDR_DU_CHAR)

    def get_active_du_char_name(self):
        """Return the active DU character's name (per DU_BASES), or None."""
        cid = self.get_du_char()
        for char_name, info in DU_BASES.items():
            if info["du_id"] == cid:
                return char_name
        return None

    def in_du(self) -> bool:
        return self.get_mode() == 0x01

    def write_music(self, track: int):
        """Write the battle music track byte (BL polling path)."""
        try:
            self.pine.write8(ADDR_MUSIC, track & 0xFF)
        except Exception:
            pass

    def write_battle_mod(self, value: int):
        """Write the battle-modifier word (0x00020003 = HP drain, 0 = none).
        Used by the polling-based HP Drain Trap path so a received trap is
        applied to the upcoming fight rather than baked into the seed."""
        try:
            self.pine.write32(ADDR_BATTLE_MOD, value & 0xFFFFFFFF)
        except Exception:
            pass

    def any_fight_loading(self) -> bool:
        """Returns True if a fight is loading or in progress.
        Uses screen ID — only safe to install cave on world map (0x0108)."""
        screen = self.get_screen()
        # Only safe on world map screen
        return screen != SCREEN_WORLD_MAP

    def get_battle_state(self, char_name: str) -> int:
        if char_name not in DU_BASES:
            return 0
        base = DU_BASES[char_name]["base"]
        return self.pine.read32(base + OFFSET_BATTLE)

    def get_saga(self, char_name: str) -> int:
        if char_name not in DU_BASES:
            return 0
        base = DU_BASES[char_name]["base"]
        return self.pine.read8(base + OFFSET_SAGA)

    def get_battle_completion(self, char_name: str) -> int:
        if char_name not in DU_BASES:
            return 0
        base = DU_BASES[char_name]["base"]
        return self.pine.read8(base + OFFSET_BATTLE_COMP)

    # ── Fight detection ───────────────────────────────────────────────────────

    def current_fight_key(self):
        """Best-effort (char, saga, battle) key for the fight currently
        loading/active, using the same tracking poll_completed_fights maintains.
        Returns None if not resolvable. Used by the BL music-write path."""
        if not self.in_du():
            return None
        active_char_id = self.get_du_char()
        active_char = None
        for char_name, info in DU_BASES.items():
            if info["du_id"] == active_char_id:
                active_char = char_name
                break
        if not active_char:
            return None
        bs = self.get_battle_state(active_char)
        battle_low = bs & 0xFF
        saga_id = self.get_saga(active_char)
        if battle_low in (0xFF, 0x00):
            # fall back to last-tracked battle (set while in battle screens)
            return (getattr(self, "_last_char", active_char),
                    getattr(self, "_last_saga", 0),
                    getattr(self, "_last_battle", 0))
        return (active_char, saga_id, battle_low)

    def poll_completed_fights(self) -> list:
        """
        Poll for completed DU fights using screen transitions.

        WIN  = screen transitions 0x0109 (DU Battle) -> 0x010A (Results WIN)
        LOSS = screen transitions 0x0109 (DU Battle) -> 0x0108 (World Map)

        Track last_battle/last_saga only while in battle-related screens
        to avoid reading stale values from world map idle state.
        """
        completed = []
        if not self.in_du():
            self._prev_screen = self.get_screen()
            return completed

        screen = self.get_screen()
        prev_screen = getattr(self, '_prev_screen', screen)
        active_char_id = self.get_du_char()

        # Find active character
        active_char = None
        for char_name, info in DU_BASES.items():
            if info["du_id"] == active_char_id:
                active_char = char_name
                break

        if active_char:
            # Track battle state while in battle-related screens
            if screen in (SCREEN_WORLD_MAP, SCREEN_DU_BATTLE,
                          SCREEN_RESULTS_WIN, SCREEN_SHENRON):
                bs = self.get_battle_state(active_char)
                battle_low = bs & 0xFF
                saga_id = self.get_saga(active_char)
                if battle_low not in (0xFF, 0x00):
                    self._last_battle = battle_low
                    self._last_saga = saga_id
                    self._last_char = active_char

            # WIN: DU Battle -> Results Screen
            if prev_screen == SCREEN_DU_BATTLE and screen == SCREEN_RESULTS_WIN:
                key = (getattr(self, '_last_char', active_char),
                       getattr(self, '_last_saga', 0),
                       getattr(self, '_last_battle', 0))
                if key in FIGHT_LOCATIONS:
                    completed.append(FIGHT_LOCATIONS[key])

        self._prev_screen = screen
        return completed

    # ── Shop ──────────────────────────────────────────────────────────────────

    def is_shop_open(self) -> bool:
        return self.get_screen() == SCREEN_SHOP

    def find_shop_base(self, use_cache=True):
        """
        Locate the live shop struct dynamically. Returns the first valid
        ess_shop.c anchor. Use find_all_shop_bases() to get all instances.
        """
        bases = self.find_all_shop_bases(use_cache=use_cache)
        return bases[0] if bases else None

    def find_all_shop_bases(self, use_cache=True):
        """
        Find ALL ess_shop.c instances in 0x00880000-0x0089FFFF and return
        their anchor addresses. There can be 2-3 instances; we write to all
        so the active/displayed one always gets our AP stock.
        """
        # Validate cache — it stores a list now
        if use_cache and getattr(self, "_shop_sig_cache", None):
            still_valid = []
            for a in self._shop_sig_cache:
                try:
                    if (self.pine.read32(a) == SHOP_SIG0
                            and self.pine.read32(a + 4) == SHOP_SIG1):
                        still_valid.append(a)
                except Exception:
                    pass
            if still_valid:
                self._shop_sig_cache = still_valid
                return still_valid
            self._shop_sig_cache = None

        # Scan full region for all instances
        found = []
        addr = SHOP_SCAN_START
        while addr < SHOP_SCAN_END:
            try:
                if (self.pine.read32(addr) == SHOP_SIG0
                        and self.pine.read32(addr + 4) == SHOP_SIG1):
                    found.append(addr)
                    addr += 8  # skip past this match
                    continue
            except Exception:
                pass
            addr += 4
        self._shop_sig_cache = found if found else None
        return found

    def _shop_count_addr(self, sig_addr):
        return sig_addr + SHOP_OFF_COUNT_FROM_SIG

    def _shop_items_addr(self, sig_addr):
        return sig_addr + SHOP_OFF_ITEMS_FROM_SIG

    def write_shop_stock(self, pool_entries: list):
        """Write AP stock to ALL live ess_shop.c instances so whichever one
        the game displays from gets our capsules."""
        bases = self.find_all_shop_bases()
        if not bases:
            return False
        for sig in bases:
            items_base = self._shop_items_addr(sig)
            count_addr = self._shop_count_addr(sig)
            count = min(len(pool_entries), SHOP_MAX_SLOTS)
            for i in range(count):
                disp_idx, _own_idx, _name = pool_entries[i]
                entry = items_base + i * SHOP_STRUCT_SIZE
                self.pine.write32(entry + SHOP_OFF_DISPLAY,  disp_idx)
                self.pine.write32(entry + SHOP_OFF_RECEIVED, disp_idx)
                self.pine.write32(entry + SHOP_OFF_PRICE,    SHOP_PRICE)
                self.pine.write32(entry + SHOP_OFF_FLAGS,    0x02)
            self.pine.write32(count_addr, count)
        return True

    def grant_skill(self, skill_name: str):
        """Grant a skill capsule by writing 1 to its DU-RT and RT addresses.
        SKILL_CAPSULES holds NTSC-U addresses; translate to the active version."""
        entry = SKILL_CAPSULES.get(skill_name)
        if not entry:
            return
        du_rt, rt = entry
        du_rt_shift = DU_RT_CAPS_BASE - NTSC_DU_RT_CAPS_BASE
        rt_shift    = RT_CAPS_BASE - NTSC_RT_CAPS_BASE
        self.pine.write8(du_rt + du_rt_shift, 0x01)
        self.pine.write8(rt + rt_shift, 0x01)

    def grant_item_capsule(self, capsule_name: str):
        """Grant an equipment/consumable capsule. Same mechanism as grant_skill
        (write 1 to DU-RT + RT); ITEM_CAPSULES holds NTSC-U (du_rt, rt) addrs,
        translated to the active version via the same base shifts."""
        entry = ITEM_CAPSULES.get(capsule_name)
        if not entry:
            return
        du_rt, rt = entry
        du_rt_shift = DU_RT_CAPS_BASE - NTSC_DU_RT_CAPS_BASE
        rt_shift    = RT_CAPS_BASE - NTSC_RT_CAPS_BASE
        self.pine.write8(du_rt + du_rt_shift, 0x01)
        self.pine.write8(rt + rt_shift, 0x01)

    def read_dragon_ball_byte(self, char_name: str) -> int:
        """Read a character's Dragon Ball collection bitfield (bits 0-6)."""
        addr = DRAGON_BALL_ADDRS.get(char_name)
        if addr is None:
            return 0
        try:
            return self.pine.read8(addr)
        except Exception:
            return 0

    def reapply_skills(self, skills: set):
        """Re-grant all received skills (handles load resets)."""
        for skill_name in skills:
            self.grant_skill(skill_name)

    def apply_skill_locks(self, granted: set):
        """
        Write the full skill lock state: 1 for AP-granted skills, 0 for all
        others. This gates skills so the player can only obtain them via AP,
        suppressing natural in-game unlocks. Call only on DU world map / shop.

        SKILL_CAPSULES holds NTSC-U absolute addresses. We translate each to the
        active version using the per-version cap-table bases (offsets are
        identical across versions). On NTSC-U the translation is a no-op.
        """
        rt_shift   = RT_CAPS_BASE - NTSC_RT_CAPS_BASE
        du_rt_shift = DU_RT_CAPS_BASE - NTSC_DU_RT_CAPS_BASE
        for skill_name, (du_rt, rt) in SKILL_CAPSULES.items():
            val = 0x01 if skill_name in granted else 0x00
            self.pine.write8(du_rt + du_rt_shift, val)
            self.pine.write8(rt + rt_shift, val)

    # ── Dragon Arena ──────────────────────────────────────────────────────────

    def unlock_dragon_arena(self):
        """Write 1 to the 3 Dragon Arena Ticket tables to unlock the mode."""
        self.pine.write8(DA_TICKET_DISPLAY, 0x01)
        self.pine.write8(DA_TICKET_OWNERSHIP, 0x01)
        self.pine.write8(DA_TICKET_DU_RT, 0x01)

    def lock_dragon_arena(self):
        """Write 0 to the 3 ticket tables to keep the mode locked."""
        self.pine.write8(DA_TICKET_DISPLAY, 0x00)
        self.pine.write8(DA_TICKET_OWNERSHIP, 0x00)
        self.pine.write8(DA_TICKET_DU_RT, 0x00)

    def get_da_screen_on_charsel(self) -> bool:
        return self.get_screen() == SCREEN_DA_CHARSEL

    def find_da_count_addr(self, use_cache=True):
        """
        Locate the live arena-list count dynamically. The struct is allocated
        per-session and the magic's offset from the count is NOT constant, but
        the 8-byte signature '03 00 FF FF 02 00 02 00' sits at a fixed offset:
        count = signature_addr + 0x0C. Validated against a sane fight range.
        The result is cached; the scan only reruns on a cache miss.
        """
        SIG0 = 0xFFFF0003  # little-endian read32 of bytes 03 00 FF FF
        SIG1 = 0x00020002  # little-endian read32 of bytes 02 00 02 00

        # 1) Validate the cached address first (cheap)
        if use_cache and getattr(self, "_da_count_cache", None) is not None:
            sig_addr = self._da_count_cache - 0x0C
            try:
                if (self.pine.read32(sig_addr) == SIG0
                        and self.pine.read32(sig_addr + 4) == SIG1):
                    cnt = self.pine.read32(self._da_count_cache)
                    if 1 <= cnt <= 380:
                        return self._da_count_cache
            except Exception:
                pass
            self._da_count_cache = None

        # 2) Check known/observed addresses first (instant — no scan needed).
        KNOWN_SIG_ADDRS = [
            0x00890740, 0x00893740, 0x00893700,
            0x0088DC80, 0x0088DF00,
            0x00A149C0, 0x00A91B00,
            0x0089F580,
        ]
        for sig_addr in KNOWN_SIG_ADDRS:
            cnt_addr = sig_addr + 0x0C
            try:
                if (self.pine.read32(sig_addr) == SIG0
                        and self.pine.read32(sig_addr + 4) == SIG1):
                    cnt = self.pine.read32(cnt_addr)
                    if 1 <= cnt <= 380:
                        self._da_count_cache = cnt_addr
                        return cnt_addr
            except Exception:
                pass

        # 3) Fallback: scan known regions if not found in priority list.
        # Three tight scan windows based on all observed signature locations.
        # Each window covers a cluster of observed addresses with margin.
        scan_windows = [
            (0x0088D000, 0x0088F000),  # 0x0088DC80, 0x0088DF00
            (0x00890000, 0x0089F800),  # 0x00890740, 0x00893700, 0x00893740, 0x0089F580
            (0x00A14000, 0x00A16000),  # 0x00A149C0
            (0x00A91000, 0x00A92000),  # 0x00A91B00 (back from stage select)
        ]
        for scan_start, scan_end in scan_windows:
            addr = scan_start
            while addr < scan_end:
                try:
                    if self.pine.read32(addr) == SIG0 and self.pine.read32(addr + 4) == SIG1:
                        cnt_addr = addr + 0x0C
                        cnt = self.pine.read32(cnt_addr)
                        if 1 <= cnt <= 380:
                            self._da_count_cache = cnt_addr
                            return cnt_addr
                except Exception:
                    pass
                addr += 4
        return None

    def clamp_da_opponent_count(self, max_count: int):
        """Force the arena opponent list count to max_count, but only WRITE when
        the current value actually exceeds max_count. Reading first and skipping
        unnecessary writes minimizes how often we poke the list struct, shrinking
        the window where a write could land during the fight-load teardown and
        crash the emulator."""
        cnt_addr = self.find_da_count_addr()
        if cnt_addr is None:
            return
        try:
            current = self.pine.read32(cnt_addr)
        except Exception:
            return
        # Only clamp when needed; if already within the limit, do nothing.
        if not (1 <= current <= 380) or current <= max_count:
            return
        try:
            self.pine.write32(cnt_addr, max_count)
        except Exception:
            pass

    def read_da_clear_flag(self, index: int) -> int:
        return self.pine.read8(ADDR_DA_CLEAR_BASE + index)

    def clear_shop(self):
        """Empty the shop (count = 0) across all live instances.
        Also writes to the fallback hardcoded address as a safety net."""
        # Write to all dynamically-found instances
        for sig in self.find_all_shop_bases():
            self.pine.write32(self._shop_count_addr(sig), 0)
        # Fallback: also zero the original hardcoded count address in case
        # the game repopulated an instance we didn't find via scan
        self.pine.write32(ADDR_SHOP_COUNT, 0)

    def read_capsule_owned(self, ownership_index: int, display_index: int = None) -> int:
        """Read whether a capsule was purchased.
        BL uses the quantity table indexed by display index; NTSC-U uses the
        ownership table indexed by own_idx."""
        if SHOP_PURCHASE_BY_DISPLAY and display_index is not None:
            return self.pine.read8(SHOP_PURCHASE_BASE + display_index)
        return self.pine.read8(SHOP_PURCHASE_BASE + ownership_index)

    def read_shop_slot0_display(self) -> int:
        """Read the display index of shop slot 0 (to detect game repopulation).
        Returns -1 if the live shop struct isn't found."""
        sig = self.find_shop_base()
        if sig is None:
            return -1
        return self.pine.read32(self._shop_items_addr(sig) + SHOP_OFF_DISPLAY)

    def clear_capsule_owned(self, ownership_index: int, display_index: int = None):
        """Reset purchase flag to 0 — capsules are AP triggers, not kept.
        BL clears the quantity table by display index; NTSC-U the ownership table."""
        if SHOP_PURCHASE_BY_DISPLAY and display_index is not None:
            self.pine.write8(SHOP_PURCHASE_BASE + display_index, 0x00)
        else:
            self.pine.write8(SHOP_PURCHASE_BASE + ownership_index, 0x00)

    # ── Saga lockout ─────────────────────────────────────────────────────────

    def unlock_saga(self, char_name: str, saga_id: int):
        """
        Allow the given saga for a DU character by writing
        the event dispatcher byte. Only writes if currently locked.
        """
        if char_name not in DU_BASES:
            return
        base = DU_BASES[char_name]["base"]
        disp_addr = base + 0x16
        # Dispatcher values: 0x64=Saiyan, 0x66=Frieza, 0x67=Cell, 0x69=Buu
        DISP = {0x00: 0x64, 0x01: 0x66, 0x02: 0x67, 0x03: 0x69}
        if saga_id in DISP:
            self.pine.write8(disp_addr, DISP[saga_id])

    # ── Cave 2 (character lock) ───────────────────────────────────────────────

    def cave2_installed(self) -> bool:
        try:
            if ADDR_INTERCEPT2 is None:
                return False
            return self.pine.read32(ADDR_INTERCEPT2) == CAVE2_JUMP
        except Exception:
            return False

    def install_cave2(self):
        if ADDR_INTERCEPT2 is None:
            self.logger.info("[B3] Cave2 (char locks) not supported for this version")
            return
        # Use hardcoded bytes for NTSC-U (verified working), dynamic for other versions
        crc = getattr(self, '_version', {}).get('game_id', '')
        if ADDR_INTERCEPT2 == 0x001F2B54:
            # NTSC-U — use the tested hardcoded cave2 bytes
            cave2_code = CAVE2_CODE
        else:
            # Other versions (BL etc.) — generate dynamically
            cave2_code = build_cave2()
        self.pine.write_bytes(ADDR_CAVE2, cave2_code)
        expected_first = int.from_bytes(cave2_code[:4], "little")
        actual_first = self.pine.read32(ADDR_CAVE2)
        if actual_first != expected_first:
            self.logger.error(
                f"[B3] Cave2 write failed at 0x{ADDR_CAVE2:08X}: "
                f"expected 0x{expected_first:08X}, got 0x{actual_first:08X}; hook not installed"
            )
            return
        self.pine.write32(ADDR_INTERCEPT2, CAVE2_JUMP)
        if self.cave2_installed():
            self.logger.info(f"[B3] Cave2 (char locks) installed at 0x{ADDR_CAVE2:08X}")
        else:
            self.logger.error("[B3] Cave2 installation failed!")

    def restore_cave2(self):
        self.pine.write32(ADDR_INTERCEPT2, ORIG_INSTR2)

    def update_lock_table(self, unlocked: set):
        """Write the lock table to RAM. Cave reads this on every save/load."""
        for i, (char_name, _) in enumerate(LOCK_TABLE_CHARS):
            val = 0x01 if char_name in unlocked else 0x00
            self.pine.write8(ADDR_LOCK_TABLE + i, val)

    def read_zenie_rt(self) -> int:
        """Read the real-time Zenie counter. A genuine shop purchase deducts
        from this; saving or editing capsules does NOT. Used to gate shop-check
        detection so bulk inventory writes (save/edit-capsule) can't be mistaken
        for purchases. Returns -1 on failure.

        Reads the LIVE module attribute (patched by _load_version_addrs) so the
        version-specific address is always used (NTSC-U 0x00543D28 vs BL
        0x0058F718)."""
        try:
            import sys
            addr = getattr(sys.modules[__name__], "ADDR_ZENIE_RT", None)
            if addr is None:
                return -1
            return self.pine.read32(addr)
        except Exception:
            return -1

    def write_zenie(self, amount: int):
        """Add Zenie to all distinct counters so every context (shop, DU, saved)
        reflects it. Addresses are de-duplicated so versions where two counters
        share an address (e.g. BL saved==DU) don't double-add."""
        seen = set()
        for addr in (ADDR_ZENIE_RT, ADDR_ZENIE_DU, ADDR_ZENIE_SAVED):
            if addr is None or addr in seen:
                continue
            seen.add(addr)
            try:
                current = self.pine.read32(addr)
                self.pine.write32(addr, current + amount)
            except Exception:
                pass

    def apply_character_locks(self, unlocked: set):
        """
        Write character visibility bytes based on unlocked set.
        Also updates the cave2 lock table for persistence across save/load.
        """
        for char_name, addr in DU_CHAR_CAPSULES.items():
            if char_name in unlocked:
                self.pine.write8(addr, 0x01)
            else:
                self.pine.write8(addr, 0x00)
        # Also update cave2 lock table
        self.update_lock_table(unlocked)

    def show_character(self, char_name: str):
        """Unlock a character in DU character select."""
        if char_name in DU_CHAR_CAPSULES:
            self.pine.write8(DU_CHAR_CAPSULES[char_name], 0x01)
            self.logger.info(f"[B3] Character unlocked: {char_name}")
