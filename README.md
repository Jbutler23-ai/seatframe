# Seatframe

Seatframe is the beginning of an offline 3D seat-preview system in Python. Pick a section, row, and seat, then compare the view toward a playing area or concert stage.

The larger goal is to support US NFL, MLB, NHL, and NBA venues, with event layouts and walking routes to concessions. That coverage will need venue data and validation. No real stadium models or ticket inventory are included here.

## Starting point

The starter has one fictional arena fixture, a small seating section, a perspective camera, and static SVG previews for game and concert layouts. The game view contains a court; the concert view adds a stage. Both use the same seat coordinates. Simple stand outlines provide context.

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

The [system plan](docs/plan.md) covers venue generation, seat identity, event configurations, visibility, software rendering, camera animation, route finding, editing, and validation. It separates the offline engine from the later work of obtaining and checking real venue data.

All fixtures are fictional and created for this project. The starter runs without internet access, a GPU, Docker, sound, accounts, or external services. Code and fixtures are under the [MIT license](LICENSE).
