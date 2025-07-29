import zipfile
import io
import logging
from typing import Union, Dict

logger = logging.getLogger(__name__)


class ZipExtractor:
    """
    A utility class to extract files from a ZIP archive provided as a file path or bytes.

    Args:
        zippath (Union[str, bytes]): Path to the ZIP file on disk or bytes representing a ZIP archive.

    Attributes:
        zippath (Union[str, bytes]): The source ZIP file path or bytes.
        zip_file (zipfile.ZipFile | None): Internal ZipFile object, opened on demand.
    """

    def __init__(self, zippath: Union[str, bytes]):
        self.zippath = zippath
        self.zip_file: zipfile.ZipFile | None = None
        if isinstance(self.zippath, str):
            logger.info(f"ZipExtractor initialized with path: {zippath}")
        else:
            logger.info("ZipExtractor initialized with bytes")

    def _open_zip(self) -> None:
        """
        Opens the ZIP archive if it is not already opened.

        Raises:
            RuntimeError: If the file is not a valid ZIP archive.
        """
        if self.zip_file is None:
            try:
                if isinstance(self.zippath, str):
                    self.zip_file = zipfile.ZipFile(self.zippath, "r")
                    logger.info(f"Opened ZIP file from path: {self.zippath}")
                else:
                    self.zip_file = zipfile.ZipFile(io.BytesIO(self.zippath))
                    logger.info("Opened ZIP file from byte content.")
            except zipfile.BadZipFile as e:
                logger.error("The provided file is not a valid ZIP archive.")
                raise RuntimeError(
                    "The provided file is not a valid ZIP archive."
                ) from e

    def extract_file(self, filename: str) -> bytes:
        """
        Extracts a single file from the ZIP archive by name.

        Args:
            filename (str): The name of the file to extract from the ZIP.

        Returns:
            bytes: The content of the extracted file.

        Raises:
            FileNotFoundError: If the specified file is not found in the ZIP archive.
            RuntimeError: If the ZIP archive could not be opened.
            Exception: For any other errors during extraction.
        """
        self._open_zip()
        if self.zip_file is None:
            raise RuntimeError("Failed to open the ZIP archive.")

        try:
            if filename in self.zip_file.namelist():
                with self.zip_file.open(filename) as extracted_file:
                    content = extracted_file.read()
                    logger.info(f"Successfully extracted file: {filename}")
                    return content
            else:
                logger.warning(f"File not found in ZIP archive: {filename}")
                raise FileNotFoundError(f"{filename} not found in the ZIP archive.")
        except Exception:
            logger.exception("An error occurred while extracting a file.")
            raise
        finally:
            self._close_zip()

    def extract_all(self) -> Dict[str, bytes]:
        """
        Extracts all files from the ZIP archive.

        Returns:
            Dict[str, bytes]: A dictionary mapping file names to their extracted byte content.

        Raises:
            RuntimeError: If the ZIP archive could not be opened.
            Exception: For any other errors during extraction.
        """
        self._open_zip()

        if self.zip_file is None:
            raise RuntimeError("Failed to open the ZIP archive.")

        try:
            files = {
                name: self.zip_file.read(name) for name in self.zip_file.namelist()
            }
            logger.info(f"Successfully extracted {len(files)} files.")
            return files
        except Exception:
            logger.exception("An error occurred while extracting all files.")
            raise
        finally:
            self._close_zip()

    def _close_zip(self) -> None:
        """
        Closes the ZIP archive if it is open.
        """
        if self.zip_file is not None:
            self.zip_file.close()
            self.zip_file = None
            logger.info("ZIP file closed.")
