# RTCW CVar Reference

> Flags: **S** = Server info | **U** = Userinfo | **R** = Read-only | **I** = Init (set at startup) | **A** = Archive (saved to config) | **L** = Latch (requires restart) | **C** = Cheat | **?** = Unknown/game module

---

## Graphics & Rendering

### Display & Resolution

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_fullscreen` | `0` | AL | Fullscreen mode |
| `r_mode` | `4` | AL | Resolution mode index |
| `r_customwidth` | `1600` | AL | Custom resolution width |
| `r_customheight` | `1024` | AL | Custom resolution height |
| `r_customPixelAspect` | `1` | AL | Custom pixel aspect ratio |
| `r_noborder` | `0` | AL | Borderless window |
| `r_allowResize` | `0` | AL | Allow window resizing |
| `r_centerWindow` | `0` | AL | Center window on screen |
| `r_windowPosx` | `565` | A | Window X position |
| `r_windowPosy` | `201` | A | Window Y position |
| `r_displayRefresh` | `0` | L | Display refresh rate |
| `r_swapInterval` | `0` | AL | VSync (0=off, 1=on) |
| `r_uiFullScreen` | `1` | — | UI fullscreen mode |
| `r_availableModes` | *(list)* | R | Available screen resolutions |
| `r_sdlDriver` | `windows` | R | SDL display driver |

### Texture & Image Quality

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_picmip` | `1` | AL | Texture mip level (lower = sharper) |
| `r_picmip2` | `2` | AL | Secondary texture mip level |
| `r_texturebits` | `32` | AL | Texture colour depth |
| `r_colorbits` | `32` | AL | Colour buffer bits |
| `r_depthbits` | `24` | AL | Depth buffer bits |
| `r_stencilbits` | `0` | AL | Stencil buffer bits |
| `r_roundImagesDown` | `1` | AL | Round image sizes down to power of 2 |
| `r_lowMemTextureSize` | `0` | AL | Low memory texture size cap |
| `r_lowMemTextureThreshold` | `15.0` | AL | Low memory threshold (MB) |
| `r_rmse` | `0.0` | AL | Texture compression error threshold |
| `r_detailtextures` | `1` | AL | Enable detail textures |
| `r_simpleMipMaps` | `1` | AL | Use simple mip map generation |
| `r_textureMode` | `GL_LINEAR_MIPMAP_NEAREST` | A | Texture filtering mode |
| `r_intensity` | `1` | L | Texture intensity |
| `r_colorMipLevels` | `0` | L | Colourise mip levels (debug) |

### OpenGL Extensions

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_allowExtensions` | `1` | AL | Allow OpenGL extensions |
| `r_ext_compressed_textures` | `0` | AL | Compressed texture support |
| `r_ext_multitexture` | `1` | AL | Multitexture support |
| `r_ext_compiled_vertex_array` | `1` | AL | Compiled vertex array support |
| `r_ext_texture_env_add` | `1` | AL | Texture env add extension |
| `r_ext_texture_filter_anisotropic` | `0` | AL | Anisotropic texture filtering |
| `r_ext_max_anisotropy` | `2` | AL | Max anisotropy level |
| `r_ext_multisample` | `0` | AL | Multisample antialiasing |
| `r_ext_NV_fog_dist` | `1` | AL | NVIDIA fog distance extension |
| `r_ext_ATI_pntriangles` | `0` | AL | ATI PN triangles extension |
| `r_glIgnoreWicked3D` | `0` | AL | Ignore Wicked3D driver quirks |
| `r_ignorehwgamma` | `0` | AL | Ignore hardware gamma |
| `r_allowSoftwareGL` | `0` | L | Allow software OpenGL fallback |

### Lighting & Shadows

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_dynamiclight` | `1` | A | Enable dynamic lights |
| `r_dlightScale` | `1.0` | A | Dynamic light scale |
| `r_dlightBacks` | `1` | A | Light back surfaces |
| `r_ambientScale` | `0.5` | C | Ambient light scale |
| `r_directedScale` | `1` | C | Directed light scale |
| `r_mapOverBrightBits` | `2` | L | Map overbright bits |
| `r_overBrightBits` | `0` | AL | Overbright bits |
| `r_fullbright` | `0` | L | Full bright mode (cheat) |
| `r_lightmap` | `0` | C | Show lightmaps only |
| `r_debuglight` | `0` | — | Debug lighting |

