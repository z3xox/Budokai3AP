from BaseClasses import Region, MultiWorld
from .data.MapLocations import INTERACT_KIND, INTERACT_REGION
from .Locations import (
    B3Location,
    DU_BATTLE_LOCATIONS,
    DU_BATTLE_LOCATIONS_MAP_HELPER,
    INTERACT_LOCATIONS,
    SHOP_LOCATIONS,
    DU_COMPLETION_LOCATIONS,
    DRAGON_ARENA_LOCATIONS,
    DRAGON_BALL_LOCATIONS,
    WISH_LOCATIONS,
)

# DU characters and which saga unlocks gate their later fights.
# Format: character_name -> { saga_name -> [location names in that saga] }
DU_CHARACTER_SAGAS = {
    "Goku": {
        "Saiyan":  ["Goku DU - Raditz", "Goku DU - Nappa", "Goku DU - Vegeta"],
        "Frieza":  ["Goku DU - Recoome", "Goku DU - Ginyu",
                    "Goku DU - Frieza Final Form", "Goku DU - Frieza 100%"],
        "Cell":    ["Goku DU - Perfect Cell"],
        "Buu":     ["Goku DU - Majin Vegeta", "Goku DU - Majin Buu",
                    "Goku DU - Vegito vs Buuhan", "Goku DU - Super Buu (Inside Buu)",
                    "Goku DU - Kid Buu"],
    },
    "Kid Gohan": {
        "Saiyan":  ["Kid Gohan DU - Piccolo", "Kid Gohan DU - Saibaman",
                    "Kid Gohan DU - Nappa"],
        "Frieza":  ["Kid Gohan DU - Recoome", "Kid Gohan DU - Frieza 3rd Form"],
    },
    "Teen Gohan": {
        "Cell":    ["Teen Gohan DU - Piccolo", "Teen Gohan DU - Krillin",
                    "Teen Gohan DU - Goku", "Teen Gohan DU - Perfect Cell",
                    "Teen Gohan DU - Super Perfect Cell"],
    },
    "Adult Gohan": {
        "Buu":     ["Adult Gohan DU - Goten", "Adult Gohan DU - Videl",
                    "Adult Gohan DU - Dabura", "Adult Gohan DU - Majin Buu",
                    "Adult Gohan DU - Super Buu"],
    },
    "Vegeta": {
        "Saiyan":  ["Vegeta DU - Goku", "Vegeta DU - Kid Gohan"],
        "Frieza":  ["Vegeta DU - Recoome", "Vegeta DU - Frieza 1st Form",
                    "Vegeta DU - Frieza Final Form", "Vegeta DU - Cooler"],
        "Cell":    ["Vegeta DU - Android 17", "Vegeta DU - Android 18",
                    "Vegeta DU - Semi-Perfect Cell", "Vegeta DU - Perfect Cell"],
        "Buu":     ["Vegeta DU - Goku (SS2)", "Vegeta DU - Majin Buu",
                    "Vegeta DU - Super Buu (Gohan Absorbed)",
                    "Vegeta DU - Super Buu (Gohan Absorbed) [Supreme Kai]",
                    "Vegeta DU - Super Buu (Inside Buu)",
                    "Vegeta DU - Super Buu (Inside Buu) [Supreme Kai]",
                    "Vegeta DU - Kid Buu", "Vegeta DU - Broly",
                    "Vegeta DU - Broly [Goku Friendship]",
                    "Vegeta DU - Gotenks (SS)", "Vegeta DU - Goku (SS4)"],
    },
    "Krillin": {
        "Saiyan":  ["Krillin DU - Nappa", "Krillin DU - Saibaman"],
        "Frieza":  ["Krillin DU - Recoome", "Krillin DU - Ginyu as Goku",
                    "Krillin DU - Frieza 2nd Form", "Krillin DU - Frieza Final Form",
                    "Krillin DU - Frieza Final Form (Ginyu)"],
        "Cell":    ["Krillin DU - Perfect Cell"],
    },
    "Piccolo": {
        "Saiyan":  ["Piccolo DU - Raditz (SBC)", "Piccolo DU - Kid Gohan",
                    "Piccolo DU - Saibamen", "Piccolo DU - Goku",
                    "Piccolo DU - Nappa", "Piccolo DU - Vegeta",
                    "Piccolo DU - Raditz (Kame House)"],
        "Frieza":  ["Piccolo DU - Frieza 2nd Form", "Piccolo DU - Frieza 3rd Form",
                    "Piccolo DU - Frieza Final Form", "Piccolo DU - Cooler",
                    "Piccolo DU - Metal Cooler"],
        "Cell":    ["Piccolo DU - Dr. Gero", "Piccolo DU - Imperfect Cell",
                    "Piccolo DU - Imperfect Cell (Baba)", "Piccolo DU - Perfect Cell",
                    "Piccolo DU - Android 17"],
        "Buu":     ["Piccolo DU - Dabura", "Piccolo DU - Super Buu",
                    "Piccolo DU - Broly"],
    },
    "Tien": {
        "Saiyan":  ["Tien DU - Saibamen", "Tien DU - Nappa"],
        "Cell":    ["Tien DU - Semi-Perfect Cell", "Tien DU - Cell Jr."],
        "Buu":     ["Tien DU - Super Buu (Gotenks)", "Tien DU - Super Buu (Gotenks/Chiaotzu)",
                    "Tien DU - Yamcha"],
    },
    "Yamcha": {
        "Saiyan":  ["Yamcha DU - Saibamen"],
        "Cell":    ["Yamcha DU - Dr. Gero"],
        "Buu":     ["Yamcha DU - Tien", "Yamcha DU - Vegeta"],
    },
    "Uub": {
        "Buu":     ["Uub DU - Goku (WT)", "Uub DU - Majin Buu",
                    "Uub DU - Vegeta & Goku", "Uub DU - Goku (Roshi)",
                    "Uub DU - Omega Shenron"],
    },
    "Broly": {
        "Buu":     ["Broly DU - Videl", "Broly DU - Kid Trunks",
                    "Broly DU - Goten", "Broly DU - Gohan",
                    "Broly DU - Gohan (WT post-game)", "Broly DU - Gohan (Rematch)",
                    "Broly DU - Goku"],
    },
}


