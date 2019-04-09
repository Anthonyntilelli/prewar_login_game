"""Pre war Login Curses Interface"""
import curses
import argparse
from typing import Any
from english_words import english_words_lower_alpha_set as ewlaps  # type: ignore
from grid.word_tools import WordsTools
from grid.settings import DifficultyType
from grid.backend import Backend
from grid.interface import Interface

# Black styling Preferred
# pylint: disable=c0330


def commands() -> Backend:
    """Parses command line arguments and returns grid backend"""

    parser = argparse.ArgumentParser(
        description="Python Game to Emulate Fallout 4 hacking Module",
        epilog="Disclaimer: Not made or endorsed by Bethesda (fan-made Game)",
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
        "-d",
        "--difficulty",
        help="increases difficulty by disabling secret chars.",
        action="store_false",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-e",
        "--easy",
        help="easy difficulty (word size between 3 and 5)",
        action="store_true",
    )
    group.add_argument(
        "-a",
        "--advance",
        help="advance difficulty (word size between 6 and 8)",
        action="store_true",
    )
    group.add_argument(
        "-E",
        "--expert",
        help="expert difficulty (word size between 9 and 10)",
        action="store_true",
    )
    group.add_argument(
        "-m",
        "--master",
        help="master difficulty (word size between 11 and 12)",
        action="store_true",
    )
    args = parser.parse_args()
    if args.easy:
        difficulty: DifficultyType = DifficultyType.EASY
    elif args.advance:
        difficulty = DifficultyType.ADVANCE
    elif args.expert:
        difficulty = DifficultyType.EXPERT
    elif args.master:
        difficulty = DifficultyType.MASTER
    else:
        parser.error("Must select a difficulty")

    settings = WordsTools()
    running_setting = settings.load_settings_diff(difficulty)
    return Backend(running_setting, ewlaps, args.tries, args.difficulty)


def main(stdscr: Any, grid: Backend) -> str:
    """
    Main Game loop (call with curses.wrapper).

    :param stdscr: Curses screen
    :param grid: game grid
    :return: game outcome screen
    """
    line_start: int = 4
    action: str = ""
    player = Interface(line_start, grid.settings)

    if curses.has_colors():
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    else:
        return "E"

    selected = False
    while True:
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

        stdscr.move(player.line, player.place)  # Move cursor back to position
        key: str = stdscr.getkey()
        action = player.keyboard_input(key)
        if action == "Q":
            return "Q"
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
            if result in ("p", "l"):
                return result
            continue  # Ensure update after pressing enter
        else:
            grid.hover(not offset_local[0], offset_local[1], offset_local[2])
        stdscr.refresh()
        curses.doupdate()


if __name__ == "__main__":
    grid_backend: Backend = commands()
    GAME_OUTCOME = curses.wrapper(main, grid_backend)
    if GAME_OUTCOME == "p":
        print("game Won: Password Found")
    elif GAME_OUTCOME == "l":
        print("Game Over: Attempts Exhausted")
    elif GAME_OUTCOME == "Q":
        print("Game Quit")
    elif GAME_OUTCOME == "E":
        print("Terminal does not support Color")
    else:
        raise ValueError(str(type(GAME_OUTCOME)))
    print("Thank you for playing")
    exit()
