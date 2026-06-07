import logging
from typing import Dict, Any, Mapping
logger = logging.getLogger(__name__)
from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import (item_table, create_item,
                    SAGA_ITEMS, CHARACTER_ITEMS, CAPSULE_ITEMS, TRAP_ITEMS)
from .Locations import location_table, get_location_names, DU_BATTLE_LOCATIONS, SHOP_LOCATIONS, DU_COMPLETION_LOCATIONS
from .Options import B3Options
from .Regions import create_regions, CHARACTER_UNLOCK_ITEMS
from worlds.LauncherComponents import Component, Type, components, launch_subprocess


def run_client():
    from worlds.budokai3.B3Client import launch_client
    launch_subprocess(launch_client, name="B3Client")


components.append(
    Component("Budokai 3 Client", func=run_client, component_type=Type.CLIENT)
)


class B3Web(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Dragon Ball Z Budokai 3 for Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["B3AP"]
    )]


class B3World(World):
    """
    Dragon Ball Z Budokai 3 — fight through Dragon Universe campaigns,
    unlock sagas, and collect capsules in a multiworld randomizer.
    Play as Goku, Vegeta, Piccolo and more across all four sagas.
    """

    game = "Dragon Ball Z Budokai 3"
    item_name_to_id  = {name: code for name, code in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = B3Options
    options: B3Options
    web = B3Web()

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        pool = []

        # Saga unlocks are NOT added to the pool — all sagas are open (the
        # saga items are precollected only, so they'd be useless filler here).

        # Character DU unlocks
        for name in CHARACTER_UNLOCK_ITEMS.values():
            pool.append(create_item(self, name))

        # Shop Restock items — one per 10 shop slots beyond the first 10
        shop_slots = int(self.options.shop_slots.value)
        restock_count = max(0, (shop_slots - 1) // 10)  # slots 11-20 ->1, 21-30 ->2, etc.
        for _ in range(restock_count):
            pool.append(create_item(self, "Shop Restock"))

        # Dragon Arena: ticket + rank ups (one per 10 fights beyond the first 10)
        da_fights = int(self.options.dragon_arena_fights.value)
        if int(self.options.arenasanity.value):
            da_fights = 380
        if da_fights > 0:
            pool.append(create_item(self, "Dragon Arena Ticket"))
            rank_up_count = max(0, (da_fights - 1) // 10)
            for _ in range(rank_up_count):
                pool.append(create_item(self, "Dragon Arena Rank Up"))

        # Add each skill capsule exactly ONCE (unique rewards, not repeated).
        skill_names = [n for n in CAPSULE_ITEMS.keys() if n.startswith("Skill: ")]
        for name in skill_names:
            pool.append(create_item(self, name))

        # Pad any remaining locations with generic filler (Zenie / traps),
        # NOT by repeating skills.
        total_locs  = len(self.multiworld.get_unfilled_locations(self.player))
        needed = max(0, total_locs - len(pool))

        zenie_names = [n for n in CAPSULE_ITEMS.keys() if n.startswith("Zenie")]
        trap_names  = list(TRAP_ITEMS.keys()) if self.options.drain_trap else []
        filler_pool = zenie_names + trap_names
        if not filler_pool:
            filler_pool = zenie_names or ["Zenie x500"]

        for i in range(needed):
            name = filler_pool[i % len(filler_pool)]
            pool.append(create_item(self, name))

        self.multiworld.itempool.extend(pool)

    def set_rules(self):
        # Victory condition: complete/reach the configured number of DU campaigns.
        du_completion_names = list(DU_COMPLETION_LOCATIONS.keys())
        required_du_count = min(
            int(self.options.required_du_completions.value),
            len(du_completion_names),
        )
        self.multiworld.completion_condition[self.player] = lambda state: (
            sum(
                1 for location_name in du_completion_names
                if state.can_reach(location_name, "Location", self.player)
            ) >= required_du_count
        )

    def generate_early(self):
        # Pick a random starting DU character
        all_du_chars = list(CHARACTER_UNLOCK_ITEMS.values())
        starting_char = self.random.choice(all_du_chars)
        self.multiworld.push_precollected(create_item(self, starting_char))
        self.starting_character = starting_char


        # All sagas unlocked from the start (saga lockout not implemented yet)
        self.multiworld.push_precollected(create_item(self, "Frieza Saga Unlock"))
        self.multiworld.push_precollected(create_item(self, "Cell Saga Unlock"))
        self.multiworld.push_precollected(create_item(self, "Buu Saga Unlock"))

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "randomize_fights":   self.options.randomize_fights.value,
            "randomize_player1":  self.options.randomize_player1.value,
            "randomize_player2":  self.options.randomize_player2.value,
            "randomize_stages":   self.options.randomize_stages.value,
            "starting_saga":      self.options.starting_saga.value,
            "shop_slots":         self.options.shop_slots.value,
            "drain_trap":         self.options.drain_trap.value,
            "required_du_completions": self.options.required_du_completions.value,
            "dragon_arena_fights":     self.options.dragon_arena_fights.value,
            "arenasanity":             self.options.arenasanity.value,
            "dragonsanity":            self.options.dragonsanity.value,
            "seed":               self.multiworld.seed_name,
            "starting_character": getattr(self, "starting_character", "Goku DU"),
        }
