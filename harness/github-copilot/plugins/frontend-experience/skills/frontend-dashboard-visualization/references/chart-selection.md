# Chart selection

| Analytical need | Default candidate | Avoid when |
| --- | --- | --- |
| Compare categories | Sorted bar or dot plot | Labels or values cannot remain readable |
| Trend over time | Line chart | Irregular observations would imply false continuity |
| Distribution | Histogram, box plot, or density | Audience cannot interpret it without explanation |
| Relationship | Scatter plot | Overplotting or sample size makes the pattern misleading |
| Part to whole | Stacked bar; pie for very few distinct parts | Precise comparison or many segments matter |
| Exact values and scanning | Table with semantic formatting | A chart would hide operational detail |
| Geography | Map | Location is not analytically meaningful |
| Flow | Flow or Sankey diagram | Path magnitude is not the question or the result is unreadable |
| Status against threshold | Labeled metric, bullet chart, or progress | A gauge adds decoration without comparison |

Use small multiples or faceting only when scales and comparisons remain clear. Label axes, units, samples, uncertainty, and missing data explicitly.
