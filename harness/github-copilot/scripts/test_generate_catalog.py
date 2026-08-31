from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import generate_catalog
import validate_primitives


class GenerateCatalogTests(unittest.TestCase):
    def test_fallback_yaml_preserves_escaped_apostrophe(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "demo.prompt.md"
            path.write_text(
                "---\n"
                "description: 'Create from this repository''s templates.'\n"
                "---\n"
                "# Demo\n",
                encoding="utf-8",
            )

            with patch.object(validate_primitives, "yaml", None):
                frontmatter, _ = generate_catalog.document_parts(path)

        self.assertEqual(
            frontmatter["description"],
            "Create from this repository's templates.",
        )

    def test_split_description_separates_explicit_use_case(self) -> None:
        description, use_case = generate_catalog.split_description(
            "Reviews API contracts. Use when an endpoint changes."
        )

        self.assertEqual(description, "Reviews API contracts.")
        self.assertEqual(use_case, "Use when an endpoint changes.")

    def test_activation_from_body_uses_first_two_bullets(self) -> None:
        body = """# Example

## When to invoke

- Review a changed API.
- Diagnose a compatibility regression.
- Ignore this third example.

## Procedure
"""

        self.assertEqual(
            generate_catalog.activation_from_body(body),
            "Review a changed API. Diagnose a compatibility regression.",
        )

    def test_activation_from_body_prefers_introductory_scope(self) -> None:
        body = """# Example

## Activation and Scope

Select this agent when an API contract needs specialist review.

- **Editing policy:** Change only contract files.

## Procedure
"""

        self.assertEqual(
            generate_catalog.activation_from_body(body),
            "Select this agent when an API contract needs specialist review.",
        )

    def test_build_catalog_covers_all_primitive_types_and_source_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for directory in ("agents", "instructions", "skills/demo-skill", "prompts", "plugins/demo-plugin", "hooks/demo-hook"):
                (root / directory).mkdir(parents=True, exist_ok=True)

            (root / "agents/demo.agent.md").write_text(
                "---\ndescription: Reviews demos. Use when a demo changes.\n---\n# Demo\n",
                encoding="utf-8",
            )
            (root / "instructions/demo.instructions.md").write_text(
                "---\napplyTo: '**/*.demo'\ndescription: Defines demo conventions.\n---\n# Demo\n",
                encoding="utf-8",
            )
            (root / "skills/demo-skill/SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: Runs the demo workflow.\n---\n"
                "# Demo\n\n## When to invoke\n\n- Run a representative demo.\n",
                encoding="utf-8",
            )
            (root / "prompts/demo.prompt.md").write_text(
                "---\ndescription: Generates a demo.\n---\n"
                "# Demo\n\n## When to Invoke\n\n- Generate a new demo.\n",
                encoding="utf-8",
            )
            (root / "plugins/demo-plugin/plugin.json").write_text(
                '{"name":"demo-plugin","version":"1.0.0","description":"Bundles demos.",'
                '"keywords":["demo"],"agents":"agents/","skills":"skills/"}\n',
                encoding="utf-8",
            )
            (root / "plugins/demo-plugin/agents").mkdir()
            (root / "plugins/demo-plugin/skills/demo-skill").mkdir(
                parents=True
            )
            (root / "plugins/demo-plugin/agents/demo.agent.md").write_text(
                "---\ndescription: Demo\n---\n", encoding="utf-8"
            )
            (
                root
                / "plugins/demo-plugin/skills/demo-skill/SKILL.md"
            ).write_text(
                "---\n"
                "name: demo-skill\n"
                "description: Runs plugin demos.\n"
                "---\n"
                "# Demo skill\n",
                encoding="utf-8",
            )
            (root / "hooks/demo-hook/hooks.json").write_text(
                '{"version":1,"hooks":{"sessionEnd":[]}}\n', encoding="utf-8"
            )
            (root / "hooks/demo-hook/README.md").write_text(
                "---\nname: Demo Hook\ndescription: Checks demos at session end.\n---\n"
                "# Demo Hook\n",
                encoding="utf-8",
            )

            source_map = {
                "demo-plugin": {
                    "componentSource": "plugin",
                    "sharedSkills": ["./skills/demo-skill/"],
                }
            }
            with (
                patch.object(generate_catalog, "SOURCE_ROOT", root),
                patch.object(
                    generate_catalog,
                    "load_plugin_sources",
                    return_value=source_map,
                ),
            ):
                catalog = generate_catalog.build_catalog()

        for heading in (
            "## Agents",
            "## Instructions",
            "## Skills",
            "## VS Code Prompts",
            "## Plugin Components",
            "## Plugins",
            "## Hooks",
        ):
            self.assertIn(heading, catalog)
        self.assertIn("Use cases", catalog)
        self.assertIn("Use when a demo changes.", catalog)
        self.assertIn("[source](", catalog)
        self.assertIn("1 agent", catalog)
        self.assertIn("demo-plugin:demo", catalog)
        self.assertIn("Plugin-owned", catalog)
        self.assertIn("Shared library copy", catalog)
        self.assertIn("sessionEnd", catalog)


if __name__ == "__main__":
    unittest.main()