### Visual Effects

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_flares` | `1` | A | Enable lens flares |
| `r_flareSize` | `40` | C | Flare size |
| `r_flareFade` | `5` | C | Flare fade speed |
| `r_flareCoeff` | `150` | C | Flare intensity coefficient |
| `r_drawSun` | `1` | A | Draw sun |
| `r_fastsky` | `0` | A | Fast sky rendering |
| `r_wolffog` | `1` | — | Enable Wolf fog |
| `r_bloom` | `0` | A | Enable bloom effect |
| `r_bloom_alpha` | `0.3` | A | Bloom alpha |
| `r_bloom_intensity` | `1.3` | A | Bloom intensity |
| `r_bloom_darken` | `4` | A | Bloom darken factor |
| `r_bloom_diamond_size` | `8` | A | Bloom diamond size |
| `r_bloom_sample_size` | `128` | AL | Bloom sample size |
| `r_bloom_fast_sample` | `0` | AL | Fast bloom sampling |
| `r_greyscale` | `0` | AL | Greyscale rendering |
| `r_anaglyphMode` | `0` | A | Anaglyph 3D mode |
| `r_stereoEnabled` | `0` | AL | Stereo rendering |
| `r_stereoSeparation` | `64` | A | Stereo eye separation |

### Performance & Debug

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_gamma` | `1` | A | Display gamma |
| `r_lodbias` | `0` | A | LOD bias |
| `r_lodscale` | `5` | C | LOD scale |
| `r_lodCurveError` | `250` | A | LOD curve error threshold |
| `r_subdivisions` | `4` | AL | Curve subdivision level |
| `r_vertexLight` | `0` | AL | Use vertex lighting |
| `r_facePlaneCull` | `1` | A | Cull back-facing surfaces |
| `r_primitives` | `0` | A | Rendering primitive mode |
| `r_inGameVideo` | `1` | A | Enable in-game video |
| `r_maxpolys` | `4096` | — | Max polygons per frame |
| `r_maxpolyverts` | `8192` | — | Max polygon vertices |
| `r_zproj` | `64` | A | Z projection distance |
| `r_znear` | `4` | C | Near clip plane |
| `r_zfar` | `0` | C | Far clip plane (0=auto) |
| `r_finish` | `0` | A | Force GL finish (sync) |
| `r_ignoreGLErrors` | `1` | A | Ignore GL errors |
| `r_ignoreFastPath` | `1` | AL | Ignore renderer fast path |
| `r_singleShader` | `0` | LC | Single shader debug mode |
| `r_speeds` | `0` | C | Show render speeds |
| `r_measureOverdraw` | `0` | C | Measure overdraw |
| `r_skipBackEnd` | `0` | C | Skip render backend |
| `r_norefresh` | `0` | C | Skip frame rendering |
| `r_drawentities` | `1` | C | Draw entities |
| `r_drawworld` | `1` | C | Draw world geometry |
| `r_drawBuffer` | `GL_BACK` | C | Draw buffer target |
| `r_novis` | `0` | C | Disable PVS culling |
| `r_nocull` | `0` | C | Disable frustum culling |
| `r_nocurves` | `0` | C | Disable curve rendering |
| `r_noportals` | `0` | C | Disable portals |
| `r_lockpvs` | `0` | C | Lock PVS for debugging |
| `r_portalOnly` | `0` | C | Render portals only |
| `r_nobind` | `0` | C | Disable texture binding |
| `r_clear` | `0` | C | Clear frame buffer |
| `r_showImages` | `0` | — | Show all loaded images |
| `r_showtris` | `0` | C | Show triangle wireframe |
| `r_shownormals` | `0` | C | Show surface normals |
| `r_showsky` | `0` | C | Show sky surfaces |
| `r_showcluster` | `0` | C | Show current cluster |
| `r_debugSurface` | `0` | C | Debug surface rendering |
| `r_debugSort` | `0` | C | Debug sort order |
| `r_bonesDebug` | `0` | C | Debug bone rendering |
| `r_verbose` | `0` | C | Verbose renderer output |
| `r_logFile` | `0` | C | Log renderer calls |
| `r_ignore` | `1` | C | Ignore renderer (test) |
| `r_marksOnTriangleMeshes` | `0` | A | Allow marks on triangle meshes |
| `r_savegameFogColor` | `0` | R | Savegame fog colour |
| `r_mapFogColor` | `0` | R | Map fog colour |
| `r_waterFogColor` | `0` | R | Water fog colour |
| `r_offsetunits` | `-2` | C | Polygon offset units |
| `r_offsetfactor` | `-1` | C | Polygon offset factor |
| `r_compressModels` | `0` | — | Compress model data |
| `r_exportCompressedModels` | `0` | — | Export compressed models |
| `r_saveFontData` | `0` | — | Save font data to disk |
| `r_printShaders` | `0` | — | Print loaded shaders |
| `r_highQualityVideo` | `1` | A | High quality video capture |
| `r_aviMotionJpegQuality` | `90` | A | AVI JPEG quality |
| `r_screenshotJpegQuality` | `90` | A | Screenshot JPEG quality |

