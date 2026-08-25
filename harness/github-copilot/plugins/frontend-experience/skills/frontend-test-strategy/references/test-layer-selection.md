# Test-layer selection

| Layer | Proves | Select when |
| --- | --- | --- |
| Static | Types, schemas, build, imports, lint invariants | The project has an existing applicable command |
| Unit | Pure transformation, validation, reducer, state transition | Behavior is independent of rendering or services |
| Component | Rendering, semantics, interaction, callbacks, local states | A component boundary can prove user-visible behavior |
| Mocked integration | Multiple components plus controlled API client behavior | Frontend states need repeatable success/failure responses |
| Contract | Consumer/provider agreement | Schema or interaction drift is a material risk |
| Service integration | Real backend components with isolated data | Mocks cannot prove serialization, auth, or service behavior |
| End-to-end | Critical journey through real UI and integrated system | Boundary and orchestration risk justify cost |
| Visual regression | Unexpected rendered changes under stable fixtures | Material layout or visual behavior must remain stable |
| Accessibility | Automated subset plus keyboard, focus, AT, zoom, contrast, motion | User interaction or content changes |
| Performance | Loading, interaction, stability, bundle or native runtime | Budget or regression risk exists |
| Discoverability | Rendered metadata, crawl, schema, manifest and previews | Public indexable web content changes |
| Device/native | Lifecycle, gesture, window, safe area, native bridge | Mobile or desktop profile applies |

Prefer the smallest layer that proves the behavior. Add layers for service, browser, device, or release boundaries rather than repeating identical assertions everywhere.
