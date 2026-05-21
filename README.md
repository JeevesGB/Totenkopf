# Totenkopf

A Hardmode Mod for **Return To Castle Wolfenstein** that tweaks enemy parameters and weapons to increase difficulty.

> ⚠️ **Work in progress**

---

### Requirements

- [iortcw](https://github.com/iortcw/iortcw) — required to run this mod
- A backup of your original RTCW installation is strongly recommended

---

### Installation

Copy `_totenkopf.pk3` into your `RTCW/Main` directory.

---


# Console Commands

## General Cheats

| Command | Effect |
|---|---|
| `/god` | God mode |
| `/noclip` | Fly through walls |
| `/notarget` | Enemies ignore you |
| `/nofatigue` | Infinite sprint |
| `/kill` | Suicide |
| `/quit` | Exit game |

---

## Give Commands

| Command | Effect |
|---|---|
| `/give all` | All Weapons, Ammo and Items |
| `/give ammo` | Max Ammo |
| `/give armor` | Max Armor |
| `/give armor 135` | Specified armor amount |
| `/give health` | Max Health |
| `/give health 157` | Specified health amount |
| `/give stamina` | Restore Stamina |

---

## Weapon Spawns 
(`/give <weapon>`)

| Command | Weapon |
|---|---|
| `/give binoculars` | Binoculars |
| `/give knife` | Knife |
| `/give luger` | Luger |
| `/give mp42` | MP40 |
| `/give thompson` | Thompson SMG |
| `/give sten` | Sten |
| `/give fg42` | FG42 |
| `/give mauser rifle` | Mauser |
| `/give sniper rifle` | Scoped Mauser |
| `/give panzerfaust` | Rocket Launcher |
| `/give flamethrower` | Flamethrower |
| `/give tesla` | Tesla |
| `/give venom` | Venom |
| `/give grenade` | Grenades |
| `/give dynamite` | Dynamite |

---

## Ammo Spawns 
(`/give <ammo>`)

| Command | Ammo |
|---|---|
| `/give 9mm` | 9mm |
| `/give 12.7mm` | Venom |
| `/give fuel` | Flamethrower fuel |
| `/give cell` | Tesla |
| `/give .30cal` | .30 cal |
| `/give .45cal` | .45 cal |

---

### HUD & Visual

| Command | Effect |
|---|---|
| `/toggle cg_drawfps` | FPS counter |
| `/toggle cg_drawtimer` | Show timer |
| `/toggle cg_draw2d` | Hide/show HUD |
| `/toggle cg_drawcompass` | Compass |
| `/toggle cg_gibs` | Gib effects |
| `/toggle cg_drawteamoverlay` | Team overlay |
| `/toggle r_fullscreen` | Fullscreen/windowed |

---

### Camera & View

| Command | Effect |
|---|---|
| `/cg_FOV 90` | Change FOV |
| `/cg_thirdperson 1` | Third-person camera |
| `/cg_thirdperson 0` | First-person camera |

---

### Fun / Physics

| Command | Effect |
|---|---|
| `/timescale 0.5` | Slow motion |
| `/timescale 2` | Fast motion |
| `/g_gravity 100` | Low gravity |
| `/g_speed 500` | Super speed |

---

### Server & Info

| Command | Effect |
|---|---|
| `/mapname` | Current map name |
| `/serverinfo` | Server info |
| `/cmdlist` | List all commands |
| `/dir maps` | List maps |
| `/reconnect` | Reconnect to server |
| `/screenshot` | Take screenshot |

---

## Map Warp

Use `/spdevmap <mapname>` to warp to any level.

| Map | Command |
|---|---|
| Escape! | `escape1` |
| Castle Keep | `escape2` |
| Tram Ride | `tram` |
| Village | `village1` |
| Catacombs | `crypt1` |
| Crypt | `crypt2` |
| Church | `church` |
| Olaric Boss | `boss1` |
| Forest Compound | `forest` |
| Rocket Base | `rocket` |
| Base Exterior | `baseout` |
| Airfield Assault | `assault` |
| Secret Weapons Facility | `sfm` |
| Factory | `factory` |
| Trainyard | `trainyard` |
| Secret Weapons Facility Return | `swf` |
| Norway | `norway` |
| X-Labs | `xlabs` |
| Heinrich Boss | `boss2` |
| Dam | `dam` |
| Village Revisit | `village2` |
| Chateau | `chateau` |
| Dark Tunnels | `dark` |
| Dig Site | `dig` |
| Castle Return | `castle` |
| Ending | `end` |

**Example:** `/spdevmap xlabs`

---

# Cvars
**CVars** (Console Variables) are configurable settings built into the Quake III engine that RTCW runs on. They control everything from graphics and sound to gameplay and network behaviour, and can be changed at runtime by typing them directly into the game console. Most are saved to your config file and persist between sessions.

[CVar Reference](utils/public/docs/CVARS.md)

---