### ATI TruForm

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `r_ati_truform_tess` | `1` | A | ATI TruForm tessellation |
| `r_ati_truform_normalmode` | `QUADRATIC` | A | TruForm normal mode |
| `r_ati_truform_pointmode` | `CUBIC` | A | TruForm point mode |
| `r_ati_fsaa_samples` | `1` | A | ATI FSAA sample count |
| `r_nv_fogdist_mode` | `GL_EYE_RADIAL_NV` | A | NVIDIA fog distance mode |

---

## HUD & Client Display

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cg_draw2D` | `1` | A? | Enable 2D HUD |
| `cg_drawFPS` | `1` | A? | Show FPS counter |
| `cg_drawTimer` | `1` | A? | Show game timer |
| `cg_drawStatus` | `1` | A? | Show status bar |
| `cg_drawStatusHead` | `0` | A? | Show player head on status |
| `cg_drawFrags` | `1` | A? | Show frag count |
| `cg_drawSnapshot` | `0` | A? | Show snapshot info |
| `cg_drawAmmoWarning` | `1` | A? | Show low ammo warning |
| `cg_drawAttacker` | `1` | A? | Show attacker portrait |
| `cg_drawCompass` | `1` | A? | Show compass |
| `cg_drawIcons` | `1` | A? | Draw icons |
| `cg_draw3dIcons` | `1` | A? | Draw 3D icons |
| `cg_drawRewards` | `1` | A? | Show reward messages |
| `cg_drawTeamOverlay` | `0` | A? | Show team overlay |
| `cg_hudAlpha` | `0.8` | A | HUD transparency |
| `cg_hudFiles` | `ui/hud.txt` | A? | HUD definition file |
| `cg_lagometer` | `1` | A? | Show lag-o-meter |
| `cg_shadows` | `1` | A | Enable shadows |
| `cg_skybox` | `1` | — | Enable skybox |
| `cg_gibs` | `1` | A? | Enable gibs |
| `cg_brassTime` | `2500` | A | Shell casing lifetime (ms) |
| `cg_wolfparticles` | `1` | A | Enable Wolf particles |
| `cg_bloodTime` | `120` | A? | Blood effect duration |
| `cg_particleDist` | `1024` | A? | Particle draw distance |
| `cg_particleLOD` | `0` | A? | Particle LOD level |
| `cg_coronas` | `1` | A? | Enable light coronas |
| `cg_coronafardist` | `1536` | A? | Corona draw distance |
| `cg_blinktime` | `100` | A? | Cursor blink rate |
| `cg_viewsize` | `100.000000` | A | Viewport size percentage |

---

## Crosshair

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cg_drawCrosshair` | `8` | A | Crosshair style (0=off) |
| `cg_drawCrosshairNames` | `1` | A | Show player names on crosshair |
| `cg_drawCrosshairPickups` | `1` | A | Show pickup hints |
| `cg_drawCrosshairBinoc` | `0` | A? | Crosshair with binoculars |
| `cg_drawCrosshairReticle` | `1` | A? | Show crosshair reticle |
| `cg_crosshairSize` | `32` | A? | Crosshair size |
| `cg_crosshairAlpha` | `0.5` | A? | Crosshair transparency |
| `cg_crosshairHealth` | `1` | A? | Crosshair colour by health |
| `cg_crosshairX` | `0` | A? | Crosshair X offset |
| `cg_crosshairY` | `0` | A? | Crosshair Y offset |
| `cg_reticleBrightness` | `0.7` | A? | Reticle brightness |
| `cg_drawSpreadScale` | `1` | A? | Show spread indicator |
| `cg_cursorHints` | `1` | A? | Show cursor hints |
| `cg_hintFadeTime` | `500` | A? | Hint fade time (ms) |
| `cg_marktime` | `20000` | A | Bullet mark lifetime (ms) |

---

