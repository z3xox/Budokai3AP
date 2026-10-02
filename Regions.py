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
        "Saiyan": [
            "Goku DU - Saiyan Saga - Ch.1 - Raditz",
            "Goku DU - Saiyan Saga - Ch.2 - Nappa",
            "Goku DU - Saiyan Saga - Ch.3 - Vegeta",
        ],
        "Frieza": [
            "Goku DU - Frieza Saga - Ch.1 - Recoome",
            "Goku DU - Frieza Saga - Ch.2 - Ginyu",
            "Goku DU - Frieza Saga - Ch.3 - Frieza Final Form",
            "Goku DU - Frieza Saga - Ch.4 - Frieza 100%",
        ],
        "Cell": [
            "Goku DU - Cell Saga - Ch.1 - Perfect Cell",
        ],
        "Buu": [
            "Goku DU - Buu Saga - Ch.1 - Majin Vegeta",
            "Goku DU - Buu Saga - Ch.1 - Majin Buu",
            "Goku DU - Buu Saga - Ch.1 - Vegito vs Buuhan",
            "Goku DU - Buu Saga - Ch.1 - Super Buu (Inside Buu)",
            "Goku DU - Buu Saga - Ch.1 - Kid Buu",
        ],
    },
    "Kid Gohan": {
        "Saiyan": [
            "Kid Gohan DU - Saiyan Saga - Ch.1 - Piccolo",
            "Kid Gohan DU - Saiyan Saga - Ch.2 - Saibaman",
            "Kid Gohan DU - Saiyan Saga - Ch.3 - Nappa",
        ],
        "Frieza": [
            "Kid Gohan DU - Frieza Saga - Ch.1 - Recoome",
            "Kid Gohan DU - Frieza Saga - Ch.2 - Frieza 3rd Form",
        ],
    },
    "Teen Gohan": {
        "Cell": [
            "Teen Gohan DU - Cell Saga - Ch.1 - Piccolo",
            "Teen Gohan DU - Cell Saga - Ch.2 - Krillin",
            "Teen Gohan DU - Cell Saga - Ch.2 - Goku",
            "Teen Gohan DU - Cell Saga - Ch.2 - Perfect Cell",
            "Teen Gohan DU - Cell Saga - Ch.2 - Super Perfect Cell",
        ],
    },
    "Adult Gohan": {
        "Buu": [
            "Adult Gohan DU - Buu Saga - Ch.1 - Goten",
            "Adult Gohan DU - Buu Saga - Ch.2 - Videl",
            "Adult Gohan DU - Buu Saga - Ch.2 - Dabura",
            "Adult Gohan DU - Buu Saga - Ch.3 - Majin Buu",
            "Adult Gohan DU - Buu Saga - Ch.3 - Super Buu",
        ],
    },
    "Vegeta": {
        "Saiyan": [
            "Vegeta DU - Saiyan Saga - Ch.1 - Goku",
            "Vegeta DU - Saiyan Saga - Ch.2 - Kid Gohan",
        ],
        "Frieza": [
            "Vegeta DU - Frieza Saga - Ch.1 - Recoome",
            "Vegeta DU - Frieza Saga - Ch.2 - Frieza 1st Form",
            "Vegeta DU - Frieza Saga - Ch.3 - Frieza Final Form",
            "Vegeta DU - Frieza Saga - Ch.3 - Cooler",
        ],
        "Cell": [
            "Vegeta DU - Cell Saga - Ch.1 - Android 17",
            "Vegeta DU - Cell Saga - Ch.1 - Android 18",
            "Vegeta DU - Cell Saga - Ch.2 - Semi-Perfect Cell",
            "Vegeta DU - Cell Saga - Ch.3 - Perfect Cell",
        ],
        "Buu": [
            "Vegeta DU - Buu Saga - Ch.1 - Goku (SS2)",
            "Vegeta DU - Buu Saga - Ch.1 - Majin Buu",
            "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Gohan Absorbed)",
            "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Gohan Absorbed) [Supreme Kai]",
            "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Inside Buu)",
            "Vegeta DU - Buu Saga - Ch.2 - Super Buu (Inside Buu) [Supreme Kai]",
            "Vegeta DU - Buu Saga - Ch.2 - Kid Buu",
            "Vegeta DU - Buu Saga - Ch.2 - Broly",
            "Vegeta DU - Buu Saga - Ch.2 - Broly [Goku Friendship]",
            "Vegeta DU - Buu Saga - Ch.3 - Gotenks (SS)",
            "Vegeta DU - Buu Saga - Ch.3 - Goku (SS4)",
        ],
    },
    "Krillin": {
        "Saiyan": [
            "Krillin DU - Saiyan Saga - Ch.2 - Nappa",
            "Krillin DU - Saiyan Saga - Ch.1 - Saibaman",
        ],
        "Frieza": [
            "Krillin DU - Frieza Saga - Ch.1 - Recoome",
            "Krillin DU - Frieza Saga - Ch.2 - Ginyu as Goku",
            "Krillin DU - Frieza Saga - Ch.3 - Frieza 2nd Form",
            "Krillin DU - Frieza Saga - Ch.4 - Frieza Final Form",
            "Krillin DU - Frieza Saga - Ch.4 - Frieza Final Form (Ginyu)",
        ],
        "Cell": [
            "Krillin DU - Cell Saga - Ch.1 - Perfect Cell",
        ],
    },
    "Piccolo": {
        "Saiyan": [
            "Piccolo DU - Saiyan Saga - Ch.1 - Raditz (SBC)",
            "Piccolo DU - Saiyan Saga - Ch.2 - Kid Gohan",
            "Piccolo DU - Saiyan Saga - Ch.3 - Saibamen",
            "Piccolo DU - Saiyan Saga - Ch.2 - Goku",
            "Piccolo DU - Saiyan Saga - Ch.4 - Nappa",
            "Piccolo DU - Saiyan Saga - Ch.3 - Vegeta",
            "Piccolo DU - Saiyan Saga - Ch.1 - Raditz (Kame House)",
        ],
        "Frieza": [
            "Piccolo DU - Frieza Saga - Ch.1 - Frieza 2nd Form",
            "Piccolo DU - Frieza Saga - Ch.2 - Frieza 3rd Form",
            "Piccolo DU - Frieza Saga - Ch.2 - Frieza Final Form",
            "Piccolo DU - Frieza Saga - Ch.2 - Cooler",
            "Piccolo DU - Frieza Saga - Ch.3 - Metal Cooler",
        ],
        "Cell": [
            "Piccolo DU - Cell Saga - Ch.1 - Dr. Gero",
            "Piccolo DU - Cell Saga - Ch.2 - Imperfect Cell",
            "Piccolo DU - Cell Saga - Ch.2 - Imperfect Cell (Baba)",
            "Piccolo DU - Cell Saga - Ch.3 - Perfect Cell",
            "Piccolo DU - Cell Saga - Ch.3 - Android 17",
        ],
        "Buu": [
            "Piccolo DU - Buu Saga - Ch.1 - Dabura",
            "Piccolo DU - Buu Saga - Ch.1 - Super Buu",
            "Piccolo DU - Buu Saga - Ch.2 - Broly",
        ],
    },
    "Tien": {
        "Saiyan": [
            "Tien DU - Saiyan Saga - Ch.1 - Saibamen",
            "Tien DU - Saiyan Saga - Ch.2 - Nappa",
        ],
        "Cell": [
            "Tien DU - Cell Saga - Ch.1 - Semi-Perfect Cell",
            "Tien DU - Cell Saga - Ch.2 - Cell Jr.",
        ],
        "Buu": [
            "Tien DU - Buu Saga - Ch.1 - Super Buu (Gotenks)",
            "Tien DU - Buu Saga - Ch.1 - Super Buu (Gotenks/Chiaotzu)",
            "Tien DU - Buu Saga - Ch.2 - Yamcha",
        ],
    },
    "Yamcha": {
        "Saiyan": [
            "Yamcha DU - Saiyan Saga - Ch.1 - Saibamen",
        ],
        "Cell": [
            "Yamcha DU - Cell Saga - Ch.1 - Dr. Gero",
        ],
        "Buu": [
            "Yamcha DU - Buu Saga - Ch.1 - Tien",
            "Yamcha DU - Buu Saga - Ch.1 - Vegeta",
        ],
    },
    "Uub": {
        "Buu": [
            "Uub DU - Buu Saga - Ch.1 - Goku (WT)",
            "Uub DU - Buu Saga - Ch.2 - Majin Buu",
            "Uub DU - Buu Saga - Ch.2 - Vegeta & Goku",
            "Uub DU - Buu Saga - Ch.3 - Goku (Roshi)",
            "Uub DU - Buu Saga - Ch.4 - Omega Shenron",
        ],
    },
    "Broly": {
        "Buu": [
            "Broly DU - Buu Saga - Ch.1 - Videl",
            "Broly DU - Buu Saga - Ch.1 - Kid Trunks",
            "Broly DU - Buu Saga - Ch.1 - Goten",
            "Broly DU - Buu Saga - Ch.1 - Gohan",
            "Broly DU - Buu Saga - Ch.1 - Gohan (WT post-game)",
            "Broly DU - Buu Saga - Ch.1 - Gohan (Rematch)",
            "Broly DU - Buu Saga - Ch.1 - Goku",
        ],
    },
}


