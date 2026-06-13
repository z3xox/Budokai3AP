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


class RandomizeMusic(Toggle):
    """Randomize the battle music track in Dragon Universe fights. Each matchup
    gets a random track (0-22). Cosmetic only — no effect on logic or checks."""
    display_name = "Randomize Music"
    default = 0


class RandomizeTransformations(Toggle):
    """Give randomized fighters a random starting transformation/form each fight
    (e.g. spawn as SSJ, Perfect Cell, a fusion). Applies to whichever sides are
    randomized (follows Randomize Player 1 / Player 2). Base form is included in
    the random pool, so not every fighter spawns transformed."""
    display_name = "Randomize Transformations"
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


class Goal(Choice):
    """How to win.
      du_completions      = complete the required number of Dragon Universe runs
      dark_star_dragon_balls = collect the required number of Dark Star Dragon
                               Balls (shuffled McGuffins) scattered in the pool
      both                = satisfy BOTH conditions
    """
    display_name = "Goal"
    option_du_completions = 0
    option_dark_star_dragon_balls = 1
    option_both = 2
    default = 1


class DarkStarBallsRequired(Range):
    """How many Dark Star Dragon Balls must be collected to win (for the
    dark_star_dragon_balls / both goals)."""
    display_name = "Dark Star Dragon Balls Required"
    range_start = 1
    range_end = 7
    default = 7


class DarkStarBallsTotal(Range):
    """How many Dark Star Dragon Balls are placed in the pool. Should be >= the
    required count; extras make them easier to find."""
    display_name = "Dark Star Dragon Balls Total"
    range_start = 1
    range_end = 7
    default = 7


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
    default = 10


class Arenasanity(Toggle):
    """Add ALL 380 Dragon Arena fights as checks. Overrides Dragon Arena Fights
    when enabled. Disabled by default."""
    display_name = "Arenasanity"
    default = 0


class Dragonsanity(Toggle):
    """Add Dragon Ball collection (7 per DU character = 77) and Shenron wishes
    (1 per character = 11) as checks. Enabled by default."""
    display_name = "Dragonsanity"
    default = 1


class StartingCharacter(Choice):
    """Which Dragon Universe character you start with already unlocked. That
    character's DU unlock is precollected and removed from the item pool (since
    you begin with it). Use 'random' (the default) to have a random one picked
    for you per seed."""
    display_name = "Starting DU Character"
    option_goku = 0
    option_kid_gohan = 1
    option_teen_gohan = 2
    option_adult_gohan = 3
    option_vegeta = 4
    option_krillin = 5
    option_piccolo = 6
    option_tien = 7
    option_yamcha = 8
    option_uub = 9
    option_broly = 10
    default = "random"


@dataclass
class B3Options(PerGameCommonOptions):
    goal: Goal
    starting_character: StartingCharacter
    dark_star_balls_required: DarkStarBallsRequired
    dark_star_balls_total: DarkStarBallsTotal
    randomize_fights: RandomizeFights
    randomize_player1: RandomizePlayer1
    randomize_player2: RandomizePlayer2
    randomize_stages: RandomizeStages
    randomize_music: RandomizeMusic
    randomize_transformations: RandomizeTransformations
    shop_slots: ShopSlots
    drain_trap: DrainTrap
    required_du_completions: RequiredDUCompletions
    dragon_arena_fights: DragonArenaFights
    arenasanity: Arenasanity
    dragonsanity: Dragonsanity