## Field of View & Camera

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cg_fov` | `100` | A? | Field of view |
| `cg_zoomfov` | `22.5` | A? | Zoom FOV |
| `cg_zoomDefaultBinoc` | `22.5` | A? | Binoculars default zoom FOV |
| `cg_zoomDefaultSniper` | `15` | A? | Sniper default zoom FOV |
| `cg_zoomDefaultSnooper` | `40` | A? | Snooper default zoom FOV |
| `cg_zoomDefaultFG` | `55` | A? | FG42 default zoom FOV |
| `cg_zoomStepBinoc` | `3` | A? | Binoculars zoom step |
| `cg_zoomStepSniper` | `2` | A? | Sniper zoom step |
| `cg_zoomStepSnooper` | `5` | A? | Snooper zoom step |
| `cg_zoomStepFG` | `10` | A? | FG42 zoom step |
| `cg_useWeapsForZoom` | `1` | A? | Use weapon input for zoom |
| `cg_fixedAspect` | `0` | AL | Fixed aspect ratio mode |
| `cg_fixedAspectFOV` | `1` | A | Adjust FOV for aspect ratio |
| `cg_stereoSeparation` | `0` | R | Stereo separation |
| `cg_cameraOrbitDelay` | `50` | A? | Camera orbit delay (ms) |

---

## Weapons

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cg_drawGun` | `1` | A? | Draw weapon model |
| `cg_drawFPGun` | `1` | A? | Draw first-person weapon |
| `cg_drawAllWeaps` | `1` | A? | Show all weapons on HUD |
| `cg_cycleAllWeaps` | `1` | A? | Cycle through all weapons |
| `cg_weaponCycleDelay` | `150` | A? | Weapon cycle delay (ms) |
| `cg_autoswitch` | `2` | A | Auto weapon switch mode |
| `cg_useSuggestedWeapons` | `1` | A | Use suggested weapon loadout |
| `cg_emptyswitch` | `0` | UA | Switch on empty weapon |
| `cg_autoactivate` | `1` | UA | Auto-activate items |
| `cg_recoilPitch` | `0` | R | Recoil pitch value |

---

