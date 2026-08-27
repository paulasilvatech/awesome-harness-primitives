---
name: minecraft-plugin-development
description: >-
  Guides Paper, Spigot, and Bukkit Minecraft server plugin development for plugin.yml setup,
  JavaPlugin bootstrap, commands, listeners, schedulers, player state, arenas, minigames,
  persistent progression, economy, configuration, Adventure text, and version-safe API usage. Use
  this skill when asked to build a Minecraft plugin, add a Paper command, fix a Bukkit listener,
  implement minigame mechanics, add perks or quests, or debug server plugin behavior.
---

<!-- Generated from harness/github-copilot/skills/minecraft-plugin-development/SKILL.md by harness/claude-code/scripts/convert_from_copilot.py. Edit the source, not this file. -->

# Minecraft plugin development

Build and modify Java Minecraft server plugins in the Paper, Spigot, and Bukkit ecosystem, including gameplay-heavy, cooldown-based, config-driven, multi-arena, match-heavy, and persistent-brawl systems. Keep runtime registration, thread safety, gameplay state, configuration, persistence, and validation aligned with the project’s targeted server API.

## When to invoke

- "Build a Minecraft plugin."
- "Add a Paper command and plugin.yml entry."
- "Fix this Bukkit listener."
- "Implement a minigame mechanic with arenas and phases."
- "Add a perk, quest, economy, or persistent profile system."

## Limits

- In scope: Paper, Spigot, Bukkit plugin development; `plugin.yml`; commands; tab completion; listeners; schedulers; configs; permissions; Adventure text; player state; minigame flow; arena instances; map copies; loot; waves; persistent profiles; perks; buffs; quests; economy; PvP/PvE game loops; Java-based architecture, debugging, refactoring, and feature implementation.
- Out of scope by default: Fabric mods, Forge mods, client mods, and Bedrock add-ons.
- If the user says "Minecraft plugin" but the stack is unclear, determine whether the project is Paper/Spigot/Bukkit or a modding stack before editing.

## Project discovery

Check these files and concepts before changing behavior:

- `plugin.yml`
- `pom.xml`, `build.gradle`, or `build.gradle.kts`
- main class extending `JavaPlugin`
- command executors and tab completers
- listener classes
- config bootstrap for `config.yml`, messages, kits, arenas, or custom YAML files
- generated resource output such as `target/classes`, `build/resources`, or copied plugin jars
- scheduler usage through Bukkit scheduler APIs
- player data, team state, arena state, or match state containers

Identify the server API and version target, build system, Java version, startup registration, gameplay lifecycle, timers, scheduled tasks, teams, arenas, match state, config, and persistence before making a coherent change.

## Core implementation rules

| Area | Rule |
| --- | --- |
| Server API | If the project targets Paper APIs, keep using Paper-first APIs unless Spigot/Bukkit compatibility is explicitly required. Do not assume an API exists across versions; check dependencies and surrounding style. |
| Registration | When adding commands, permissions, or listeners, update `plugin.yml`, startup registration in `onEnable`, permission checks, and related config/message keys together. |
| Main thread | Do not touch world state, entities, inventories, scoreboards, or most Bukkit API objects from async tasks unless the API explicitly permits it. Use async for I/O or heavy work, then switch back to the main thread. |
| State modeling | Prefer explicit match/game phase, player role/class, cooldown, team membership, arena assignment, and alive/eliminated/spectating/queued state over scattered booleans. |
| Arena isolation | Isolate `per-arena` and per-game visibility, chat recipients, scoreboards, loot, broadcasts, and entity ownership. Do not let one arena observe or mutate another. |
| Config | Keep damage, cooldowns, rewards, durations, messages, map settings, and toggles config-backed with stable names, defaults, and validation. |
| Reloads | Avoid promising safe hot reload unless the code already supports it; reload must handle caches, scheduled tasks, and gameplay state consistently. |

## Commands, listeners, tasks, and state

For commands, add the `plugin.yml` declaration, implement executor and tab completion when needed, validate `CommandSender` before casting to `Player`, separate parsing from permission and gameplay logic, and send clear feedback.

```yaml
commands:
  arena:
    description: Join or leave an arena
    usage: /arena <join|leave>
```

```java
@Override
public void onEnable() {
    ArenaCommand command = new ArenaCommand(gameService);
    PluginCommand arena = getCommand("arena");
    if (arena != null) {
        arena.setExecutor(command);
        arena.setTabCompleter(command);
    }
}
```

For listeners, guard early, verify player/arena/phase ownership, avoid expensive work in hot events such as move, damage, or interact spam, and centralize repeated checks.

For scheduled tasks, store task handles when cancellation matters, cancel tasks in `onDisable` and when a match or arena ends, avoid overlapping tasks for the same concern, prefer one authoritative game loop, and make countdown or refill tasks self-cancel when the game leaves the expected state.

```java
Bukkit.getScheduler().runTaskAsynchronously(plugin, () -> {
    PlayerData data = repository.load(playerId);
    Bukkit.getScheduler().runTask(plugin, () -> {
        Player player = Bukkit.getPlayer(playerId);
        if (player != null && player.isOnline()) {
            scoreboard.update(player, data);
        }
    });
});
```

