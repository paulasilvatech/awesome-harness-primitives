# Draw.io mxGraph File Format

A `.drawio` file is XML in the mxGraph format. Knowing the shape lets you author or post-process diagrams by hand when the MCP is not enough.

## Top-level structure

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Context" id="page1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10"
                  guides="1" tooltips="1" connect="1" arrows="1"
                  fold="1" page="1" pageWidth="1169" pageHeight="826"
                  math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- nodes and edges go here, parent="1" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

`id="0"` and `id="1"` are the required base layers. Every node and edge sets `parent="1"` (or the id of a container).

## A node (vertex)

```xml
<mxCell id="apim" value="API Management"
        style="shape=mscae/.../API_Management.svg;html=1;..."
        vertex="1" parent="1">
  <mxGeometry x="320" y="160" width="64" height="64" as="geometry" />
</mxCell>
```

- `style` carries the shape. For official Azure icons use the Azure stencil style; for a plain box use `rounded=1;whiteSpace=wrap;html=1`. For a custom SVG, use `shape=image;image=data:image/svg+xml,<url-encoded-svg>`.
- `mxGeometry` sets position and size.

## An edge

```xml
<mxCell id="e1" value="HTTPS" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;"
        edge="1" parent="1" source="apim" target="model">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

- `source` and `target` reference node ids.
- `edgeStyle=orthogonalEdgeStyle` gives clean right-angle routing.

## A container (boundary)

```xml
<mxCell id="rg" value="Resource group"
        style="rounded=0;dashed=1;verticalAlign=top;html=1;fillColor=none;"
        vertex="1" parent="1">
  <mxGeometry x="280" y="120" width="480" height="320" as="geometry" />
</mxCell>
```

Put child nodes inside by setting their `parent="rg"` and using geometry relative to the container.

## Using official icons

- The simplest portable path is to embed the official SVG inline as an `image` shape (`shape=image;image=data:image/svg+xml,...`) so the file is self-contained.
- Alternatively reference the draw.io Azure stencils (`shape=mscae/...` or `mxgraph.azure...`). These require the matching shape library in the viewer. Verify the style string in your draw.io version.

## Export to SVG

- In draw.io: File, Export as, SVG (embed images for a self-contained file).
- Headless: use the draw.io desktop CLI or the diagrams.net export, where available.

## Sources

- [draw.io XML and mxGraph](https://www.drawio.com/doc/faq/format-of-files)
- [draw.io Azure shapes](https://www.drawio.com/doc/faq/shapes-azure)
- [mxGraph user object and styles](https://www.drawio.com/doc/faq/custom-shapes)