## Movement & Camera Bob

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cg_bobup` | `0.005` | A? | View bob up amplitude |
| `cg_bobpitch` | `0.002` | A? | View bob pitch |
| `cg_bobroll` | `0.002` | A? | View bob roll |
| `cg_runpitch` | `0.002` | A? | Run pitch |
| `cg_runroll` | `0.005` | A? | Run roll |

---

## Mouse & Input

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `sensitivity` | `5` | A | Mouse sensitivity |
| `m_pitch` | `0.022` | A | Mouse pitch scale |
| `m_yaw` | `0.022` | A | Mouse yaw scale |
| `m_forward` | `0.25` | A | Mouse forward scale |
| `m_side` | `0.25` | A | Mouse side scale |
| `m_filter` | `0` | A | Mouse input smoothing |
| `cl_mouseAccel` | `0` | A | Mouse acceleration |
| `cl_mouseAccelStyle` | `0` | A | Mouse accel style |
| `cl_mouseAccelOffset` | `5` | A | Mouse accel offset |
| `cl_freelook` | `1` | A | Enable free look (mouselook) |
| `cl_yawspeed` | `140` | A | Keyboard yaw speed |
| `cl_pitchspeed` | `140` | A | Keyboard pitch speed |
| `cl_anglespeedkey` | `1.5` | — | Angle speed key modifier |
| `cl_run` | `1` | A | Always run |
| `in_mouse` | `1` | A | Mouse input enabled |
| `in_nograb` | `0` | A | Disable mouse grab |
| `in_joystick` | `0` | AL | Enable joystick input |
| `in_keyboardDebug` | `0` | A | Keyboard debug output |
| `joy_threshold` | `0.15` | A | Joystick dead zone |
| `ui_mousePitch` | `0` | — | Invert mouse pitch in UI |

### Joystick Axes

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `j_pitch` | `0.022` | A | Joystick pitch scale |
| `j_yaw` | `-0.022` | A | Joystick yaw scale |
| `j_forward` | `-0.25` | A | Joystick forward scale |
| `j_side` | `0.25` | A | Joystick side scale |
| `j_up` | `0` | A | Joystick up scale |
| `j_pitch_axis` | `3` | A | Joystick pitch axis index |
| `j_yaw_axis` | `2` | A | Joystick yaw axis index |
| `j_forward_axis` | `1` | A | Joystick forward axis index |
| `j_side_axis` | `0` | A | Joystick side axis index |
| `j_up_axis` | `4` | A | Joystick up axis index |

---

## Sound

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `s_volume` | `0.468750` | A | Sound effects volume |
| `s_musicvolume` | `0.166667` | A | Music volume |
| `s_doppler` | `1` | A | Enable Doppler effect |
| `s_muteWhenMinimized` | `0` | A | Mute when window minimised |
| `s_muteWhenUnfocused` | `0` | A | Mute when window unfocused |
| `s_useOpenAL` | `1` | AL | Use OpenAL backend |
| `s_initsound` | `1` | — | Initialise sound on startup |
| `s_backend` | `OpenAL` | R | Active sound backend |
| `s_muted` | `0` | R | Sound muted state |
| `s_currentMusic` | *(track)* | — | Currently playing music file |
| `s_alDriver` | `OpenAL32.dll` | AL | OpenAL driver DLL |
| `s_alDevice` | `` | AL | OpenAL output device |
| `s_alInputDevice` | `` | AL | OpenAL input device |
| `s_alAvailableDevices` | *(list)* | R | Available output devices |
| `s_alAvailableInputDevices` | *(list)* | R | Available input devices |
| `s_alCapture` | `1` | AL | Enable audio capture |
| `s_alPrecache` | `1` | A | Precache OpenAL sources |
| `s_alGain` | `1.0` | A | OpenAL master gain |
| `s_alSources` | `128` | A | Max OpenAL sources |
| `s_alDopplerFactor` | `1.0` | A | Doppler effect factor |
| `s_alDopplerSpeed` | `9000` | A | Doppler speed of sound |
| `s_alMinDistance` | `256` | A | Min attenuation distance |
| `s_alMaxDistance` | `1024` | A | Max attenuation distance |
| `s_alRolloff` | `1.3` | A | Rolloff factor |
| `s_alGraceDistance` | `512` | A | Grace zone distance |
| `s_alTalkAnims` | `160` | A | Talk animation threshold |

---

## Network

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `net_ip` | `0.0.0.0` | L | Server/client IPv4 bind address |
| `net_ip6` | `::` | L | Server/client IPv6 bind address |
| `net_port` | `27960` | L | Network port |
| `net_port6` | `27960` | L | IPv6 network port |
| `net_enabled` | `3` | AL | Network enabled flags |
| `net_mcast6addr` | *(addr)* | AL | IPv6 multicast address |
| `net_mcast6iface` | `0` | AL | IPv6 multicast interface |
| `net_dropsim` | `` | — | Packet drop simulation |
| `net_qport` | `5201` | I | Client query port |
| `net_socksEnabled` | `0` | AL | Enable SOCKS proxy |
| `net_socksServer` | `` | AL | SOCKS server address |
| `net_socksPort` | `1080` | AL | SOCKS server port |
| `net_socksUsername` | `` | AL | SOCKS username |
| `net_socksPassword` | `` | AL | SOCKS password |
| `showpackets` | `0` | — | Show outgoing packets |
| `showdrop` | `0` | — | Show dropped packets |
| `debug_protocol` | `` | — | Protocol debug string |

---

## Client

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cl_maxpackets` | `38` | A | Max packets per second |
| `cl_packetdup` | `1` | A | Duplicate packets sent |
| `cl_maxPing` | `800` | A | Max acceptable ping |
| `cl_timeNudge` | `0` | — | Interpolation time nudge |
| `cl_timeout` | `200` | — | Connection timeout (s) |
| `cl_nodelta` | `0` | — | Disable delta compression |
| `cl_shownet` | `0` | — | Show network traffic |
| `cl_showSend` | `0` | — | Show sent data |
| `cl_showTimeDelta` | `0` | — | Show time delta |
| `cl_showmouserate` | `0` | — | Show mouse input rate |
| `cl_freezeDemo` | `0` | — | Freeze demo playback |
| `cl_avidemo` | `0` | — | Capture demo to AVI |
| `cl_forceavidemo` | `0` | — | Force AVI capture |
| `cl_aviFrameRate` | `25` | A | AVI capture frame rate |
| `cl_aviMotionJpeg` | `1` | A | Use JPEG compression for AVI |
| `cl_timedemoLog` | `` | A | Timedemo log file |
| `cl_autoRecordDemo` | `0` | A | Auto-record demos |
| `cl_allowDownload` | `0` | A | Allow downloading from server |
| `cl_lanForcePackets` | `1` | A | Force LAN packet rate |
| `cl_guidServerUniq` | `1` | A | Unique GUID per server |
| `cl_consoleKeys` | `~ \` 0x7e 0x60` | A | Keys to open console |
| `cl_noprint` | `0` | — | Suppress console output |
| `cl_debugMove` | `0` | — | Debug movement |
| `cl_debugTranslation` | `0` | — | Debug string translation |
| `cl_conXOffset` | `0` | — | Console X offset |
| `cl_serverStatusResendTime` | `750` | — | Server status resend time |
| `cl_motd` | `1` | — | Show message of the day |
| `cl_motdString` | `` | R | MOTD string from server |
| `cl_waitForFire` | `0` | R | Wait for fire input |
| `cl_running` | `1` | R | Client is running |
| `cl_paused` | `0` | R | Client is paused |
| `cl_language` | `0` | A | Client language |
| `cl_renderer` | `opengl1` | AL | Renderer module |
| `cl_anonymous` | `0` | UA | Anonymous mode |
| `cl_useMumble` | `0` | AL | Enable Mumble integration |
| `cl_mumbleScale` | `0.0254` | A | Mumble position scale |
| `cl_guid` | *(hash)* | UR | Client GUID |

