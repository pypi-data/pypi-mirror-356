#!/usr/bin/env python3.10

import curses
import random
import time


class Star:
    """Defines the properties of the ascii stars displayed in the animation"""

    __slots__ = ("y", "x", "move_timer", "move_interval")

    def __init__(self, max_y, max_x, valid):
        self.move_interval = random.randint(8, 12)
        self.move_timer = self.move_interval
        self.reposition(max_y, max_x, valid)

    def reposition(self, max_y, max_x, valid):
        while True:
            y = random.randrange(max_y)
            x = random.randrange(max_x)
            if valid(y, x):
                self.y = y
                self.x = x
                return

    def tick(self, max_y, max_x, valid):
        self.move_timer -= 1
        if self.move_timer <= 0:
            # time to hop
            self.reposition(max_y, max_x, valid)
            self.move_interval = random.randint(8, 12)
            self.move_timer = self.move_interval


def ft_ascii(stdscr):
    """Displays a splash art and quote with some animation"""

    ASCII_ART = [
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣤⣤⣤⠄⠀⠀⠀⠀⣤⣤⣤⣤⣤⠄⠀⣤⣤⣤⣤⣤⣤⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⣿⣿⣿⠟⠁⠀⠀⣿⣿⣿⣿⣿⣿⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⣿⠟⠁⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀",
        "⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀",
        "⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀",
        "⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀",
        "⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀",
        "⣾⣿⣿⣿⣿⣿⣥⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⣠⣾⠀",
        "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⣠⣾⣿⣿⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠿⠿⠿⠿⠿⠿⠀⠠⠾⠿⠿⠿⠿⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠛⠛⠛⠛",
    ]
    QUOTE = "“Swim Hard. Dream Big”"

    STAR_COUNT = 50
    ANIM_DURATION = 8.0
    TWINKLE_FRAMES = 4
    FRAME_DELAY = 0.08

    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    max_y, max_x = stdscr.getmaxyx()
    art_h = len(ASCII_ART)
    art_w = max(len(line) for line in ASCII_ART)
    top_y = (max_y - art_h) // 2
    left_x = (max_x - art_w) // 2
    quote_y = top_y + art_h + 1
    quote_x = (max_x - len(QUOTE)) // 2

    def valid(y, x):
        return not (top_y - 1 <= y <= quote_y + 1 and left_x - 1 <= x <=
                    left_x + art_w + 1)

    # Draw art + quote one time
    for i, line in enumerate(ASCII_ART):
        stdscr.addstr(top_y + i, left_x, line)
    stdscr.addstr(quote_y, quote_x, QUOTE)

    stars = [Star(max_y, max_x, valid) for _ in range(STAR_COUNT)]
    frame = 0
    char_idx = 0
    t_start = time.time()

    while time.time() - t_start < ANIM_DURATION:
        # Erase old stars
        for s in stars:
            try:
                stdscr.addch(s.y, s.x, ' ')
            except curses.error:
                pass

        frame += 1

        if frame % TWINKLE_FRAMES == 0:
            char_idx ^= 1

        for s in stars:
            s.tick(max_y, max_x, valid)

        ch = ['×', '+'][char_idx]
        for s in stars:
            try:
                stdscr.addch(s.y, s.x, ch)
            except curses.error:
                pass

        stdscr.refresh()
        time.sleep(FRAME_DELAY)

    for s in stars:
        try:
            stdscr.addch(s.y, s.x, ' ')
        except curses.error:
            pass
    stdscr.refresh()
    curses.curs_set(1)


def main():
    """Main function"""
    curses.wrapper(ft_ascii)


if __name__ == "__main__":
    main()
