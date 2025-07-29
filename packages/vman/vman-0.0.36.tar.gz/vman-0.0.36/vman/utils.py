""" Functions used in vman.py

The majority of these functions comes in the form 'execute_or_exit(...)'
indicating that if some function fails the program will sys.exit(...).
"""

# Standard Library
import os
import sys
import json
import shlex
import tomllib
import logging
import subprocess

# Locals
from . import constants

logger = logging.getLogger(__name__)

def load_config_or_exit() -> dict:
    """ Loads into memory the config.toml file located at CONFIG_PATH

    Parameters
    ----------
    None

    Returns
    -------
    config : dict

    Notes
    -----
    The loading of the file can cause two known exceptions to raise:
        - FileNotFoundError
            File does not exist at CONFIG_PATH

        - tomllib.TOMLDecodeError
            config.toml is not a valid TOML file.

    The program will sys.exit(constants.USER_ERROR) in case of an error
    with a helpful message.
    """
    try:
        with open(constants.CONFIG_PATH, 'rb') as config_fp:
            config = tomllib.load(config_fp)

    except FileNotFoundError:
        logger.error(f"vman configuration file does not exist at:"
                     " " f"'{constants.CONFIG_PATH}'")
        sys.exit(constants.USER_ERROR)

    except tomllib.TOMLDecodeError as parsing_error:
        logger.error(f"error parsing vman config file at:"
                     " " f"'{constants.CONFIG_PATH}'"
                     f"\n{parsing_error}")
        sys.exit(constants.USER_ERROR)

    logger.debug(f"{constants.CONFIG_PATH} loaded into memory.")
    return config

def get_urls_path_or_exit(config: dict) -> str:
    """ Location of the urls.json file

    Chooses by default the urls.json located in the same directory as
    vman.py, except that custom-urls is enabled in config.toml.

    Parameters
    ----------
    config : dict
             The loaded config.toml into memory that could have the
             option [custom-urls].
             
    Returns
    -------
    path : str
           Location of the urls.json.

    Notes
    -----
    The parsing of the file can cause the known exception to raise:
        - KeyError
            Custom urls enabled but path option is not in config.toml.

    The program will sys.exit(constants.USER_ERROR) in case of an error
    with a helpful message.
    """

    urls_path = os.path.join(constants.SRC_PATH, 'urls.json')
    if (config.get('custom-urls') is not None
            and config['custom-urls'].get('enabled')):

        try:
            urls_path = config['custom-urls']['path']
            logger.debug(f"{urls_path} is the one in config.toml")

        except KeyError:
            logger.error(
                f"[custom-urls] is enabled at: '{constants.CONFIG_PATH}'"
                " " "but a path was not given, it should be like this:"
                "\n[custom-urls]"
                "\nenabled = true"
                "\npath = '/home/user-name/.config/vman/urls.json'"
                )
            sys.exit(constants.USER_ERROR)

    else:
        logger.debug(f"urls.json provided: '{urls_path}' is the one in"
                     " " "src directory")
    return urls_path

def get_author_or_exit(
    author_terminal: str | None,
    author_config: str | None
) -> str:
    """ Author of the video manuals

    Chooses by default the author_terminal but if it was not set then
    chooses the one in the author_config - config.toml.

    Parameters
    ----------
    author_terminal : str | None
                  The author provided in the CLI as an option.

    author_config : str | None
        The author provided in the config.toml.
             
    Returns
    -------
    author : str
             Author that the user wants to consume.

    Notes
    -----
    The program will sys.exit(constants.USER_ERROR) with a helpful message
    in case that neither author_terminal nor author_config are provided.
    """

    # Nothing was provided.
    if author_terminal is None and author_config is None:
        logger.error(
            f"error parsing vman config file at:"
            " " f"'{constants.CONFIG_PATH}'"
            "\nconfig file does not have a default author"
            "\ne.g: author = 'distrotube'")
        sys.exit(constants.USER_ERROR)

    author = author_terminal if author_terminal is not None else author_config
    logger.debug(f"Author provided: {author}")
    return author

