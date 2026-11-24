# Seatframe system plan

The first real venue is Gainbridge Fieldhouse. Start with its basketball layout, then a separately documented concert configuration. The larger product will cover US NFL, MLB, NHL, and NBA venues through the same venue-pack format. A user selects a section, row, and seat, moves from an overview into that view, compares seats, checks modeled obstructions, and locates concessions along permitted walking routes.

The repository currently contains a Gainbridge source record plus a fictional geometry test fixture and static game/concert previews. There is no Gainbridge mesh or verified seat-coordinate set yet. Everything below is planned. A convincing stadium image alone does not establish an accurate seat view.

## Data and coverage

Begin with the [Gainbridge modeling brief](gainbridge.md). Reconcile the available section maps, seating references, concession locations, and event layouts. Build original geometry from sources that can be used for that purpose. Record which dimensions are measured, inferred, or still unknown, and establish calibration points before evaluating seat views.

Real-venue modeling requires usable source data, permission to distribute any supplied assets, a seat manifest, event-specific layouts, and checks against the building. A public map or existing online viewer is a reference, not an already acquired geometry dataset. Do not silently fill gaps with invented dimensions and label the result verified. An early Gainbridge reconstruction may remain approximate while those gaps are resolved.

Keep separate synthetic fixtures for numerical tests, malformed inputs, unusual bowl shapes, and configurable obstructions. After the Gainbridge workflow is established, extend the format to football bowls, asymmetric baseball parks, and basketball/hockey conversions. National coverage is a venue-by-venue modeling and validation effort, not a list of renamed copies of the same bowl.

Record each pack's source, units, revision, supported configurations, validation evidence, and coverage. Distinguish synthetic geometry, approximate reconstructions, and validated measurements. A venue shared by several teams should retain one building identity, with dated configurations and aliases. Unsupported seats or event layouts must remain unavailable rather than pointing to a nearby substitute.

## Geometry and seat identity

Develop a versioned format for parametric seating tiers, curved rows, aisles, portals, floors, overhangs, rails, columns, screens, and optional local mesh assets. Compile editable parameters into a scene graph and collision geometry. Preserve stable section/row/seat identifiers through compilation and edits; do not assume numbering is continuous or that adjacent numbers are physically adjacent.

Map seats to floor coordinates, orientation, and a configurable eye offset. Check units, axes, transforms, bounds, duplicate identifiers, impossible row spacing, and intersections. Import/export must preserve the same seat positions and route connections. Define migrations and reject unsupported versions before replacing a usable pack.

First milestone: map the Gainbridge source coverage and build a first tier reconstruction with explicit measurement assumptions. Verify a supported set of section/row/seat identifiers against the references before exposing their views. An independent reader should recover the same seat positions from an exported pack. Keep unknown seats unsupported.

## Event layouts

Represent sports surfaces, stages, floor seats, standing areas, production towers, suspended equipment, closed sections, and route restrictions as explicit configurations over the building. Baseball geometry and temporary concert seating cannot be approximated by renaming the basketball court.

Layout edits must update visibility, seat availability in the model, routing, and cached views together. A modeled seat being selectable is not a claim that a ticket is available for sale. Check edits that remove a selected seat, change its view, or disconnect its access route. Keep the last valid revision when an update fails.

## Cameras, sightlines, and animation

Implement seat-oriented cameras, adjustable eye height and field of view, near-plane clipping, picking, and overview-to-seat transitions. Use explicit assumptions for seated or standing spectators. Projecting from the middle of a section is not a substitute for resolving a selected seat.

Build a spatial index for ray/triangle intersections and obstruction queries. Compare the accelerated path against an independent brute-force reference. Distinguish opaque obstructions from glass and netting; define what the visualization does with each material. Measure visibility toward specified regions of the field or stage rather than issuing one unexplained seat-quality score.

