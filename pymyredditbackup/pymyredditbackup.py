#!/usr/bin/env python3
"""Contains the main package functionality."""

import logging


# Use root python logger to set loglevel to INFO
logging.basicConfig(level=logging.INFO)


def main() -> None:
    """Do the main thing."""
    logging.info("hello world")
