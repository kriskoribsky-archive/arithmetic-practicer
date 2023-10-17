# arithmetic multipliers
ADDITION = 1
SUBTRACTION = 1.11
MULTIPLICATION = 1.25
DIVISION = 1.32



# useful ANSI escape sequences to be used on windows with colorama package
CLEAR_CONSOLE = "\x1b[2J"
CURSOR_UP_ONE = "\x1b[1A"
ERASE_LINE = "\x1b[2K"
COLOR_RESET = "\033[39m"

# useful helper function for removing last line from console
def erase_line(lines=1):
    for _ in range(lines):
        print(CURSOR_UP_ONE, end="")
        print(ERASE_LINE, end="")
