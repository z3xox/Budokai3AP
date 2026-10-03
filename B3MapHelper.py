"""
B3MapHelper — makes the Dragon Universe world map show what there is to do.

The game hides most interaction points until the player hovers over them, keeps
some behind a second playthrough, and moves to the next saga the moment a story
fight is won. With the helper on, the client owns the map instead:

  * every point of the current chapter is on the map, with an overworld marker
    and a coloured dot on the overview (red fight, green talk, blue battle spot,
    yellow item, orange Dragon Ball)
  * second-playthrough, capsule and level requirements on points are removed
  * a saga is split into chapters (what the game places between two story
    fights); a purple marker opens the next chapter, a pink one the previous
  * winning a saga's last fight no longer leaves the saga: a white marker on the
    last chapter goes to the next saga, a grey one on the first chapter goes back
  * winning the story's last fight no longer ends the Dragon Universe either: a
    white marker appears that plays the ending when the player is done
  * the name shown when hovering over a point says what is there: the
    Archipelago item of an open check, or what a marker does (see B3Labels)

Point lists come from data/MapData.py and data/MapDataBL.py (generated from the
game files), one per supported game version; the addresses for each version are
in MAP_VERSIONS (data/Constants.py). On any other version the helper stays off.
"""
import json
import math
import os
import struct
import time
from logging import Logger
from typing import Optional

from .data.Constants import (
    DU_BASES, DU_MODE, ADDR_MODE, ADDR_DU_CHAR, ADDR_SCREEN, OFFSET_SAGA, OFFSET_DRAGONBALLS,
    SCREEN_WORLD_MAP, SCREEN_DU_BATTLE, SCREEN_RESULTS_WIN,
    MAP_HELPER_CRC, MAP_VERSIONS, VERSIONS, MAP_POINTS_OFF, MAP_POINT_COUNT, MAP_POINT_SIZE,
    MAP_POINT_REQ_CAPSULE, MAP_POINT_REQ_EQUIPPED, MAP_POINT_CONDITION, MAP_POINT_LEVEL_MIN, MAP_POINT_DONE,
    OFFSET_EVENT_QUEUED, SAGA_EVENT_CLASSES,
    ENDING_EVENT_CLASSES,
    MAP_DOT_TEXTURE,
    MAP_DOT_PALETTE, SAGA_UNLOCK_IDS, FIGHT_LOCATIONS,
    MAP_HUD_LABELS, MAP_LABEL_FIRST, MAP_POINT_TYPE, MAP_PLAYER_POS,
)
from .data import MapData, MapDataBL
from .data.MapLocations import INTERACT_BY_EVENT, CHAR_NAMES, place_name
from . import B3Labels

NONE = 0xFFFFFFFF
SAGA_NAMES = ["Saiyan", "Frieza", "Cell", "Buu"]
SAGA_UNLOCK_NAMES = {saga: name for name, saga in SAGA_UNLOCK_IDS.items()}

SETTLE_TICKS   = 3        # quiet polls on the map before the point table is touched
COLOR_REFRESH  = 5.0      # seconds between full rewrites of the dot colours (a loaded
                          # savestate brings back old memory without telling anyone)
CHAIN_RING     = 1300.0   # distance from the real spot for the later steps of a chain
MARKER_SLOTS   = 4        # table slots kept free for the chapter / saga markers
MARKER_FLAGS, MARKER_TYPE, MARKER_Y, MARKER_RADIUS = 0x1, 2, 100.0, 1000.0
SPOT_GRID      = 500      # search step for a free marker position

DOT_COLORS = {
    "fight":        (1.0, 0.15, 0.15),   # a fight, or a talk scene that runs into one
    "talk":         (0.2, 1.0, 0.2),
    "battle_spot":  (0.2, 0.6, 1.0),
    "dragon_ball":  (1.0, 0.55, 0.0),
    "item":         (1.0, 1.0, 0.2),
    "chapter":      (0.75, 0.2, 1.0),    # next chapter (purple)
    "chapter_back": (1.0, 0.45, 0.75),   # previous chapter (pink)
    "saga":         (1.0, 1.0, 1.0),     # next saga (white)
    "saga_back":    (0.5, 0.5, 0.5),     # previous saga (grey)
    "ending":       (1.0, 1.0, 1.0),     # finish the Dragon Universe (white)
    "other":        (1.0, 1.0, 1.0),
}


def f2w(value) -> int:
    return struct.unpack("<I", struct.pack("<f", float(value)))[0]


def w2f(word: int) -> float:
    return struct.unpack("<f", struct.pack("<I", word))[0]


def is_pointer(value: int) -> bool:
    return 0x00100000 <= value < 0x02000000


def event_name(code: int) -> str:
    return f"{code >> 16}:{code & 0xFFFF}"


def saga_block(char_id: int, saga_byte: int) -> Optional[int]:
    """Which of a character's point lists the saga byte stands for. It is not
    always the saga number: Uub and Broly only have the Buu block, and Vegeta's
    first saga reports 5."""
    if char_id in (0x11, 0x22):
        return 3
    if char_id == 0x07 and saga_byte == 5:
        return 0
    return saga_byte if saga_byte < 4 else None


def is_story_fight(pt) -> bool:
    """A fight the game itself shows on the map: winning it moves the story on."""
    return (pt.fight and pt.next is not None and not pt.flags & 0xC0
            and 5400 <= (pt.code >> 16) < 5800)


