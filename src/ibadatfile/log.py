"""Logging configuration for ibadatfile."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Get a logger for the given name.

    Args:
        name: The name of the logger, will be prefixed with 'llmling_agent.'

    Returns:
        A logger instance
    """
    return logging.getLogger(f"ibadatfile.{name}")
