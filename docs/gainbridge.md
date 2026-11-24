# Gainbridge Fieldhouse: first venue

Build Gainbridge before expanding to other US stadiums and arenas. The first usable model should support a documented basketball configuration, a separately specified concert configuration, a checked subset of seats, and routes to selected concessions.

## What is available now

The [source record](../data/venues/gainbridge-fieldhouse.json) holds the venue identity, reference links, and two concession entries from the official guide. It is a research record, not a renderable arena file. Its empty model and coordinate fields mean the geometry has not been established, not that the venue has no seats or amenities.

- The [venue's dining page](https://www.gainbridgefieldhouse.com/dining) links its current concourse and concession guide.
- The [official guide](https://www.gainbridgefieldhouse.com/assets/doc/Dining-at-Gainbridge-Fieldhouse-9515cde05e.pdf) associates concessions with levels and sections. It is not a measured 3D plan or a live opening-status feed.
- The [Pacers virtual venue](https://pacers.io-media.com/) is a seating reference. Its existence does not supply a reusable mesh, a full seat-coordinate table, or permission to copy its assets.
- The [venue's veranda information](https://www.gainbridgefieldhouse.com/verandas) explains that end-stage setups can obstruct those areas. Concert geometry needs to be tied to a particular configuration.

Sources were checked on November 24, 2026. Links and a small set of public facts are included; the source maps, viewer code, imagery, and meshes are not copied into this repository.

## Modeling work

1. Establish source coverage and the usable input files. Keep coordinates, units, section identifiers, revisions, and source provenance together.
2. Reconstruct the court, bowl, tiers, aisles, and section boundaries. Mark inferred dimensions explicitly. Establish calibration points and a coordinate frame before assigning seat positions.
3. Add row rise/run, numbering direction, missing seats, eye offsets, rails, overhangs, screens, and other view-changing structures. Unknown seats must not silently borrow another seat's view.
4. Compare supported views against independent references. Include corner seats, front/back rows, upper tiers, and known obstructions. A reconstruction stays approximate until the evidence supports a stronger claim.
5. Add one concert configuration with its own stage, floor seats, equipment, closures, and validation. There is no universal Gainbridge concert stage layout.
6. Locate the selected concessions within a walking graph. Section labels alone cannot establish walking distance, elevator access, or a permitted route.

The existing `demo-arena.json` is only a geometry test fixture. Its section 101, row count, seat spacing, court size, and stage dimensions are invented and must not be presented as Gainbridge measurements.

## Offline preparation

Runtime code must not depend on the linked sites being reachable. Any reference material used during an offline coding task must be prepared beforehand under the applicable upload and reuse rules. This record identifies sources but does not make their full contents available offline.

The first implementation can progress on the renderer, venue format, editor, and explicit approximate geometry using available inputs. Accurate seat-level claims remain blocked until the relevant measurements and references are available. Do not infer those measurements from the venue name.
