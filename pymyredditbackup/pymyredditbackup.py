#!/usr/bin/env python3
"""Contains the main package functionality."""

import argparse
import dataclasses
import enum
import getpass
import logging
import os
import pathlib
import shutil
import sys
import tempfile
import typing

import dacite

import praw

import prawcore

import yaml


dataclass = dataclasses.dataclass
field = dataclasses.field
List = typing.List


class ExitCode(enum.Enum):
    """Provides exit codes for scripts."""

    SUCCESS = 0
    INVALID_PRAW_INI_FILE = 1
    INVALID_CLIENT_INFORMATION = 2
    INVALID_LOGIN_INFORMATION = 3


@dataclass
class RedditMessage:
    """Holds the userdata."""

    author: str
    title: str
    date: str
    content: str


@dataclass
class RedditUserData:
    """Holds the userdata."""

    username: str
    message_list: List[RedditMessage] = field(default_factory=list)


def praw_reddit_from_ini(praw_ini_path: str) -> praw.Reddit:
    """Get Reddit instance from praw.ini file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = pathlib.Path(temp_dir)
        logging.debug("Temp dir: %s", temp_dir_path)
        # Change to temporary directory. PRAW reads praw.ini from pwd
        os.chdir(temp_dir_path)
        shutil.copy(praw_ini_path, temp_dir_path / "praw.ini")
        logging.debug("Temp dir contents: %s", os.listdir(temp_dir_path))
        # Get login information. This must be a user who is autorized with the app
        username = input("Username: ")
        password = getpass.getpass()
        return praw.Reddit(username=username, password=password, user_agent="pyMyRedditBackup")


def praw_get_my_comments(redditor: praw.models.Redditor) -> None:
    """Get the redditor's comments."""
    for comment in redditor.comments.new(limit=None):
        logging.info("User comment: %s", comment.body)


def praw_get_my_submissions(redditor: praw.models.Redditor) -> None:
    """Get the redditor's comments."""
    for submission in redditor.submissions.new(limit=None):
        logging.info("User submission: %s", submission.title)


def praw_get_my_saved(redditor: praw.models.Redditor) -> None:
    """Get the redditor's comments."""
    for thing in redditor.saved(limit=10):
        if isinstance(thing, praw.models.Submission):
            logging.info("Saved submission: %s", thing.title)
        elif isinstance(thing, praw.models.Comment):
            logging.info("Save comment: %s", thing.body)


def praw_get_my_upvoted(redditor: praw.models.Redditor) -> None:
    """Get the redditor's comments."""
    for thing in redditor.upvoted(limit=10):
        if isinstance(thing, praw.models.Submission):
            logging.info("Upvoted submission: %s", thing.title)
        elif isinstance(thing, praw.models.Comment):
            logging.info("Upvoted comment: %s", thing.body)


def praw_get_my_messages(reddit: praw.Reddit) -> None:
    """Get the redditor's comments."""
    for message in reddit.inbox.all(limit=10):
        if isinstance(message, praw.models.Message):
            logging.info("Message subject: %s", message.subject)


def main() -> None:
    """Do the main thing."""
    # Get arguments
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "-p", "--praw-ini", required=True, help="praw.ini file which contains the client_id and client_secret",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show DEBUG level logging messages in the terminal",
    )
    args = parser.parse_args()
    # Use root python logger to set loglevel
    if args.verbose is True:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    # Get absolute praw.ini file path
    msg = RedditMessage("me", "hello", "today", "hello there.")
    msg_list = [msg]
    me = RedditUserData("gg", msg_list)
    logging.info(me)
    dd = dataclasses.asdict(me)
    yd = yaml.dump(dd)
    logging.info(yd)
    dd2 = yaml.load(yd, Loader=yaml.SafeLoader)
    logging.info(dd2)
    me2 = dacite.from_dict(data_class=RedditUserData, data=dd2)
    logging.info(me2)
    if me == me2:
        logging.info("works")
    else:
        logging.info("doesn't works")
    sys.exit()
    praw_ini_path = os.path.abspath(args.praw_ini)
    # Check if praw.ini file exists
    if os.path.isfile(praw_ini_path):
        logging.debug("Using praw.ini file: %s", praw_ini_path)
    else:
        logging.critical("Given path is not a file: %s", praw_ini_path)
        sys.exit(ExitCode.INVALID_PRAW_INI_FILE.value)
    try:
        reddit = praw_reddit_from_ini(praw_ini_path)
        logging.debug("Login successful for %s.", reddit.user.me())
    except prawcore.exceptions.ResponseException:
        logging.critical("Unauthorized client error: Wrong client_id or client_secret in praw.ini")
        logging.debug("Traceback: ", exc_info=True)
        sys.exit(ExitCode.INVALID_CLIENT_INFORMATION.value)
    except prawcore.exceptions.OAuthException:
        logging.critical("Login authentication error: Wrong username or password")
        logging.debug("Traceback: ", exc_info=True)
        sys.exit(ExitCode.INVALID_LOGIN_INFORMATION.value)
    # Print out all ids of user's data, in newest order
    praw_get_my_comments(reddit.user.me())
    praw_get_my_submissions(reddit.user.me())
    praw_get_my_saved(reddit.user.me())
    praw_get_my_upvoted(reddit.user.me())
    praw_get_my_messages(reddit)
    # Successful exit
    sys.exit(ExitCode.SUCCESS.value)
