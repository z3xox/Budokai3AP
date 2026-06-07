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
| `randomize_stages` | true | Randomize battle stages |
| `shop_slots` | 30 | Skill Shop checks (0–50); shows 10 at a time, more via Shop Restock |
| `drain_trap` | false | Include HP Drain traps |
| `required_du_completions` | 1 | DU campaigns needed to win (1–11) |
| `dragonsanity` | 0 | Add Dragon Ball collection (7 per character = 77) and Shenron wishes |
| `dragon_arena_fights` | 0 | Dragon Arena fights (0–380) |

## Checks
- **DU fights (~100)** — win a fight = a check (Goku, Vegeta, Piccolo, Krillin, Tien, Broly, the Gohans, Uub, Yamcha)
- **Skill Shop (0–50)** — buy a capsule = a check; capsules are just triggers (not kept)
- **DU completions** — finish a campaign
- **Dragon Arena Fights** Up to 380 Checks
- **Dragonballs & Wishes** 88

## Items
- **Character unlocks (11)** — start with one random DU character, unlock the rest
- **Skills (54)** — Super Saiyan forms, Kamehameha, Final Flash, Fusions/Potara, Breakthroughs, etc. Gated: only obtainable via AP
- **Shop Restock** — reveals more shop capsules
- **Zenie** bundles, **HP Drain Trap** (optional)

## Victory
Complete the required number of Dragon Universe campaigns.

## Known limitations
- Saga lockout not implemented (all sagas open)
- Some unlocks need one normal in-game save to persist into menus

## Troubleshooting
- *Client can't find game* → check PCSX2 is running Budokai 3 (CRC `c97ef0a4`) with PINE enabled
