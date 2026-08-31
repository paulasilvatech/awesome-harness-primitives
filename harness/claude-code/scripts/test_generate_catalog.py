from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import generate_catalog


class ClaudeCatalogTests(unittest.TestCase):
    def test_collect_lists_every_plugin_component_separately(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = {
                "AGENTS_ROOT": root / "agents",
                "RULES_ROOT": root / "rules",
                "SKILLS_ROOT": root / "skills",
                "COMMANDS_ROOT": root / "commands",
                "HOOKS_ROOT": root / "hooks",
                "PLUGINS_ROOT": root / "plugins",
                "PLUGIN_PROVENANCE_PATH": root / "plugin-sources.json",
            }
            for name, path in paths.items():
                if name == "PLUGIN_PROVENANCE_PATH":
                    continue
                path.mkdir(parents=True)
            paths["PLUGIN_PROVENANCE_PATH"].write_text(
                json.dumps(
                    {
                        "plugins": {
                            "demo-plugin": {
                                "upstreamRepository": (
                                    "https://github.com/github/awesome-copilot"
                                )
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            plugin = paths["PLUGINS_ROOT"] / "demo-plugin"
            (plugin / ".claude-plugin").mkdir(parents=True)
            (plugin / "agents").mkdir()
            (plugin / "skills/demo-skill").mkdir(parents=True)
            (plugin / "commands").mkdir()
            (plugin / "hooks").mkdir()
            (plugin / "extensions/demo-extension").mkdir(parents=True)

            (plugin / ".claude-plugin/plugin.json").write_text(
                json.dumps(
                    {
                        "name": "demo-plugin",
                        "version": "1.0.0",
                        "description": "Demo plugin.",
                    }
                ),
                encoding="utf-8",
            )
            (plugin / "agents/demo-agent.md").write_text(
                "---\nname: demo-agent\ndescription: Reviews demos.\n---\n# Demo\n",
                encoding="utf-8",
            )
            (plugin / "skills/demo-skill/SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: Runs demos.\n---\n# Demo\n",
                encoding="utf-8",
            )
            (plugin / "commands/demo-command.md").write_text(
                "---\ndescription: Starts demos.\n---\n# Demo\n",
                encoding="utf-8",
            )
            (plugin / "hooks/hooks.json").write_text(
                '{"hooks":{"SessionEnd":[]}}\n',
                encoding="utf-8",
            )
            (plugin / ".mcp.json").write_text(
                '{"mcpServers":{"demo-mcp":{"type":"stdio"}}}\n',
                encoding="utf-8",
            )
            (plugin / "extensions/demo-extension/package.json").write_text(
                '{"name":"demo-extension","description":"Shows demos."}\n',
                encoding="utf-8",
            )

            with patch.multiple(generate_catalog, **paths):
                data = generate_catalog.collect()
                catalog = generate_catalog.render(data)

        qualified = {
            f"{item['plugin']}:{item['name']}"
            for item in data["plugin-components"]
        }
        self.assertEqual(
            qualified,
            {
                "demo-plugin:demo-agent",
                "demo-plugin:demo-command",
                "demo-plugin:demo-extension",
                "demo-plugin:demo-mcp",
                "demo-plugin:demo-skill",
                "demo-plugin:hooks",
            },
        )
        self.assertIn("## Plugin Components", catalog)
        self.assertIn("Copied payload; not a Claude component", catalog)
        self.assertEqual(
            data["plugins"][0]["upstream"],
            "https://github.com/github/awesome-copilot",
        )
        self.assertIn(
            "[github/awesome-copilot]"
            "(https://github.com/github/awesome-copilot)",
            generate_catalog.render_index(
                generate_catalog.page_definitions(data),
                Path("/tmp/docs/catalog/claude-code.md"),
                Path("/tmp/docs/catalog/claude-code"),
            ),
        )


if __name__ == "__main__":
    unittest.main()
