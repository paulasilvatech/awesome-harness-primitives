"""Synthetic regression tests; no .NET, container, or Azure execution."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from dotnet_common import InputError, framework_family, read_json
from inventory_dotnet import inventory, main as inventory_main
from validate_container_target import main as target_main, validate


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "application"
        self.root.mkdir()

    def write(self, name, content, encoding="utf-8"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding=encoding)
        return path

    def modern_project(self):
        return self.write(
            "Web/Web.csproj",
            '<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup>'
            '<TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>',
        )

    def test_sdk_project_and_solution_are_inventoried_without_execution(self):
        self.modern_project()
        self.write("Application.slnx", '<Solution><Project Path="Web/Web.csproj" /></Solution>')
        report = inventory(self.root)
        self.assertEqual(report["status"], "inventory-complete")
        self.assertEqual(report["solutions"], ["Application.slnx"])
        project = report["projects"][0]
        self.assertTrue(project["sdk_style"])
        self.assertEqual(project["declared_frameworks"], ["net10.0"])
        self.assertTrue(project["requires_msbuild_evaluation"])

    def test_legacy_namespaced_visual_basic_and_utf16(self):
        self.write(
            "Legacy.vbproj",
            '<?xml version="1.0" encoding="utf-16"?>'
            '<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">'
            '<PropertyGroup><TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion></PropertyGroup>'
            '<Import Project="Microsoft.VisualBasic.targets" /></Project>',
            encoding="utf-16",
        )
        project = inventory(self.root)["projects"][0]
        self.assertEqual(project["declared_frameworks"], ["net472"])
        self.assertEqual(project["framework_families"], ["net-framework"])
        self.assertFalse(project["sdk_style"])
        self.assertEqual(project["explicit_imports"], 1)

    def test_multitargeting_and_conditions_are_not_evaluated(self):
        self.write(
            "Shared.fsproj",
            '<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup Condition="\'$(Mode)\' == \'All\'">'
            '<TargetFrameworks>netstandard2.0;net10.0</TargetFrameworks></PropertyGroup></Project>',
        )
        project = inventory(self.root)["projects"][0]
        self.assertEqual(project["declared_frameworks"], ["net10.0", "netstandard2.0"])
        self.assertTrue(project["contains_conditions"])
        self.assertTrue(project["requires_msbuild_evaluation"])

    def test_shared_properties_are_not_invented_as_effective_targets(self):
        self.write("Web.csproj", '<Project Sdk="Microsoft.NET.Sdk.Web" />')
        self.write(
            "Directory.Build.props",
            '<Project><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup></Project>',
        )
        report = inventory(self.root)
        self.assertEqual(report["status"], "inventory-incomplete")
        self.assertEqual(report["projects"][0]["declared_frameworks"], [])
        self.assertEqual(report["shared_build_files"][0]["declared_frameworks"], ["net10.0"])
        self.assertFalse(report["shared_build_files"][0]["evaluated"])

    def test_unresolved_target_values_are_not_echoed(self):
        self.write(
            "App.csproj",
            '<Project><PropertyGroup><TargetFramework>not-a-tfm-PRIVATE_SENTINEL</TargetFramework>'
            '</PropertyGroup></Project>',
        )
        report = inventory(self.root)
        self.assertEqual(report["status"], "inventory-incomplete")
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(report))

    def test_project_references_normalize_windows_separators(self):
        self.write("Library/Lib.csproj", '<Project><TargetFramework>netstandard2.0</TargetFramework></Project>')
        self.write(
            "Web/Web.csproj",
            '<Project><TargetFramework>net10.0</TargetFramework><ItemGroup>'
            '<ProjectReference Include="..\\Library\\Lib.csproj" /></ItemGroup></Project>',
        )
        report = inventory(self.root)
        web = next(project for project in report["projects"] if project["path"] == "Web/Web.csproj")
        self.assertEqual(web["project_references"], ["Library/Lib.csproj"])
        self.assertEqual(report["status"], "inventory-complete")

    def test_missing_external_and_dynamic_references_are_incomplete(self):
        self.write(
            "App.csproj",
            '<Project><TargetFramework>net10.0</TargetFramework><ItemGroup>'
            '<ProjectReference Include="../outside.csproj" />'
            '<ProjectReference Include="missing.csproj" />'
            '<ProjectReference Include="$(SharedProject)" />'
            '</ItemGroup></Project>',
        )
        (self.root.parent / "outside.csproj").write_text("PRIVATE_SENTINEL", encoding="utf-8")
        report = inventory(self.root)
        self.assertEqual(report["status"], "inventory-incomplete")
        self.assertEqual(len(report["coverage"]["warnings"]), 3)
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(report))

    def test_known_build_output_and_explicit_exclusions_are_not_read(self):
        self.modern_project()
        self.write("OBJ/Generated.csproj", "not xml")
        self.write("vendor/Legacy.csproj", "not xml")
        report = inventory(self.root, exclude_dirs=("vendor",))
        self.assertEqual(len(report["projects"]), 1)
        self.assertEqual(report["status"], "inventory-complete")
        self.assertIn("vendor", report["coverage"]["excluded_directory_names"])

    def test_symlinked_files_and_directories_are_reported_not_followed(self):
        self.modern_project()
        outside = self.root.parent / "outside"
        outside.mkdir()
        (outside / "Secret.cs").write_text("PRIVATE_SENTINEL", encoding="utf-8")
        try:
            (self.root / "linked").symlink_to(outside, target_is_directory=True)
            (self.root / "Linked.cs").symlink_to(outside / "Secret.cs")
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        report = inventory(self.root)
        self.assertEqual(report["status"], "inventory-incomplete")
        self.assertEqual(len(report["coverage"]["warnings"]), 2)
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(report))

    def test_oversized_and_unsupported_encoding_inputs_are_visible(self):
        self.modern_project()
        self.write("Large.cs", "x" * 1000)
        (self.root / "Legacy.cs").write_bytes(b"\xffnot-utf8")
        report = inventory(self.root, max_bytes=300)
        self.assertEqual(report["status"], "inventory-incomplete")
        reasons = [warning["reason"] for warning in report["coverage"]["warnings"]]
        self.assertIn("file exceeds 300 bytes", reasons)
        self.assertIn("text is not UTF-8 or BOM-marked UTF-16", reasons)

    def test_web_forms_without_project_requires_manual_assessment(self):
        self.write("Default.aspx", '<%@ Page Language="C#" %>')
        report = inventory(self.root)
        self.assertEqual(report["status"], "inventory-incomplete")
        self.assertEqual(report["signals"][0]["signal"], "web-forms")
        self.assertEqual(report["projects"], [])

    def test_signals_include_locations_not_source_or_secret_values(self):
        self.modern_project()
        self.write(
            "web.config",
            '<configuration>\n<system.web><authentication mode="Windows" /></system.web>\n'
            '<connectionStrings><add name="db" connectionString="PRIVATE_SENTINEL" /></connectionStrings>'
            '</configuration>',
        )
        self.write("Interop.cs", 'using System.Drawing;\n[DllImport("PRIVATE_SENTINEL.dll")]')
        report = inventory(self.root)
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(report))
        signals = {item["signal"]: item for item in report["signals"]}
        self.assertEqual(signals["system-web"]["line"], 2)
        self.assertEqual(signals["native-interop"]["line"], 2)
        self.assertEqual(signals["drawing-review"]["confidence"], "heuristic")

    def test_package_names_are_collected_without_versions_or_credentials(self):
        self.write(
            "App.csproj",
            '<Project><TargetFramework>net10.0</TargetFramework><ItemGroup>'
            '<PackageReference Include="Example.Library" Version="PRIVATE_SENTINEL" />'
            '</ItemGroup></Project>',
        )
        self.write("packages.config", '<packages><package id="Legacy.Library" version="PRIVATE_SENTINEL" /></packages>')
        self.write("NuGet.Config", '<configuration><secret value="PRIVATE_SENTINEL" /></configuration>')
        report = inventory(self.root)
        self.assertEqual(report["projects"][0]["package_references"], ["Example.Library"])
        self.assertEqual(report["package_configs"][0]["package_ids"], ["Legacy.Library"])
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(report))

    def test_malformed_xml_and_dtds_fail_closed(self):
        for content in (
            '<Project><PRIVATE_SENTINEL',
            '<!DOCTYPE Project [<!ENTITY secret "PRIVATE_SENTINEL">]><Project />',
        ):
            with self.subTest(content=content):
                self.write("App.csproj", content)
                stdout, stderr = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                    result = inventory_main([str(self.root)])
                self.assertEqual(result, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertNotIn("PRIVATE_SENTINEL", stderr.getvalue())

    def test_invalid_roots_limits_and_exclusions_are_rejected(self):
        for root, limit, exclusions in (
            (self.root / "missing", 100, ()),
            (self.root, 0, ()),
            (self.root, 100, ("../outside",)),
        ):
            with self.subTest(root=root, limit=limit, exclusions=exclusions):
                with self.assertRaises(InputError):
                    inventory(root, limit, exclusions)

    def test_inventory_is_deterministic_and_does_not_mutate_source(self):
        project = self.modern_project()
        before = project.read_bytes()
        first = inventory(self.root)
        self.assertEqual(first, inventory(self.root))
        self.assertEqual(project.read_bytes(), before)
        self.assertEqual(list(self.root.rglob("*.json")), [])

    def test_cli_distinguishes_complete_incomplete_and_invalid_input(self):
        self.modern_project()
        for root, expected in ((self.root, 0), (self.root / "missing", 2)):
            with self.subTest(root=root):
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(inventory_main([str(root)]), expected)
        self.write("Unresolved.csproj", "<Project />")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(inventory_main([str(self.root)]), 1)


class ContainerTargetTests(unittest.TestCase):
    linux = {"Os": "linux", "Architecture": "amd64"}
    windows = {"Os": "windows", "Architecture": "amd64", "OsVersion": "10.0.20348.100"}

    def test_linux_amd64_modern_dotnet_fits_both_http_profiles(self):
        for target in ("aca", "appservice-linux"):
            with self.subTest(target=target):
                report = validate([self.linux], target, "net10.0", 8080, 8080)
                self.assertEqual(report["status"], "platform-consistent")
                self.assertTrue(report["unchecked"])
                self.assertEqual(report["policy"]["verified_on"], "2026-09-15")

    def test_windows_framework_fits_verified_windows_profile(self):
        report = validate(self.windows, "appservice-windows", "net481", 80, 80)
        self.assertEqual(report["status"], "platform-consistent")

    def test_windows_image_cannot_pass_linux_or_aca(self):
        for target in ("aca", "appservice-linux"):
            with self.subTest(target=target):
                report = validate(self.windows, target, "net10.0", 8080, 8080)
                self.assertEqual(report["status"], "incompatible")

    def test_linux_image_cannot_pass_windows_target(self):
        self.assertEqual(
            validate(self.linux, "appservice-windows", "net10.0", 8080, 8080)["status"],
            "incompatible",
        )

    def test_arm_and_x86_images_are_not_silently_accepted(self):
        for architecture in ("arm64", "arm", "386"):
            with self.subTest(architecture=architecture):
                image = dict(self.linux, Architecture=architecture)
                self.assertEqual(validate(image, "aca", "net10.0", 8080, 8080)["status"], "incompatible")

    def test_framework_standard_and_windows_tfms_do_not_pass_linux(self):
        for framework in ("net48", "net472", "netstandard2.0", "net10.0-windows10.0.19041.0", "net10.0-android"):
            with self.subTest(framework=framework):
                self.assertEqual(validate(self.linux, "aca", framework, 8080, 8080)["status"], "incompatible")

    def test_non_windows_platform_tfm_cannot_pass_windows(self):
        self.assertEqual(
            validate(self.windows, "appservice-windows", "net10.0-ios", 80, 80)["status"],
            "incompatible",
        )

    def test_windows_server_2025_and_unverified_bases_are_rejected(self):
        for build in ("26100", "14393", "99999"):
            with self.subTest(build=build):
                image = dict(self.windows, OsVersion=f"10.0.{build}.100")
                self.assertEqual(validate(image, "appservice-windows", "net48", 80, 80)["status"], "incompatible")

    def test_framework_481_and_ltsc2019_are_not_mixed(self):
        image = dict(self.windows, OsVersion="10.0.17763.100")
        self.assertEqual(validate(image, "appservice-windows", "net48", 80, 80)["status"], "platform-consistent")
        self.assertEqual(validate(image, "appservice-windows", "net481", 80, 80)["status"], "incompatible")

    def test_port_mismatch_is_not_a_pass(self):
        report = validate(self.linux, "aca", "net10.0", 8080, 80)
        self.assertEqual(report["status"], "incompatible")
        self.assertIn("port", report["problems"][0])

    def test_invalid_metadata_is_an_input_error_not_a_green_fallback(self):
        invalid = [
            {}, [], [self.linux, self.linux], "linux",
            {"Os": "linux", "Architecture": None},
            {"Os": "windows", "Architecture": "amd64"},
            dict(self.windows, OsVersion="ltsc2022"),
            {"manifests": [{"platform": {"os": "linux", "architecture": "amd64"}}]},
        ]
        for document in invalid:
            with self.subTest(document=document):
                with self.assertRaises(InputError):
                    validate(document, "aca", "net10.0", 8080, 8080)

    def test_invalid_target_framework_and_ports_are_rejected(self):
        for target, framework, listener in (
            ("unknown", "net10.0", 8080),
            ("aca", "$(Framework)", 8080),
            ("aca", "net10.0;net48", 8080),
            ("aca", "net10.0", True),
            ("aca", "net10.0", 0),
            ("aca", "net10.0", 65536),
        ):
            with self.subTest(target=target, framework=framework, listener=listener):
                with self.assertRaises(InputError):
                    validate(self.linux, target, framework, listener, 8080)

    def test_inspection_environment_and_labels_are_not_echoed(self):
        image = dict(self.linux, Config={"Env": ["SECRET=PRIVATE_SENTINEL"], "Labels": {"private": "PRIVATE_SENTINEL"}})
        self.assertNotIn("PRIVATE_SENTINEL", json.dumps(validate(image, "aca", "net10.0", 8080, 8080)))

    def test_cli_exit_codes_and_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inspect.json"
            args = [
                "--image-inspect", str(path), "--target", "aca", "--framework", "net10.0",
                "--listen-port", "8080", "--target-port", "8080",
            ]
            for document, expected in (
                (json.dumps(self.linux), 0),
                (json.dumps(self.windows), 1),
                ('{"Os":"windows","Os":"linux","Architecture":"amd64"}', 2),
                ("not JSON PRIVATE_SENTINEL", 2),
            ):
                with self.subTest(document=document):
                    path.write_text(document, encoding="utf-8")
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                        self.assertEqual(target_main(args), expected)
                    self.assertNotIn("PRIVATE_SENTINEL", stdout.getvalue() + stderr.getvalue())

    def test_read_json_rejects_linked_or_oversized_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inspect.json"
            path.write_text(json.dumps(self.linux), encoding="utf-8")
            with self.assertRaises(InputError):
                read_json(path, max_bytes=1)
            link = Path(directory) / "link.json"
            try:
                link.symlink_to(path)
            except OSError as error:
                self.skipTest(f"symlink creation unavailable: {error}")
            with self.assertRaises(InputError):
                read_json(link)

    def test_framework_classification(self):
        expected = {
            "net48": "net-framework", "net481": "net-framework", "net472": "net-framework",
            "netstandard2.0": "net-standard", "netcoreapp3.1": "net-core",
            "net10.0": "modern-dotnet", "net10.0-windows": "modern-dotnet",
            "$(Target)": "unknown", "net600": "unknown",
        }
        for framework, family in expected.items():
            with self.subTest(framework=framework):
                self.assertEqual(framework_family(framework), family)


if __name__ == "__main__":
    unittest.main()