def free_spot(points, avoid=()):
    """Spot farthest from every point of the saga (and from `avoid`), inside the
    area the saga's own points cover — the maps are not all the same size."""
    xs, zs = [p.x for p in points], [p.z for p in points]
    taken = list(zip(xs, zs)) + list(avoid)
    cells = [(x, z) for x in range(min(xs), max(xs) + 1, SPOT_GRID)
             for z in range(min(zs), max(zs) + 1, SPOT_GRID)]
    return max(cells, key=lambda c: min((c[0] - x) ** 2 + (c[1] - z) ** 2 for x, z in taken))


SMALL_RADIUS = 500           # the smallest radius that works as the game has it
USUAL_RADIUS = 1000
WORLD_SCENE_DONOR = 0x00     # Goku: his saga-ending scenes all change the world


def previous_saga(sagas: dict, char_id: int, block: int):
    """(marker event, start event of the previous saga, its block), or None.

    A saga's start scene refills the map but does not change the world. Earth
    and Namek only swap in the scenes that END a saga (script tag 0x2F picks the
    world, 0x32 reloads the map): 101 goes to Namek, 103 back to Earth. So when
    the previous saga is on the other world the marker carries one of those, and
    the saga start it queues is replaced by the one wanted.

    A story that ends with the saga in question has that scene without the world
    change (Kid Gohan's ends on Namek: his 103 just plays and stays). The scenes
    are the same for everyone apart from that, so Goku's is used instead."""
    earlier = [b for b in sagas if b < block]
    if not earlier:
        return None
    prev = max(earlier)
    start = ((100 + 2 * prev) << 16) | char_id
    if (prev == 1) == (block == 1):                     # same world
        return start, start, prev
    ending, owner = (101, 0) if prev == 1 else (103, 1)
    goes_on = any(b > owner for b in sagas)             # the story continues after that saga
    return (ending << 16) | (char_id if goes_on else WORLD_SCENE_DONOR), start, prev


def point_radius(pt) -> int:
    """How close the player has to be. Height counts, and one point (a hidden
    spot in Teen Gohan's Cell saga, radius 250 at ground level) is so small
    that flying over it never reaches it: it gets the usual size."""
    return pt.radius if pt.radius >= SMALL_RADIUS else USUAL_RADIUS


def point_words(pt, x, z, place_type=None) -> list:
    """The 16 words of a point table entry, with no capsule or level requirement.
    `place_type` replaces the point's own location type (see MapHelper._label)."""
    return [pt.code, pt.flags, pt.type if place_type is None else place_type,
            f2w(point_radius(pt)), f2w(x), f2w(pt.y), f2w(z),
            0, NONE, 0, 0, NONE, NONE, NONE, 100, 0]


def marker_words(code, x, z, place_type=None) -> list:
    return [code, MARKER_FLAGS, MARKER_TYPE if place_type is None else place_type,
            f2w(MARKER_RADIUS), f2w(x), f2w(MARKER_Y), f2w(z),
            0, NONE, 0, 0, NONE, NONE, NONE, 100, 0]


def saga_byte(char_id: int, block: int) -> int:
    """The saga number the game (and FIGHT_LOCATIONS) uses for a point list:
    the reverse of saga_block."""
    if char_id == 0x11:
        return 4
    if char_id == 0x22 or (char_id == 0x07 and block == 0):
        return 5
    return block


def wanted_points(points, done) -> list:
    """(point, x, z) for everything of `points` that should be on the map now.

    Several events often share one position (steps of a chain, or versions of a
    point for different levels): the first is at the real spot, the later ones
    on a ring around it, each keeping its place as others get done.
    Points that lead to one fight (its versions, and talk scenes that run
    straight into it) are shown as one point: the first that is not done.
    If there are more points than the table holds, later chain steps wait until
    earlier ones are done."""
    hidden, fights = set(done), set()
    for pt in points:
        if pt.code in done or pt.fight_key is None:
            continue
        if pt.fight_key in fights:
            hidden.add(pt.code)                         # the same fight is already on the map
        fights.add(pt.fight_key)
    chains = {}
    for pt in points:
        chains.setdefault((pt.x, pt.z), []).append(pt)
    heads, later = [], []
    for pt in points:
        if pt.code in hidden:
            continue
        chain = chains[(pt.x, pt.z)]
        rank = chain.index(pt)
        if rank == 0:
            heads.append((pt, pt.x, pt.z))
            continue
        angle = 2 * math.pi * (rank - 1) / max(1, len(chain) - 1)
        entry = (pt, pt.x + CHAIN_RING * math.cos(angle), pt.z + CHAIN_RING * math.sin(angle))
        first_open = next(p for p in chain if p.code not in hidden)
        (heads if pt is first_open else later).append(entry)
    return (heads + later)[:MAP_POINT_COUNT - MARKER_SLOTS]


