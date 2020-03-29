#!/usr/bin/env python3
"""Contains the main package functionality."""

import argparse
import getpass
import logging
import os
import shutil
import sys
import tempfile

import praw

import prawcore


def praw_reddit_from_ini(praw_ini_path: str) -> None:
    """Get Reddit instance from praw.ini file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        logging.debug("Temp dir: %s", temp_dir)
        # Change to temporary directory. PRAW reads praw.ini from pwd
        os.chdir(temp_dir)
        shutil.copy(praw_ini_path, temp_dir + "/praw.ini")
        logging.debug("Temp dir contents: %s", os.listdir(temp_dir))
        # Get login information. This must be a user who is autorized with the app
        username = input("Username: ")
        password = getpass.getpass()
        return praw.Reddit(username=username, password=password, user_agent=f"pyMyRedditBackup")


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
    praw_ini_path = os.path.abspath(args.praw_ini)
    # Check if praw.ini file exists
    if os.path.isfile(praw_ini_path):
        logging.debug("Using praw.ini file: %s", praw_ini_path)
    else:
        logging.critical("Given path is not a file: %s", praw_ini_path)
        sys.exit(1)
    try:
        reddit = praw_reddit_from_ini(praw_ini_path)
        logging.info("Status: %s", reddit.user.me())
    except prawcore.exceptions.ResponseException:
        logging.critical("Unauthorized client error: Wrong client_id or client_secret in praw.ini")
        logging.debug("Traceback: ", exc_info=True)
        sys.exit(2)
    except prawcore.exceptions.OAuthException:
        logging.critical("Login authentication error: Wrong username or password")
        logging.debug("Traceback: ", exc_info=True)
        sys.exit(3)
