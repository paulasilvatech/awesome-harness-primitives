#!/usr/bin/env python3
"""Build the draw.io showcase gallery for the azure-architecture-diagrams skill.

The gallery demonstrates that the skill is not tied to one layout. It produces
multiple editable draw.io pages, each using the paulasilva-ms visual language and
the right diagram shape for a different architecture question.
"""

from __future__ import annotations

import html
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "showcase-diagrams.drawio"

WIDE = (1600, 900)
PORTRAIT = (1000, 1300)

COLORS = {
    "red": "#F25022",
    "green": "#7FBA00",
    "blue": "#00A4EF",
    "yellow": "#FFB900",
    "ink": "#181B1F",
    "muted": "#5E636B",
    "line": "#DCE0E5",
    "paper": "#FFFFFF",
    "bg": "#FAFBFC",
}

ICON_APIM = "azure.apim"
ICON_ENTRA = "azure.entra"
ICON_FOUNDRY = "azure.foundry"
ICON_MONITOR = "azure.monitor"
ICON_REDIS = "azure.redis"
ICON_SEARCH = "azure.search"

SERVICE_APIM = "Azure API Management"
SERVICE_FOUNDRY = "Azure AI Foundry Agent Service"

ICON_STYLE = {
    "box": "rounded=1;whiteSpace=wrap;html=1;",
    "user": "shape=mxgraph.basic.user;html=1;",
    "database": "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;",
    "github": "shape=mxgraph.gcp2.github;html=1;",
    ICON_APIM: "sketch=0;html=1;shape=mxgraph.azure.api_management_services;",
    ICON_ENTRA: "sketch=0;html=1;shape=mxgraph.azure.azure_active_directory;",
    ICON_FOUNDRY: "sketch=0;html=1;shape=mxgraph.azure.machine_learning;",
    "azure.keyvault": "sketch=0;html=1;shape=mxgraph.azure.key_vaults;",
    ICON_MONITOR: "sketch=0;html=1;shape=mxgraph.azure.monitor;",
    "azure.openai": "sketch=0;html=1;shape=mxgraph.azure.cognitive_services;",
    ICON_REDIS: "sketch=0;html=1;shape=mxgraph.azure.azure_cache_redis;",
    ICON_SEARCH: "sketch=0;html=1;shape=mxgraph.azure.azure_search;",
}


def enc(value: str) -> str:
    return html.escape(value, quote=True)


