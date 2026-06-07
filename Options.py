from dataclasses import dataclass
from Options import Toggle, Choice, Range, PerGameCommonOptions


class RandomizeFights(Toggle):
    """Master toggle for randomizing Dragon Universe fights. If off, no fight
    randomization happens regardless of the per-player toggles below."""
    display_name = "Randomize Fights"
    default = 1


class RandomizePlayer1(Toggle):
    """Randomize the player-controlled character (P1) in DU fights.
    Only applies when Randomize Fights is on."""
    display_name = "Randomize Player 1"
    default = 0


class RandomizePlayer2(Toggle):
    """Randomize the opponent character (P2) in DU fights.
    Only applies when Randomize Fights is on."""
    display_name = "Randomize Player 2"
    default = 1


class RandomizeStages(Toggle):
    """Randomize battle stages in Dragon Universe fights."""
    display_name = "Randomize Stages"
    default = 1


class RandomizeTransformations(Toggle):
    """Give randomized fighters a random starting transformation/form each fight
    (e.g. spawn as SSJ, Perfect Cell, a fusion). Applies to whichever sides are
    randomized (follows Randomize Player 1 / Player 2). Base form is included in
    the random pool, so not every fighter spawns transformed."""
    display_name = "Randomize Transformations"
    default = 0


class StartingSaga(Choice):
    """Which saga Goku starts with unlocked in Dragon Universe."""
    display_name = "Starting Saga"
    option_saiyan = 0
    option_frieza = 1
    option_cell = 2
    option_buu = 3
    default = 0


class ShopSlots(Range):
    """Number of AP shop capsule locations (0 to disable). Shop shows 10 at a time; restocks reveal more."""
    display_name = "Shop Slots"
    range_start = 0
    range_end = 50
    default = 30


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


class DragonArenaFights(Range):
    """Number of Dragon Arena fights as AP checks (0 to disable Dragon Arena).
    The arena shows 10 at a time; 'Dragon Arena Rank Up' items reveal more.
    Max 380 (the full arena ladder). Ignored if Arenasanity is enabled."""
    display_name = "Dragon Arena Fights"
    range_start = 0
    range_end = 380
    default = 0


class Arenasanity(Toggle):
    """Add ALL 380 Dragon Arena fights as checks. Overrides Dragon Arena Fights
    when enabled. Disabled by default."""
    display_name = "Arenasanity"
    default = 0


class Dragonsanity(Toggle):
    """Add Dragon Ball collection (7 per DU character = 77) and Shenron wishes
    (1 per character = 11) as checks. Disabled by default."""
    display_name = "Dragonsanity"
    default = 0


@dataclass
class B3Options(PerGameCommonOptions):
    randomize_fights: RandomizeFights
    randomize_player1: RandomizePlayer1
    randomize_player2: RandomizePlayer2
    randomize_stages: RandomizeStages
    randomize_transformations: RandomizeTransformations
    starting_saga: StartingSaga
    shop_slots: ShopSlots
    drain_trap: DrainTrap
    required_du_completions: RequiredDUCompletions
    dragon_arena_fights: DragonArenaFights
    arenasanity: Arenasanity
    dragonsanity: Dragonsanity
