#!/usr/bin/env python
"""Pre war Login Curses Interface."""
import curses
import argparse
from sys import stderr
from typing import Any, Tuple
from english_words import english_words_lower_alpha_set as ewlaps  # type: ignore
from grid.settings import (
    DEFAULT_EASY,
    DEFAULT_ADVANCED,
    DEFAULT_EXPERT,
    DEFAULT_MASTER,
    SettingGrid,
)
from grid.backend import Backend
from grid.interface import Interface

# Black styling Preferred
# pylint: disable=c0330, R0912


def commands() -> Backend:
    """Parse command line arguments and returns grid."""
    parser = argparse.ArgumentParser(
        description="Python Game to Emulate Fallout 4 hacking Module",
        epilog="Disclaimer: Not made or endorsed by Bethesda (fan-made Game)",
    )
    help_action = """
    Set Game Difficulty
      easy - word size between 3 and 5
      advance - word size between 6 and 8
      expert - word size between 9 and 10
      master - word size between 11 and 12
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "action", choices=("easy", "advanced", "expert", "master"), help=help_action
    )
    parser.add_argument(
        "-t",
        "--tries",
        help="Number of tries",
        type=int,
        default="4",
        choices=range(3, 11),
    )
    parser.add_argument(
        "-s",
        "--secret",
        help="increases difficulty by disabling secret chars.",
        action="store_false",
    )
    args = parser.parse_args()
    if args.action == "easy":
        difficulty: SettingGrid = DEFAULT_EASY
    elif args.action == "advanced":
        difficulty = DEFAULT_ADVANCED
    elif args.action == "expert":
        difficulty = DEFAULT_EXPERT
    elif args.action == "master":
        difficulty = DEFAULT_MASTER
    else:
        parser.error(f"Unknown action ({args.action})")
    return Backend(difficulty, ewlaps, args.tries, args.secret)


def main(stdscr: Any, grid: Backend) -> Tuple[str, int]:
    """
    Set up Main loop and run main game loop.

    Call this function 'curses.wrapper'.
    :param stdscr: Curses screen
    :param grid: game grid
    :return: Game message and exit code
    """
    line_start: int = 4
    action: str = ""
    player = Interface(line_start, grid.settings)

    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    else:
        return "Terminal does not support Color", 4

    terminal_x: int = 1  # Must be a min of 54
    terminal_y: int = 1  # Must be a min of 21
    selected: bool = False
    while True:
        if curses.is_term_resized(terminal_y, terminal_x):
            terminal_y, terminal_x = stdscr.getmaxyx()
            if terminal_x <= 54 or terminal_y <= 21:
                return "The terminal is too narrow (min 54) or short (min 21)", 3
        stdscr.clear()

        stdscr.addstr(
            0, 0, "Welcome to ROBCO Industries (TM) TermLink", curses.color_pair(2)
        )
        stdscr.addstr(1, 0, "Password Required", curses.color_pair(2))
        if grid.tries == 1:
            color: int = 1
        else:
            color = 2
        # chr(9608) is black bar
        stdscr.addstr(
            2,
            0,
            "Attempts Remaining: " + f"{chr(9608)} " * grid.tries,
            curses.color_pair(color),
        )
        for i in range(line_start, grid.settings.NUM_OF_ROWS + line_start, 1):
            stdscr.addstr(i, 0, grid.full_row_str(i - line_start), curses.color_pair(2))

        # Move cursor back to position
        stdscr.move(player.line, player.place)
        key: str = stdscr.getkey()
        action = player.keyboard_input(key)
        if action == "Q":
            return "Game Quit", 0
        if action == "S":
            selected = True

        # Update cursor location
        stdscr.move(player.line, player.place)
        offset_local = player.exact_grid_location()
        if selected:
            result: str = grid.select(
                not offset_local[0], offset_local[1], offset_local[2]
            )
            selected = False
            if result == "p":
                return "Game Won: Password Found", 0
            if result == "l":
                return "Game Over: Attempts Exhausted", 0
            continue  # Ensure update after pressing enter
        else:
            grid.hover(not offset_local[0], offset_local[1], offset_local[2])
        stdscr.refresh()
        curses.doupdate()


if __name__ == "__main__":
    grid_backend: Backend = commands()
    MESSAGE, EXIT_CODE = curses.wrapper(main, grid_backend)
    if EXIT_CODE != 0:  # Error
        print(f"Error: {MESSAGE}", file=stderr)
    else:
        print(MESSAGE)
        print("Thank you for playing!")
    exit(EXIT_CODE)
