# Names and ids for the Dragon Universe interaction points that become locations
# with the Interactsanity option: talk scenes and item pickups. Built from
# MapData (the point lists) and the place names the game shows on hover.
#
# No Archipelago imports here: the client's map helper uses this as well.
from .Constants import DU_BASES, MAP_PLACES_EARTH, MAP_PLACES_NAMEK
from .MapData import SAGA_POINTS

SAGA_NAMES = ["Saiyan", "Frieza", "Cell", "Buu"]
CHAR_NAMES = {info["du_id"]: name for name, info in DU_BASES.items()}
NAMEK_BLOCK = 1                      # the Frieza saga is the one played on Namek
INTERACT_ID_OFFSET = 0x20000         # added to the location base id: + ((class - 2000) << 8 | id)
# Places that say nothing about where a point is.
VAGUE_PLACES = {"Plains", "Sky", "Planet Namek", "???", "Battle Point", "Save Point"}


def place_name(block: int, place_type: int) -> str:
    table = MAP_PLACES_NAMEK if block == NAMEK_BLOCK else MAP_PLACES_EARTH
    return table.get(place_type, "???")


def interact_kind(pt):
    """'talk' or 'item' for a point that Interactsanity makes a location, else None.
    Fights (and talk scenes that run straight into one), battle spots and Dragon
    Balls are left out: they are locations of their own, or repeatable."""
    cls = pt.code >> 16
    if pt.fight or pt.starts_fight:
        return None
    if 5000 <= cls < 5400:
        return "talk"
    if 2000 <= cls < 2400 and not pt.flags & 0x10:
        return "item"
    return None


def _build():
    names, kinds, regions, by_event = {}, {}, {}, {}
    for char_id, sagas in SAGA_POINTS.items():
        char = CHAR_NAMES[char_id]
        for block, saga in sagas.items():
            prefix = f"{char} DU - {SAGA_NAMES[block]} Saga - "
            landmarks = [(pt.x, pt.z, place_name(block, pt.type)) for pt in saga["points"]
                         if place_name(block, pt.type) not in VAGUE_PLACES]
            talks, items = {}, 0
            for pt in saga["points"]:
                kind = interact_kind(pt)
                if kind is None:
                    continue
                place = place_name(block, pt.type)
                if kind == "talk":
                    talks[place] = talks.get(place, 0) + 1
                    name = f"{prefix}{place} Talk {talks[place]}"
                else:
                    items += 1
                    name = f"{prefix}Item {items}"
                    if place not in VAGUE_PLACES:
                        name += f" ({place})"
                    elif landmarks:
                        near = min(landmarks, key=lambda m: (m[0] - pt.x) ** 2 + (m[1] - pt.z) ** 2)
                        name += f" (near {near[2]})"
                cls, ident = pt.code >> 16, pt.code & 0xFFFF
                names[name] = INTERACT_ID_OFFSET + ((cls - 2000) << 8 | ident)
                kinds[name] = kind
                regions[name] = (char, SAGA_NAMES[block])
                by_event[pt.code] = name
    return names, kinds, regions, by_event


# name -> id offset; name -> "talk" / "item"; name -> (character, saga); event code -> name
INTERACT_LOCATION_OFFSETS, INTERACT_KIND, INTERACT_REGION, INTERACT_BY_EVENT = _build()