### VoIP

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `cl_voip` | `1` | A | Enable VoIP |
| `cl_voipProtocol` | `opus` | UR | VoIP codec protocol |
| `cl_voipSend` | `0` | — | Currently transmitting VoIP |
| `cl_voipSendTarget` | `spatial` | — | VoIP send target |
| `cl_voipGainDuringCapture` | `0.2` | A | Gain reduction during capture |
| `cl_voipCaptureMult` | `2.0` | A | Capture signal multiplier |
| `cl_voipUseVAD` | `0` | A | Voice activity detection |
| `cl_voipVADThreshold` | `0.25` | A | VAD threshold |
| `cl_voipShowMeter` | `1` | A | Show VoIP level meter |

---

## Server

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `sv_hostname` | `noname` | SA | Server name |
| `sv_maxclients` | `64` | SAL | Max connected clients |
| `sv_fps` | `20` | — | Server tick rate |
| `sv_timeout` | `120` | — | Client timeout (s) |
| `sv_zombietime` | `2` | — | Zombie client timeout (s) |
| `sv_reconnectlimit` | `3` | — | Max reconnect attempts |
| `sv_allowDownload` | `1` | — | Allow clients to download files |
| `sv_allowAnonymous` | `0` | S | Allow anonymous connections |
| `sv_privateClients` | `0` | S | Reserved private client slots |
| `sv_privatePassword` | `` | — | Password for private slots |
| `sv_floodProtect` | `1` | SA | Flood protection |
| `sv_minRate` | `0` | SA | Minimum client rate |
| `sv_maxRate` | `0` | SA | Maximum client rate |
| `sv_dlRate` | `100` | SA | Download rate limit |
| `sv_dlURL` | `` | SA | Redirect download URL |
| `sv_minPing` | `0` | SA | Minimum allowed ping |
| `sv_maxPing` | `0` | SA | Maximum allowed ping |
| `sv_keywords` | `` | S | Server keywords |
| `sv_killserver` | `0` | — | Shutdown server |
| `sv_showloss` | `0` | — | Show packet loss |
| `sv_padPackets` | `0` | — | Pad packets to min size |
| `sv_banFile` | `serverbans.dat` | A | Ban list file |
| `sv_lanForceRate` | `1` | A | Force rate on LAN |
| `sv_master3` | `` | A | Master server 3 |
| `sv_master4` | `` | A | Master server 4 |
| `sv_master5` | `` | A | Master server 5 |
| `sv_paused` | `0` | R | Server is paused |
| `sv_running` | `0` | R | Server is running |
| `sv_pure` | `0` | s | Pure server mode |
| `sv_voip` | `1` | L | Server VoIP enabled |
| `sv_voipProtocol` | `opus` | sR | Server VoIP protocol |
| `sv_cheats` | `1` | sR | Cheats enabled |
| `sv_serverid` | `0` | sR | Unique server ID |
| `sv_referencedPaks` | `` | sR | Referenced pak checksums |
| `sv_referencedPakNames` | `` | sR | Referenced pak names |
| `sv_paks` | `` | sR | Loaded pak checksums |
| `sv_pakNames` | `` | sR | Loaded pak names |
| `sv_mapChecksum` | `` | R | Current map checksum |
| `mapname` | `nomap` | SR | Current map name |
| `nextmap` | `` | — | Next map to load |
| `rconPassword` | `` | — | Remote console password |
| `rconAddress` | `` | — | Remote console address |
| `sv_packetdelay` | `0` | C | Simulated server packet delay |
| `cl_packetdelay` | `0` | C | Simulated client packet delay |

---

## Game & Gameplay

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `g_gametype` | `2` | SAL | Game type |
| `g_gameskill` | `1` | SAL | Game skill level |
| `g_spSkill` | `2` | AL | SP skill level |
| `dmflags` | `0` | SA | Deathmatch flags |
| `fraglimit` | `20` | SA | Frag limit |
| `timelimit` | `0` | SA | Time limit |
| `capturelimit` | `8` | A? | CTF capture limit |
| `g_friendlyFire` | `1` | A? | Friendly fire |
| `g_warmup` | `20` | A? | Warmup time (s) |
| `g_doWarmup` | `0` | A? | Enable warmup period |
| `g_maxGameClients` | `0` | A? | Max game clients |
| `g_teamAutoJoin` | `0` | A? | Auto-join team |
| `g_teamForceBalance` | `0` | A? | Force team balance |
| `g_log` | `games.log` | A? | Game log file |
| `g_logsync` | `0` | A? | Sync game log writes |
| `g_banIPs` | `` | A? | Banned IP list |
| `g_reloading` | `0` | R | Game is reloading |
| `g_missionStats` | `0` | R | Mission stats |
| `g_localTeamPref` | `` | — | Preferred local team |
| `g_spScores1`–`5` | `` | A | SP score slots |
| `g_spAwards` | `` | A | SP awards |
| `g_spVideos` | `` | A | SP cutscene videos |
| `g_botsFile` | `` | RI | Bots definition file |
| `g_arenasFile` | `` | RI | Arenas definition file |
| `com_blood` | `1` | A | Enable blood effects |

