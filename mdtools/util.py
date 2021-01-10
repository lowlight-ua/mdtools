"""General helpers."""


from typing import Optional, Dict
from pathlib import Path, PurePosixPath
import re


def href_to_path(found_in: Path, base_dir: Path, href: str) -> Path:
    """Converts:
       - from a link target (aka href) as specified in markdown
       - to an absolute Path on disk.

    found_in: the Path of the file containing the link.
    base_dir: the Path of the base directory of the markdown file tree.
    href: the target href as specified in the markdown link.

    Absolute hrefs (/absolute/path.md) are resolved w.r.t. the base directory.
    Relative hrefs (relative/path.md) are resolved w.r.t. the containing file.
    Empty hrefs are considered the same target as the containing file itself.
    """

    if not href:
        # Markdown link was in the form: [text](#anchor)
        ret = found_in
    else:
        # There may be a better check for absolute href
        abs_ = (href[0:1] == '/')
        if abs_:
            # Link is in the form of [text](/absolute/path.md)
            ret = base_dir.joinpath(href[1:]).resolve()
        else:
            # Link is in the form of [text](relative/path.md)
            ret = found_in.parent.joinpath(href).resolve()

    return ret


def path_to_href(path: Path, relative_to: Path) -> Optional[str]:
    """ Converts an absolute Path to a relative href target, suitable for inclusion
    into a markdown file. An inverse of hrefToPath.

    Example:
    path = "C:/source/docs/A/B/C.md"
    relative_to = "C:/source/docs/A"
    output = "B/C.md"

    path: a Path of a file.
    relative_to: the base directory, relative to which the href will be expressed.
    return: a target string, or None if impossible.
    """

    try:
        return str(PurePosixPath(path.relative_to(relative_to)))
    except ValueError:
        return None


colorize_setting: bool = False


__clrd: Dict[str, str] = {
    ""     :'\33[0m',

    "BOLD"    :'\33[1m',
    "ITALIC"  :'\33[3m',
    "URL"     :'\33[4m',
    "BLINK"   :'\33[5m',
    "BLINK2"  :'\33[6m',
    "SELECTED":'\33[7m',

    "BLACK" :'\33[30m',
    "RED"   :'\33[31m',
    "GREEN" :'\33[32m',
    "YELLOW":'\33[33m',
    "BLUE"  :'\33[34m',
    "VIOLET":'\33[35m',
    "BEIGE" :'\33[36m',
    "WHITE" :'\33[37m',

    "BLACKBG" :'\33[40m',
    "REDBG"  :'\33[41m',
    "GREENBG" :'\33[42m',
    "YELLOWBG":'\33[43m',
    "BLUEBG"  :'\33[44m',
    "VIOLETBG":'\33[45m',
    "BEIGEBG" :'\33[46m',
    "WHITEBG" :'\33[47m',

    "GREY"   :'\33[90m',
    "RED2"   :'\33[91m',
    "GREEN2" :'\33[92m',
    "YELLOW2":'\33[93m',
    "BLUE2"  :'\33[94m',
    "VIOLET2":'\33[95m',
    "BEIGE2" :'\33[96m',
    "WHITE2" :'\33[97m',

    "GREYBG"   :'\33[100m',
    "REDBG2"   :'\33[101m',
    "GREENBG2" :'\33[102m',
    "YELLOWBG2":'\33[103m',
    "BLUEBG2 " :'\33[104m',
    "VIOLETBG2":'\33[105m',
    "BEIGEBG2" :'\33[106m',
    "WHITEBG2" :'\33[107m'
}

def clr(code: str) -> str:
    """If `colorize_setting` is True, return an Ascii color code. If not, return empty string."""
    return __clrd[code] if colorize_setting else ''