# Extra fights that are only locations with the map helper on (same layout).
DU_CHARACTER_SAGAS_MAP_HELPER = {
    "Goku": {
        "Saiyan":  ["Goku DU - Tien (World Tournament)"],
        "Frieza":  ["Goku DU - Cooler", "Goku DU - Vegeta (Namek)", "Goku DU - Metal Cooler",
                    "Goku DU - Cooler (Rematch)", "Goku DU - Frieza Final Form (Cooler Route)"],
        "Buu":     ["Goku DU - Uub", "Goku DU - Broly", "Goku DU - Gotenks (as Gogeta)",
                    "Goku DU - Omega Shenron", "Goku DU - Vegito vs Buuhan (2nd Route)",
                    "Goku DU - Super Buu (Inside Buu) (2nd Route)",
                    "Goku DU - Gotenks (as Gogeta) (Ending)"],
    },
    "Kid Gohan": {
        "Saiyan":  ["Kid Gohan DU - Goku", "Kid Gohan DU - Saibaman (2nd Route)"],
        "Frieza":  ["Kid Gohan DU - Goku (Namek)", "Kid Gohan DU - Cooler"],
    },
    "Teen Gohan": {
        "Cell":    ["Teen Gohan DU - Tien", "Teen Gohan DU - Yamcha"],
    },
    "Adult Gohan": {
        "Buu":     ["Adult Gohan DU - Vegeta", "Adult Gohan DU - Piccolo",
                    "Adult Gohan DU - Dabura (2nd Route)", "Adult Gohan DU - Majin Vegeta",
                    "Adult Gohan DU - Kid Buu", "Adult Gohan DU - Broly"],
    },
    "Vegeta": {
        "Buu":     ["Vegeta DU - Adult Gohan", "Vegeta DU - Piccolo"],
    },
    "Yamcha": {
        "Saiyan":  ["Yamcha DU - Saibamen (2nd Route)"],
    },
}

# Saga Locks option: item needed to move on to a saga.
SAGA_UNLOCK_ITEM = {
    "Frieza": "Frieza Saga Unlock",
    "Cell":   "Cell Saga Unlock",
    "Buu":    "Buu Saga Unlock",
}