# Extra fights that are only locations with the map helper on (same layout).
DU_CHARACTER_SAGAS_MAP_HELPER = {
    "Goku": {
        "Saiyan": [
            "Goku DU - Saiyan Saga - Ch.1 - Tien (World Tournament)",
        ],
        "Frieza": [
            "Goku DU - Frieza Saga - Ch.4 - Cooler",
            "Goku DU - Frieza Saga - Ch.4 - Vegeta (Namek)",
            "Goku DU - Frieza Saga - Ch.5 - Metal Cooler",
            "Goku DU - Frieza Saga - Ch.5 - Cooler (Rematch)",
            "Goku DU - Frieza Saga - Ch.3 - Frieza Final Form (Cooler Route)",
        ],
        "Buu": [
            "Goku DU - Buu Saga - Ch.1 - Uub",
            "Goku DU - Buu Saga - Ch.1 - Broly",
            "Goku DU - Buu Saga - Ch.2 - Gotenks (as Gogeta)",
            "Goku DU - Buu Saga - Ch.2 - Omega Shenron",
            "Goku DU - Buu Saga - Ch.1 - Vegito vs Buuhan (2nd Route)",
            "Goku DU - Buu Saga - Ch.1 - Super Buu (Inside Buu) (2nd Route)",
            "Goku DU - Buu Saga - Ch.2 - Gotenks (as Gogeta) (Ending)",
        ],
    },
    "Kid Gohan": {
        "Saiyan": [
            "Kid Gohan DU - Saiyan Saga - Ch.1 - Goku",
            "Kid Gohan DU - Saiyan Saga - Ch.2 - Saibaman (2nd Route)",
        ],
        "Frieza": [
            "Kid Gohan DU - Frieza Saga - Ch.2 - Goku (Namek)",
            "Kid Gohan DU - Frieza Saga - Ch.3 - Cooler",
        ],
    },
    "Teen Gohan": {
        "Cell": [
            "Teen Gohan DU - Cell Saga - Ch.2 - Tien",
            "Teen Gohan DU - Cell Saga - Ch.2 - Yamcha",
        ],
    },
    "Adult Gohan": {
        "Buu": [
            "Adult Gohan DU - Buu Saga - Ch.2 - Vegeta",
            "Adult Gohan DU - Buu Saga - Ch.2 - Piccolo",
            "Adult Gohan DU - Buu Saga - Ch.2 - Dabura (2nd Route)",
            "Adult Gohan DU - Buu Saga - Ch.3 - Majin Vegeta",
            "Adult Gohan DU - Buu Saga - Ch.4 - Kid Buu",
            "Adult Gohan DU - Buu Saga - Ch.5 - Broly",
        ],
    },
    "Vegeta": {
        "Buu": [
            "Vegeta DU - Buu Saga - Ch.1 - Adult Gohan",
            "Vegeta DU - Buu Saga - Ch.1 - Piccolo",
        ],
    },
    "Yamcha": {
        "Saiyan": [
            "Yamcha DU - Saiyan Saga - Ch.1 - Saibamen (2nd Route)",
        ],
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
        dragonsanity = int(world.options.dragonsanity.value)   # 1 = balls + wishes, 2 = wishes
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
        ball_locations = DRAGON_BALL_LOCATIONS if dragonsanity == 1 else {}
        for name, loc_id in {**ball_locations, **WISH_LOCATIONS}.items():
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
