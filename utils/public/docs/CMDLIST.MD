# RTCW Command Reference

## General Cheats

| `/god` | God mode |

| `/noclip` | Fly through walls |

| `/notarget` | Enemies ignore you |

| `/nofatigue` | Infinite sprint |

| `/kill` | Suicide |

| `/quit` | Exit game |


---

## Give Commands

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

| `/give 9mm` | 9mm |

| `/give 12.7mm` | Venom |

| `/give fuel` | Flamethrower fuel |

| `/give cell` | Tesla |

| `/give .30cal` | .30 cal |

| `/give .45cal` | .45 cal |


---

### HUD & Visual

| `/toggle cg_drawfps` | FPS counter |

| `/toggle cg_drawtimer` | Show timer |

| `/toggle cg_draw2d` | Hide/show HUD |

| `/toggle cg_drawcompass` | Compass |

| `/toggle cg_gibs` | Gib effects |

| `/toggle cg_drawteamoverlay` | Team overlay |

| `/toggle r_fullscreen` | Fullscreen/windowed |

---

### Camera & View

| `/cg_fov 125` | Change FOV |

| `/cg_thirdperson 1` | Third-person camera |

| `/cg_thirdperson 0` | First-person camera |


---

### Fun / Physics

| `/timescale 0.5` | Slow motion |

| `/timescale 2` | Fast motion |

| `/g_gravity 100` | Low gravity |

| `/g_speed 500` | Super speed |


---

### Server & Info

| `/mapname` | Current map name |

| `/serverinfo` | Server info |

| `/cmdlist` | List all commands |

| `/dir maps` | List maps |

| `/reconnect` | Reconnect to server |

| `/screenshot` | Take screenshot |


---

## Map Warp
Use `/spdevmap <mapname>` to warp to any level.

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

### Movement / World

| ``noclip`` | Fly through walls. |

| ``notarget`` | Enemies ignore you. |

| ``god`` | Invincibility. |

| ``nofatigue`` | Unlimited Stamina. |

| ``give all`` | All Weapons and Ammo. |

| ``give health`` | Full Health. |

| ``kill`` | Kill/Respawn. |


---

## Position / Camera

| ``viewpos`` | Prints your current XYZ coordinates. |

| ``setviewpos X Y Z`` | Teleport to coordinates. |

| ``setCameraOrigin X Y Z`` | Move camera to position. |

| ``startCamera <name>`` | Play a camera script. |

| ``stopCamera`` | Stop camera script. |


---

## Rendering / Graphics

| ``gfxinfo`` | Shows GPU/OpenGL info. |

| ``imagelist`` | Lists all loaded textures. |

| ``shaderlist`` | Lists all loaded shaders. |

| ``modellist`` | Lists all loaded models |

| ``skinlist`` | Lists all loaded skins. |

| ``taginfo`` | Shows model tag info. |

| ``levelshot`` | Takes a level thumbnail screenshot |

| ``cropimages`` | Crops loaded images |

---

## Testing

| ``testmodel <name>`` | Preview a model in game. |

| ``testgun <name>`` | Preview a weapon model. |

| ``nextframe`` | Step through model animation frames. |

| ``prevframe`` | Reverse through model animation frames. |

| ``nextskin`` | Cycle through model skins. |

| ``prevskin`` | Reverse through model skins. |

---

## System / Debug

| ``meminfo`` | Shows memory usage. |

| ``vminfo`` | Shows virtual machine info. |

| ``updatehunkusage`` | Updates hunk memory tracker. |

| ``condump <file.txt>`` | Dump console to a text file. |

| ``cvarlist`` | List all console variables. |

| ``cvar_modified`` | List cvars changed from default. |

| ``status`` | Server/client status info. |

| ``systeminfo`` | Full system info dump. |

| ``clientinfo`` | Your client info. |

| ``configstrings`` | Dump all config strings. |
