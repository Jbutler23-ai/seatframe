"""Write a single fictional seat-view SVG without modifying the input."""

import argparse
import os
from pathlib import Path
import sys

from .geometry import SeatframeError, load_arena
from .rendering import render_svg


def main(argv=None):
    parser = argparse.ArgumentParser(prog="seatframe", description="Draw a static fictional game or concert seat view.")
    parser.add_argument("arena", type=Path)
    parser.add_argument("--section", type=int, required=True)
    parser.add_argument("--row", type=int, required=True)
    parser.add_argument("--seat", type=int, required=True)
    parser.add_argument("--layout", choices=("game", "concert"), default="game")
    parser.add_argument("--eye-height", type=float, default=1.15, help="eye height above the row platform, in meters")
    parser.add_argument("--fov", type=float, default=60, help="vertical field of view, 10 to 120 degrees")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        arena = load_arena(args.arena)
        if args.section != arena.section:
            raise SeatframeError(f"The example has only section {arena.section}")
        svg = render_svg(arena, args.row, args.seat, args.eye_height, args.fov, args.layout)
        if args.output.resolve() == args.arena.resolve():
            raise SeatframeError("Output cannot replace the arena input")
        if args.output.exists() or args.output.is_symlink():
            raise SeatframeError(f"Output already exists: {args.output}")
        if not args.output.parent.is_dir():
            raise SeatframeError(f"Output directory does not exist: {args.output.parent}")
        identity = None
        try:
            with args.output.open("x", encoding="utf-8", newline="\n") as stream:
                info = os.fstat(stream.fileno())
                identity = (info.st_dev, info.st_ino)
                stream.write(svg)
        except BaseException:
            if identity is not None:
                try:
                    info = args.output.lstat()
                    if identity == (info.st_dev, info.st_ino):
                        args.output.unlink()
                except OSError:
                    pass
            raise
        print(f"Wrote fictional {args.layout} view: {args.output}")
        return 0
    except (SeatframeError, OSError, UnicodeError, ValueError, RuntimeError, OverflowError) as error:
        print(f"seatframe: {error}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("seatframe: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
