""" Path to href conversion (and back). """


from mdtools import util


def path_to_href_abs(target, base_dir):
    """ Generate absolute href (/root/a/b/c.md)

    - target: Path to target
    - base_dir_abs: The Path to base directory, used to generate absolute hrefs
    - Output: href if successful, or None.
    """

    href = util.path_to_href(target, base_dir)
    if href:
        return '/' + href


def path_to_href_rel(target, base_rel):
    """ Generate relative href (b/c.md)

    - target: Path to target
    - base_rel: The Path to the file containing the link, used to generate relative hrefs
    - Output: href if successful, or None.
    """

    if target == base_rel:
        # The target is actually the file itself.
        return ''

    else:
        # The directory containing the markdown file that contains the offending link
        base_dir_rel = base_rel.parent

        # Try to find a relative path without going up ("..")
        href = util.path_to_href(target, base_dir_rel)
        if href:
            return href
        else:
            # Try to find a relative path with going up ("..").
            max_up = 3      # Max number of "ups" allowed
            dir_up = ''
            for _ in range(max_up):
                dir_up = dir_up + '../'
                base_dir_rel = base_dir_rel.parent
                href = util.path_to_href(target, base_dir_rel)
                if href:
                    # Found
                    return dir_up + href