def saga_unlocks_needed(char_name: str, saga_name: str = None) -> list:
    """Saga Unlock items a character needs to reach `saga_name` (default: to reach
    the end of the story). The saga the story starts in is always open; every
    later saga, up to the one asked for, needs its item."""
    sagas = list(DU_CHARACTER_SAGAS[char_name])
    last = sagas.index(saga_name) if saga_name else len(sagas) - 1
    return [SAGA_UNLOCK_ITEM[name] for name in sagas[1:last + 1]]


CHARACTER_UNLOCK_ITEMS = {
    "Goku":        "Goku DU",
    "Kid Gohan":   "Kid Gohan DU",
    "Teen Gohan":  "Teen Gohan DU",
    "Adult Gohan": "Adult Gohan DU",
    "Vegeta":      "Vegeta DU",
    "Krillin":     "Krillin DU",
    "Piccolo":     "Piccolo DU",
    "Tien":        "Tien DU",
    "Yamcha":      "Yamcha DU",
    "Uub":         "Uub DU",
    "Broly":       "Broly DU",
}


def create_regions(world):
    multiworld = world.multiworld
    player = world.player
    map_helper = bool(world.options.map_helper.value)
    saga_locks = bool(world.options.saga_locks.value)
    # Interactsanity: 1 = items, 2 = talks, 3 = both
    interact_kinds = {1: {"item"}, 2: {"talk"}, 3: {"item", "talk"}}.get(
        int(world.options.interactsanity.value), set())

    def has_all(items):
        """Access rule: every item of `items` is held (items may be empty)."""
        items = [name for name in items if name]
        return lambda state: all(state.has(name, player) for name in items)

    def story_items(location_char: str) -> list:
        """A character's DU unlock, plus every Saga Unlock the story needs. Used
        where the saga is not known (Dragon Balls, wishes, completing the DU)."""
        char = "Adult Gohan" if location_char == "Gohan" else location_char
        items = [CHARACTER_UNLOCK_ITEMS.get(char)]
        if saga_locks and char in DU_CHARACTER_SAGAS:
            items += saga_unlocks_needed(char)
        return items

    # Menu region
    menu = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)

    # Shop region - always accessible. Slots beyond the first 10 require
    # "Shop Restock" items (each restock unlocks the next 10 capsules).
    shop_slots = 50
    try:
        shop_slots = int(world.options.shop_slots.value)
    except Exception:
        pass
    shop_region = Region("Shop", player, multiworld)
    shop_items = list(SHOP_LOCATIONS.items())[:shop_slots]
    for slot_i, (name, loc_id) in enumerate(shop_items):
        if loc_id is None:
            continue
        loc = B3Location(player, name, loc_id, shop_region)
        # Slot index 0-9 = always available; 10-19 need 1 restock; 20-29 need 2; etc.
        restocks_needed = slot_i // 10
        if restocks_needed > 0:
            loc.access_rule = (lambda state, n=restocks_needed:
                               state.has("Shop Restock", player, n))
        shop_region.locations.append(loc)
    multiworld.regions.append(shop_region)
    menu.connect(shop_region)

    # Dragon Arena region — gated by the ticket; fights revealed by Rank Ups
    da_fights = 0
    try:
        da_fights = int(world.options.dragon_arena_fights.value)
        if int(world.options.arenasanity.value):
            da_fights = 380
    except Exception:
        pass
    if da_fights > 0:
        da_region = Region("Dragon Arena", player, multiworld)
        da_items = list(DRAGON_ARENA_LOCATIONS.items())[:da_fights]
        for slot_i, (name, loc_id) in enumerate(da_items):
            loc = B3Location(player, name, loc_id, da_region)
            # Every fight needs the ticket; fights past the first 10 need Rank Ups
            rank_ups_needed = slot_i // 10
            def make_rule(n):
                if n == 0:
                    return lambda state: state.has("Dragon Arena Ticket", player)
                return lambda state: (state.has("Dragon Arena Ticket", player)
                                      and state.has("Dragon Arena Rank Up", player, n))
            loc.access_rule = make_rule(rank_ups_needed)
            da_region.locations.append(loc)
        multiworld.regions.append(da_region)
        menu.connect(da_region)

    # Dragon Balls & Wishes (dragonsanity) — gated behind the matching character
    dragonsanity = False
    try:
        dragonsanity = bool(int(world.options.dragonsanity.value))
    except Exception:
        pass
    if dragonsanity:
        # Location char name -> unlock item name (Gohan = Adult Gohan DU)
        char_to_item = {
            "Goku": "Goku DU", "Kid Gohan": "Kid Gohan DU",
            "Teen Gohan": "Teen Gohan DU", "Gohan": "Adult Gohan DU",
            "Vegeta": "Vegeta DU", "Krillin": "Krillin DU",
            "Piccolo": "Piccolo DU", "Tien": "Tien DU", "Yamcha": "Yamcha DU",
            "Uub": "Uub DU", "Broly": "Broly DU",
        }
        db_region = Region("Dragon Balls", player, multiworld)
        for name, loc_id in {**DRAGON_BALL_LOCATIONS, **WISH_LOCATIONS}.items():
            # Extract the character from the location name
            if name.startswith("Dragon Ball: "):
                ch = name[len("Dragon Ball: "):].rsplit(" #", 1)[0]
            else:  # "Wish: <char>"
                ch = name[len("Wish: "):]
            item_name = char_to_item.get(ch)
            loc = B3Location(player, name, loc_id, db_region)
            if item_name:
                # The balls are spread over a character's sagas and the wish needs
                # all seven, so with Saga Locks they ask for every saga of the story.
                loc.access_rule = has_all(story_items(ch))
            db_region.locations.append(loc)
        multiworld.regions.append(db_region)
        menu.connect(db_region)

    # DU completion region - client sends these when the DU credits screen is reached.
    # Each "Complete <Char> DU" requires owning that character's DU unlock item
    # (otherwise the player can't play, let alone complete, that DU). Without
    # this rule every completion is reachable from start -> goal is trivially met
    # at sphere 0 -> empty playthrough.
    du_complete_region = Region("DU Completions", player, multiworld)
    for name, loc_id in DU_COMPLETION_LOCATIONS.items():
        loc = B3Location(player, name, loc_id, du_complete_region)
        # "Complete Goku DU" -> "Goku DU", "Complete Kid Gohan DU" -> "Kid Gohan DU"
        char = name[len("Complete "):]  # e.g. "Kid Gohan DU"
        unlock_item = char if char in CHARACTER_UNLOCK_ITEMS.values() else None
        if unlock_item:
            loc.access_rule = has_all(story_items(char[:-len(" DU")]))
        du_complete_region.locations.append(loc)
    multiworld.regions.append(du_complete_region)
    menu.connect(du_complete_region)

    # Create regions per character per saga
    for char_name, sagas in DU_CHARACTER_SAGAS.items():
        char_unlock = CHARACTER_UNLOCK_ITEMS.get(char_name)

        for saga_name, locations in sagas.items():
            region_name = f"{char_name} DU - {saga_name} Saga"
            region = Region(region_name, player, multiworld)

            for loc_name in locations:
                if loc_name in DU_BATTLE_LOCATIONS:
                    loc = B3Location(player, loc_name,
                                     DU_BATTLE_LOCATIONS[loc_name], region)
                    region.locations.append(loc)
            if map_helper:
                for loc_name in DU_CHARACTER_SAGAS_MAP_HELPER.get(char_name, {}).get(saga_name, []):
                    loc = B3Location(player, loc_name,
                                     DU_BATTLE_LOCATIONS_MAP_HELPER[loc_name], region)
                    region.locations.append(loc)
            for loc_name, loc_id in INTERACT_LOCATIONS.items():
                if (INTERACT_KIND[loc_name] in interact_kinds
                        and INTERACT_REGION[loc_name] == (char_name, saga_name)):
                    region.locations.append(B3Location(player, loc_name, loc_id, region))

            multiworld.regions.append(region)

            # Connect from menu. A DU saga-region requires owning that character's
            # DU unlock and, with Saga Locks, the unlock of every saga the story
            # passes through to get there (the saga it starts in is always open).
            needed = [char_unlock]
            if saga_locks:
                needed += saga_unlocks_needed(char_name, saga_name)
            entrance = menu.connect(region)
            entrance.access_rule = has_all(needed)
