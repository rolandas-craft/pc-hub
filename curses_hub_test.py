import sys,os
import curses

def pc_hub_screen(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    stdscr.border(0)
    stdscr.addstr(1, 2, "📟 PC-Hub", curses.A_BOLD)
    stdscr.addstr(3, 4, "1 - Show Network Stats")
    stdscr.addstr(4, 4, "2 - View Network Log")
    stdscr.addstr(5, 4, "3 - Exit")
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key == ord('1'):
            stdscr.clear()
            stdscr.border(0)
            stdscr.addstr(1, 2, "⬆️ Sent: 123 MB")
            stdscr.addstr(2, 2, "⬇️ Received: 456 MB")
            stdscr.addstr(4, 2, "Press any key to return...")
            stdscr.getch()
        elif key == ord('2'):
            stdscr.clear()
            stdscr.border(0)
            stdscr.addstr(1, 2, "📊 [PC-Hub] Network Log:")
            stdscr.addstr(3, 2, "2025-07-20 08:10 | 12.3 MB | 8.5 MB")
            stdscr.addstr(4, 2, "2025-07-20 08:20 | 14.1 MB | 9.2 MB")
            stdscr.addstr(6, 2, "Press any key to return...")
            stdscr.getch()
        elif key == ord('3'):
            break

        stdscr.clear()
        stdscr.border(0)
        stdscr.addstr(1, 2, "📟 PC-Hub", curses.A_BOLD)
        stdscr.addstr(3, 4, "1 - Show Network Stats")
        stdscr.addstr(4, 4, "2 - View Network Log")
        stdscr.addstr(5, 4, "3 - Exit")
        stdscr.refresh()

def main():
    curses.wrapper(pc_hub_screen)

if __name__ == "__main__":
    main()