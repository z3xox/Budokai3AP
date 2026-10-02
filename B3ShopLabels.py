"""
B3ShopLabels — shows Archipelago item names in the Skill Shop's list.

The shop's capsules are stand-ins: buying one sends a check. The game draws a
capsule's name from a sheet of small images, one per capsule (two sheets are
loaded: one for the list, one for the highlighted row). Those images are as wide
as the capsule's own name, often too narrow for an item name, so for each
capsule on sale the client

  * picks a wide name image the shop does not show (a "donor"),
  * draws the item name into it (see B3Labels), and
  * points the capsule's entry in the sheet at the donor's image.

The sheets move: each time the shop is entered the game may load them somewhere
else, and the old copies stay in memory looking just the same. So the sheets are
never searched for by their looks. The game's own table of loaded files says
where each one is now and whether it has finished loading; only those are
touched. Everything is put back when the shop is left, if they are still loaded.
"""
from logging import Logger

from . import B3Labels
from .data.Constants import (
    MAP_HELPER_CRC, MAP_VERSIONS, FILE_TABLE_ENTRIES, FILE_ENTRY_SIZE, FILE_ENTRY_POINTER,
    FILE_ENTRY_STATE, FILE_LOADED,
)

AMT_MAGICS = (0x544D4123, 0x544D4121)        # '#AMT' as stored, '!AMT' once loaded
MIN_NAMES = 500                              # a capsule name sheet holds ~579 images
TABLE = 0x20                                 # sheet: offset table of its images' entries
ENTRY_WORDS = 12                             # image entry: [2] format, [4] width | height << 16,
                                             # [5] pixel data, [6] its size, [9] palette (offsets)
SAMPLES = 12                                 # drawn words checked per name to see it is still there


def is_pointer(value: int) -> bool:
    return 0x00100000 <= value < 0x02000000


class Sheet:
    """One loaded capsule name sheet and what was done to it."""

    def __init__(self, addr: int, count: int, offsets: list, widths: list):
        self.addr, self.count = addr, count
        self.offsets = offsets     # each image's entry offset, as the game loaded it
        self.widths = widths
        self.applied = None        # what is drawn: tuple of (capsule, text, suffix, colour)
        self.redirected = {}       # capsule -> donor it points at
        self.drawn = {}            # capsule -> [(address, word)] samples of what was drawn
        self.written = {}          # donor -> the words drawn into it last
        self.backup = {}           # donor -> [(address, word)]: the donor's own name