For per-player, per-match, and long-lived player state, define ownership clearly, clean up on quit, kick, death, match end, and plugin disable, avoid stale maps keyed by `Player`, and prefer `UUID` for persistent tracking unless a live player object is strictly needed.

When the project uses Adventure or MiniMessage, follow the existing formatting approach for player-facing and game-specific text, avoid mixing legacy color codes and Adventure styles without a reason, and keep gameplay-facing messages configurable.

## High-risk areas

Pay extra attention when editing damage handling, custom combat logic, death/respawn/spectator/elimination flow, arena join/leave flow, scoreboards, boss bars, inventory mutation, kit distribution, async database or file access, economy, quest, perk and profile mutation, custom event dispatch, extension registries, version-sensitive API calls, shutdown and cleanup in `onDisable`, cross-arena visibility/chat/broadcast isolation, map copy/unload/folder deletion, mob/NPC/projectile/temporary entity ownership, and chest/container or resource refill systems, and in-memory caches.

## Procedure

1. Identify the server API/version, build system, Java version, main plugin class, `plugin.yml`, commands, listeners, and relevant config.
2. Map player lifecycle, game phases, scheduled tasks, team/arena/match state, persistence, and generated resources before editing.
3. Read bundled references on demand for the feature area named below.
4. Implement the smallest coherent code, resource, and registration change.
5. Validate build output, resource generation, config defaults, and runtime lifecycle paths.

## Progressive disclosure and bundled resources

Load these references only when the task touches the named area:

- `references/project-patterns.md`: high-level architecture patterns seen in real gameplay plugins.
- `references/bootstrap-registration.md`: `onEnable`, command wiring, listener registration, and shutdown expectations.
- `references/state-sessions-and-phases.md`: player session modeling, game phases, match state, and reconnect-safe logic.
- `references/config-data-and-async.md`: config managers, database-backed player data, async flushes, and UI refresh tasks.
- `references/maps-heroes-and-feature-modules.md`: map rotation, hero/class systems, and modular feature growth.
- `references/minigame-instance-flow.md`: arena instances, countdowns, loot refreshes, wave systems, visibility isolation, and entity-to-game ownership.
- `references/persistent-progression-and-events.md`: long-running PvP servers with profiles, perks, buffs, quests, economy, custom domain events, and extension registries.
- `references/build-test-and-runtime-validation.md`: Maven or Gradle packaging, shaded dependencies, generated resources, soft dependencies, config validation commands, and first-round server test plans.

## Gotchas

- **Never cast `CommandSender` to `Player` without checking**: console and command blocks can execute commands.
- **Never mutate Bukkit world state from async tasks**: use the scheduler to hand off to the main thread.
- Forgetting listener registration or `plugin.yml` command declarations makes correct Java code unreachable.
- Long-lived maps keyed by `Player` can leak; use `UUID` for persistent state.
- Repeating tasks must stop after round, arena, or plugin shutdown.
- Hardcoded gameplay constants should usually live in config.
- Paper-only APIs break Spigot targets unless compatibility is explicit.
- Stateful plugins often break under reload; treat reload as a lifecycle feature, not a free operation.
- Broadcasting, showing players, or applying scoreboards across unrelated game instances breaks arena isolation.
- Generated files under `target/classes` or `build/resources` are not source; edit `src/main/resources` instead.

## Output expectations

Produce runnable Java code, not pseudo-code, unless the user asks for design only. For substantial requests, report current plugin context and assumptions, gameplay or lifecycle impact, code changes, required registration or config updates, validation, remaining risks, and thread-safety notes.

## Output template

```markdown
## Minecraft plugin change — <feature or bug>

**Status:** implemented | design only | blocked
**Server API:** Paper | Spigot | Bukkit | unknown
**Version assumptions:** <API and Java version>

### Current plugin context
- Main class: `<class extending JavaPlugin>`
- Registration touched: `plugin.yml`, `onEnable`, listeners, commands, permissions
- Gameplay lifecycle impact: <players, arenas, tasks, persistence>

### Changes
| File | Change | Reason |
| --- | --- | --- |
| `src/main/java/...` | <code behavior> | <why> |
| `src/main/resources/plugin.yml` | <command/permission> | <why> |

### Validation
- Build: pass | fail | not run
- Runtime registration: verified | not verified
- Thread-safety and cleanup paths: verified | risks listed
```

## Quality gate

- [ ] The targeted server API and version assumptions are explicit.
- [ ] `plugin.yml` matches implemented commands, permissions, and main class behavior.
- [ ] Command sender types are checked before casting to `Player`.
- [ ] Listener and command registration is wired through `onEnable`.
- [ ] Scheduler usage respects Bukkit main-thread boundaries.
- [ ] Config keys exist or have defaults and validation.
- [ ] State cleanup covers player quit, kick, death, match end, and `onDisable` where relevant.
- [ ] Per-arena chat, visibility, scoreboards, broadcasts, temporary worlds, mobs, tasks, and generated resources are isolated or cleaned up.
- [ ] Build/test/runtime validation from the project’s existing Maven or Gradle setup was run when available.
