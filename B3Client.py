"""
Dragon Ball Z Budokai 3 — Archipelago Client
Connects to PCSX2 via PINE and the AP server simultaneously.

Usage:
  python B3Client.py
  python B3Client.py --connect archipelago.gg:38281 --password mypass
"""
import asyncio
import traceback
import random
from typing import Optional

import Utils
from CommonClient import (
    CommonContext, get_base_parser, server_loop,
    gui_enabled, logger, ClientCommandProcessor,
)
from NetUtils import NetworkItem, ClientStatus

from .B3Interface import B3Interface, build_cave
from .data.Constants import (
    FIGHT_LOCATIONS, ROSTER, STAGES, CAPSULE_SHOP_IDS,
    SAGA_UNLOCK_IDS, DU_BASES,
)


# ─── COMMAND PROCESSOR ───────────────────────────────────────────────────────

class B3CommandProcessor(ClientCommandProcessor):
    def _cmd_status(self):
        """Show connection and game state."""
        ctx: B3Context = self.ctx
        logger.info(f"[B3] Connected to game: {ctx.connected_to_game}")
        logger.info(f"[B3] Connected to server: {ctx.server is not None}")
        logger.info(f"[B3] Cave installed: {ctx.iface.cave_installed()}")
        logger.info(f"[B3] Checks sent: {len(ctx.checked_locations)}")

    def _cmd_cave(self):
        """Reinstall the fight randomization cave."""
        ctx: B3Context = self.ctx
        if not ctx.connected_to_game:
            logger.info("[B3] Not connected to game.")
            return
        ctx.cave_paused = False
        ctx.install_cave()
        logger.info("[B3] Cave reinstalled.")

    def _cmd_restore(self):
        """Remove the code cave and pause auto-reinstall. Use /cave to reinstall."""
        ctx: B3Context = self.ctx
        ctx.iface.restore_original()
        ctx.cave_paused = True
        logger.info("[B3] Cave removed. Use /cave to reinstall.")


# ─── GAME CONTEXT ─────────────────────────────────────────────────────────────

