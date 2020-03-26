#!/usr/bin/env python3
"""Contains the main package functionality."""

import getpass
import logging
import sys

import praw

import prawcore


def main() -> None:
    """Do the main thing."""
    # Use root python logger to set loglevel to INFO
    logging.basicConfig(level=logging.INFO)
    username = input("Username: ")
    password = getpass.getpass()
    try:
        reddit = praw.Reddit(username=username, password=password, user_agent=f"pyMyRedditBackup")
        logging.info("Status: %s", reddit.user.me())
    except prawcore.exceptions.ResponseException:
        logging.critical("Unauthorized client error: Wrong client_id or client_secret in praw.ini")
        logging.debug("Traceback: ", exc_info=True)
        sys.exit(1)
    except prawcore.exceptions.OAuthException:
        logging.critical("Login authentication error: Wrong username or password")
        logging.debug("Traceback: ", exc_info=True)
        sys.exit(2)