def load_urls_or_exit(urls_path: str) -> dict:
    """ Load urls.json into memory

    Parameters
    ----------
    urls_path : str
                Location of the JSON file.

    Returns
    -------
    urls : dict

    Notes
    -----
    The loading of the file can cause two known exceptions to raise:
        - FileNotFoundError
            File does not exist at CONFIG_PATH

        - json.JSONDecodeError
            urls.json is not a valid JSON file.

    The program will sys.exit(constants.USER_ERROR) in case of an error
    with a helpful message.
    """

    try:
        with open(urls_path, 'r', encoding="utf-8") as json_fp:
            urls = json.load(json_fp)

    except FileNotFoundError:
        logger.error(f"vman urls json file does not exist at:"
                     " " f"'{urls_path}'")
        sys.exit(constants.USER_ERROR)

    except json.JSONDecodeError as parsing_error:
        logger.error(f"error parsing vman urls json file at: '{urls_path}'"
                     f"\n{parsing_error}")
        sys.exit(constants.USER_ERROR)

    logger.debug(f"{urls_path} loaded into memory.")
    return urls

def get_author_urls_or_exit(author: str, urls: dict) -> dict:
    """ Urls of the videos that are exlusive to the author

    Parameters
    ----------
    author : str
             Author name that hopefully appears in urls.json

    urls : dict
           urls.json file loaded into memory.

    Returns
    -------
    author_urls : dict
                  Exclusive videos

    Notes
    -----
    The parsing of the file can cause the known exception to raise:
        - KeyError
            Author does not exist in urls.json

    The program will sys.exit(constants.NO_AUTHOR_ERROR) in case of
    the error raising with a helpful message.
    """

    try:
        author_urls = urls[author]

    except KeyError:
        logger.error(f"The author '{author}' does not exist in urls.json")
        sys.exit(constants.NO_AUTHOR_ERROR)

    logger.debug(f"Author '{author}' exists")
    return author_urls

def get_media_player_or_exit(
    media_player_terminal: str | None,
    media_player_config: str | None
) -> str:
    """ Media player that will play the video manual

    Chooses by default the media_player_terminal but if it was not set then
    chooses the one in the media_player_config.

    Parameters
    ----------
    media_player_terminal : str | None
                            The media player provided in the CLI as an
                            option.

    media_player_config : str | None
                          The media player provided in the config.toml.
                        
    Returns
    -------
    media_player : str
                   Program that will be used to view the video.

    Notes
    -----
    The program will sys.exit(constants.USER_ERROR) with a helpful message
    in case that neither media_player_terminal nor media_player_config are
    provided.
    """
    if media_player_terminal is None and media_player_config is None:
        logger.error(
            f"error parsing vman config file at:"
            " " f"'{constants.CONFIG_PATH}'"
            "\nconfig file does not have a default media player"
            "\ne.g: media_player = 'xdg-open'")
        sys.exit(constants.USER_ERROR)

    media_player = (media_player_terminal if media_player_terminal is not None
            else media_player_config)

    logger.debug(f"Media player provided: '{media_player}'")
    return media_player

def get_video_url_or_exit(
    video: str,
    author: str,
    author_urls: str,
) -> str:
    """ Url of the video that belongs to the author

    Parameters
    ----------
    video : str
            Video that the user wants to consume.

    author : str
             Author of the video.

    author_urls : dict
                  Video urls made by author.

    Returns
    -------
    video_url : str
                URL of the vide.

    Notes
    -----
    The parsing of the file can cause the known exception to raise:
        - KeyError
            The autor does not have a video about that manual.

    The program will sys.exit(constants.NO_VIDEO_MANUAL_ERROR) in case of
    the error with a helpful message.
    """

    try:
        video_url = author_urls[video]

    except KeyError:
        logger.error(
            f"The author '{author}' does not have a manual about '{video}'")
        sys.exit(constants.NO_VIDEO_MANUAL_ERROR)

    logger.debug(f"Author '{author}' video url of '{video}' is '{video_url}'")
    return video_url

def play_video(media_player: str, video_url: str):
    """ Executes in a subprocess the media player with the video url
    
    Parameters
    ----------
    media_player : str
    vide_url : str
    """
    logger.debug(f"Playing {video_url=} using {media_player=}")
    subprocess.run(shlex.split(f"{media_player} '{video_url}'"), check=True)
