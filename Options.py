from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Choice, Range, PerGameCommonOptions


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


class StartWithDragonRadar(DefaultOnToggle):
    """Start every Dragon Universe with the Dragon Radar already obtained, so you
    can immediately track Dragon Balls instead of having to find the radar first.
    Applies to whichever character's DU you are playing. On by default."""
    display_name = "Start with Dragon Radar"


class DeathLink(Toggle):
    """When ON, losing a Dragon Universe battle sends a death to everyone else in
    the multiworld playing with DeathLink, and receiving a death drains your
    fighter's health so the opponent finishes you (forcing a loss in your current
    fight). If you're not in a fight when a death arrives, it applies to your
    next fight."""
    display_name = "Death Link"
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


class Dragonsanity(Choice):
    """Checks from the Dragon Balls.
      off    = none
      wishes = each character's Shenron wish is a check (11). Picking up a
               Dragon Ball just gives the Dragon Ball.
      all    = every Dragon Ball picked up is a check as well (7 per character
               = 77), so a pickup gives the ball and an Archipelago item (default)
    """
    display_name = "Dragonsanity"
    option_off = 0
    option_all = 1
    option_wishes = 2
    alias_false = 0
    alias_true = 1
    default = 1


class MapHelper(Toggle):
    """Make the Dragon Universe map show what there is to do (NTSC-U only).

    Every interaction of the current chapter is on the map with a marker and a
    coloured dot (red fight, green talk, blue battle spot, yellow item, orange
    Dragon Ball), requirements from a second playthrough are removed, and winning
    a saga's last fight no longer leaves the saga: purple / pink markers move
    between chapters, a white marker goes to the next saga and a grey one back.

    Also adds 28 fights as locations that are otherwise only reachable on a
    second playthrough or an alternate route."""
    display_name = "Map Helper"
    default = 0


class MapFreeTravel(Toggle):
    """Only with Map Helper. OFF (default): the next-chapter marker only appears
    once you have beaten the story fight that opens that chapter, and the
    next-saga marker once you have beaten the saga's last fight, so the markers
    are for moving around what you already reached. ON: they are always there,
    so a story fight can be skipped."""
    display_name = "Map Free Travel"
    default = 0


class MapItemLabels(DefaultOnToggle):
    """Only with Map Helper. The name shown when you hover over a map point says
    what is there: for an open check, the Archipelago item and who it is for,
    coloured by importance (plum = progression, blue = useful, cyan = filler,
    salmon = trap); for a marker, what it does. OFF: the game's place names."""
    display_name = "Map Item Labels"


class ShopItemLabels(DefaultOnToggle):
    """The Skill Shop's list shows the Archipelago item each capsule sends, and
    who it is for, in place of the capsule's own name (same colours as the map
    labels). OFF: the capsules keep their names. NTSC-U only."""
    display_name = "Shop Item Labels"


class SagaLocks(Toggle):
    """Lock the Frieza, Cell and Buu sagas behind 'Saga Unlock' items. A character
    can only move on to a saga once its item is found; the saga a character's story
    starts in is always open. Needs Map Helper (turned on automatically)."""
    display_name = "Saga Locks"
    default = 0


class Interactsanity(Choice):
    """Make the other interaction points of the Dragon Universe map locations:
    visiting one sends its check. Battle spots (blue) are never included, and
    fights and Dragon Balls are locations of their own.
      off   = none
      items = item pickups, the yellow dots (204)
      talks = talk scenes, the green dots (312)
      both  = items and talks (516)
    Needs Map Helper (turned on automatically): many of these points are hidden
    or need a second playthrough without it."""
    display_name = "Interactsanity"
    option_off = 0
    option_items = 1
    option_talks = 2
    option_both = 3
    default = 0


class FighterUnlocks(DefaultOnToggle):
    """Make the 27 fighters without a Dragon Universe of their own (Frieza, Cell,
    Trunks, Goten, Bardock...) 'Fighter' items: they stay locked in every mode,
    the Dragon Arena included, until found. The eleven Dragon Universe characters
    are unlocked by their own 'DU' item, as before. OFF: those 27 are left as
    your save has them."""
    display_name = "Fighter Unlocks"


class ExtraSkills(DefaultOnToggle):
    """Add every other skill capsule in the game as items, as far as there is
    room: the 27 other fighters' attacks, transformations and Breakthroughs, the
    fusion forms' skills, and the Dragon Universe characters' remaining ones
    (187 capsules). Like the other skills they can then only be obtained through
    Archipelago. They take the place of filler and never crowd out anything
    else; when not all fit, Breakthroughs go in first."""
    display_name = "Extra Skills"


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
    start_with_dragon_radar: StartWithDragonRadar
    required_du_completions: RequiredDUCompletions
    dragon_arena_fights: DragonArenaFights
    arenasanity: Arenasanity
    dragonsanity: Dragonsanity
    map_helper: MapHelper
    map_free_travel: MapFreeTravel
    map_item_labels: MapItemLabels
    shop_item_labels: ShopItemLabels
    saga_locks: SagaLocks
    interactsanity: Interactsanity
    fighter_unlocks: FighterUnlocks
    extra_skills: ExtraSkills
    death_link: DeathLink
