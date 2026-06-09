from BaseClasses import Region, MultiWorld
from .Locations import (
    B3Location,
    DU_BATTLE_LOCATIONS,
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
        "Frieza":  ["Kid Gohan DU - Recoome", "Kid Gohan DU - First Form Frieza"],
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
        "Frieza":  ["Vegeta DU - Recoome", "Vegeta DU - Frieza (1st Form)",
                    "Vegeta DU - Frieza (Final Form)", "Vegeta DU - Cooler"],
        "Cell":    ["Vegeta DU - Android 17", "Vegeta DU - Android 18",
                    "Vegeta DU - Cell (17 Absorbed)", "Vegeta DU - Cell (Perfect)"],
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
                    "Krillin DU - Frieza Second Form", "Krillin DU - Frieza Final Form",
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
        "Cell":    ["Piccolo DU - Dr. Gero", "Piccolo DU - Cell 1st Form",
                    "Piccolo DU - Cell 1st Form (Baba)", "Piccolo DU - Perfect Cell",
                    "Piccolo DU - Android 17"],
        "Buu":     ["Piccolo DU - Dabura", "Piccolo DU - Super Buu",
                    "Piccolo DU - Broly"],
    },
    "Tien": {
        "Saiyan":  ["Tien DU - Saibamen", "Tien DU - Nappa"],
        "Cell":    ["Tien DU - Cell 2nd Form", "Tien DU - Cell Jr."],
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

SAGA_UNLOCK_ITEMS = {
    "Frieza": "Frieza Saga Unlock",
    "Cell":   "Cell Saga Unlock",
    "Buu":    "Buu Saga Unlock",
}

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
                loc.access_rule = (lambda inm: (lambda state: state.has(inm, player)))(item_name)
            db_region.locations.append(loc)
        multiworld.regions.append(db_region)
        menu.connect(db_region)

    # DU completion region - client sends these when the DU credits screen is reached.
    du_complete_region = Region("DU Completions", player, multiworld)
    for name, loc_id in DU_COMPLETION_LOCATIONS.items():
        loc = B3Location(player, name, loc_id, du_complete_region)
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

            multiworld.regions.append(region)

            # Connect from menu with access rules
            entrance = menu.connect(region)
            entrance.access_rule = (lambda cn, sn: lambda state: (
                (cn is None or state.has(cn, player)) and
                (sn == "Saiyan" or
                 (sn == "Frieza" and state.has("Frieza Saga Unlock", player)) or
                 (sn == "Cell"   and state.has("Cell Saga Unlock", player)) or
                 (sn == "Buu"    and state.has("Buu Saga Unlock", player)))
            ))(char_unlock, saga_name)
