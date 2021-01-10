"""Utilities for fixing."""


def fixes(what):
    """Decorator that links a fixing function to an issue type."""
    def dec(func):
        setattr(what, "fixed_by", func)
    return dec


def choose(max_):
    """ Make the user choose a number in the range of 0...max. """

    choice = 0

    while True:
        choice = input("      Choose (Enter to skip): ")
        if not choice or choice == '':
            break

        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice < 0 or choice >= max_:
            continue

        else: return choice