class Page:
    def __init__(self, name: str, width: int = WIDE[0], height: int = WIDE[1]):
        self.name = name
        self.width = width
        self.height = height
        self.root = ET.Element("root")
        ET.SubElement(self.root, "mxCell", {"id": "0"})
        ET.SubElement(self.root, "mxCell", {"id": "1", "parent": "0"})

    def cell(self, cell_id: str, value: str, style: str, x: int, y: int, w: int, h: int, parent: str = "1") -> None:
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {
                "id": cell_id,
                "value": value,
                "style": style,
                "vertex": "1",
                "parent": parent,
            },
        )
        ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})

    def title(self, title: str, subtitle: str) -> None:
        self.cell(
            "title",
            f"&lt;b&gt;&lt;font style='font-size:24px'&gt;{enc(title)}&lt;/font&gt;&lt;/b&gt;&lt;br&gt;&lt;font color='{COLORS['muted']}'&gt;{enc(subtitle)}&lt;/font&gt;",
            "text;html=1;align=left;verticalAlign=top;fontColor=#181B1F;",
            36,
            24,
            self.width - 72,
            64,
        )
        stripe_x = 36
        for idx, color in enumerate(("red", "green", "blue", "yellow")):
            self.cell(f"stripe_{idx}", "", f"rounded=0;fillColor={COLORS[color]};strokeColor=none;", stripe_x + idx * 28, 92, 22, 5)

    def boundary(self, cell_id: str, label: str, x: int, y: int, w: int, h: int, fill: str, stroke: str, text: str | None = None) -> None:
        text_color = text or stroke
        self.cell(
            cell_id,
            f"  {enc(label)}",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={COLORS['line']};strokeWidth=1.5;verticalAlign=top;align=left;spacing=8;fontStyle=1;fontSize=13;fontColor={text_color};arcSize=3;",
            x,
            y,
            w,
            h,
        )

    def node(self, cell_id: str, title: str, detail: str, x: int, y: int, w: int, h: int, accent: str, icon: str = "box") -> None:
        value = f"&lt;b&gt;{enc(title)}&lt;/b&gt;&lt;br&gt;&lt;font color='{COLORS['muted']}'&gt;{enc(detail)}&lt;/font&gt;"
        self.cell(
            cell_id,
            value,
            "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#E8EBEF;strokeWidth=1.5;align=left;verticalAlign=top;spacing=9;spacingLeft=14;fontSize=11;fontColor=#181B1F;arcSize=8;",
            x,
            y,
            w,
            h,
        )
        self.cell(f"{cell_id}_a", "", f"rounded=0;fillColor={COLORS[accent]};strokeColor=none;", x, y, 5, h)
        self.cell(
            f"{cell_id}_i",
            "",
            f"{ICON_STYLE.get(icon, ICON_STYLE['box'])}verticalLabelPosition=bottom;verticalAlign=top;",
            x + w - 48,
            y + 14,
            30,
            30,
        )

    def step(self, cell_id: str, label: str, x: int, y: int, w: int, h: int, accent: str) -> None:
        self.cell(
            cell_id,
            f"&lt;b&gt;{enc(label)}&lt;/b&gt;",
            f"rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor={COLORS[accent]};strokeWidth=2;align=center;verticalAlign=middle;fontSize=12;fontColor=#181B1F;arcSize=8;",
            x,
            y,
            w,
            h,
        )

    def edge(self, cell_id: str, source: str, target: str, label: str, color: str = "muted", dashed: bool = False) -> None:
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor={COLORS[color]};strokeWidth=2;endArrow=block;fontSize=11;labelBackgroundColor=#FFFFFF;"
        if dashed:
            style += "dashed=1;"
        cell = ET.SubElement(
            self.root,
            "mxCell",
            {"id": cell_id, "value": enc(label), "style": style, "edge": "1", "parent": "1", "source": source, "target": target},
        )
        ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})

    def diagram(self) -> ET.Element:
        diagram = ET.Element("diagram", {"name": self.name, "id": self.name.lower().replace(" ", "-")})
        model = ET.SubElement(
            diagram,
            "mxGraphModel",
            {
                "dx": "1600",
                "dy": "900",
                "grid": "1",
                "gridSize": "10",
                "guides": "1",
                "connect": "1",
                "arrows": "1",
                "page": "1",
                "pageWidth": str(self.width),
                "pageHeight": str(self.height),
                "math": "0",
                "background": COLORS["bg"],
            },
        )
        model.append(self.root)
        return diagram


def system_context() -> Page:
    p = Page("01 System Context")
    p.title("System Context", "Best when the audience needs the actors, boundaries, and external dependencies first.")
    p.boundary("b_system", "SYSTEM BOUNDARY · Contoso AI platform", 330, 150, 860, 430, "#FFF6F2", COLORS["red"])
    p.node("dev", "Developer", "Uses GitHub Copilot in the IDE", 80, 290, 190, 80, "ink" if "ink" in COLORS else "blue", "user")
    p.node("ghe", "GitHub Enterprise", "Policy and GitHub Copilot controls", 380, 230, 230, 90, "blue", "github")
    p.node("apim", SERVICE_APIM, "Private gateway and tool policy", 690, 230, 230, 90, "yellow", ICON_APIM)
    p.node("foundry", SERVICE_FOUNDRY, "Runs agent threads and tools", 880, 410, 250, 90, "green", ICON_FOUNDRY)
    p.node("systems", "Enterprise systems", "Private APIs, data and records", 1260, 300, 220, 90, "ink" if "ink" in COLORS else "blue", "database")
    p.edge("e1", "dev", "ghe", "GitHub Copilot request", "blue")
    p.edge("e2", "ghe", "apim", "MCP registry and tools", "yellow")
    p.edge("e3", "apim", "foundry", "authenticated HTTPS", "green")
    p.edge("e4", "foundry", "systems", "governed tool access", "muted")
    return p


def component_map() -> Page:
    p = Page("02 Component Map")
    p.title("Component Map", "Best when engineers need runtime responsibilities without deployment detail.")
    p.boundary("b_runtime", "AGENT RUNTIME · model routing, context, tools and telemetry", 180, 140, 1240, 560, "#FFFAEE", "#AA7800")
    p.node("router", "Model router", "Classifies task, cost and risk", 250, 250, 210, 90, "yellow", "box")
    p.node("foundry", SERVICE_FOUNDRY, "Threads, runs and orchestration", 560, 250, 240, 90, "green", ICON_FOUNDRY)
    p.node("tools", "MCP tool surface", "Small, governed tool contracts", 900, 250, 220, 90, "blue", "box")
    p.node("redis", "Azure Managed Redis", "Semantic cache and session state", 300, 470, 220, 90, "green", ICON_REDIS)
    p.node("search", "Azure AI Search", "Ranked enterprise retrieval", 610, 470, 220, 90, "blue", ICON_SEARCH)
    p.node("monitor", "Azure Monitor", "Traces, token and cost signals", 920, 470, 220, 90, "red", ICON_MONITOR)
    p.edge("e1", "router", "foundry", "route by class", "yellow")
    p.edge("e2", "foundry", "tools", "invoke tool", "blue")
    p.edge("e3", "foundry", "redis", "cache read/write", "green")
    p.edge("e4", "foundry", "search", "retrieve context", "blue")
    p.edge("e5", "foundry", "monitor", "OpenTelemetry", "red", True)
    return p


