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
    GAME_ID, GAME_CRC, DU_BASES, FIGHT_LOCATIONS, ROSTER, STAGES, CAPSULE_SHOP_IDS,
    ADDR_CAVE, ADDR_DEBUG, ADDR_SCRATCH, ADDR_INTERCEPT, ADDR_RETURN,
    CAVE_JUMP, ORIG_INSTR,
    ADDR_SCREEN, ADDR_MODE, ADDR_DU_CHAR, ADDR_ZENIE_RT,
    ADDR_ZENIE_DU, ADDR_ZENIE_SAVED,
    ADDR_P1_CHAR, ADDR_P1_CHAR_T4, ADDR_P1_CAPS,
    ADDR_P2_CHAR, ADDR_P2_CHAR_T4, ADDR_P2_CAPS,
    ADDR_STAGE_SELECT, ADDR_BATTLE_MOD,
    ADDR_SHOP_STRUCT_BASE, SHOP_STRUCT_SIZE, SHOP_DISPLAY_BASE,
    SHOP_OWNERSHIP_BASE, SHOP_PRICE, SHOP_MAX_SLOTS, ADDR_SHOP_COUNT,
    SHOP_SIG0, SHOP_SIG1, SHOP_OFF_COUNT_FROM_SIG, SHOP_OFF_ITEMS_FROM_SIG,
    SHOP_SCAN_START, SHOP_SCAN_END,
    SHOP_OFF_DISPLAY, SHOP_OFF_RECEIVED, SHOP_OFF_PRICE, SHOP_OFF_FLAGS,
    SHOP_CAPSULE_POOL,
    SKILL_CAPSULES,
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


