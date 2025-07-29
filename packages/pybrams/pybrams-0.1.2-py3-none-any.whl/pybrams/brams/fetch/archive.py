"""
Provides access to the local BRAMS WAV archive.

Includes functions to verify archive accessibility and extract WAV files
from ZIP archives using system codes and timestamps.
"""

import os
from pybrams.brams.formats.zip import ZipExtractor
from pybrams.utils import Config
import logging

logger = logging.getLogger(__name__)

base_path = Config.get(__name__, "base_path")


def is_archive_reachable():
    """
    Check whether the configured BRAMS archive directory is accessible.

    Raises:
        FileNotFoundError: If the archive path does not exist or is not a directory.
        PermissionError: If the archive path exists but is not readable.

    Returns:
        bool: True if the archive path exists and is readable.
    """
    if not os.path.exists(base_path) or not os.path.isdir(base_path):
        error_message = (
            f"BRAMS archive path does not exist or is not a directory: {base_path}"
        )
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        os.listdir(base_path)

    except PermissionError as e:
        error_message = (
            f"Permission denied: Cannot read the BRAMS archive directory: {base_path}"
        )
        logger.error(error_message)
        raise PermissionError(error_message) from e

    return True


def get(
    system_code: str, year: int, month: int, day: int, hours: int, minutes: int
) -> bytes:
    """
    Extract a specific WAV file from a ZIP archive in the BRAMS directory.

    Args:
        system_code (str): Code of the BRAMS system (e.g., "B12345").
        year (int): Four-digit year (e.g., 2025).
        month (int): Month (1–12).
        day (int): Day of the month.
        hours (int): Hour of the WAV file (0–23).
        minutes (int): Minute of the WAV file (e.g., 0, 15, 30, 45).

    Returns:
        bytes: Contents of the extracted WAV file.

    Raises:
        FileNotFoundError: If the ZIP or WAV file does not exist.
        RuntimeError: If extraction fails for any reason.
    """
    zip_name = f"RAD_BEDOUR_{year:04}{month:02}{day:02}_{hours:02}00_{system_code}.zip"
    wav_name = f"RAD_BEDOUR_{year:04}{month:02}{day:02}_{hours:02}{minutes:02}_{system_code}.wav"
    zip_path = os.path.join(
        base_path, system_code[:6], f"{year:04}", f"{month:02}", zip_name
    )

    return ZipExtractor(zip_path).extract_file(wav_name)