def deployment_topology() -> Page:
    p = Page("03 Deployment Topology")
    p.title("Deployment Topology", "Best when the question is where services live, how private access works, and what identity crosses boundaries.")
    p.boundary("sub", "AZURE SUBSCRIPTION · production landing zone", 110, 130, 1360, 620, "#EEF7FF", COLORS["blue"])
    p.boundary("rg", "RESOURCE GROUP · rg-agentic-prod", 170, 205, 1240, 460, "#FFFAEE", "#AA7800")
    p.boundary("vnet", "VNET · private endpoints and workload subnet", 230, 285, 1120, 300, "#F4FAEE", "#4A7A00")
    p.node("entra", "Microsoft Entra ID", "Managed identity and RBAC", 230, 220, 210, 80, "blue", ICON_ENTRA)
    p.node("apim", SERVICE_APIM, "Private endpoint ingress", 300, 370, 220, 80, "yellow", ICON_APIM)
    p.node("foundry", SERVICE_FOUNDRY, "Agent runtime", 610, 370, 240, 80, "green", ICON_FOUNDRY)
    p.node("search", "Azure AI Search", "Private index endpoint", 930, 325, 220, 80, "blue", ICON_SEARCH)
    p.node("redis", "Azure Managed Redis", "Private cache endpoint", 930, 460, 220, 80, "green", ICON_REDIS)
    p.node("kv", "Azure Key Vault", "Secrets and keys, narrow access", 300, 500, 220, 80, "red", "azure.keyvault")
    p.node("mon", "Azure Monitor", "Logs and traces", 1190, 460, 170, 80, "blue", ICON_MONITOR)
    p.edge("e1", "entra", "apim", "MI token", "blue")
    p.edge("e2", "apim", "foundry", "private HTTPS", "yellow")
    p.edge("e3", "foundry", "search", "RAG", "blue")
    p.edge("e4", "foundry", "redis", "memory", "green")
    p.edge("e5", "foundry", "mon", "telemetry", "muted", True)
    return p


def critical_path() -> Page:
    p = Page("04 Critical Path")
    p.title("Critical Path Flow", "Best when the audience needs to understand one run end-to-end and where controls are applied.")
    p.boundary("path", "ONE AGENT RUN · numbered flow with control points", 90, 155, 1420, 520, "#F8F9FA", COLORS["muted"])
    steps = [
        ("s1", "1. Request", "Developer asks GitHub Copilot", 150, "user", "blue"),
        ("s2", "2. Validate", "APIM checks token and policy", 390, ICON_APIM, "yellow"),
        ("s3", "3. Cache", "Redis semantic cache lookup", 630, ICON_REDIS, "green"),
        ("s4", "4. Retrieve", "Azure AI Search context pack", 870, ICON_SEARCH, "blue"),
        ("s5", "5. Run", "Foundry agent executes tools", 1110, ICON_FOUNDRY, "green"),
    ]
    for cell_id, title, detail, x, icon, accent in steps:
        p.node(cell_id, title, detail, x, 285, 190, 92, accent, icon)
    p.node("s6", "6. Observe", "Trace, tokens, cost and errors", 630, 500, 250, 90, "red", ICON_MONITOR)
    for idx in range(1, 5):
        p.edge(f"e{idx}", f"s{idx}", f"s{idx+1}", "next", "blue")
    p.edge("e5", "s5", "s6", "OpenTelemetry", "red", True)
    return p