def build_cave(matchups: dict, randomize_stages: bool = True) -> bytes:
    # Validate matchups
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

        # Drain trap
        if data.get("drain"):
            a.write_word(ADDR_BATTLE_MOD, 0x00020003)

        # P1 character + clear template + Breakthrough block
        if data.get("write_p1", True):
            a.write_word(ADDR_P1_CHAR,   p1["char"])
            a.write_word(ADDR_P1_CHAR_T4, 0)
            a.write_word(ADDR_P1_CAPS + 0x00, cap_word(p1["bt"]))
            a.write_word(ADDR_P1_CAPS + 0x04, 0xFFFFFFFF)
            a.write_word(ADDR_P1_CAPS + 0x08, 0xFFFFFFFF)
            a.write_word(ADDR_P1_CAPS + 0x0C, 0xFFFFFFFF)

        # P2 character + clear template + Breakthrough block
        if data.get("write_p2", True):
            a.write_word(ADDR_P2_CHAR,   p2["char"])
            a.write_word(ADDR_P2_CHAR_T4, 0)
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
            if crc == GAME_CRC:
                self._game_id = gid or GAME_ID
                self.logger.info(f"[B3] Connected to PCSX2 - DBZ Budokai 3 NTSC-U confirmed")
                return True
            elif not crc:
                self.logger.warning("[B3] CRC empty - game may still be loading")
                return False
            else:
                self.logger.warning(f"[B3] Wrong game CRC: {crc!r} (expected {GAME_CRC})")
                return False
        except Exception as e:
            self.logger.warning(f"[B3] Connect error: {e}")
            return False

    def disconnect(self):
        self.pine.disconnect()
        self._game_id = None
        self._cave_installed = False

    def is_connected(self) -> bool:
        return self.pine.is_connected() and self._game_id is not None

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
        # Verify cave fits in allocated space
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
        Locate the live shop struct dynamically. It is allocated per-load and
        relocates after other menus, but is anchored by the 'ess_shop.c' string.
        Relative to the string: count at +0x88, item list at +0x98.
        Returns the string address (the anchor), or None if not found.
        """
        # 1) Validate cached anchor cheaply
        if use_cache and getattr(self, "_shop_sig_cache", None) is not None:
            a = self._shop_sig_cache
            try:
                if (self.pine.read32(a) == SHOP_SIG0
                        and self.pine.read32(a + 4) == SHOP_SIG1):
                    return a
            except Exception:
                pass
            self._shop_sig_cache = None

        # 2) Scan for the signature
        addr = SHOP_SCAN_START
        while addr < SHOP_SCAN_END:
            try:
                if (self.pine.read32(addr) == SHOP_SIG0
                        and self.pine.read32(addr + 4) == SHOP_SIG1):
                    self._shop_sig_cache = addr
                    return addr
            except Exception:
                pass
            addr += 4
        return None

    def _shop_count_addr(self, sig_addr):
        return sig_addr + SHOP_OFF_COUNT_FROM_SIG

    def _shop_items_addr(self, sig_addr):
        return sig_addr + SHOP_OFF_ITEMS_FROM_SIG

    def write_shop_stock(self, pool_entries: list):
        """
        Write AP-controlled shop stock to the live shop struct, located
        dynamically via the 'ess_shop.c' anchor (the struct relocates after
        other menus load). Returns True if written, False if the shop struct
        wasn't found (in which case we must NOT write — avoids corrupting other
        menus that reuse the buffer, which caused the black-screen hang).
        """
        sig = self.find_shop_base()
        if sig is None:
            return False
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
        """Grant a skill capsule by writing 1 to its DU-RT and RT addresses."""
        entry = SKILL_CAPSULES.get(skill_name)
        if not entry:
            return
        du_rt, rt = entry
        self.pine.write8(du_rt, 0x01)
        self.pine.write8(rt, 0x01)

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
        """
        for skill_name, (du_rt, rt) in SKILL_CAPSULES.items():
            val = 0x01 if skill_name in granted else 0x00
            self.pine.write8(du_rt, val)
            self.pine.write8(rt, val)

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

        # 2) Scan for the signature. Count = signature + 0x0C.
        # The struct lands in one of two deterministic regions depending on
        # entry path: ~0x00890000 (from main menu) or ~0x00A91000 (back from
        # stage select). Scan both tight windows rather than one huge range.
        scan_windows = [
            (0x00890000, 0x00895000),
            (0x00A90000, 0x00A95000),
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
        """Clamp the arena opponent list count so only max_count fights show.
        Locates the count dynamically (address varies per session) and caches it.
        Only clamps DOWN — never raises above what the game has unlocked."""
        cnt_addr = self.find_da_count_addr()
        if cnt_addr is None:
            return
        try:
            current = self.pine.read32(cnt_addr)
        except Exception:
            return
        if current > max_count:
            self.pine.write32(cnt_addr, max_count)

    def read_da_clear_flag(self, index: int) -> int:
        return self.pine.read8(ADDR_DA_CLEAR_BASE + index)

    def clear_shop(self):
        """Empty the shop (count = 0) — used when no AP capsules remain to sell.
        Only acts if the live shop struct is found."""
        sig = self.find_shop_base()
        if sig is None:
            return
        self.pine.write32(self._shop_count_addr(sig), 0)

    def read_capsule_owned(self, ownership_index: int) -> int:
        """Read whether a capsule is owned (1) or not (0)."""
        return self.pine.read8(SHOP_OWNERSHIP_BASE + ownership_index)

    def read_shop_slot0_display(self) -> int:
        """Read the display index of shop slot 0 (to detect game repopulation).
        Returns -1 if the live shop struct isn't found."""
        sig = self.find_shop_base()
        if sig is None:
            return -1
        return self.pine.read32(self._shop_items_addr(sig) + SHOP_OFF_DISPLAY)

    def clear_capsule_owned(self, ownership_index: int):
        """Reset ownership to 0 — we use capsules as AP triggers, player doesn't keep them."""
        self.pine.write8(SHOP_OWNERSHIP_BASE + ownership_index, 0x00)

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
            return self.pine.read32(ADDR_INTERCEPT2) == CAVE2_JUMP
        except Exception:
            return False

    def install_cave2(self):
        # Install the character-lock cave first, verify that it actually landed,
        # then install the hook. This prevents 0x001F2B54 from jumping into
        # garbage if the cave write failed or the cave address changed.
        self.pine.write_bytes(ADDR_CAVE2, CAVE2_CODE)
        expected_first = int.from_bytes(CAVE2_CODE[:4], "little")
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

    def write_zenie(self, amount: int):
        """Add Zenie to all three counters so every context (shop, DU, saved)
        reflects it: real-time (0x543D28), DU total (0x4C6F08), and the
        memory-card/saved total (0x495568)."""
        for addr in (ADDR_ZENIE_RT, ADDR_ZENIE_DU, ADDR_ZENIE_SAVED):
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