---

## Physics & Simulation

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `timescale` | `1` | sC | Time scale (0.5=slow, 2=fast) |
| `fixedtime` | `0` | C | Fixed frame time |
| `timedemo` | `0` | C | Timedemo mode |
| `cm_playerCurveClip` | `1` | A? | Player clip against curves |

---

## System & Engine

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `com_maxfps` | `100` | A | Maximum FPS |
| `com_maxfpsUnfocused` | `0` | A | FPS cap when unfocused |
| `com_maxfpsMinimized` | `0` | A | FPS cap when minimised |
| `com_hunkMegs` | `256` | AL | Memory hunk size (MB) |
| `com_hunkused` | `3093888` | — | Current hunk memory used |
| `com_speeds` | `0` | — | Show frame timing breakdown |
| `com_showtrace` | `0` | C | Show collision traces |
| `com_buildScript` | `0` | — | Build script mode |
| `com_busyWait` | `0` | A | Busy-wait instead of sleep |
| `com_introplayed` | `1` | A | Intro video has played |
| `com_recommendedSet` | `1` | A | Recommended settings applied |
| `com_altivec` | `0` | A | Enable AltiVec SIMD |
| `com_ansiColor` | `0` | A | ANSI colour in console |
| `com_pipefile` | `` | AL | Pipe file for commands |
| `com_homepath` | `` | I | User home path override |
| `com_basegame` | `main` | I | Base game folder |
| `com_cameraMode` | `0` | C | Camera mode |
| `com_standalone` | `0` | R | Standalone game mode |
| `com_unfocused` | `0` | R | Window unfocused state |
| `com_minimized` | `0` | R | Window minimised state |
| `com_errorMessage` | `` | R | Last error message |
| `com_abnormalExit` | `0` | R | Abnormal exit flag |
| `com_gamename` | `wolfsp` | SI | Game name identifier |
| `com_protocol` | `50` | SI | Current network protocol |
| `com_legacyprotocol` | `49` | I | Legacy protocol version |
| `version` | `iortcw 1.51c-SP...` | SR | Engine version string |
| `protocol` | `49` | R | Protocol version |
| `developer` | `0` | — | Developer mode |
| `dedicated` | `0` | L | Dedicated server mode |
| `logfile` | `2` | — | Console log mode |
| `devdll` | `1` | ? | Developer DLL mode |

### File System

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `fs_basepath` | *(game dir)* | I | Base game path |
| `fs_homepath` | *(user dir)* | I | User data path |
| `fs_steampath` | *(steam dir)* | I | Steam installation path |
| `fs_gogpath` | `` | I | GOG installation path |
| `fs_game` | `` | sI | Current mod folder |
| `fs_basegame` | `` | I | Base game folder name |
| `fs_debug` | `0` | — | File system debug output |

### Virtual Machine

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `vm_cgame` | `0` | A | CGame VM type (0=native) |
| `vm_game` | `0` | A | Game VM type |
| `vm_ui` | `0` | A | UI VM type |
| `vm_minQvmHunkMegs` | `2` | A | Min QVM hunk memory |

---

## Console & Debug

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `scr_conspeed` | `3` | — | Console scroll speed |
| `con_notifytime` | `3` | — | Notification display time (s) |
| `con_autochat` | `1` | A | Console auto-chat |
| `con_autoclear` | `1` | A | Clear console input on submit |
| `con_debug` | `1` | A | Console debug output |
| `activeAction` | `` | — | Currently active action |
| `username` | `name` | — | System username |
| `arch` | `win_mingw x86` | — | CPU/platform architecture |
| `debuggraph` | `0` | C | Enable debug graph |
| `graphheight` | `32` | C | Debug graph height |
| `graphscale` | `1` | C | Debug graph scale |
| `graphshift` | `0` | C | Debug graph shift |
| `timegraph` | `0` | C | Enable time graph |

---

## Bots

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `bot_enable` | `1` | — | Enable bot support |
| `bot_minplayers` | `0` | — | Min players (fill with bots) |
| `bot_thinktime` | `100` | — | Bot think interval (ms) |
| `bot_reachability` | `0` | — | Show bot reachability |
| `bot_groundonly` | `1` | — | Bots use ground paths only |
| `bot_rocketjump` | `1` | — | Allow bots to rocket-jump |
| `bot_grapple` | `0` | — | Allow bots to use grapple |
| `bot_nochat` | `0` | — | Disable bot chat |
| `bot_fastchat` | `0` | — | Speed up bot chat |
| `bot_testichat` | `0` | — | Test inline bot chat |
| `bot_testrchat` | `0` | — | Test random bot chat |
| `bot_reloadcharacters` | `0` | — | Reload bot characters |
| `bot_developer` | `0` | — | Bot developer mode |
| `bot_debug` | `0` | — | Bot debug output |

