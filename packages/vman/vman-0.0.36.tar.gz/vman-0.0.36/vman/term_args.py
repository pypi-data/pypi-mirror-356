""" Single function just to parse CLI args """

# Standard Library
import sys
import logging
import argparse

# Local
from . import constants
from ._version import __version__

logger = logging.getLogger(__name__)

def term_args() -> argparse.Namespace:
    """
    Analyzes sys.argv to map the text to options.

    Parameters
    ----------
    None

    Returns
    -------
    term args : argparse.Namespace
                C struct in python where each member is an option. 
    """

    # NO ARGUMENTS
    if len(sys.argv) == 1:
        logger.error(
            "What video manual do you want?\n"
            "For example, try 'vman ls'."
        )
        sys.exit(constants.USER_ERROR)

    parser = argparse.ArgumentParser(
        prog="vman",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage='%(prog)s [video] [author] [options]',
        description="vman - Video Man Pages",
        epilog=f"""
EXIT STATUS
    0       Successful program execution.
    1       Usage, syntax or configuration file error.
    2       Operational error.
    3       A child process returned a non-zero exit status.
    8       Author was not found.
    16      Video manual was not found.

FILES
    CONFIG = {constants.CONFIG_PATH}
    LOGS = {constants.LOGS_PATH}
"""
    )

    parser.add_argument(
        '-v','--version',
        action='version',
        version=f"""
%(prog)s v{__version__}
Copyright (C) 2025 Sivefunc
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by a human"""
    )

    parser.add_argument(
        'video',
        help="Video to consult in the video manual, e.g 'ls'",
        type=str,
        nargs="?",
        metavar="[VIDEO]"
    )

    parser.add_argument(
        '-a',
        '--author',
        help="Author of the video to consult, e.g 'roberteldersoftware'",
        type=str,
        metavar="AUTHOR"
    )

    parser.add_argument(
        '-p',
        '--player',
        help="Path to media player to use instead of the one defined in config",
        type=str,
        metavar="PATH"
    )

    parser.add_argument(
        '--only-url',
        help="Do not reproduce the video, returns the url",
        action='store_true',
    )

    parser.add_argument(
        '--urls',
        help="List all the video manuals in JSON format",
        action='store_true',
    )

    parser.add_argument(
        '--verbose',
        help="Detailed output at console",
        action='store_true',
    )

    args = parser.parse_args()

    if not args.video and not args.urls:
        logger.error('No video provided to play')
        sys.exit(constants.USER_ERROR)

    return args