class Saga:
    """One character's saga: its points and how its chapters connect."""

    def __init__(self, char_id: int, block: int, sagas: dict):
        data = sagas[block]
        self.char_id, self.block = char_id, block
        self.key = f"{char_id}:{block}"
        self.points = data["points"]
        self.by_code = {p.code: p for p in self.points}
        self.start = ((100 + 2 * block) << 16) | char_id
        self.chapters = max(p.chapter for p in self.points) + 1
        # scene -> chapter it opens: the scene after each chapter's story fight, plus
        # the scene each marker carries (one that hands control back on the map; the
        # extractor leaves out those that run on into an ending, a saga change or
        # another round of the fight)
        self.chapter_of_scene = {self.start: 0}
        for pt in self.points:
            if is_story_fight(pt) and pt.chapter + 1 < self.chapters:
                self.chapter_of_scene.setdefault(pt.next, pt.chapter + 1)
        self.opening = {0: self.start}
        for chapter, code in data["openers"].items():
            self.opening[chapter] = code
            self.chapter_of_scene[code] = chapter
        self.fight_codes = {p.code for p in self.points
                            if (p.fight or p.starts_fight) and (p.code >> 16) // 100 != 24}
        # points whose fight, once won, ends the saga
        self.enders = set(data.get("enders", ()))
        # saga exit (next saga) and the way back
        marker = data["marker"]
        self.exit = marker[0] if marker else None
        later = [b for b in sagas if b > block]
        self.exit_target = min(later) if marker and later else None
        self.next_spot = (marker[1], marker[2]) if marker else free_spot(self.points)
        self.back_spot = free_spot(self.points, [self.next_spot])
        self.end_spot = free_spot(self.points, [self.next_spot, self.back_spot])
        self.previous = previous_saga(sagas, char_id, block)
        # every code the helper may put on (and so may take off) the map
        self.managed = set(self.by_code) | set(self.opening.values())
        self.managed.update((cls << 16) | char_id for cls in SAGA_EVENT_CLASSES)
        if self.previous:
            self.managed.add(self.previous[0])


class MapHelper:
    def __init__(self, pine, logger: Logger):
        self.pine = pine
        self.logger = logger
        self.enabled = False
        self.free_travel = False      # chapter / saga markers without winning the fights first
        self.saga_locks = False       # moving on to a saga needs its unlock item
        self.unlocked_sagas = set()   # saga blocks (1-3) whose unlock item is held
        self.state_path: Optional[str] = None
        self.labels = True            # redraw the hover label of the nearest point
        self.item_labels = {}         # location name -> (item text, " (player)", importance):
                                      # what is at each open check (filled by the client)
        self.visited = []             # events the player just started (the client turns
                                      # them into Interactsanity checks and empties the list)
        self._sagas = {}
        self.set_version(MAP_HELPER_CRC)
        self._reset_state()
        self._reset_session()
        self._patched = False

    # ── Setup ────────────────────────────────────────────────────────────────

    @staticmethod
    def supported(crc: str) -> bool:
        return (crc or "").lower() in MAP_VERSIONS

    def set_version(self, crc: str):
        """Use the addresses and point lists of the game version `crc` (one that
        supported() accepts)."""
        crc = (crc or "").lower()
        if getattr(self, "crc", None) == crc:
            return
        game = VERSIONS[crc]
        self.crc = crc
        self.v = MAP_VERSIONS[crc]
        self.points = {"MapData": MapData, "MapDataBL": MapDataBL}[self.v["points"]].SAGA_POINTS
        self._addr_mode = game.get("addr_mode", ADDR_MODE)
        self._addr_du_char = game.get("addr_du_char", ADDR_DU_CHAR)
        self._addr_screen = game.get("addr_screen", ADDR_SCREEN)
        self._du_base = {info["du_id"]: info["base"]
                         for info in game.get("du_bases", DU_BASES).values()}
        self._sagas = {}

    def _reset_state(self):
        self.done = {}             # char id -> event codes done
        self.chapter_at = {}       # "char:block" -> chapter shown
        self.reached = {}          # "char:block" -> furthest chapter reached
        self.finished = set()      # "char:block" of sagas whose last fight was won
        self.ending = {}           # char id -> scene that leads to the ending the player earned
        self.current_fight = None  # fight in progress

    def _reset_session(self):
        """What is only known while the player stays in one Dragon Universe session."""
        self._key = None
        self._last_event = None
        self._leaving = False       # a saga marker was used: let the saga change happen
        self._ending_ok = False     # the ending marker was used: let the ending happen
        self._redirect = None       # going back: start event of the previous saga
        self._quiet = 0
        self._after_win = False     # a fight was just won (its scenes may still be running)
        self._map_owned = False     # the map was synced at least once this session
        self._colors = {}           # slot -> colour words last written
        self._colors_at = 0.0
        self._told = None           # last thing logged, so it is only said once
        self._placed = {}           # event -> (x, z, colour name) of what the last sync put on the map
        self._label = None          # the label image in use (see _label_slot)
        self._label_shown = None    # (event, text, colour) drawn into it
        self._label_backup = None   # what the image held before: (words, palette words)

    def load_state(self, path: str):
        self.state_path = path
        self._reset_state()
        try:
            with open(path) as fh:
                saved = json.load(fh)
            self.done = {int(k): set(v) for k, v in saved.get("done", {}).items()}
            self.chapter_at = dict(saved.get("chapter", {}))
            self.reached = dict(saved.get("reached", {}))
            self.finished = set(saved.get("finished", []))
            self.ending = {int(k): v for k, v in saved.get("ending", {}).items()}
            self.current_fight = saved.get("fight")
        except FileNotFoundError:
            pass
        except Exception as e:
            self.logger.warning(f"[B3] Map helper: could not read {path}: {e}")

    def save_state(self):
        if not self.state_path:
            return
        state = {"done": {str(k): sorted(v) for k, v in self.done.items()},
                 "chapter": self.chapter_at, "reached": self.reached,
                 "finished": sorted(self.finished), "fight": self.current_fight,
                 "ending": {str(k): v for k, v in self.ending.items()}}
        try:
            os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
            with open(self.state_path, "w") as fh:
                json.dump(state, fh)
        except Exception as e:
            self.logger.debug(f"[B3] Map helper: could not save state: {e}")

    def _saga(self, char_id: int, block) -> Optional[Saga]:
        sagas = self.points.get(char_id)
        if sagas is None or block not in sagas:
            return None
        if (char_id, block) not in self._sagas:
            self._sagas[(char_id, block)] = Saga(char_id, block, sagas)
        return self._sagas[(char_id, block)]

    def status(self) -> str:
        if not self.enabled:
            return "off"
        if self._key is None:
            return "on (not in Dragon Universe)"
        saga = self._saga(*self._key)
        chapter = min(self.chapter_at.get(saga.key, 0), saga.chapters - 1)
        return (f"on — {SAGA_NAMES[saga.block]} saga, chapter {chapter + 1} of {saga.chapters}, "
                f"{len(self.done.get(saga.char_id, ()))} points done")

    # ── Code patches ─────────────────────────────────────────────────────────

    def _dot_cave(self) -> list:
        """Replaces the overview's dot draw call: copies the slot's colour from
        the table into the dot instance, then tail-calls the real draw."""
        return [
            0x00144100,                                    # sll  t0,s4,4
            0x3C090000 | (self.v["dot_table"] >> 16),       # lui  t1,hi(table)
            0x35290000 | (self.v["dot_table"] & 0xFFFF),    # ori  t1,t1,lo(table)
            0x01094021,                                    # addu t0,t0,t1
            0x8C890030,                                    # lw   t1,0x30(a0)    ; dot instance
            0x8D0A0000, 0xAD2A0050,                        # r -> instance+0x50
            0x8D0A0004, 0xAD2A0054,                        # g -> instance+0x54
            0x8D0A0008,                                    # lw   t2,8(t0)
            0x08000000 | ((self.v["dot_fn"] >> 2) & 0x03FFFFFF),   # j draw
            0xAD2A0058,                                    # b -> instance+0x58 (delay slot)
        ]

    def _apply_patches(self):
        """(Re)write the code patches. Checked on every sync: a loaded savestate
        or a reload puts the original code back."""
        p = self.pine
        cave = self._dot_cave()
        sites = [self.v["patch_marker"], *self.v["patch_minimap"]]
        addrs = ([a for a, _, _ in sites] + [self.v["dot_draw"]]
                 + [self.v["dot_cave"] + 4 * i for i in range(len(cave))])
        now = p.read32_many(addrs)
        for (addr, orig, new), cur in zip(sites, now):
            if cur == orig:
                p.write32(addr, new)
            elif cur != new:
                return False                               # not the code we expect: leave it all alone
        hook = 0x0C000000 | (self.v["dot_cave"] >> 2)       # jal cave
        if now[len(sites)] not in (self.v["orig_dot_draw"], hook):
            return False
        for i, word in enumerate(cave):
            if now[len(sites) + 1 + i] != word:
                p.write32(self.v["dot_cave"] + 4 * i, word)
        if now[len(sites)] != hook:
            p.write32(self.v["dot_draw"], hook)
        self._patched = True
        return True

    def release(self):
        """Put the original code back (leaving Dragon Universe, or helper off).
        The cave sits in memory the game may reuse, so the hook is only kept
        while the map it serves is in use."""
        if not self._patched:
            return
        self._patched = False
        try:
            for addr, orig, new in (self.v["patch_marker"], *self.v["patch_minimap"]):
                if self.pine.read32(addr) == new:
                    self.pine.write32(addr, orig)
            if self.pine.read32(self.v["dot_draw"]) != self.v["orig_dot_draw"]:
                self.pine.write32(self.v["dot_draw"], self.v["orig_dot_draw"])
            self._set_palette(grey=False)
            self._restore_label()
        except Exception:
            pass

    def set_enabled(self, enabled: bool):
        if self.enabled and not enabled:
            self.release()
            self._reset_session()
        self.enabled = enabled

    def _set_palette(self, grey: bool):
        """The dot texture is red; made grey, the per-dot colour tints it."""
        p = self.pine
        hud = p.read32(self.v["hud_ptr"])
        if not is_pointer(hud):
            return
        sheet = p.read32(hud + 0x64)
        if not is_pointer(sheet):
            return
        entry = sheet + p.read32(sheet + 0x20 + 4 * MAP_DOT_TEXTURE)
        palette = sheet + p.read32(entry + 0x24) + 0x20
        if not is_pointer(palette):
            return
        now = p.read32_many([palette + 4 * i for i in range(len(MAP_DOT_PALETTE))])
        for i, (red, cur) in enumerate(zip(MAP_DOT_PALETTE, now)):
            level = red & 0xFF
            tinted = (red & 0xFF000000) | (level << 16) | (level << 8) | level
            have, want = (red, tinted) if grey else (tinted, red)
            if cur == have and have != want:               # only ever touch the palette we know
                p.write32(palette + 4 * i, want)

    def _write_colors(self, kinds: dict):
        """kinds: slot -> colour name for every occupied slot."""
        now = time.monotonic()
        if now - self._colors_at > COLOR_REFRESH:
            self._colors, self._colors_at = {}, now
        for slot, kind in kinds.items():
            words = tuple(f2w(v) for v in DOT_COLORS[kind])
            if self._colors.get(slot) != words:
                for j, word in enumerate(words):
                    self.pine.write32(self.v["dot_table"] + 16 * slot + 4 * j, word)
                self._colors[slot] = words

    # ── Hover labels ─────────────────────────────────────────────────────────
    # The name the game shows for a point is the label image of its location
    # type. Every point the helper places gets one type, the widest label, and
    # that image is redrawn for the point the player is nearest to.

    def _label_slot(self):
        """Find the label image to draw into: dict(type, width, height, data, size,
        palette), or None when no usable sheet is loaded."""
        p = self.pine
        hud = p.read32(self.v["hud_ptr"])
        sheet = p.read32(hud + MAP_HUD_LABELS) if is_pointer(hud) else 0
        if not is_pointer(sheet):
            return None
        if self._label and self._label["sheet"] == sheet:
            return self._label
        count = p.read32(sheet + 0x10)
        if not MAP_LABEL_FIRST < count <= 64:
            return None
        offsets = p.read32_many([sheet + 0x20 + 4 * k for k in range(count)])
        best = None
        for k in range(MAP_LABEL_FIRST, count):
            if not offsets[k]:
                continue
            entry = p.read32_many([sheet + offsets[k] + 4 * i for i in range(12)])
            width, height = entry[4] & 0xFFFF, entry[4] >> 16
            if entry[2] != 0x14 or entry[6] < width * height // 2:    # 16-colour images only
                continue
            if best is None or width > best["width"]:
                best = {"sheet": sheet, "type": k - MAP_LABEL_FIRST, "width": width,
                        "height": height, "data": sheet + entry[5] + 0x20, "size": entry[6],
                        "palette": sheet + entry[9] + 0x20}
        self._label, self._label_shown, self._label_backup = best, None, None
        return best

    def _label_text(self, saga: Saga, code: int, kind: str):
        """(text, player suffix, colour name) for the label of one map point."""
        if kind == "chapter":
            return "Next Chapter", "", "place"
        if kind == "chapter_back":
            return "Previous Chapter", "", "place"
        if kind == "saga":
            return f"Next Saga: {SAGA_NAMES[saga.exit_target]}", "", "place"
        if kind == "saga_back":
            return f"Previous Saga: {SAGA_NAMES[saga.previous[2]]}", "", "place"
        if kind == "ending":
            return "Finish Dragon Universe", "", "place"
        if kind == "dragon_ball":
            # The pickups do not name a ball: the game gives a random missing one
            # each time. The client counts them instead (the n-th ball collected is
            # check #n), so every pickup leads to the same check: the next number.
            balls = self.pine.read8(self._du_base[saga.char_id] + OFFSET_DRAGONBALLS)
            have = bin(balls & 0x7F).count("1")
            if have < 7:
                owner = CHAR_NAMES[saga.char_id].replace("Adult Gohan", "Gohan")
                location = f"Dragon Ball: {owner} #{have + 1}"
                if location in self.item_labels:
                    return self.item_labels[location]
            return "Dragon Ball", "", "place"
        if kind == "battle_spot":
            return "Battle Point", "", "place"
        pt = saga.by_code.get(code)
        if pt is None:
            return "???", "", "place"
        location = INTERACT_BY_EVENT.get(code)
        if pt.fight_key is not None:
            location = FIGHT_LOCATIONS.get((CHAR_NAMES[saga.char_id],
                                            saga_byte(saga.char_id, saga.block),
                                            pt.fight_key & 0xFF))
        if location in self.item_labels:
            return self.item_labels[location]
        return place_name(saga.block, pt.type), "", "place"

    def _update_label(self, saga: Saga, base: int):
        """Draw the label for the point the player is nearest to."""
        label = self._label_slot() if self.labels else None
        if label is None or not self._placed:
            return
        p = self.pine
        px, pz = (struct.unpack("<f", struct.pack("<I", w))[0]
                  for w in p.read32_many([base + MAP_PLAYER_POS, base + MAP_PLAYER_POS + 8]))
        code = min(self._placed, key=lambda c: (self._placed[c][0] - px) ** 2
                                               + (self._placed[c][1] - pz) ** 2)
        text, suffix, colour = self._label_text(saga, code, self._placed[code][2])
        shown = (code, text + suffix, colour)
        palette = B3Labels.palette(B3Labels.INK_COLORS.get(colour, B3Labels.INK_COLORS["place"]))
        now = p.read32_many([label["palette"] + 4 * i for i in range(len(palette))])
        if shown == self._label_shown and now == palette:
            return                                      # already there, and not reloaded since
        words = label["size"] // 4
        addrs = [label["data"] + 4 * i for i in range(words)]
        current = p.read32_many(addrs)
        if now[1] != palette[1] and self._label_backup is None:
            self._label_backup = (current, now)         # the game's own image
        fitted, font = B3Labels.fit(text, suffix, label["width"], label["height"])
        image = B3Labels.pack_4bit(
            B3Labels.render(fitted, font, label["width"], label["height"]), label["size"])
        p.write32_many([(a, w) for a, w, old in zip(addrs, image, current) if w != old]
                       + [(label["palette"] + 4 * i, w) for i, w in enumerate(palette)])
        self._label_shown = shown

    def _restore_label(self):
        """Put the game's own label image back."""
        if self._label and self._label_backup:
            words, palette = self._label_backup
            hud = self.pine.read32(self.v["hud_ptr"])
            if is_pointer(hud) and self.pine.read32(hud + MAP_HUD_LABELS) == self._label["sheet"]:
                self.pine.write32_many(
                    [(self._label["data"] + 4 * i, w) for i, w in enumerate(words)]
                    + [(self._label["palette"] + 4 * i, w) for i, w in enumerate(palette)])
        self._label, self._label_shown, self._label_backup = None, None, None

    # ── The poll ─────────────────────────────────────────────────────────────

    def tick(self):
        """Call on every client poll."""
        if not self.enabled:
            return
        p = self.pine
        if p.read8(self._addr_mode) != DU_MODE:
            if self._key is not None:
                self.release()
                self._reset_session()
            return
        char_id = p.read8(self._addr_du_char)
        du = self._du_base.get(char_id)
        saga = None
        if du is not None:
            saga = self._saga(char_id, saga_block(char_id, p.read8(du + OFFSET_SAGA)))
        if saga is None:
            self._quiet = 0
            return
        key = (char_id, saga.block)
        if key != self._key:
            if self._key is not None and self._key[0] != char_id:
                self._reset_session()                      # another character: a new session
            self._key, self._leaving, self._redirect, self._quiet = key, False, None, 0
            self._ending_ok = False
            self._told = None
            self.logger.info(f"[B3] Map helper: {SAGA_NAMES[saga.block]} saga "
                             f"({len(saga.points)} points, {saga.chapters} chapters)")
        done = self.done.setdefault(char_id, set())
        chapter = min(self.chapter_at.get(saga.key, 0), saga.chapters - 1)
        screen = p.read16(self._addr_screen)
        if screen == SCREEN_RESULTS_WIN:
            self._after_win = True
        elif screen == SCREEN_DU_BATTLE:
            self._after_win = False

        # what is running right now
        task = p.read32(self.v["event_task"])
        event = p.read32(task + 0x14) if is_pointer(task) else None
        if event is not None and event != self._last_event:
            chapter = self._on_event(saga, event, chapter, done)
        self._last_event = event
        self._track_fight(saga, du, screen, event, done)
        self._hold_saga(saga, du, event)

        # own the map, but only once it has been idle for a moment
        if (screen != SCREEN_WORLD_MAP or event is not None or self._leaving
                or p.read32(self.v["event_pending"]) != NONE):      # something is about to run
            self._quiet = 0
            return
        self._quiet += 1
        if self._quiet < SETTLE_TICKS:
            return
        base = p.read32(self.v["map_ptr"])
        if not is_pointer(base):
            return
        if self._quiet % SETTLE_TICKS:
            if self._map_owned:
                self._update_label(saga, base)          # every poll: the player moves
            return
        self._after_win = False
        if not self._apply_patches():
            if self._told != "patch":
                self._told = "patch"
                self.logger.warning("[B3] Map helper: unexpected game code, leaving the map alone.")
            return
        self._sync_map(saga, base + MAP_POINTS_OFF, chapter, done)
        self._map_owned = True
        self._update_label(saga, base)

    def _on_event(self, saga: Saga, event: int, chapter: int, done: set) -> int:
        """A new event started. Returns the chapter to show from now on."""
        char_id = saga.char_id
        pt = saga.by_code.get(event)
        if pt is not None and not pt.fight:
            # A talk scene or a pickup: visiting it is all there is to do. (Fights are
            # done when won, see _track_fight; battle spots are fights and repeatable.)
            self.visited.append(event)
            if event not in done:
                done.add(event)
                self.save_state()
        first_block = min(self.points[char_id])
        exit_shown = saga.exit_target is not None and chapter == saga.chapters - 1
        going_back = (saga.previous and chapter == 0 and event == saga.previous[0]
                      and not (exit_shown and event == saga.exit))
        if (event == ((100 + 2 * first_block) << 16) | char_id and not self._map_owned):
            # The story's first scene, before the helper touched the map this
            # session: a new game. Forget what was done in the last run.
            self.done[char_id] = set()
            done.clear()
            for block in self.points[char_id]:
                k = f"{char_id}:{block}"
                self.chapter_at.pop(k, None)
                self.reached.pop(k, None)
                self.finished.discard(k)
            self.ending.pop(char_id, None)
            self.current_fight = None
            self.save_state()
            self.logger.info("[B3] Map helper: new Dragon Universe run, map progress reset.")
            return 0
        if event == self.ending.get(char_id) and not self._after_win:
            # the ending marker: this time the ending the scene queues goes through
            self._ending_ok = True
            self.logger.info("[B3] Map helper: finishing the Dragon Universe.")
        elif going_back:
            start, prev_block = saga.previous[1], saga.previous[2]
            self._leaving, self._redirect = True, start
            self.chapter_at[f"{char_id}:{prev_block}"] = 0
            self.save_state()
            self.logger.info(f"[B3] Map helper: going back to the {SAGA_NAMES[prev_block]} saga.")
        elif saga.exit is not None and event == saga.exit:
            self._leaving = True
            self.logger.info("[B3] Map helper: moving on to the next saga.")
        elif event in saga.chapter_of_scene:
            chapter = saga.chapter_of_scene[event]
            self.chapter_at[saga.key] = chapter
            self.reached[saga.key] = max(self.reached.get(saga.key, 0), chapter)
            self._quiet = 0
            self.save_state()
            self.logger.info(f"[B3] Map helper: chapter {chapter + 1} of {saga.chapters}.")
        elif pt is not None and pt.fight:
            if pt.next is not None:          # battle spots queue nothing: repeatable, never done
                self.current_fight = event
                self.save_state()
        return chapter

    def _track_fight(self, saga: Saga, du: int, screen: int, event, done: set):
        """Mark a fight done when it is won."""
        if self.current_fight is None and screen == SCREEN_DU_BATTLE:
            # A fight's own event is over too quickly to catch, but the scene it
            # queued stays in the DU struct for the whole battle.
            queued = self.pine.read32(du + OFFSET_EVENT_QUEUED[0])
            self.current_fight = next((pt.code for pt in saga.points
                                       if pt.fight and pt.next == queued), None)
        if self.current_fight is None:
            return
        if screen == SCREEN_RESULTS_WIN:
            # everything that leads to this fight is done together
            won = saga.by_code.get(self.current_fight)
            follow_up = won.next if won else None
            for pt in saga.points:
                if pt.code == self.current_fight or (follow_up is not None
                                                     and pt.fight_key == follow_up):
                    done.add(pt.code)
            self.current_fight = None
            self.save_state()
        elif screen == SCREEN_WORLD_MAP and event is None:
            self.current_fight = None        # lost or backed out: stays on the map
            self.save_state()

    def exit_locked(self, saga: Saga) -> bool:
        return (self.saga_locks and saga.exit_target is not None
                and saga.exit_target not in self.unlocked_sagas)

    def _hold_saga(self, saga: Saga, du: int, event):
        """Keep the player in the saga: a saga change the game queues is taken
        back out, unless a saga marker was used. The saga's own start scene is
        left alone (a new game queues it to set the map up). The story's ending
        is held the same way, until the ending marker is used."""
        p = self.pine
        addrs = [self.v["event_pending"]] + [du + off for off in OFFSET_EVENT_QUEUED]
        for addr, code in zip(addrs, p.read32_many(addrs)):
            if code == NONE:
                continue
            fighting = saga.by_code.get(self.current_fight) if self.current_fight is not None else None
            if fighting is not None and code == fighting.next and not self._after_win:
                # A fight that leads straight to the saga's end (Tien's Nappa,
                # Piccolo's last on Namek) has it queued from the start, and the
                # rest of the client knows the fight by it: it is only taken out
                # once the fight is won. (Only for the fight being fought: the
                # same event queued by a scene after another fight is held as usual.)
                continue
            if (code >> 16) in ENDING_EVENT_CLASSES:
                if self._ending_ok:
                    continue
                p.write32(addr, NONE)
                if event is not None and self.ending.get(saga.char_id) != event:
                    # the scene running now is the one that leads to this ending:
                    # it goes on the map as the ending marker
                    self.ending[saga.char_id] = event
                    self.save_state()
                    self.logger.info("[B3] The story's last fight is won. Take the white marker "
                                     "on the map when you want to finish this Dragon Universe.")
                continue
            if (code >> 16) not in SAGA_EVENT_CLASSES:
                continue
            if self._redirect is not None:
                # going back: whatever saga start gets queued becomes the previous saga's
                if code not in (self._redirect, event):
                    p.write32(addr, self._redirect)
            elif not self._leaving and (code >> 16) != 100 + 2 * saga.block:
                p.write32(addr, NONE)
                if (code >> 16) != 101 + 2 * saga.block:
                    continue          # left over from getting here, not this saga's end
                # Only a scene after the saga's last fight, or that fight itself once
                # won, queues the saga's end: the saga is finished.
                if saga.key not in self.finished:
                    self.finished.add(saga.key)
                    self.save_state()
                if self._told != saga.key:
                    self._told = saga.key
                    if self.exit_locked(saga):
                        self.logger.info(
                            f"[B3] {SAGA_NAMES[saga.block]} saga finished. The next saga is locked: "
                            f"find '{SAGA_UNLOCK_NAMES[saga.exit_target]}'.")
                    else:
                        self.logger.info(
                            f"[B3] {SAGA_NAMES[saga.block]} saga finished. Take the white marker "
                            f"on the map to move on to the next saga.")

    def saga_finished(self, saga: Saga) -> bool:
        """Was the saga's last fight won? Recorded when the game queues the saga's
        end; the fights won say the same, should that have been missed."""
        return (saga.key in self.finished
                or not saga.enders.isdisjoint(self.done.get(saga.char_id, ())))

    def _markers(self, saga: Saga, chapter: int) -> dict:
        """event -> (colour name, x, z) for the chapter and saga markers."""
        markers = {}
        reached = self.reached.get(saga.key, 0)
        if chapter + 1 in saga.opening and (self.free_travel or reached > chapter):
            markers[saga.opening[chapter + 1]] = ("chapter", *saga.next_spot)
        if chapter - 1 in saga.opening:
            markers[saga.opening[chapter - 1]] = ("chapter_back", *saga.back_spot)
        if (saga.exit_target is not None and chapter == saga.chapters - 1 and not self.exit_locked(saga)
                and (self.free_travel or self.saga_finished(saga))):
            markers[saga.exit] = ("saga", *saga.next_spot)
        if saga.previous and chapter == 0:
            markers.setdefault(saga.previous[0], ("saga_back", *saga.back_spot))
        ending = self.ending.get(saga.char_id)
        if ending is not None and (ending >> 16) % 100 == saga.char_id \
                and ((ending >> 16) - 5400) // 100 == saga.block:
            saga.managed.add(ending)
            markers.setdefault(ending, ("ending", *saga.end_spot))
        return markers

    def _kind(self, saga: Saga, markers: dict, code: int, flags: int) -> str:
        if code in markers:
            return markers[code][0]
        block = (code >> 16) // 100 * 100
        if 5400 <= block <= 5700 or code in saga.fight_codes:
            return "fight"
        if 5000 <= block <= 5300:
            return "talk"
        if block == 2400:
            return "battle_spot"
        if 2000 <= block <= 2300:
            return "dragon_ball" if flags & 0x10 else "item"
        return "other"

    def _sync_map(self, saga: Saga, table: int, chapter: int, done: set):
        """Make the point table hold exactly the current chapter and its markers."""
        p = self.pine
        markers = self._markers(saga, chapter)
        label = self._label_slot() if self.labels else None
        place_type = label["type"] if label else None   # one label for all: see _update_label
        want = {pt.code: point_words(pt, x, z, place_type) for pt, x, z in wanted_points(
            [pt for pt in saga.points if pt.chapter == chapter], done)}
        for code, (_, x, z) in markers.items():
            want[code] = marker_words(code, x, z, place_type)
        placed = {code: (w2f(words[4]), w2f(words[6])) for code, words in want.items()}

        slots = [table + i * MAP_POINT_SIZE for i in range(MAP_POINT_COUNT)]
        codes = p.read32_many(slots)
        used = [i for i, code in enumerate(codes) if code not in (0, NONE)]
        fields = p.read32_many([slots[i] + off for i in used
                                for off in (0x04, 0x10, 0x18, MAP_POINT_REQ_CAPSULE,
                                            MAP_POINT_LEVEL_MIN, MAP_POINT_TYPE,
                                            MAP_POINT_REQ_EQUIPPED, 0x0C, MAP_POINT_CONDITION,
                                            MAP_POINT_CONDITION + 4, MAP_POINT_CONDITION + 8)])
        kinds, free, changed = {}, [i for i, code in enumerate(codes) if code in (0, NONE)], 0
        on_map = {}                                         # event -> colour name, for what we placed
        for n, i in enumerate(used):
            code = codes[i]
            flags, x, z, capsule, level_min, place, equipped, radius, *condition = \
                fields[11 * n:11 * n + 11]
            if code in want:
                words = want.pop(code)
                if place != words[2]:
                    p.write32(slots[i] + MAP_POINT_TYPE, words[2])
                if condition != words[8:11]:
                    # A scene can show a point only while a story variable has
                    # some value (Piccolo's two Central City talks: one each way).
                    p.write32_many([(slots[i] + MAP_POINT_CONDITION + 4 * k, words[8 + k])
                                    for k in range(3)])
                    changed += 1
                if radius != words[3]:                      # the game put the point back itself
                    p.write32(slots[i] + 0x0C, words[3])
                    changed += 1
                if capsule != NONE:                         # second-play / capsule lock
                    p.write32(slots[i] + MAP_POINT_REQ_CAPSULE, NONE)
                if equipped != NONE:
                    # A scene can put a point back with a skill that has to be
                    # equipped (Goku's Frieza fight after he turns Super Saiyan):
                    # the point would be hidden, and its other version is merged away.
                    p.write32(slots[i] + MAP_POINT_REQ_EQUIPPED, NONE)
                    changed += 1
                if level_min != NONE:                       # level lock
                    p.write32(slots[i] + MAP_POINT_LEVEL_MIN, NONE)
                    p.write32(slots[i] + MAP_POINT_LEVEL_MIN + 4, 100)
                if (x, z) != (words[4], words[6]):
                    p.write32(slots[i] + 0x10, words[4])
                    p.write32(slots[i] + 0x18, words[6])
                    changed += 1
                kinds[i] = on_map[code] = self._kind(saga, markers, code, flags)
            elif code & ~MAP_POINT_DONE in saga.managed:    # done, another chapter, an old marker
                p.write32(slots[i], NONE)
                free.append(i)
                changed += 1
            else:
                kinds[i] = self._kind(saga, markers, code, flags)
        free.sort()
        for code, words in want.items():
            if not free:
                self.logger.debug("[B3] Map helper: point table full")
                break
            i = free.pop(0)
            for j in range(1, len(words)):
                p.write32(slots[i] + 4 * j, words[j])
            p.write32(slots[i], words[0])                   # event code last: the slot goes live here
            kinds[i] = on_map[code] = self._kind(saga, markers, code, words[1])
            changed += 1
        self._set_palette(grey=True)
        self._write_colors(kinds)
        self._placed = {code: (*placed[code], kind) for code, kind in on_map.items()}
        if changed:
            self.logger.debug(f"[B3] Map helper: map updated ({changed} changes, {len(done)} done)")
