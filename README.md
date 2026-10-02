# DBZ Budokai 3 — Archipelago

An [Archipelago](https://archipelago.gg) randomizer for **Dragon Ball Z: Budokai 3** (PS2, Greatest Hits / SLUS-20998) via **PCSX2**.

Dragon Universe fights, the Skill Shop, character unlocks, and skill capsules become Archipelago checks and items.

> Alpha — back up your saves.

## Requirements
- PCSX2 with **PINE** enabled
- DBZ Budokai 3 (Greatest Hits, CRC `c97ef0a4`)

## Setup
1. Drop `budokai3.apworld` into Archipelago's `custom_worlds/`.
2. Enable PINE in PCSX2 and load Budokai 3.
3. Edit `budokai3_player.yaml` (see options below), put it in `Players/`, and generate.
4. Launch the **Budokai 3 Client**, connect to your server. It auto-detects the game.
5. Play — win DU fights and buy shop capsules to send checks.

## Options
| Option | Default | Description |
|---|---|---|
| `starting_saga` | 0 | 0=Saiyan, 1=Frieza, 2=Cell, 3=Buu (lockout not active yet) |
| `randomize_fights` | true | Master toggle for DU fight randomization |
| `randomize_player1` | false | Randomize your character (P1) |
| `randomize_player2` | true | Randomize the opponent (P2) |
| `randomize_transformations` | false | Give randomized fighters a random starting transformation/form each fight |
| `randomize_stages` | true | Randomize battle stages |
| `shop_slots` | 30 | Skill Shop checks (0–50); shows 10 at a time, more via Shop Restock |
| `drain_trap` | false | Include HP Drain traps |
| `required_du_completions` | 1 | DU campaigns needed to win (1–11) |
| `dragonsanity` | all | `all`: every Dragon Ball picked up (77) and each character's Shenron wish (11) is a check. `wishes`: only the wishes; a pickup just gives the ball. `off`: neither |
| `dragon_arena_fights` | 0 | Dragon Arena fights (0–380) |
| `map_helper` | false | Show every interaction on the Dragon Universe map and move between chapters / sagas with markers (see below). Adds 28 fights as checks |
| `map_free_travel` | false | With `map_helper`: off = the next-chapter / next-saga marker only appears once you beat the fight that opens it. On = always there, so story fights can be skipped |
| `map_item_labels` | true | With `map_helper`: hovering over a map point shows the Archipelago item waiting there and who it is for (plum = progression, blue = useful, cyan = filler, salmon = trap), and what each marker does |
| `shop_item_labels` | true | The Skill Shop's list shows the Archipelago item each capsule sends and who it is for, coloured like the map labels |
| `saga_locks` | false | Frieza, Cell and Buu sagas need a `Saga Unlock` item to move on to (turns `map_helper` on) |
| `fighter_unlocks` | true | The 27 fighters without a Dragon Universe (Frieza, Cell, Trunks...) are `Fighter` items; locked in every mode until found |
| `extra_skills` | true | Every other skill capsule (187: the other fighters' skills and Breakthroughs, fusion forms, the remaining DU character skills) becomes an item, as far as there is room |
| `interactsanity` | off | Visiting map points sends checks: `items` (204 pickups), `talks` (312 talk scenes) or `both` (turns `map_helper` on) |

## Map helper
With `map_helper` on, the Dragon Universe map shows everything the current chapter has to offer, each with an overworld marker and a coloured dot on the overview map:

| Dot | Meaning |
|---|---|
| Red | a fight (or a talk scene that runs straight into one) |
| Green | a talk scene |
| Blue | a battle spot |
| Yellow / orange | an item / a Dragon Ball |
| Purple / pink | next / previous chapter |
| White / grey | next / previous saga |

- A saga is split into **chapters**: what the game places between two story fights. Winning a story fight opens the next chapter; the purple and pink markers move between the chapters you have opened.
- Winning a saga's last fight no longer leaves the saga. Take the **white** marker on the last chapter when you are done with it; the **grey** marker on the first chapter goes back.
- Winning the story's last fight no longer ends the Dragon Universe either: a **white** marker appears that plays the ending when you want to finish.
- Requirements from a second playthrough are removed, so every route's fights are on the map.
- `/map` in the client shows its state; `/map off` and `/map on` switch it for the session.
- Greatest Hits / NTSC-U (CRC `c97ef0a4`) only.

## Checks
- **DU fights (100, or 128 with `map_helper`)** — win a fight = a check (Goku, Vegeta, Piccolo, Krillin, Tien, Broly, the Gohans, Uub, Yamcha)
- **Skill Shop (0–50)** — buy a capsule = a check; capsules are just triggers (not kept)
- **DU completions** — finish a campaign
- **Dragon Arena Fights** Up to 380 Checks
- **Wishes (11)**, and with `dragonsanity: all` every **Dragon Ball** picked up (77)
- **Map interactions (0–516)** — with `interactsanity`: every item pickup and/or talk scene on the Dragon Universe map

## Items
- **Character unlocks (11)** — start with one random DU character, unlock the rest
- **Skills (57)** — Super Saiyan forms, Kamehameha, Final Flash, Fusions/Potara, Breakthroughs, etc. Gated: only obtainable via AP
- **Fighters (27)** — with `fighter_unlocks`: everyone who has no Dragon Universe of their own
- **Extra skills (up to 187)** — with `extra_skills`: every other skill capsule, placed where filler would go
- **Shop Restock** — reveals more shop capsules
- **Saga Unlocks (3)** — with `saga_locks`: Frieza, Cell and Buu Saga Unlock
- **Zenie** and **Experience** bundles (filler), **HP Drain Trap** (optional). Experience goes to the Dragon Universe character you are playing; the level-ups come with the next fight you win

## Victory
Complete the required number of Dragon Universe campaigns.

## Known limitations
- Saga locks and the map helper only work on the NTSC-U version (CRC `c97ef0a4`)
- Some unlocks need one normal in-game save to persist into menus

## Troubleshooting
- *Client can't find game* → check PCSX2 is running Budokai 3 (CRC `c97ef0a4`) with PINE enabled