class B3Context(CommonContext):
    command_processor = B3CommandProcessor
    game = "Dragon Ball Z Budokai 3"
    items_handling = 0b111   # receive all items

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.iface = B3Interface(logger)
        self.connected_to_game: bool = False
        self.slot_data: Optional[dict] = None

        # Fight randomization state
        self.matchups: dict = {}       # (char, saga, battle) → {p1,p2,stage_id,drain}
        self.cave_installed: bool = False
        self.cave_paused: bool = False  # set True by /restore to prevent auto-reinstall
        self.unlocked_characters: set = set()  # populated from slot_data on connect
        self._prev_screen_for_locks: int = -1

        self.granted_skills: set = set()  # skills received from AP

        # Shop state
        # The pool of capsules (from slot_data seed) — up to 50, shown 10 at a time
        self.shop_pool: list = []          # list of (display_idx, own_idx, name)
        self.restocks_received: int = 0    # number of "Shop Restock" items received
        self.shop_purchased: set = set()   # pool indices already bought (by position)
        self.shop_checks_sent: set = set() # location names already sent
        self._shop_was_open: bool = False

        # Received items state
        self._received_zenie: int = 0
        self._last_received_index: int = 0

        # DU completion/goal state
        self.completed_dus: set = set()
        self._prev_screen_du_complete: int = -1
        self._goal_sent: bool = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})
            logger.info(f"[B3] Slot data: {self.slot_data}")
            asyncio.create_task(self._on_connected())

    async def _on_connected(self):
        """Called when AP server connection is established."""
        # Set starting character from slot data
        starting = self.slot_data.get("starting_character", "Goku DU") if self.slot_data else "Goku DU"
        char_name = starting[:-3] if starting.endswith(" DU") else starting
        self.unlocked_characters = {char_name}
        logger.info(f"[B3] Starting character: {char_name}")

        if self.connected_to_game:
            logger.info("[B3] AP server connected — building matchups and installing cave...")
            self._build_matchups()
            self._build_shop_pool()
            if not self.iface.any_fight_loading():
                self.install_cave()
            else:
                logger.info("[B3] Fight in progress, cave will install after fight ends.")
            # Install character lock cave
            self.iface.install_cave2()
            # Apply character locks immediately
            self.iface.apply_character_locks(self.unlocked_characters)
            logger.info(f"[B3] Character locks applied. Unlocked: {self.unlocked_characters}")
        else:
            logger.info("[B3] AP server connected. Cave will install when game connects.")

    # ── Item handling ─────────────────────────────────────────────────────────

    def _process_received_items(self):
        """Apply newly received items to the game."""
        if not self.connected_to_game:
            return

        items = self.items_received[self._last_received_index:]
        for item in items:
            name = self.item_names.lookup_in_game(item.item)
            logger.info(f"[B3] Received item: {name}")
            self._apply_item(name)
        self._last_received_index = len(self.items_received)

    def _apply_item(self, name: str):
        """Write the effect of a received item to game memory."""
        if name in SAGA_UNLOCK_IDS:
            # Saga lockout not implemented yet — sagas are always open
            logger.info(f"[B3] Saga item received (no lockout): {name}")

        elif name.endswith(" DU"):
            char = name[:-3]
            self.unlocked_characters.add(char)
            self.iface.show_character(char)
            logger.info(f"[B3] DU unlocked: {char}")

        elif name == "Shop Restock":
            self.restocks_received = min(self.restocks_received + 1, 4)
            logger.info(f"[B3] Shop Restock received! Now {self.restocks_received} restocks "
                        f"({(self.restocks_received + 1) * 10} capsules unlocked)")
            if self.iface.is_shop_open():
                self._refresh_shop()

        elif name.startswith("Skill: "):
            skill_name = name[len("Skill: "):]
            self.granted_skills.add(skill_name)
            self.iface.grant_skill(skill_name)
            logger.info(f"[B3] Skill granted: {skill_name}")

        elif name.startswith("Zenie"):
            amounts = {"Zenie x500": 500, "Zenie x1000": 1000, "Zenie x2000": 2000}
            self.iface.write_zenie(amounts.get(name, 0))

        elif name == "HP Drain Trap":
            # Drain trap is handled per-fight in matchup data
            logger.info("[B3] HP Drain Trap received! Will apply to next fight.")

    # ── Matchup / cave ────────────────────────────────────────────────────────

    def _build_matchups(self):
        """
        Build fight matchups from slot data.
        Respects randomize_fights (master), randomize_player1, randomize_player2.
        """
        seed = self.slot_data.get("seed") if self.slot_data else None
        rng = random.Random(seed)
        roster_names = list(ROSTER.keys())
        stage_ids = list(STAGES.values())
        drain_trap = bool(self.slot_data.get("drain_trap", 0)) if self.slot_data else False
        randomize_stages = bool(self.slot_data.get("randomize_stages", 1)) if self.slot_data else True

        master = bool(self.slot_data.get("randomize_fights", 1)) if self.slot_data else True
        rand_p1 = bool(self.slot_data.get("randomize_player1", 0)) if self.slot_data else False
        rand_p2 = bool(self.slot_data.get("randomize_player2", 1)) if self.slot_data else True
        # Master toggle gates both
        rand_p1 = rand_p1 and master
        rand_p2 = rand_p2 and master

        self.matchups = {}
        for key in FIGHT_LOCATIONS:
            p1_name = rng.choice(roster_names)
            p2_name = rng.choice([n for n in roster_names if n != p1_name])
            p1_char, p1_bt = ROSTER[p1_name]
            p2_char, p2_bt = ROSTER[p2_name]
            stage_id = rng.choice(stage_ids) if randomize_stages else 0x05

            drain = False
            if drain_trap and rng.random() < 0.2:
                drain = True

            self.matchups[key] = {
                "p1": {"char": p1_char, "bt": p1_bt, "name": p1_name},
                "p2": {"char": p2_char, "bt": p2_bt, "name": p2_name},
                "stage_id": stage_id,
                "drain": drain,
                "write_p1": rand_p1,
                "write_p2": rand_p2,
            }

        # If nothing is randomized (no P1, no P2, no stages, no drain), skip cave entirely
        self._cave_needed = rand_p1 or rand_p2 or randomize_stages or drain_trap
        logger.info(f"[B3] Built {len(self.matchups)} matchups "
                    f"(P1={rand_p1}, P2={rand_p2}, stages={randomize_stages})")

    def install_cave(self):
        """Build and install the MIPS code cave."""
        if not self.matchups:
            self._build_matchups()
        # If nothing needs randomizing, don't install the cave at all
        if not getattr(self, "_cave_needed", True):
            logger.info("[B3] No randomization enabled — skipping fight cave.")
            return
        randomize_stages = bool(self.slot_data.get("randomize_stages", 1)) if self.slot_data else True
        cave_code = build_cave(self.matchups, randomize_stages=randomize_stages)
        self.iface.install_cave(cave_code)
        self.cave_installed = self.iface.cave_installed()

    # ── Shop ─────────────────────────────────────────────────────────────────

    def _build_shop_pool(self):
        """Build the shop capsule pool. Uses the FIXED pool order so the AP
        location names (Shop: <capsule>) match the in-game shop slot contents,
        making hints meaningful. No per-seed shuffle — the capsules are just
        AP check triggers, so a fixed order loses nothing."""
        from .data.Constants import SHOP_CAPSULE_POOL
        shop_slots = self.slot_data.get("shop_slots", 50) if self.slot_data else 50
        self.shop_pool = list(SHOP_CAPSULE_POOL)[:shop_slots]
        logger.info(f"[B3] Shop pool built: {len(self.shop_pool)} capsules (fixed order)")

    def _visible_shop_entries(self):
        """
        Return the up-to-10 capsules currently shown in the shop:
        the first 10 unpurchased capsules from the unlocked portion of the pool.
        Unlocked size = (restocks + 1) * 10.
        """
        unlocked_size = (self.restocks_received + 1) * 10
        available = [(i, entry) for i, entry in enumerate(self.shop_pool[:unlocked_size])
                     if i not in self.shop_purchased]
        return available[:10]   # list of (pool_index, (disp, own, name))

    def _refresh_shop(self):
        """Write the current visible shop entries to game memory."""
        visible = self._visible_shop_entries()
        entries = [entry for _i, entry in visible]
        self.iface.write_shop_stock(entries)
        # Remember which pool indices are in which slot for purchase detection
        self._visible_pool_indices = [i for i, _e in visible]

    def _handle_shop(self):
        """
        Detect shop open/refresh and purchases; rotate stock.

        The Skill Shop keeps screen ID 0x0016 but repopulates the item struct
        at 0x0088DCFC with random capsules each time it opens. We detect that
        repopulation (slot 0 display index differs from what we wrote) and
        immediately overwrite with our AP stock.
        """
        if not self.shop_pool:
            return

        on_shop_screen = self.iface.is_shop_open()  # 0x0016 (skill menu/shop)

        if not on_shop_screen:
            self._shop_was_open = False
            self._last_written_slot0 = None
            return

        # Log once when entering shop
        if not self._shop_was_open:
            slot0 = self.iface.read_shop_slot0_display()
            logger.info(f"[B3] Shop screen detected (0x0016). Slot0 display=0x{slot0:X}, "
                        f"pool={len(self.shop_pool)}, restocks={self.restocks_received}")

        # We're on the skill menu/shop screen. Check if the game repopulated
        # the struct with its own random stock (our write got overwritten).
        visible = self._visible_shop_entries()
        if not visible:
            # No capsules left to sell (all bought, awaiting a restock) — empty the shop
            self.iface.clear_shop()
            self._shop_was_open = True
            return

        expected_slot0 = visible[0][1][0]  # display index we want in slot 0
        actual_slot0 = self.iface.read_shop_slot0_display()

        last_written = getattr(self, "_last_written_slot0", None)

        if actual_slot0 != expected_slot0 and actual_slot0 != last_written:
            # Game repopulated the shop — overwrite with our stock
            self._refresh_shop()
            self._last_written_slot0 = expected_slot0

        # Watch for purchases via ownership flips
        vis_indices = getattr(self, "_visible_pool_indices", [])
        for pool_idx in list(vis_indices):
            if pool_idx in self.shop_purchased:
                continue
            _disp, own_idx, name = self.shop_pool[pool_idx]
            if self.iface.read_capsule_owned(own_idx) == 0x01:
                self.iface.clear_capsule_owned(own_idx)
                self.shop_purchased.add(pool_idx)
                loc_name = f"Shop: {name}"
                if loc_name not in self.shop_checks_sent:
                    self.shop_checks_sent.add(loc_name)
                    asyncio.create_task(self._send_check(loc_name))
                    logger.info(f"[B3] Shop purchase: {name} -> {loc_name}")
                self._refresh_shop()
                self._last_written_slot0 = self._visible_shop_entries()[0][1][0] \
                    if self._visible_shop_entries() else None

        self._shop_was_open = True

    async def _send_check(self, location_name: str):
        """Send a location check to the AP server."""
        if not self.server or not self.slot:
            logger.info(f"[B3] Fight complete: {location_name} (not connected to server)")
            return
        # Look up location ID from our location table
        from .Locations import location_table
        loc_id = location_table.get(location_name)
        if loc_id is None:
            logger.warning(f"[B3] Unknown location: {location_name}")
            return
        if loc_id not in self.checked_locations:
            await self.send_msgs([{"cmd": "LocationChecks",
                                   "locations": [loc_id]}])
            logger.info(f"[B3] Check sent: {location_name} (id={loc_id})")
        else:
            logger.info(f"[B3] Already checked: {location_name}")

    async def _handle_du_completion(self, screen: int):
        """Award one check per DU campaign when the game reaches DU Credits."""
        from .data.Constants import SCREEN_DU_CREDITS
        from .Locations import DU_COMPLETION_BY_CHAR_ID

        prev_screen = getattr(self, "_prev_screen_du_complete", -1)
        self._prev_screen_du_complete = screen

        # Only fire on entering credits, not every frame while credits are active.
        if screen != SCREEN_DU_CREDITS or prev_screen == SCREEN_DU_CREDITS:
            return

        char_id = self.iface.get_du_char()
        loc_name = DU_COMPLETION_BY_CHAR_ID.get(char_id)
        if not loc_name:
            logger.warning(f"[B3] DU credits reached for unknown DU char id 0x{char_id:02X}")
            return

        if char_id not in self.completed_dus:
            self.completed_dus.add(char_id)
            logger.info(f"[B3] DU complete: {loc_name} ({len(self.completed_dus)} total)")
            await self._send_check(loc_name)
        else:
            logger.info(f"[B3] DU credits reached again: {loc_name} already counted")

        required = int(self.slot_data.get("required_du_completions", 1)) if self.slot_data else 1
        required = max(1, min(required, 11))
        if not self._goal_sent and len(self.completed_dus) >= required:
            if self.server and self.slot:
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self._goal_sent = True
            logger.info(f"[B3] Goal achieved: {len(self.completed_dus)}/{required} DU completions")


