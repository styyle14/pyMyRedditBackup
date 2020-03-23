#!/usr/bin/env python3
"""Contains the main package functionality."""

import getpass
import logging


# Use root python logger to set loglevel to INFO
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Do the main thing."""
    username = input("Username: ")
    password = getpass.getpass()
    logging.info("Username: %s", username)
    logging.info("Password: %s", password)
