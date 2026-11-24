"""Static fictional game and concert wireframes, without occlusion simulation."""

from html import escape
import json
import math

from .geometry import HEIGHT, WIDTH, SeatframeError, look_at, project, seat_eye


def render_svg(arena, row, seat, eye_height=1.15, fov_degrees=60, layout="game"):
    if layout not in ("game", "concert"):
        raise SeatframeError("Layout must be game or concert")
    eye = seat_eye(arena, row, seat, eye_height)
    camera = look_at(eye)
    half_x, half_y = arena.playing_length / 2, arena.playing_width / 2
    floor = [(-half_x, -half_y, 0), (half_x, -half_y, 0), (half_x, half_y, 0), (-half_x, half_y, 0)]
    if any(project(point, camera, fov_degrees) is None for point in floor):
        raise SeatframeError("The playing surface crosses the camera near plane; choose another view")
    lines = []

    def line(first, second, color="#738ba2", width=1):
        a, b = project(first, camera, fov_degrees), project(second, camera, fov_degrees)
        if a is None or b is None:
            raise SeatframeError("Scene geometry crosses the near plane; choose another view")
        lines.append(f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" stroke="{color}" stroke-width="{width}"/>')

    def loop(points, color="#738ba2", width=1):
        for first, second in zip(points, points[1:] + points[:1]):
            line(first, second, color, width)

    # These outlines suggest a bowl; only the selected bank has seat coordinates.
    for index in range(arena.rows):
        outward = index * arena.row_depth
        z = arena.first_row_height + index * arena.row_rise
        outer_x = half_x + 4 + outward
        far_y = arena.front_distance + outward
        line((-outer_x, far_y, z), (outer_x, far_y, z))
        line((-outer_x, -half_y, z), (-outer_x, far_y, z))
        line((outer_x, -half_y, z), (outer_x, far_y, z))
    loop(floor, "#355a70", 2)
    stage = None
    if layout == "game":
        line((0, -half_y, 0), (0, half_y, 0), "#22856d", 2)
        radius = arena.playing_width * 0.12
        loop([(radius * math.cos(i * math.tau / 32), radius * math.sin(i * math.tau / 32), 0) for i in range(32)], "#22856d", 2)
        for sign in (-1, 1):
            x, inner = sign * half_x, sign * arena.playing_length * 0.32
            loop([(x, -half_y * 0.36, 0), (inner, -half_y * 0.36, 0), (inner, half_y * 0.36, 0), (x, half_y * 0.36, 0)], "#22856d", 2)
    else:
        stage = {"width": arena.playing_length * 0.5, "depth": arena.playing_width * 0.3,
                 "height": 1.0, "center_y": arena.playing_width * 0.25,
                 "screen_width": arena.playing_length * 0.45, "screen_height": 4.0}
        sx, sy, cy, z = stage["width"] / 2, stage["depth"] / 2, stage["center_y"], stage["height"]
        base = [(-sx, cy - sy, 0), (sx, cy - sy, 0), (sx, cy + sy, 0), (-sx, cy + sy, 0)]
        top = [(x, y, z) for x, y, _ in base]
        loop(base, "#8250a1", 2)
        loop(top, "#8250a1", 2)
        for first, second in zip(base, top):
            line(first, second, "#8250a1", 2)
        screen_x, screen_top = stage["screen_width"] / 2, z + stage["screen_height"]
        loop([(-screen_x, cy + sy, z), (screen_x, cy + sy, z), (screen_x, cy + sy, screen_top), (-screen_x, cy + sy, screen_top)], "#8250a1", 3)
    metadata = {"version": 1, "synthetic": True, "layout": layout, "arena_id": arena.id,
                "section": arena.section, "row": row, "seat": seat, "eye_height": eye_height,
                "vertical_fov_degrees": fov_degrees, "eye": list(eye), "target": [0, 0, 0],
                "viewport": [WIDTH, HEIGHT], "stage": stage}
    title = escape(arena.name)
    subtitle = f'Section {arena.section} / Row {row} / Seat {seat} / Eye +{eye_height:g} m / Vertical FOV {fov_degrees:g} degrees'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="540" viewBox="0 0 960 540" role="img" aria-labelledby="title description">
<title id="title">{title}: fictional {layout} seat view</title>
<desc id="description">Schematic wireframe with no occlusion, textures, people, or sightline rating. The fixed camera target is ground origin.</desc>
<metadata>{escape(json.dumps(metadata, sort_keys=True, allow_nan=False))}</metadata>
<defs><clipPath id="view"><rect x="0" y="92" width="960" height="372"/></clipPath></defs>
<rect width="960" height="540" fill="#eff4f7"/>
<g clip-path="url(#view)" fill="none">{"".join(lines)}</g>
<rect width="960" height="92" fill="#ffffff"/>
<text x="24" y="25" font-family="sans-serif" font-size="12" font-weight="bold" fill="#49667d">SEATFRAME / FICTIONAL GEOMETRY / {layout.upper()}</text>
<text x="24" y="52" font-family="sans-serif" font-size="22" fill="#203c51">{escape(arena.name[:68])}</text>
<text x="24" y="77" font-family="sans-serif" font-size="13" fill="#49667d">{subtitle}</text>
<rect y="464" width="960" height="76" fill="#ffffff"/>
<text x="24" y="489" font-family="sans-serif" font-size="13" fill="#49667d">Synthetic arena outlines. {"Game markings" if layout == "game" else "Raised stage and backscreen"}. Fixed target: (0, 0, 0) m.</text>
<text x="24" y="514" font-family="sans-serif" font-size="12" fill="#637a8b">Schematic preview. Obstructions, textures and animation are not modeled yet.</text>
</svg>
'''