# ─── PCSX2 SYNC TASK ─────────────────────────────────────────────────────────

async def pcsx2_sync_task(ctx: B3Context):
    logger.info("[B3] Starting connector, waiting for PCSX2...")

    while not ctx.exit_event.is_set():
        try:
            if not ctx.iface.is_connected():
                connected = ctx.iface.connect()
                if connected:
                    ctx.connected_to_game = True
                    logger.info("[B3] Connected to game")
                    # Build matchups only if already connected to AP server
                    if ctx.slot_data:
                        ctx._build_matchups()
                        if not ctx.shop_pool:
                            ctx._build_shop_pool()
                        if not ctx.iface.any_fight_loading():
                            ctx.install_cave()
                        # Important: if AP connects before PCSX2, cave2 was never installed.
                        # Install the title/New Game character-lock hook here too.
                        ctx.iface.install_cave2()
                        ctx.iface.apply_character_locks(ctx.unlocked_characters)
                        logger.info(f"[B3] Character locks/cave2 applied on game connect. Unlocked: {ctx.unlocked_characters}")
                    else:
                        logger.info("[B3] Connected to game. Waiting for AP server connection to install cave...")
                    # Check if cave needs reinstall
                else:
                    ctx.connected_to_game = False
                    await asyncio.sleep(3)
                    continue

            # Reinstall cave if it got wiped — only when no fight is loading
            # and randomization is actually enabled
            if (not ctx.iface.cave_installed() and ctx.matchups and not ctx.cave_paused
                    and getattr(ctx, "_cave_needed", True)):
                if not ctx.iface.any_fight_loading():
                    logger.info("[B3] Cave missing, reinstalling...")
                    ctx.install_cave()

            # Reinstall character-lock cave if it got wiped. This is separate from the fight randomizer cave.
            if ctx.slot_data and not ctx.iface.cave2_installed():
                logger.info("[B3] Cave2 missing, reinstalling character-lock hook...")
                ctx.iface.install_cave2()

            # Process received items from server
            ctx._process_received_items()

            screen = ctx.iface.get_screen()

            # DU Credits completion checks / YAML goal count
            await ctx._handle_du_completion(screen)

            # Reapply character locks on key screen transitions:
            # - 0x0004: title screen (save loaded here)
            # - 0x0106: DU title screen (before character select)
            prev_screen_locks = getattr(ctx, '_prev_screen_locks', -1)
            if screen != prev_screen_locks:
                if screen in (0x0004, 0x0106):
                    ctx.iface.apply_character_locks(ctx.unlocked_characters)
                    logger.info(f"[B3] Locks reapplied on screen 0x{screen:04X}")
            ctx._prev_screen_locks = screen

            # Poll for completed fights
            completed = ctx.iface.poll_completed_fights()
            for loc_name in completed:
                await ctx._send_check(loc_name)

            # Reapply character locks periodically (in case game resets them on load)
            if not hasattr(ctx, '_lock_reapply_counter'):
                ctx._lock_reapply_counter = 0
            ctx._lock_reapply_counter += 1
            if ctx._lock_reapply_counter >= 50:  # every ~5 seconds
                ctx._lock_reapply_counter = 0
                ctx.iface.apply_character_locks(ctx.unlocked_characters)
                # Gate skills: only on DU world map (0x0108) or shop (0x0016)
                scr = ctx.iface.get_screen()
                if scr in (0x0108, 0x0016):
                    ctx.iface.apply_skill_locks(ctx.granted_skills)

            # Handle shop
            if ctx.slot_data and not ctx.shop_pool:
                ctx._build_shop_pool()
            ctx._handle_shop()

            await asyncio.sleep(0.1)

        except ConnectionError:
            logger.warning("[B3] Lost connection to PCSX2, retrying...")
            ctx.iface.disconnect()
            ctx.connected_to_game = False
            await asyncio.sleep(3)

        except Exception as e:
            logger.error(f"[B3] Error: {traceback.format_exc()}")
            await asyncio.sleep(1)


# ─── LAUNCHER ────────────────────────────────────────────────────────────────

def launch_client():
    Utils.init_logging("B3Client")

    async def main():
        parser = get_base_parser()
        args = parser.parse_args()
        ctx = B3Context(args.connect, args.password)

        logger.info("[B3] Connecting to AP server...")
        ctx.server_task = asyncio.create_task(
            server_loop(ctx), name="Server Loop"
        )
        ctx.tags.add("Client")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.pcsx2_sync_task = asyncio.create_task(
            pcsx2_sync_task(ctx), name="PCSX2 Sync"
        )

        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await asyncio.sleep(3)
            await ctx.pcsx2_sync_task

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()


if __name__ == "__main__":
    launch_client()
