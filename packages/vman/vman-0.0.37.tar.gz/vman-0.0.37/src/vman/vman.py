""" Entry point """

# Standard Library
import sys
import json
import logging
import logging.config

# Local
from ._version import __version__

from . import constants
from . import term_args
from .utils import (
    load_config_or_exit,
    get_urls_path_or_exit,
    load_urls_or_exit,
    get_video_url_or_exit,
    get_author_or_exit,
    get_author_urls_or_exit,
    get_media_player_or_exit,
    play_video
)

def main():
    """ Entry Point Function """
    # One time logger initialization
    with (open(constants.LOGGER_CONFIG_PATH, 'r', encoding="utf-8")
          as logger_config_fp):
        logger_config = json.load(logger_config_fp)

    logger_config['handlers']['file']['filename'] = constants.LOGS_PATH
    logging.config.dictConfig(logger_config)
    # End of one time initialization

    # Logger for each module
    logger = logging.getLogger(__name__)

    try:
        # Command Line Interface
        terminal = term_args.term_args()

        if terminal.verbose:
            # Initialize one more time to change logging level
            logger_config['handlers']['console']['level'] = 'DEBUG'
            logging.config.dictConfig(logger_config)

        logging.debug('PROGRAM START')

        # Loading Files
        config = load_config_or_exit()
        urls_path = get_urls_path_or_exit(config)
        urls = load_urls_or_exit(urls_path)

        # Print all the Urls
        if terminal.urls:
            print(json.dumps(urls, indent=4))
            sys.exit(constants.SUCCESS)

        # Get Video made by Author
        author = get_author_or_exit(terminal.author, config.get('author'))
        author_urls = get_author_urls_or_exit(author, urls)
        video_url = get_video_url_or_exit(terminal.video, author, author_urls)

        # Print only the video url
        if terminal.only_url:
            print(video_url)
            sys.exit(constants.SUCCESS)

        # Play the video
        media_player = get_media_player_or_exit(terminal.player,
                                                config.get('media_player'))
        play_video(media_player, video_url)

    except KeyboardInterrupt:
        logger.debug("Keyboard Interrupt")
        sys.exit(constants.USER_ERROR)

    except Exception:
        logger.error("OperationalError", exc_info=True)
        sys.exit(constants.OPERATIONAL_ERROR)

    sys.exit(constants.SUCCESS)

if __name__ == '__main__':
    main()
