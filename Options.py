from dataclasses import dataclass
from Options import Toggle, Choice, Range, PerGameCommonOptions


class RandomizeFights(Toggle):
    """Randomize enemy characters in Dragon Universe fights."""
    display_name = "Randomize Fights"
    default = 1


class RandomizeStages(Toggle):
    """Randomize battle stages in Dragon Universe fights."""
    display_name = "Randomize Stages"
    default = 1


class StartingSaga(Choice):
    """Which saga Goku starts with unlocked in Dragon Universe."""
    display_name = "Starting Saga"
    option_saiyan = 0
    option_frieza = 1
    option_cell = 2
    option_buu = 3
    default = 0


class ShopSlots(Range):
    """Number of AP-controlled shop slots (0 to disable shop locations)."""
    display_name = "Shop Slots"
    range_start = 0
    range_end = 10
    default = 10


class DrainTrap(Toggle):
    """Include HP Drain Trap items in the item pool."""
    display_name = "Drain Traps"
    default = 0


class RequiredDUCompletions(Range):
    """Number of Dragon Universe campaigns that must be completed to win."""
    display_name = "Required DU Completions"
    range_start = 1
    range_end = 11
    default = 1


@dataclass
class B3Options(PerGameCommonOptions):
    randomize_fights: RandomizeFights
    randomize_stages: RandomizeStages
    starting_saga: StartingSaga
    shop_slots: ShopSlots
    drain_trap: DrainTrap
    required_du_completions: RequiredDUCompletions
