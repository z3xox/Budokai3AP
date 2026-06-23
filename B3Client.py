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
from Utils import async_start
from CommonClient import (
    CommonContext, get_base_parser, server_loop,
    gui_enabled, logger, ClientCommandProcessor,
)
from NetUtils import NetworkItem, ClientStatus

from .B3Interface import B3Interface, build_cave
from .data.Constants import (
    FIGHT_LOCATIONS, ROSTER, STAGES, CAPSULE_SHOP_IDS,
    DU_BASES,
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
        self.granted_capsules: set = set()  # item capsules received from AP

        # Dragon Arena state
        self.da_ticket: bool = False         # has Dragon Arena Ticket
        self.da_rank_ups: int = 0            # number of Rank Up items
        self.da_fights_total: int = 0        # configured arena fight count
        self.da_checks_sent: set = set()     # arena fight indices already sent
        self._da_prev_clears: dict = {}      # index -> last clear flag

        # Dragonsanity state
        self.dragonsanity: bool = False
        self._db_prev: dict = {}             # char -> last dragon-ball byte
        self.db_checks_sent: set = set()     # "char#bit" already sent
        self.wish_checks_sent: set = set()   # char already wished

        # DeathLink state
        self.death_link: bool = False
        self._dl_pending_death: bool = False  # incoming death buffered to apply
        self._dl_caused: bool = False         # our loss was caused by incoming DL
        self._dl_killing: bool = False        # actively draining HP to kill self
        self._dl_fight_live: bool = False     # saw a live DU battle this fight
        self._dl_prev_end_hp: int = -1        # last fight_end_hp reading
        self._dl_loss_sent: bool = False      # already sent this fight's loss
        self._dl_win_lock: bool = False       # results-win seen -> no death this fight
        # Arena-specific deathlink state (arena loss = return to list w/o results)
        self._dl_arena_live: bool = False     # saw arena battle (0x0619) this fight
        self._dl_arena_win: bool = False      # saw arena results (0x061A/B) this fight
        self._dl_prev_screen: int = -1        # last screen for transition detection

        # Shop state
        # The pool of capsules (from slot_data seed) — up to 50, shown 10 at a time
        self.shop_pool: list = []          # list of (display_idx, own_idx, name)
        self.restocks_received: int = 0    # number of "Shop Restock" items received
        self.shop_purchased: set = set()   # pool indices already bought (by position)
        self.shop_checks_sent: set = set() # location names already sent
        self._shop_was_open: bool = False
        self._shop_zeni_high = None        # running max Zenie this shop visit (purchase gate)

        # Received items state
        self._received_zenie: int = 0
        self._last_received_index: int = 0

        # DU completion/goal state
        self.completed_dus: set = set()
        self._prev_screen_du_complete: int = -1
        self._goal_sent: bool = False
        self._music_armed: bool = True
        self._randomize_music: bool = False
        self._dark_star_balls_received: int = 0
        self._goal_label = None              # GUI goal-progress label
        self._traps_seen: int = 0            # HP Drain Traps already accounted for (baseline)
        self._traps_baselined: bool = False  # baseline set in _on_connected yet?
        self._pending_drain_traps: int = 0   # traps queued to apply to upcoming fights
        self._drain_armed: bool = True       # re-arm so each fight consumes at most one
        self._drain_active_fight: bool = False  # current fight is dedicated to a drain

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    # ── Goal counts derived from server truth (reconnect-safe) ────────────────
    # We compute these on demand from authoritative server state rather than
    # maintaining running counters. Running counters reset to 0 on reconnect and
    # either lose progress (DU completions) or rely on item replay (which also
    # re-runs cumulative side effects). Deriving from items_received /
    # checked_locations is always correct and immune to reconnects.
    def count_dark_star_balls(self) -> int:
        """Number of Dark Star Dragon Balls received (counted from the server's
        full items_received list, so reconnect-safe and never duplicated)."""
        try:
            from .Items import DARK_STAR_BALL_ITEM
            return sum(1 for it in self.items_received
                       if self.item_names.lookup_in_game(it.item) == DARK_STAR_BALL_ITEM)
        except Exception:
            return 0

    def count_du_completions(self) -> int:
        """Number of completed Dragon Universe campaigns (counted from checked
        DU-completion locations on the server, so reconnect-safe)."""
        try:
            from .Locations import DU_COMPLETION_LOCATIONS
            done_ids = set(DU_COMPLETION_LOCATIONS.values())
            return sum(1 for loc in self.checked_locations if loc in done_ids)
        except Exception:
            return 0

    def count_drain_traps(self) -> int:
        """Total HP Drain Traps received (counted from items_received, so the
        total is always correct and never duplicated on reconnect)."""
        try:
            return sum(1 for it in self.items_received
                       if self.item_names.lookup_in_game(it.item) == "HP Drain Trap")
        except Exception:
            return 0

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Dragon Ball Z Budokai 3 Archipelago Client"
        return ui

    def draw_goal_counter(self):
        """Add/update a small goal-progress label in the client's top connect
        bar (mirrors the Melee/BT2 pattern). Shows progress toward the active
        goal: Dark Star Dragon Balls, DU completions, or both. Best-effort."""
        try:
            if not getattr(self, "ui", None):
                return
            try:
                from kvui import MDLabel as Label
            except ImportError:
                from kvui import Label

            if getattr(self, "_goal_label", None) is None:
                self._goal_label = Label(text="", size_hint_x=None,
                                         width=220, halign="center")
                self.ui.connect_layout.add_widget(self._goal_label)

            sd = self.slot_data or {}
            if not sd:
                self._goal_label.text = ""
                return
            goal = int(sd.get("goal", 0))
            balls_have = self.count_dark_star_balls()
            balls_need = int(sd.get("dark_star_balls_required", 7))
            du_have = self.count_du_completions()
            du_need = max(1, min(int(sd.get("required_du_completions", 1)), 11))

            if goal == 1:        # dark_star_dragon_balls
                self._goal_label.text = f"Dark Star Balls: {balls_have}/{balls_need}"
            elif goal == 2:      # both
                self._goal_label.text = (
                    f"Balls {balls_have}/{balls_need}  DU {du_have}/{du_need}")
            else:                # du_completions
                self._goal_label.text = f"DU Completions: {du_have}/{du_need}"
        except Exception:
            pass

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})
            logger.info(f"[B3] Slot data: {self.slot_data}")
            asyncio.create_task(self._on_connected())
        elif cmd == "RoomUpdate":
            # checked_locations is only updated once the server echoes our
            # LocationChecks (not at send time). The DU-completion goal counts
            # from checked_locations, so we must re-evaluate the goal here, after
            # the echo lands — otherwise the final DU completion never triggers
            # the goal (it was counted one short at send time). Dark Star Balls
            # don't hit this because they count from items_received.
            asyncio.create_task(self._maybe_send_goal())

    def on_deathlink(self, data: dict):
        """Incoming DeathLink: buffer a death to apply to the current/next DU
        battle (the watcher applies it by draining HP)."""
        super().on_deathlink(data)
        self._dl_pending_death = True

    def _handle_deathlink(self):
        """Run every poll. Outgoing: detect our loss (fight-end HP cleared to 0
        while we stayed in DU battle, i.e. NOT the win results screen) and send a
        death. Incoming: drain HP persistently so the AI finishes us. Buffered
        until we're in a TRULY-LIVE DU battle (HP initialized); anti-chain so a
        death we were handed doesn't echo back out."""
        if not self.death_link:
            return
        # Skip if this game version doesn't have DeathLink addresses mapped.
        if not getattr(self.iface, "_deathlink_supported", False):
            return
        try:
            screen = self.iface.get_screen()
        except Exception:
            return
        in_battle = (screen == 0x0109)   # SCREEN_DU_BATTLE
        on_win = (screen == 0x010A)      # SCREEN_RESULTS_WIN

        # ── Arena outgoing detection ─────────────────────────────────────────
        # Arena has clean, distinct screens (no in-place retry popup like DU):
        #   0x0619 BATTLE -> WIN goes to 0x061A/0x061B (results/save), LOSS goes
        #   straight back to 0x0618 (opponent list). So an arena loss is a real
        #   screen transition we can catch: we were in an arena battle, then
        #   returned to the list (or entrance) without ever hitting results.
        arena_battle = (screen == 0x0619)        # SCREEN_DA_BATTLE
        arena_results = screen in (0x061A, 0x061B)  # results / save (a WIN)
        arena_list = screen in (0x0617, 0x0618)  # entrance / opponent list
        prev_screen = self._dl_prev_screen
        self._dl_prev_screen = screen

        if arena_battle:
            self._dl_arena_live = True
        if arena_results:
            self._dl_arena_win = True
        # Arena fight just ENDED if we were in arena battle last poll and now we
        # are not (and not loading into results). Decide win vs loss:
        if self._dl_arena_live and not arena_battle and (arena_list or arena_results):
            if arena_results or self._dl_arena_win:
                pass  # arena WIN -> no death
            elif not self._dl_loss_sent:
                # arena LOSS -> back to list without results
                self._dl_loss_sent = True
                if self._dl_caused:
                    self._dl_caused = False
                else:
                    async_start(self.send_death(
                        f"{self.player_names.get(self.slot, 'Player')} lost in the Dragon Arena."))
            # reset arena per-fight state once we are back on the list
            if arena_list:
                self._dl_arena_live = False
                self._dl_arena_win = False
                self._dl_loss_sent = False
                self._dl_killing = False
                self._dl_caused = False

        # Read the fight-end HP marker. NOTE: the DU battle screen (0x0109) shows
        # DURING THE LOAD, before the fight starts and before HP is initialized.
        # At fight start HP loads to a real nonzero value (~max); during load it
        # is 0; on death it clears to 0. So a fight is only TRULY LIVE when we're
        # on the battle screen AND HP has initialized (end_hp != 0). This avoids
        # draining/killing during the load window.
        try:
            end_hp = self.iface.fight_end_hp()
        except Exception:
            end_hp = -1
        prev_end = self._dl_prev_end_hp
        self._dl_prev_end_hp = end_hp

        hp_initialized = (end_hp not in (0, -1))
        truly_live = in_battle and hp_initialized

        # NEW-ATTEMPT edge: end_hp goes 0 (dead/ended) -> nonzero (a fresh fight
        # attempt has initialized). This fires on a Continue/Retry too, where the
        # screen STAYS on 0x0109 and the leave-battle reset never happens. Without
        # this, _dl_loss_sent/_dl_win_lock stay stale and a second genuine loss in
        # the same fight would be wrongly suppressed.
        new_attempt = (hp_initialized and prev_end in (0, -1))
        if new_attempt:
            self._dl_loss_sent = False
            self._dl_win_lock = False
            # Only clear the anti-chain flag if we're NOT mid-kill; a kill in
            # progress keeps _dl_caused so its resulting loss is suppressed.
            if not self._dl_killing:
                self._dl_caused = False

        # Per-fight tracking. "Live" requires HP initialized, not just the screen.
        # Leaving the battle (and not on the win screen) resets for next fight.
        if truly_live:
            self._dl_fight_live = True
        elif not on_win and not in_battle:
            # back on map/menu/charsel -> reset for next fight
            self._dl_fight_live = False
            self._dl_loss_sent = False
            self._dl_win_lock = False
            self._dl_killing = False
            self._dl_caused = False

        # Win lockout: if we ever hit the win results screen this fight, no death
        # may fire (mirrors BT2 victory-lock).
        if on_win:
            self._dl_win_lock = True

        # OUTGOING: a fresh transition of end_hp -> 0 AFTER the fight went live
        # (so the load-window 0 doesn't count), while we did NOT see the win
        # screen = our loss. Send once. Anti-chain: a loss we caused via an
        # incoming DeathLink doesn't echo back out.
        fresh_end = (end_hp == 0 and prev_end not in (0, -1))
        if (self._dl_fight_live and fresh_end and not self._dl_win_lock
                and not self._dl_loss_sent):
            self._dl_loss_sent = True
            if self._dl_caused:
                self._dl_caused = False           # suppress echo
            else:
                async_start(self.send_death(
                    f"{self.player_names.get(self.slot, 'Player')} was defeated in battle."))

        # INCOMING: apply a buffered death once the fight is TRULY LIVE. For DU
        # that means the battle screen + HP initialized; for arena it means the
        # arena battle screen (0x0619). Drain HP persistently (the AI finishes
        # us). Tag the loss as caused so it won't echo.
        incoming_live = truly_live or arena_battle
        if self._dl_pending_death and incoming_live:
            self._dl_killing = True
            self._dl_pending_death = False
            self._dl_caused = True
        if self._dl_killing:
            if (in_battle and end_hp != 0) or arena_battle:
                self.iface.kill_player()          # pin HP low; AI finishes us
            else:
                self._dl_killing = False          # fight ended / left battle

    async def _on_connected(self):
        """Called when AP server connection is established."""
        # Set starting character from slot data
        starting = self.slot_data.get("starting_character", "Goku DU") if self.slot_data else "Goku DU"
        char_name = starting[:-3] if starting.endswith(" DU") else starting
        self.unlocked_characters = {char_name}
        logger.info(f"[B3] Starting character: {char_name}")

        # Note: DU completion and Dark Star Ball goal progress are derived on
        # demand from the server's checked_locations / items_received (see
        # count_du_completions / count_dark_star_balls), so there is nothing to
        # restore here — they are always correct across reconnects.

        # HP Drain Trap baseline: traps already received before this session are
        # considered accounted-for (we can't know which were already applied to
        # fights, so we don't re-apply them — avoids dumping a stack of drains on
        # reconnect). Only traps that arrive AFTER connect queue for the next
        # fight. (Traps are filler; skipping a few received while offline is far
        # better than duplicating them.)
        self._traps_seen = self.count_drain_traps()
        self._pending_drain_traps = 0
        self._traps_baselined = True

        # Dragon Arena config
        self.da_fights_total = int(self.slot_data.get("dragon_arena_fights", 0)) if self.slot_data else 0
        if self.slot_data and int(self.slot_data.get("arenasanity", 0)):
            self.da_fights_total = 380
        self.dragonsanity = bool(self.slot_data.get("dragonsanity", 0)) if self.slot_data else False

        # DeathLink
        self.death_link = bool(self.slot_data.get("death_link", 0)) if self.slot_data else False
        if self.death_link:
            async_start(self.update_death_link(True))
            logger.info("[B3] DeathLink enabled.")

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
        if name == "Dark Star Dragon Ball":
            # No counter to maintain — the goal derives the count directly from
            # items_received (reconnect-safe). Just re-check the goal.
            logger.info("[B3] Dark Star Dragon Ball received "
                        f"({self.count_dark_star_balls()} total)")
            asyncio.create_task(self._maybe_send_goal())
            return

        if name.endswith(" DU"):
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
                # Hint the newly-revealed capsules
                asyncio.create_task(self._hint_shop_items())

        elif name.startswith("Skill: "):
            skill_name = name[len("Skill: "):]
            self.granted_skills.add(skill_name)
            self.iface.grant_skill(skill_name)
            logger.info(f"[B3] Skill granted: {skill_name}")

        elif name.startswith("Capsule: "):
            capsule_name = name[len("Capsule: "):]
            self.granted_capsules.add(capsule_name)
            self.iface.grant_item_capsule(capsule_name)
            logger.info(f"[B3] Capsule granted: {capsule_name}")

        elif name == "Dragon Arena Ticket":
            self.da_ticket = True
            self.iface.unlock_dragon_arena()
            logger.info("[B3] Dragon Arena Ticket received — mode unlocked.")

        elif name == "Dragon Arena Rank Up":
            self.da_rank_ups += 1
            logger.info(f"[B3] Dragon Arena Rank Up! Now {self.da_rank_ups} "
                        f"({(self.da_rank_ups + 1) * 10} fights available)")

        elif name.startswith("Zenie"):
            amounts = {"Zenie x500": 500, "Zenie x1000": 1000, "Zenie x2000": 2000}
            self.iface.write_zenie(amounts.get(name, 0))

        elif name == "HP Drain Trap":
            # No per-item increment (that would re-queue every trap on reconnect
            # when items replay). The pending count is derived: total HP Drain
            # Traps received minus how many we've already applied to fights. See
            # _service_drain_trap.
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
        randomize_music = bool(self.slot_data.get("randomize_music", 0)) if self.slot_data else False
        from .data.Constants import MUSIC_TRACKS

        master = bool(self.slot_data.get("randomize_fights", 1)) if self.slot_data else True
        rand_p1 = bool(self.slot_data.get("randomize_player1", 0)) if self.slot_data else False
        rand_p2 = bool(self.slot_data.get("randomize_player2", 1)) if self.slot_data else True
        rand_xform = bool(self.slot_data.get("randomize_transformations", 0)) if self.slot_data else False
        # Master toggle gates both
        rand_p1 = rand_p1 and master
        rand_p2 = rand_p2 and master

        from .data.Constants import TRANSFORMATIONS

        def pick_form(char_name):
            """Pick a random valid form for a character (0 = base included)."""
            if not rand_xform:
                return 0
            # ROSTER "Adult Gohan" maps to TRANSFORMATIONS "Gohan"
            key = "Gohan" if char_name == "Adult Gohan" else char_name
            entry = TRANSFORMATIONS.get(key)
            if not entry:
                return 0
            _cid, forms = entry
            # Pool = base (0) + all valid form indices
            pool = [0] + list(forms.keys())
            return rng.choice(pool)

        self.matchups = {}
        for key in FIGHT_LOCATIONS:
            p1_name = rng.choice(roster_names)
            p2_name = rng.choice([n for n in roster_names if n != p1_name])
            p1_char, p1_bt = ROSTER[p1_name]
            p2_char, p2_bt = ROSTER[p2_name]
            stage_id = rng.choice(stage_ids) if randomize_stages else 0x05
            music = rng.choice(MUSIC_TRACKS) if randomize_music else None

            p1_form = pick_form(p1_name) if rand_p1 else 0
            p2_form = pick_form(p2_name) if rand_p2 else 0

            # HP Drain is NO LONGER pre-scattered here. It is an Archipelago TRAP
            # item: when an "HP Drain Trap" is received, it is applied to the next
            # fight via the polling path (_service_drain_trap). So matchups never
            # carry a static drain flag.
            drain = False

            self.matchups[key] = {
                "p1": {"char": p1_char, "bt": p1_bt, "name": p1_name, "form": p1_form},
                "p2": {"char": p2_char, "bt": p2_bt, "name": p2_name, "form": p2_form},
                "stage_id": stage_id,
                "music": music,
                "drain": drain,
                "write_p1": rand_p1,
                "write_p2": rand_p2,
            }

        # If nothing is randomized (no P1, no P2, no stages, no music), skip cave
        # entirely. Drain is no longer cave-based (it's a polling trap), so it no
        # longer forces the cave on.
        self._cave_needed = rand_p1 or rand_p2 or randomize_stages or randomize_music
        self._randomize_music = randomize_music
        logger.info(f"[B3] Built {len(self.matchups)} matchups "
                    f"(P1={rand_p1}, P2={rand_p2}, stages={randomize_stages}, music={randomize_music})")

    def install_cave(self):
        """Build and install the MIPS code cave."""
        if not self.matchups:
            self._build_matchups()
        # If nothing needs randomizing, don't install the cave at all
        if not getattr(self, "_cave_needed", True):
            logger.info("[B3] No randomization enabled — skipping fight cave.")
            return
        randomize_stages = bool(self.slot_data.get("randomize_stages", 1)) if self.slot_data else True
        # NTSC-U bakes the music write into the cave; BL writes it via polling.
        music_in_cave = (getattr(self, "_randomize_music", False)
                         and self.iface.music_cave_supported())
        cave_code = build_cave(self.matchups, randomize_stages=randomize_stages,
                               music_in_cave=music_in_cave)
        self.iface.install_cave(cave_code)
        self.cave_installed = self.iface.cave_installed()

    def _service_music(self):
        """BL music-write path. On NTSC-U the music is baked into the cave, so
        this is a no-op there. On BL the cave1 intercept fires too early for
        music; instead we write the upcoming fight's track the moment the battle
        becomes active.

        Timing matters: the battle music is loaded DURING the load, before the
        DU-battle screen settles. Writing on screen==0x0109 is too late (it ends
        up changing the NEXT/post-fight track). The reliable trigger — the same
        one the battle detector uses — is the battle field at base+OFFSET_BATTLE
        transitioning from idle (0xFF) to a real battle id (non-0xFF / non-0x00).
        We write once on that transition and re-arm when it returns to idle.
        """
        if not getattr(self, "_randomize_music", False):
            return
        if self.iface.music_cave_supported():
            return  # NTSC-U: handled in the cave
        if not self.iface.in_du():
            self._music_armed = True
            return

        active = self.iface.get_active_du_char_name()
        if not active:
            return
        battle = self.iface.get_battle_state(active) & 0xFF
        idle = battle in (0xFF, 0x00)

        if idle:
            # Between fights: re-arm so the next fight gets its music written.
            self._music_armed = True
            return

        # Battle field is active. Write on the transition, then re-assert for a
        # short window to cover the race where the game loads its own track just
        # after the field flips (a single early write can otherwise be clobbered).
        if getattr(self, "_music_armed", True):
            saga = self.iface.get_saga(active)
            key = (active, saga, battle)
            mu = self.matchups.get(key)
            track = mu.get("music") if mu else None
            if track is not None:
                self.iface.write_music(track)
                self._music_track_pending = track
                self._music_reassert = 5   # re-write on the next few polls too
                logger.info(f"[B3] Music track {track} written for {key}")
            else:
                self._music_track_pending = None
                self._music_reassert = 0
            self._music_armed = False
        elif getattr(self, "_music_reassert", 0) > 0 and \
                getattr(self, "_music_track_pending", None) is not None:
            self.iface.write_music(self._music_track_pending)
            self._music_reassert -= 1

    def _service_drain_trap(self):
        """Apply received HP Drain Traps to upcoming fights. Runs every poll.

        New traps are detected by comparing the current total (counted from
        items_received) against a baseline set at connect, so a reconnect never
        re-applies old traps. When a trap is pending and a fight starts, we
        dedicate that trap to THIS fight and then re-assert the HP-drain battle
        modifier every poll until the fight ends — the game reads 0x44B708
        continuously, and a single write at the fight-load transition gets
        overwritten during init, so it must be held for the fight's duration."""
        # don't act until the connect baseline is set, or we'd treat all
        # previously-received traps as new on the first poll.
        if not getattr(self, "_traps_baselined", False):
            return
        # pick up any newly-arrived traps since the baseline
        total = self.count_drain_traps()
        if total > self._traps_seen:
            self._pending_drain_traps += (total - self._traps_seen)
            self._traps_seen = total
            logger.info(f"[B3] HP Drain Trap queued "
                        f"({self._pending_drain_traps} pending).")

        try:
            screen = self.iface.get_screen()
        except Exception:
            return
        # "In a real fight" = the DU battle screen specifically (0x0109). Using
        # the raw battle_state instead would also be true during character
        # select / fight setup, which would consume a trap before the actual
        # fight. The DeathLink path uses this same screen gate.
        in_fight = (screen == 0x0109)   # SCREEN_DU_BATTLE

        if not in_fight:
            # not in an actual fight (char select, results, map, load) — clear
            # the per-fight drain and re-arm for the next real fight
            self._drain_active_fight = False
            self._drain_armed = True
            return

        # A fight is active. If a trap is pending and this fight isn't already
        # dedicated to a drain, consume one trap for it.
        if not getattr(self, "_drain_active_fight", False):
            if self._pending_drain_traps > 0 and getattr(self, "_drain_armed", True):
                self._pending_drain_traps -= 1
                self._drain_active_fight = True
                self._drain_armed = False
                logger.info(f"[B3] HP Drain Trap applied to this fight "
                            f"({self._pending_drain_traps} pending).")

        # While this fight is drained, RE-ASSERT the modifier every poll so it
        # sticks through init overwrites and for the whole fight.
        if getattr(self, "_drain_active_fight", False):
            self.iface.write_battle_mod(0x00020003)   # HP drain

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

    def _handle_dragonsanity(self):
        """Detect Dragon Ball collection (bit flips) and Shenron wishes.

        Guarded so it never fires on garbage reads (e.g. during game shutdown
        or outside Dragon Universe): only runs while in DU, rejects invalid
        bytes (valid = 0x00-0x7F, only bits 0-6), and only accepts a value once
        we've seen it stable.
        """
        if not self.dragonsanity:
            return

        # Only operate inside Dragon Universe. Outside DU (incl. shutdown /
        # menu teardown) these addresses hold stale/garbage data.
        if not self.iface.in_du():
            return

        from .data.Constants import DRAGON_BALL_ADDRS
        # Dragon Balls: watch each character's bitfield for bits going 0->1.
        self._db_scan_counter = getattr(self, "_db_scan_counter", 0) + 1
        if self._db_scan_counter >= 10:
            self._db_scan_counter = 0
            for ch in DRAGON_BALL_ADDRS:
                cur = self.iface.read_dragon_ball_byte(ch)
                # Reject invalid/garbage reads: valid Dragon Ball byte uses only
                # bits 0-6 (0x00-0x7F). Anything else (0xFF, high bit set) is
                # garbage — skip without updating prev so we don't latch it.
                if cur < 0 or cur > 0x7F:
                    continue
                prev = self._db_prev.get(ch, None)
                # On first valid sight, just record it — do NOT fire (avoids
                # mass-firing if the first read happens to have bits set from a
                # save already in progress; pre-collected balls are rare and not
                # worth the false-positive risk on shutdown).
                if prev is None:
                    self._db_prev[ch] = cur
                    continue
                for bit in range(7):
                    mask = 1 << bit
                    key = f"{ch}#{bit}"
                    if key in self.db_checks_sent:
                        continue
                    now_set = bool(cur & mask)
                    was_set = bool(prev & mask)
                    if now_set and not was_set:  # genuine 0->1 we observed
                        self.db_checks_sent.add(key)
                        loc_name = f"Dragon Ball: {ch} #{bit + 1}"
                        asyncio.create_task(self._send_check(loc_name))
                        logger.info(f"[B3] {loc_name}")
                self._db_prev[ch] = cur

        # Wishes: fire when on the Shenron summon screen, for the ACTIVE DU
        # character (not based on having all balls). One wish per character.
        if self.iface.get_screen() == 0x010B:  # SCREEN_SHENRON
            active = self.iface.get_active_du_char_name()
            if active:
                loc_char = "Gohan" if active == "Adult Gohan" else active
                if loc_char not in self.wish_checks_sent:
                    self.wish_checks_sent.add(loc_char)
                    loc_name = f"Wish: {loc_char}"
                    asyncio.create_task(self._send_check(loc_name))
                    logger.info(f"[B3] {loc_name}")

    def _handle_dragon_arena(self):
        """Gate the arena opponent list and detect fight wins.

        Conservative about WHEN it touches memory: the arena list struct is torn
        down when a fight starts, so writing the clamp during that transition can
        crash the emulator. We clamp ONLY on the stable list screen (0x0618) and
        detect wins ONLY on the results/save screens (0x061A/0x061B) — never
        during the battle-load transition (0x0619) or entrance (0x0617).
        """
        if self.da_fights_total <= 0:
            return

        screen = self.iface.get_screen()

        # Clamp the visible opponent count — ONLY on the stable list screen, and
        # only after it has been stable for a few polls. The arena list struct is
        # torn down when a fight starts; for a frame or two the screen still reads
        # 0x0618 while the struct is half-freed. A scan/write landing in that
        # window crashes PCSX2. To avoid it we: (1) require the list screen to be
        # stable for several consecutive polls (skip the just-entered / about-to-
        # leave frames), (2) reuse the cached count address instead of forcing a
        # fresh full scan every poll, and (3) read the current count first and
        # only write when it actually exceeds the allowed value.
        prev_da_screen = getattr(self, "_prev_da_screen", -1)
        if screen == 0x0618:
            if prev_da_screen != 0x0618:
                # Just entered the list screen: invalidate cache ONCE so the next
                # stable poll does a fresh lookup, and start the settle counter.
                self.iface._da_count_cache = None
                self._da_list_settle = 0
            else:
                self._da_list_settle = getattr(self, "_da_list_settle", 0) + 1
            # Only touch memory once the list has clearly settled (not the entry
            # frame, not the teardown frame).
            if getattr(self, "_da_list_settle", 0) >= 3:
                allowed = min((self.da_rank_ups + 1) * 10, self.da_fights_total)
                self.iface.clamp_da_opponent_count(allowed)
        else:
            self._da_list_settle = 0
        self._prev_da_screen = screen

        # Win detection — ONLY on results/save screens, never during the battle
        # load. Throttled to ~once per second (380 flag reads is expensive).
        if screen in (0x061A, 0x061B):  # results or post-battle save
            self._da_scan_counter = getattr(self, "_da_scan_counter", 0) + 1
            if self._da_scan_counter >= 10:  # every ~1 second at 0.1s poll
                self._da_scan_counter = 0
                for idx in range(self.da_fights_total):
                    if idx in self.da_checks_sent:
                        continue
                    flag = self.iface.read_da_clear_flag(idx)
                    prev = self._da_prev_clears.get(idx, None)
                    # Fire if newly cleared (0->1) OR already cleared on first sight
                    if flag == 1 and (prev is None or prev == 0):
                        self.da_checks_sent.add(idx)
                        loc_name = f"Dragon Arena Fight {idx + 1}"
                        asyncio.create_task(self._send_check(loc_name))
                        logger.info(f"[B3] Dragon Arena win: {loc_name}")
                    self._da_prev_clears[idx] = flag

    def _handle_shop(self):
        """
        Detect shop open/refresh and purchases; rotate stock.

        The Skill Shop struct is allocated dynamically and relocates after other
        menus load. We locate it via the 'ess_shop.c' anchor. We only act when
        that anchor is present (find_shop_base != None) — this both finds the
        right address after relocation AND prevents writing into other menus
        that share screen 0x0016 (which caused the black-screen hang).
        """
        if not self.shop_pool:
            return

        on_shop_screen = self.iface.is_shop_open()  # 0x0016 (skill menu/shop)
        if not on_shop_screen:
            self._shop_was_open = False
            self._last_written_slot0 = None
            self._shop_qty_baseline = None
            self._shop_zeni_high = None
            return

        # Confirm the REAL shop is loaded by locating its anchor. If not found,
        # this 0x0016 screen is some other menu — do nothing (no corruption).
        shop_base = self.iface.find_shop_base()
        if shop_base is None:
            self._shop_was_open = False
            self._last_written_slot0 = None
            return

        # Log once when entering shop, and force a rewrite on fresh entry
        if not self._shop_was_open:
            slot0 = self.iface.read_shop_slot0_display()
            logger.info(f"[B3] Shop detected (ess_shop.c @ 0x{shop_base:X}). "
                        f"Slot0=0x{slot0:X}, pool={len(self.shop_pool)}, "
                        f"restocks={self.restocks_received}")
            self._last_written_slot0 = None
            visible = self._visible_shop_entries()
            # Capture the qty baseline RIGHT NOW, before any purchase detection,
            # snapshotting whatever the current capsule inventory is. This
            # absorbs any bulk writes from edit-capsule menus or a save that
            # happened while we were off the shop screen, so re-entering the
            # shop never mistakes an already-populated inventory for purchases.
            self._visible_pool_indices = [i for i, _e in visible]
            base_snapshot = {}
            for i in self._visible_pool_indices:
                disp_idx, own_idx, _ = self.shop_pool[i]
                base_snapshot[i] = self.iface.read_capsule_owned(own_idx, disp_idx)
            self._shop_qty_baseline = base_snapshot
            _z = self.iface.read_zenie_rt()
            self._shop_zeni_high = _z if _z >= 0 else None
            if visible:
                self._refresh_shop()
                self._last_written_slot0 = visible[0][1][0]
                self._shop_was_open = True
                # Hint the capsules now for sale so the player knows the stock
                self._last_hinted_count = len(visible)
                asyncio.create_task(self._hint_shop_items())
                return
            else:
                self.iface.clear_shop()
                self._shop_was_open = True
                return

        # We're on the skill menu/shop screen. Check if the game repopulated
        # the struct with its own random stock (our write got overwritten).
        visible = self._visible_shop_entries()
        if not visible:
            # No AP capsules available (all bought, waiting for restock).
            # Keep clearing every poll so the game can't repopulate with its
            # own stock after re-entry or relocation.
            self.iface.clear_shop()
            self._shop_was_open = True
            return

        expected_slot0 = visible[0][1][0]  # display index we want in slot 0
        actual_slot0 = self.iface.read_shop_slot0_display()

        # Watch for purchases via ownership flips — do this BEFORE re-asserting
        # stock, otherwise we rewrite the just-bought item back into the shop
        # before recording the purchase (causes an infinite restock loop).
        # Watch for purchases. In BL the purchase table is the general capsule
        # quantity inventory, so a non-zero value can mean "already owned from
        # normal play", not "just bought". We therefore track a per-visit
        # baseline and only fire when the quantity INCREASES above it.
        vis_indices = getattr(self, "_visible_pool_indices", [])
        baseline = getattr(self, "_shop_qty_baseline", None)
        if baseline is None:
            baseline = {}
            for i in vis_indices:
                disp_idx, own_idx, _ = self.shop_pool[i]
                baseline[i] = self.iface.read_capsule_owned(own_idx, disp_idx)
            self._shop_qty_baseline = baseline

        # Positive purchase evidence: a real shop purchase DEDUCTS Zenie.
        # Saving and editing/equipping capsules do NOT. But Zenie can also
        # INCREASE mid-shop (the player spawns money, or receives a Zenie AP
        # item while the shop is open), so a fixed entry snapshot is wrong. We
        # instead track the running MAXIMUM Zenie seen during this visit and
        # treat a value BELOW that peak as spending. Increases just raise the
        # peak; a drop below it is a real purchase.
        zeni_now = self.iface.read_zenie_rt()
        zeni_high = getattr(self, "_shop_zeni_high", None)
        if zeni_now >= 0:
            if zeni_high is None or zeni_now > zeni_high:
                zeni_high = zeni_now
                self._shop_zeni_high = zeni_high
        zeni_spent = (
            zeni_high is not None and zeni_now >= 0 and zeni_now < zeni_high
        )

        # Collect every visible slot whose owned-quantity rose above baseline.
        increased = []
        for pool_idx in list(vis_indices):
            if pool_idx in self.shop_purchased:
                continue
            disp_idx, own_idx, name = self.shop_pool[pool_idx]
            cur = self.iface.read_capsule_owned(own_idx, disp_idx)
            base = baseline.get(pool_idx, 0)
            if cur > base:
                increased.append((pool_idx, disp_idx, own_idx, name, base, cur))

        purchase_made = False
        # Non-purchase bulk write if NO Zenie was spent (current not below the
        # visit peak), OR more than one slot changed, OR a slot jumped by >1.
        bulk_write = (
            not zeni_spent or
            len(increased) > 1 or
            any((cur - base) > 1 for _, _, _, _, base, cur in increased)
        )
        if increased and bulk_write:
            for pool_idx, _disp, _own, _name, _base, cur in increased:
                baseline[pool_idx] = cur
            self._shop_qty_baseline = baseline
            logger.info(f"[B3] Ignored capsule-inventory change "
                        f"({len(increased)} slot(s), zeni_spent={zeni_spent}, "
                        f"zeni_high={zeni_high}, zeni_now={zeni_now}) "
                        f"— not a purchase.")
        else:
            for pool_idx, disp_idx, own_idx, name, base, cur in increased:
                logger.info(f"[B3] Shop purchase detected: {name} "
                            f"(disp={disp_idx}, {base}->{cur}, "
                            f"zeni {zeni_high}->{zeni_now})")
                self.iface.clear_capsule_owned(own_idx, disp_idx)
                self.shop_purchased.add(pool_idx)
                baseline[pool_idx] = 0
                # Reset the peak to the current Zenie so the NEXT purchase needs
                # a fresh drop (otherwise every poll after one buy looks spent).
                if zeni_now >= 0:
                    self._shop_zeni_high = zeni_now
                    zeni_high = zeni_now
                purchase_made = True
                loc_name = f"Shop: {name}"
                if loc_name not in self.shop_checks_sent:
                    self.shop_checks_sent.add(loc_name)
                    asyncio.create_task(self._send_check(loc_name))
                    logger.info(f"[B3] Shop check sent: {name} -> {loc_name}")
        # Recompute visible after recording purchases so re-assert uses fresh set
        visible = self._visible_shop_entries()
        if not visible:
            self.iface.clear_shop()
            self._shop_was_open = True
            return
        expected_slot0 = visible[0][1][0]

        # Re-assert our stock whenever slot0 doesn't match what we expect,
        # OR whenever slot0 isn't any of our pool's display indices (meaning the
        # game repopulated with its own stock — e.g. after World Tournament),
        # OR right after a purchase (the game auto-refills emptied slots from
        # its native stock, which we must overwrite with our reduced set).
        our_display_set = {e[0] for _i, e in
                           [(i, self.shop_pool[i]) for i in range(len(self.shop_pool))]}
        if (purchase_made or actual_slot0 != expected_slot0
                or actual_slot0 not in our_display_set):
            self._refresh_shop()
            self._last_written_slot0 = expected_slot0

        # Re-hint if the number of visible capsules grew (e.g. a Shop Restock
        # arrived). Re-sending is safe — the server skips existing hints.
        last_hinted_count = getattr(self, "_last_hinted_count", 0)
        if len(visible) > last_hinted_count:
            self._last_hinted_count = len(visible)
            asyncio.create_task(self._hint_shop_items())

        self._shop_was_open = True
        return

    async def _hint_shop_items(self):
        """Create AP hints for the capsules currently for sale, so the player
        sees what each shop location contains. Re-sending is safe: the server
        silently skips hints that already exist, so this reliably covers items
        newly revealed by a Shop Restock without duplicating existing hints."""
        if not self.server or not self.slot:
            return
        from .Locations import location_table
        visible = self._visible_shop_entries()
        loc_ids = []
        for _pool_idx, entry in visible:
            disp_idx, own_idx, name = entry
            loc_name = f"Shop: {name}"
            loc_id = location_table.get(loc_name)
            if loc_id is not None and loc_id not in self.checked_locations:
                loc_ids.append(loc_id)
        if loc_ids:
            await self.send_msgs([{"cmd": "LocationScouts",
                                   "locations": loc_ids,
                                   "create_as_hint": 2}])
            logger.info(f"[B3] Sent/refreshed {len(loc_ids)} shop hints.")

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

        # Dedupe against the server's checked_locations (reconnect-safe) rather
        # than an in-memory set, so a reconnect doesn't re-send and the goal
        # count (derived from checked_locations) stays correct.
        from .Locations import DU_COMPLETION_LOCATIONS
        loc_id = DU_COMPLETION_LOCATIONS.get(loc_name)
        if loc_id is not None and loc_id not in self.checked_locations:
            logger.info(f"[B3] DU complete: {loc_name}")
            await self._send_check(loc_name)
        else:
            logger.info(f"[B3] DU credits reached again: {loc_name} already counted")

        await self._maybe_send_goal()

    async def _maybe_send_goal(self):
        """Goal-aware victory check: DU completions, Dark Star Dragon Balls, or
        both, per the 'goal' slot_data option."""
        if self._goal_sent or not (self.server and self.slot):
            return
        sd = self.slot_data or {}
        goal = int(sd.get("goal", 0))

        required_du = max(1, min(int(sd.get("required_du_completions", 1)), 11))
        du_ok = self.count_du_completions() >= required_du

        balls_required = int(sd.get("dark_star_balls_required", 7))
        balls_have = self.count_dark_star_balls()
        balls_ok = balls_have >= balls_required

        if goal == 1:        # dark_star_dragon_balls
            met = balls_ok
        elif goal == 2:      # both
            met = du_ok and balls_ok
        else:                # du_completions
            met = du_ok

        if met:
            await self.send_msgs([{"cmd": "StatusUpdate",
                                   "status": ClientStatus.CLIENT_GOAL}])
            self._goal_sent = True
            logger.info(f"[B3] Goal achieved (goal={goal}).")


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
                        # Install cave2 only when past title screen (screen != 0)
                        # to avoid crashing on BL where the intercept fires during init.
                        screen = ctx.iface.get_screen()
                        if screen != 0:
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

            # Reinstall character-lock cave if it got wiped. Skip on title screen (screen=0).
            if ctx.slot_data and not ctx.iface.cave2_installed() and ctx.iface.get_screen() != 0:
                logger.info("[B3] Cave2 missing, reinstalling character-lock hook...")
                ctx.iface.install_cave2()

            # Process received items from server
            ctx._process_received_items()

            # Update the GUI goal-progress label (best-effort).
            ctx.draw_goal_counter()

            screen = ctx.iface.get_screen()

            # DeathLink — run every poll, independent of other handlers, since it
            # only needs screen + HP. Wrapped so a transient read error can't
            # break the cycle.
            if ctx.death_link:
                try:
                    ctx._handle_deathlink()
                except Exception as e:
                    logger.debug(f"[B3] deathlink error: {e}")

            # DU Credits completion checks / YAML goal count
            await ctx._handle_du_completion(screen)

            # During the credits/completion screen (0x010C) the game performs a
            # heavy full-save. Suspend our memory writes here so a PINE write
            # can't land mid-save and corrupt game state. Detection (reads) and
            # server comms continue normally; we resume writes once off-screen.
            if screen == 0x010C:
                await asyncio.sleep(0.1)
                continue

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

            # BL music-write path (no-op on NTSC-U / when music randomization off)
            ctx._service_music()

            # HP Drain Trap: apply a received trap to the next fight
            ctx._service_drain_trap()

            # Start with Dragon Radar: grant the radar to the active DU character
            if ctx.slot_data and ctx.slot_data.get("start_with_dragon_radar", 1):
                try:
                    if ctx.iface.in_du() and ctx.iface.grant_dragon_radar():
                        logger.debug("[B3] Dragon Radar granted to active DU character")
                except Exception as e:
                    logger.debug(f"[B3] radar grant error: {e}")

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
                    # Re-assert received item capsules (load can reset RT flags)
                    for cap in ctx.granted_capsules:
                        ctx.iface.grant_item_capsule(cap)
                    # Maintain Dragon Arena ticket lock state
                    if ctx.da_fights_total > 0:
                        if ctx.da_ticket:
                            ctx.iface.unlock_dragon_arena()
                        else:
                            ctx.iface.lock_dragon_arena()

            # Reapply character locks immediately on arena charsel screen
            # transition — the arena char-select re-initializes capsule display
            # bytes on entry, temporarily showing all characters as unlocked.
            _prev_arena_scr = getattr(ctx, "_prev_arena_charsel", False)
            _on_arena_charsel = (ctx.iface.get_screen() == 0x0618)
            if _on_arena_charsel and not _prev_arena_scr:
                ctx.iface.apply_character_locks(ctx.unlocked_characters)
                # Invalidate arena count cache so a fresh scan happens
                ctx.iface._da_count_cache = None
            ctx._prev_arena_charsel = _on_arena_charsel

            # Handle shop — on transition TO the shop screen, immediately
            # write our stock/clear BEFORE _handle_shop runs to win the race
            # against the game's own shop-init routine.
            if ctx.slot_data and not ctx.shop_pool:
                ctx._build_shop_pool()
            _prev_shop_screen = getattr(ctx, "_prev_shop_screen", False)
            _on_shop = ctx.iface.is_shop_open()
            if _on_shop and not _prev_shop_screen:
                # Transition: just entered shop screen. Fire immediately.
                visible = ctx._visible_shop_entries()
                if visible:
                    ctx.iface.write_shop_stock([e for _, e in visible])
                else:
                    ctx.iface.clear_shop()
            ctx._prev_shop_screen = _on_shop
            ctx._handle_shop()

            # Handle Dragon Arena
            ctx._handle_dragon_arena()

            # Handle Dragonsanity (Dragon Balls + Wishes)
            ctx._handle_dragonsanity()

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