class ShopLabels:
    def __init__(self, pine, logger: Logger):
        self.pine = pine
        self.logger = logger
        self.enabled = True
        self._sheets = {}          # address -> Sheet
        self.set_version(MAP_HELPER_CRC)

    @staticmethod
    def supported(crc: str) -> bool:
        return (crc or "").lower() in MAP_VERSIONS

    def set_version(self, crc: str):
        """Use the file table and file numbers of the game version `crc`."""
        version = MAP_VERSIONS[(crc or "").lower()]
        self._table_ptr = version["file_table_ptr"]
        self._name_files = version["shop_name_files"]

    # ── Finding the sheets ───────────────────────────────────────────────────

    def _loaded_sheets(self) -> list:
        """Addresses of the capsule name sheets the game has finished loading."""
        table = self.pine.read32(self._table_ptr)
        if not is_pointer(table):
            return []
        addrs = list(range(table, table + FILE_TABLE_ENTRIES * FILE_ENTRY_SIZE, 4))
        words = self.pine.read32_many(addrs)
        pointer, state = FILE_ENTRY_POINTER // 4, FILE_ENTRY_STATE // 4
        found = []
        for i in range(1, len(words) - state):
            if (words[i] in self._name_files and words[i - 1] == 1     # an entry in use
                    and words[i + state] == FILE_LOADED and is_pointer(words[i + pointer])):
                found.append(words[i + pointer])
        return found

    def _open_sheet(self, addr: int):
        p = self.pine
        head = p.read32_many([addr, addr + 0x10])
        if head[0] not in AMT_MAGICS or not MIN_NAMES <= head[1] <= 1000:
            return None
        offsets = p.read32_many([addr + TABLE + 4 * k for k in range(head[1])])
        if any(o and not 0 < o < 0x00400000 for o in offsets):
            return None
        sizes = p.read32_many([addr + o + 0x10 for o in offsets])
        return Sheet(addr, head[1], offsets, [s & 0xFFFF for s in sizes])

    # ── Drawing ──────────────────────────────────────────────────────────────

    def update(self, wanted: list, reserved: set):
        """Call on every poll while the shop is open.

        wanted:   [(capsule display id, item text, player suffix, colour name)] for
                  the capsules on sale, in list order
        reserved: display ids that must not be used as donors (the whole shop pool)
        """
        if not self.enabled:
            return
        loaded = self._loaded_sheets()
        for addr in list(self._sheets):
            if addr not in loaded:
                del self._sheets[addr]                   # freed or moved: nothing to put back
        for addr in loaded:
            if addr not in self._sheets:
                sheet = self._open_sheet(addr)
                if sheet:
                    self._sheets[addr] = sheet
        state = tuple(wanted)
        for sheet in self._sheets.values():
            if sheet.applied != state:
                self._apply(sheet, wanted, reserved)
                self.logger.debug(f"[B3] Shop labels: {len(wanted)} name(s) drawn "
                                  f"in the sheet at 0x{sheet.addr:08X}")
            elif not self._intact(sheet):
                self._apply(sheet, wanted, reserved)     # the game wrote over them: draw again

    def _intact(self, sheet: Sheet) -> bool:
        """Do the capsules on sale still point at their donors, and do the donors
        still hold what was drawn?"""
        capsules = list(sheet.redirected)
        if not capsules:
            return True
        now = self.pine.read32_many([sheet.addr + TABLE + 4 * c for c in capsules])
        if any(cur != sheet.offsets[sheet.redirected[c]] for cur, c in zip(now, capsules)):
            return False
        samples = [pair for c in capsules for pair in sheet.drawn.get(c, [])]
        now = self.pine.read32_many([a for a, _ in samples])
        return all(cur == word for cur, (_, word) in zip(now, samples))

    def _apply(self, sheet: Sheet, wanted: list, reserved: set):
        """Draw every name on sale into its donor and point the capsule at it. A
        capsule that is no longer on sale gets its own name back; the others are
        never switched back in between, so nothing flickers."""
        taken = reserved | {capsule for capsule, _, _, _ in wanted}
        donors = sorted((k for k in range(sheet.count) if k not in taken and sheet.offsets[k]),
                        key=lambda k: -sheet.widths[k])
        on_sale = set()
        for (capsule, text, suffix, colour), donor in zip(wanted, donors):
            if capsule < sheet.count and self._draw(sheet, capsule, donor, text, suffix, colour):
                on_sale.add(capsule)
        gone = [c for c in sheet.redirected if c not in on_sale]
        self.pine.write32_many([(sheet.addr + TABLE + 4 * c, sheet.offsets[c]) for c in gone])
        for capsule in gone:
            del sheet.redirected[capsule]
            sheet.drawn.pop(capsule, None)
        sheet.applied = tuple(wanted)

    def _draw(self, sheet: Sheet, capsule: int, donor: int, text: str, suffix: str,
              colour: str) -> bool:
        p = self.pine
        addr = sheet.addr
        entry = p.read32_many([addr + sheet.offsets[donor] + 4 * i for i in range(ENTRY_WORDS)])
        fmt, width, height = entry[2], entry[4] & 0xFFFF, entry[4] >> 16
        data, size, palette = addr + entry[5] + 0x20, entry[6], addr + entry[9] + 0x20
        if fmt not in (0x13, 0x14) or not is_pointer(data) or not is_pointer(palette):
            return False
        fitted, font = B3Labels.fit(text, suffix, width, height)
        px = B3Labels.render(fitted, font, width, height, align="left")
        if fmt == 0x13:                                  # 256 colours
            words = B3Labels.pack_8bit(px, size)
            slots = [B3Labels.palette_slot_8bit(i) for i in range(B3Labels.PALETTE_SIZE)]
        else:                                            # 16 colours
            words = B3Labels.pack_4bit(px, size)
            slots = list(range(B3Labels.PALETTE_SIZE))
        colours = B3Labels.palette(B3Labels.INK_COLORS.get(colour, B3Labels.INK_COLORS["plain"]))
        writes = ([(data + 4 * i, w) for i, w in enumerate(words)]
                  + [(palette + 4 * s, w) for s, w in zip(slots, colours)])
        # Keep the donor's own name to put back later. What is there now is the
        # game's unless it is exactly what we drew last time.
        addrs = [a for a, _ in writes]
        current = p.read32_many(addrs)
        if current != sheet.written.get(donor):
            sheet.backup[donor] = list(zip(addrs, current))
        sheet.written[donor] = [w for _, w in writes]
        p.write32_many([pair for pair, old in zip(writes, current) if pair[1] != old])
        inked = [pair for pair in writes[:len(words)] if pair[1]]
        sheet.drawn[capsule] = inked[::max(1, len(inked) // SAMPLES)][:SAMPLES] + writes[len(words):]
        sheet.redirected[capsule] = donor
        p.write32(addr + TABLE + 4 * capsule, sheet.offsets[donor])
        return True

    # ── Putting things back ──────────────────────────────────────────────────

    def close(self):
        """The shop was left: restore the names in the sheets that are still loaded."""
        if not self._sheets:
            return
        try:
            loaded = self._loaded_sheets()
            for addr, sheet in self._sheets.items():
                if addr not in loaded:
                    continue
                self.pine.write32_many([(addr + TABLE + 4 * c, sheet.offsets[c])
                                        for c in sheet.redirected])
                for writes in sheet.backup.values():
                    self.pine.write32_many(writes)
        except Exception as e:
            self.logger.debug(f"[B3] Shop labels: could not restore names: {e}")
        self._sheets = {}
