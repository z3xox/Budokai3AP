import logging
from typing import Dict, Any, Mapping
logger = logging.getLogger(__name__)
from BaseClasses import Item, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import (item_table, create_item, B3Item,
                    CHARACTER_ITEMS, CAPSULE_ITEMS, TRAP_ITEMS)
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

    def create_item(self, name: str) -> B3Item:
        """Create a single item by name. Required as a World METHOD (distinct
        from the module-level helper) because Archipelago core and tools like
        Universal Tracker call multiworld.create_item(name) -> world.create_item.
        Without this override the base World.create_item raises NotImplementedError."""
        return create_item(self, name)

    def create_items(self):
        pool = []

        # Character DU unlocks — skip the starting character (it's precollected,
        # so adding it again would put a duplicate, findable copy in the pool).
        starting = getattr(self, "starting_character", None)
        for name in CHARACTER_UNLOCK_ITEMS.values():
            if name == starting:
                continue
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

        # Add each skill capsule once (guaranteed). A SECOND copy of each is
        # added to the filler pool below, so skills are less rare when there's
        # room, but the extra copies yield to space in tight configs (no
        # overflow). Skills are filler-classified (a 2nd copy just re-grants).
        skill_names = [n for n in CAPSULE_ITEMS.keys() if n.startswith("Skill: ")]
        for name in skill_names:
            pool.append(create_item(self, name))

        # Dark Star Dragon Balls (McGuffin goal items), if the goal uses them.
        from .Items import DARK_STAR_BALL_ITEM
        if int(self.options.goal.value) in (1, 2):  # dark_star or both
            total = int(self.options.dark_star_balls_total.value)
            required = int(self.options.dark_star_balls_required.value)
            total = max(total, required)  # never fewer than required
            for _ in range(total):
                pool.append(create_item(self, DARK_STAR_BALL_ITEM))

        # Pad any remaining locations with generic filler (Zenie / traps),
        # NOT by repeating skills.
        total_locs  = len(self.multiworld.get_unfilled_locations(self.player))
        needed = max(0, total_locs - len(pool))

        zenie_names = [n for n in CAPSULE_ITEMS.keys() if n.startswith("Zenie")]
        trap_names  = list(TRAP_ITEMS.keys()) if self.options.drain_trap else []
        # Item capsules add flavorful variety instead of monotonous Zenie. Each
        # capsule can appear at most once (they're unique unlocks), so draw them
        # WITHOUT replacement; fall back to Zenie once they run out.
        from .Items import ITEM_CAPSULE_ITEMS
        capsule_names = list(ITEM_CAPSULE_ITEMS.keys())
        self.random.shuffle(capsule_names)

        # Second copy of each skill, as FILLER (so skills are less rare). These
        # are consumed first from the filler budget, but only as space allows —
        # in tight configs `needed` is small and they simply don't all fit, so
        # there's no overflow. Shuffled so which skills get a 2nd copy varies.
        extra_skill_copies = list(skill_names)
        self.random.shuffle(extra_skill_copies)

        filler_cycle = zenie_names + trap_names
        if not filler_cycle:
            filler_cycle = zenie_names or ["Zenie x500"]

        for i in range(needed):
            if extra_skill_copies:
                # Place a second skill copy first (skills less rare).
                name = extra_skill_copies.pop()
            elif capsule_names:
                # ~70% capsule, ~30% Zenie/trap while capsules remain
                if self.random.random() < 0.7:
                    name = capsule_names.pop()
                else:
                    name = filler_cycle[i % len(filler_cycle)]
            else:
                name = filler_cycle[i % len(filler_cycle)]
            pool.append(create_item(self, name))

        self.multiworld.itempool.extend(pool)

    def set_rules(self):
        from .Items import DARK_STAR_BALL_ITEM
        # DU completion goal component.
        du_completion_names = list(DU_COMPLETION_LOCATIONS.keys())
        required_du_count = min(
            int(self.options.required_du_completions.value),
            len(du_completion_names),
        )

        def du_goal_met(state):
            return sum(
                1 for location_name in du_completion_names
                if state.can_reach(location_name, "Location", self.player)
            ) >= required_du_count

        def balls_goal_met(state):
            return state.has(DARK_STAR_BALL_ITEM, self.player,
                             int(self.options.dark_star_balls_required.value))

        goal = int(self.options.goal.value)
        if goal == 1:      # dark_star_dragon_balls only
            self.multiworld.completion_condition[self.player] = balls_goal_met
        elif goal == 2:    # both
            self.multiworld.completion_condition[self.player] = (
                lambda state: du_goal_met(state) and balls_goal_met(state))
        else:              # du_completions only
            self.multiworld.completion_condition[self.player] = du_goal_met

    def generate_early(self):
        # Determine the starting DU character. The YAML option lets the player
        # pick a specific one, or use 'random' (the default) to have one chosen
        # per seed. AP resolves 'random' to one of the real option values
        # (0-10) before we read it, so the value directly indexes the DU list.
        # The chosen character is precollected and removed from the item pool
        # (see create_items).
        all_du_chars = list(CHARACTER_UNLOCK_ITEMS.values())  # ["Goku DU", ...]
        idx = int(self.options.starting_character.value)
        if 0 <= idx < len(all_du_chars):
            starting_char = all_du_chars[idx]
        else:
            starting_char = self.random.choice(all_du_chars)
        self.multiworld.push_precollected(create_item(self, starting_char))
        self.starting_character = starting_char


    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "goal":               self.options.goal.value,
            "dark_star_balls_required": self.options.dark_star_balls_required.value,
            "dark_star_balls_total":    self.options.dark_star_balls_total.value,
            "randomize_fights":   self.options.randomize_fights.value,
            "randomize_player1":  self.options.randomize_player1.value,
            "randomize_player2":  self.options.randomize_player2.value,
            "randomize_stages":   self.options.randomize_stages.value,
            "randomize_music":    self.options.randomize_music.value,
            "randomize_transformations": self.options.randomize_transformations.value,
            "shop_slots":         self.options.shop_slots.value,
            "drain_trap":         self.options.drain_trap.value,
            "required_du_completions": self.options.required_du_completions.value,
            "dragon_arena_fights":     self.options.dragon_arena_fights.value,
            "arenasanity":             self.options.arenasanity.value,
            "dragonsanity":            self.options.dragonsanity.value,
            "death_link":              self.options.death_link.value,
            "seed":               self.multiworld.seed_name,
            "starting_character": getattr(self, "starting_character", "Goku DU"),
        }