def routing_decision() -> Page:
    p = Page("05 Routing Decision", PORTRAIT[0], PORTRAIT[1])
    p.title("Routing Decision", "Best when the architecture question is decision logic, not infrastructure placement.")
    p.boundary("decision", "ROUTING LOGIC · risk, context and cost", 90, 150, 820, 980, "#F8F9FA", COLORS["muted"])
    p.step("start", "Incoming agent task", 380, 230, 220, 70, "blue")
    p.step("risk", "High impact or sensitive data?", 340, 360, 300, 75, "red")
    p.step("approval", "Approval gate", 130, 515, 230, 75, "red")
    p.step("context", "Needs enterprise context?", 545, 515, 250, 75, "yellow")
    p.node("premium", "Premium route", "frontier model with reviewer", 120, 710, 240, 90, "red", ICON_FOUNDRY)
    p.node("retrieve", "RAG route", "retrieve before answer", 545, 700, 250, 90, "blue", ICON_SEARCH)
    p.node("fast", "Mini-first route", "fast and low-cost answer", 375, 875, 250, 90, "green", "azure.openai")
    p.edge("e1", "start", "risk", "classify", "blue")
    p.edge("e2", "risk", "approval", "yes", "red")
    p.edge("e3", "risk", "context", "no", "yellow")
    p.edge("e4", "approval", "premium", "approved", "red")
    p.edge("e5", "context", "retrieve", "yes", "blue")
    p.edge("e6", "context", "fast", "no", "green")
    return p


def registry_planes() -> Page:
    p = Page("06 Enterprise Registry", 2016, 1187)
    p.title("Enterprise Registry Planes", "Best for executive plus technical reviews where the network, policy, registry and use plane must fit on one canvas.")
    planes = [
        ("client", "CLIENTS · outside the corporate network", 90, 120, 1836, 115, "#F8F9FA", COLORS["ink"]),
        ("access", "PRIVATE ACCESS · Microsoft Entra Private Access", 90, 285, 1836, 120, "#EEF7FF", COLORS["blue"]),
        ("disc", "DISCOVERY PLANE · corporate VNet", 90, 455, 1836, 340, "#FFFAEE", "#AA7800"),
        ("use", "USE PLANE · authenticated tool calls", 90, 845, 1836, 120, "#F4FAEE", "#4A7A00"),
        ("gov", "IDENTITY, OBSERVABILITY AND GOVERNANCE", 90, 1015, 1836, 95, "#F7F8FA", COLORS["muted"]),
    ]
    for args in planes:
        p.boundary(*args)
    p.node("ghe", "GitHub Enterprise", "AI controls and MCP registry policy", 125, 150, 480, 70, "ink" if "ink" in COLORS else "blue", "github")
    p.node("dev", "Developer", "VS Code + GitHub Copilot", 755, 150, 420, 70, "ink" if "ink" in COLORS else "blue", "github")
    p.node("fnd", SERVICE_FOUNDRY, "Reads registry and uses tools", 1335, 150, 500, 70, "green", ICON_FOUNDRY)
    p.node("pa", "Private registry app", "Private DNS and tunnel into VNet", 125, 315, 760, 70, "blue", ICON_ENTRA)
    p.node("apim", SERVICE_APIM, "Private registry facade", 125, 500, 760, 80, "yellow", ICON_APIM)
    p.node("apic", "Azure API Center", "Source of truth for APIs and tools", 1030, 500, 760, 80, "blue", ICON_APIM)
    p.node("gw", "AI Gateway", "Validate JWT, rate-limit and log", 125, 890, 480, 70, "yellow", ICON_APIM)
    p.node("tools", "Private MCP servers", "Functions and Logic Apps, MI only", 755, 890, 480, 70, "green", "azure.containerapps")
    p.node("be", "Business backends", "Private endpoints, least privilege", 1335, 890, 480, 70, "green", "database")
    p.edge("e1", "ghe", "dev", "1", "ink" if "ink" in COLORS else "blue")
    p.edge("e2", "dev", "pa", "2 discovery", "blue")
    p.edge("e3", "pa", "apim", "3 TLS", "blue")
    p.edge("e4", "apim", "apic", "4 managed identity", "yellow")
    p.edge("e5", "fnd", "apic", "5 catalog read", "green")
    p.edge("e6", "dev", "gw", "6 use", "green")
    p.edge("e7", "gw", "tools", "7 OAuth", "green")
    p.edge("e8", "tools", "be", "8 private API", "muted")
    return p


def build() -> None:
    pages = [system_context(), component_map(), deployment_topology(), critical_path(), routing_decision(), registry_planes()]
    mxfile = ET.Element("mxfile", {"host": "app.diagrams.net", "agent": "paulasilva-ms-azure-architecture-diagrams-showcase"})
    for page in pages:
        mxfile.append(page.diagram())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(mxfile).write(OUT, encoding="utf-8", xml_declaration=True)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()