---

## Player & User Info

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `name` | `WolfPlayer` | UA | Player name |
| `model` | `bj2` | UA | Player model |
| `head` | `default` | UA | Player head model |
| `color` | `4` | UA | Player colour |
| `sex` | `male` | UA | Player sex (model voice) |
| `handicap` | `100` | UA | Player handicap |
| `rate` | `25000` | UA | Network rate (bytes/s) |
| `snaps` | `20` | UA | Snapshot rate |
| `password` | `` | U | Server password |
| `cg_predictItems` | `1` | UA | Predict item pickups |
| `cg_selectedPlayer` | `0` | A | Selected player index |
| `cg_selectedPlayerName` | `WolfPlayer` | A | Selected player name |
| `cg_currentSelectedPlayer` | `0` | A? | Current selected player |
| `cg_currentSelectedPlayerName` | `` | A? | Current selected player name |
| `cg_deferPlayers` | `1` | A? | Defer player model loads |
| `cg_forceModel` | `0` | A? | Force player model |
| `journal` | `0` | I | Journal mode |

---

## UI

| CVar | Default | Flags | Description |
| `` `` | `` `` |---|---|
| `ui_initialized` | `0` | — | UI initialised flag |
| `ui_debug` | `0` | — | UI debug mode |
| `ui_cmd` | `` | — | Pending UI command |
| `ui_limboMode` | `0` | — | Limbo mode active |
| `ui_limboOptions` | `0` | — | Limbo options |
| `ui_prevTeam` | `0` | — | Previously selected team |
| `ui_prevClass` | `0` | — | Previously selected class |
| `ui_prevWeapon` | `0` | — | Previously selected weapon |
| `ui_mousePitch` | `0` | — | UI mouse pitch |
| `ui_smallFont` | `0.25` | A | Small font scale |
| `ui_bigFont` | `0.4` | A | Large font scale |
| `ui_netSource` | `1` | A | Server browser source |
| `ui_menuFiles` | `ui/menus.txt` | A | Menu definition file |
| `ui_gametype` | `3` | A | Selected gametype |
| `ui_joinGametype` | `0` | A | Join server gametype |
| `ui_netGametype` | `3` | A | Net server gametype |
| `ui_actualNetGametype` | `0` | A | Actual net gametype |
| `ui_mapIndex` | `0` | A | Selected map index |
| `ui_currentMap` | `1` | A | Current SP map index |
| `ui_currentNetMap` | `0` | A | Current net map index |
| `ui_WolfFirstRun` | `1` | A | First run flag |
| `ui_serverStatusTimeOut` | `7000` | A | Server status timeout (ms) |
| `ui_dedicated` | `0` | A | Dedicated server mode UI |
| `ui_master` | `0` | A | Master server index |
| `ui_browserMaster` | `0` | A | Browser master index |
| `ui_browserGameType` | `0` | A | Browser game type filter |
| `ui_browserShowFull` | `1` | A | Show full servers |
| `ui_browserShowEmpty` | `1` | A | Show empty servers |
| `ui_ffa_fraglimit` | `20` | A | FFA frag limit |
| `ui_ffa_timelimit` | `0` | A | FFA time limit |
| `ui_tourney_fraglimit` | `0` | A | Tourney frag limit |
| `ui_tourney_timelimit` | `15` | A | Tourney time limit |
| `ui_team_fraglimit` | `0` | A | Team frag limit |
| `ui_team_timelimit` | `20` | A | Team time limit |
| `ui_team_friendly` | `1` | A | Team friendly fire |
| `ui_ctf_capturelimit` | `8` | A | CTF capture limit |
| `ui_ctf_timelimit` | `30` | A | CTF time limit |
| `ui_ctf_friendly` | `0` | A | CTF friendly fire |
| `ui_savegameName` | `` | R | Current savegame name |
| `ui_spSelection` | `` | R | SP map selection |
| `ui_notebookCurrentPage` | `1` | R | Notebook current page |
| `ui_cdkeychecked` | `0` | R | CD key checked flag |
| `cg_hudFiles` | `ui/hud.txt` | A? | HUD layout file |
| `cg_oldWolfUI` | `0` | A? | Use old Wolf UI style |
| `cg_quickMessageAlt` | `1` | A? | Alt quick message style |
| `cg_teamChatsOnly` | `0` | A? | Team chats only |
| `cg_teamChatTime` | `3000` | A? | Team chat display time (ms) |
| `cg_teamChatHeight` | `8` | A? | Team chat lines shown |
| `cg_clipboardName` | `` | R | Clipboard player name |
| `server1`–`16` | `` | A | Saved server addresses |
