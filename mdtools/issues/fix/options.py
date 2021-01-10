"""Defines a class to describe link fixing options."""


from dataclasses import dataclass

@dataclass
class Options:
    """Link fixing options, parsed from command line arguments."""

    mode:      str  = ''
    fuzzy:     bool = False
    colorize:  bool = False