Camera paths should avoid solid geometry, end at the selected eye point, and remain tied to the same layout revision. Crowd size, posture, equipment changes, weather, and other unmodeled conditions prevent a promise of exactly what a spectator will experience.

## Offline rendering and interaction

Keep geometry processing, visibility, and a software renderer in Python. Add clipping, a depth buffer, materials, shading, spatial culling, and levels of detail. Use instanced seating geometry instead of a complete unique mesh for every chair. Separate the cheaper interactive preview from slower cached stills.

The local interface will use bundled HTML, CSS, and JavaScript with a 2D canvas and a Python loopback service. It must run without a GPU, WebGL, downloaded assets, or a cloud renderer. Render time and image quality need measurement before promising photorealism or a frame rate.

Move compilation and rendering into cancellable workers. Bound queues and caches, discard stale results, and include venue revision, layout, seat, eye settings, and rendering settings in cache keys. Changing layouts rapidly must not show an old stage view under a new seat label.

## Concessions and walking routes

Represent concourses, portals, stairs, ramps, elevators, doors, and concessions as a graph connected to seats. Route by allowed paths and levels, not straight-line distance. Support step-free route preferences, closed links, and restricted ticket areas. A step-free route is a modeled option, not a certification of accessibility.

Return an explicit unreachable result when no permitted path exists. Keep route distance separate from any walking-time estimate. Concession names, opening conditions, and layout revisions must share provenance; an offline fixture cannot assert a stand is open in real time.

## Checks and scale

- Seat-coordinate fixtures must agree with independently calculated positions within 1e-6 meters. Export/import must preserve identifiers and supported-layout membership.
- Known camera fixtures must place reference points within one pixel of independently calculated projections at a fixed viewport. Near-plane and degenerate-camera cases must fail or clip deliberately.
- At least 10,000 seeded rays across the synthetic corpus must agree with brute-force obstruction checks, using declared distance tolerances and rules for edge contacts. Thin rails and nearly grazing rays belong in the corpus.
- Route fixtures must return the expected path or unreachable result after closures and access changes. Compare accelerated routing with a basic reference search and manually specified cases.
- Layout changes, undo/redo, interrupted saves, malformed packs, and stale worker responses must not mix revisions or replace a valid project with partial output.
- Qualify a synthetic venue with 100,000 seat records, 250,000 scene triangles, and 500 points of interest within 1 GiB of total application process memory, including workers and the viewer. Bound cached views and rendered image size. This is an unmeasured target, not the capacity of the current starter.
- Record load time, selected-seat render time, query time, image settings, corpus, hardware, and memory together. Run the supported workflow on Windows and Linux.

These checks establish behavior on known geometry. Real venues require a separate validation set with surveyed coordinates or calibrated reference views, including known obstructed seats. Test tolerances for real data must reflect its measurement uncertainty.

## Work sequence

Begin with Gainbridge's source record, the venue format, a tier reconstruction, and independent geometry fixtures. Then add a documented concert layout, camera transitions, obstruction queries, and software rendering. Build the walking graph and local editor against those shared revisions. Follow with worker coordination, caching, pack migration, failure testing, scale qualification, and additional venues.

Each area will need several implementation and validation passes. Completing an early milestone leaves the larger system and venue coverage ahead.

## Design references

- [3D Digital Venue: architectural data and seating-manifest integration](https://3ddigitalvenue.com/seat-view-technology-for-ticketing-platform-how-it-works-and-what-integration-requires/). The provider describes the data behind its models and seat-ID mapping; its service and models are not bundled here.
- [Ticketmaster Discovery API](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/). The documented event seatmap is a static image URL, not a supplied 3D seat-coordinate dataset. Live ticket integration is outside the offline engine.
- [Rams stadium navigation](https://www.therams.com/game-day/navigating). The official guide illustrates why paths and ticket-area restrictions matter when finding nearby amenities.

References inform the design. No provider code, maps, photographs, or venue meshes have been copied into this repository.
