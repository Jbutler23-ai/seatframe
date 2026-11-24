# Seatframe

Seatframe is the beginning of an offline 3D seat-preview system in Python. The first venue is Gainbridge Fieldhouse in Indianapolis. The goal is to select a section, row, and seat, compare basketball and concert views, and find nearby concessions along usable walking routes.

The larger goal is to support every US NFL, MLB, NHL, and NBA stadium or arena through versioned venue packs. Gainbridge's [source record](data/venues/gainbridge-fieldhouse.json) and [modeling brief](docs/gainbridge.md) identify the first references and missing measurements. A finished Gainbridge model and ticket inventory are not included yet.

## Starting point

The code currently has a small seating section, a perspective camera, and static SVG previews for game and concert layouts. Its fictional geometry is a test fixture, not a model of Gainbridge. The game fixture contains a court; the concert fixture adds a stage. Both use the same seat coordinates. Simple stand outlines provide context.

These are schematic views of 3D geometry. There is no animation, surface occlusion, full seating bowl, realistic lighting, concession routing, or interactive editor yet. The outlines can show through one another. This is not an actual view from a real ticketed seat.

## Run

Use Python 3.11 or newer from this directory. The starter uses only the standard library.

```sh
python -m seatframe examples/demo-arena.json --section 101 --row 4 --seat 8 --layout game --output game.svg
python -m seatframe examples/demo-arena.json --section 101 --row 4 --seat 8 --layout concert --output concert.svg
python -m unittest discover -s tests -v
```

Open the generated SVG files in a browser. Output paths must be new files in an existing directory. Change the row or seat to produce another perspective.

The fixture uses meters: x runs across the section, y runs toward the playing area, and z is up. Seat and row numbers start at 1. Later rows are farther from the playing area and higher. Eye height and vertical field of view are explicit camera settings, not measurements of a particular spectator.

## Work ahead

The [system plan](docs/plan.md) starts with Gainbridge source mapping and a measured reconstruction, then covers seat identity, event configurations, visibility, software rendering, animation, routing, editing, and validation. Estimated dimensions and unsupported seats must remain distinguishable from checked geometry.

Geometry test fixtures are fictional and created for this project. The Gainbridge record contains a few sourced public facts and links, not copied maps or a venue mesh. The starter runs without internet access, a GPU, Docker, sound, accounts, or external services. Code and original fixtures are under the [MIT license](LICENSE).
