from abc import ABCMeta, abstractmethod
from typing import Optional, Protocol

from beletapi.session import BeletSession
from beletapi.models.file import BeletFile


class DownloadProgressProtocol(Protocol):
    def __call__(
        self,
        downloaded_bytes: int,
        downloaded_segment: int,
        max_segments: int,
    ) -> None:
        pass


class DownloaderBase(metaclass=ABCMeta):
    def __init__(self, session: BeletSession) -> None:
        self._session = session

    @abstractmethod
    def download(
        self,
        file: BeletFile,
        output_filename: str,
        download_progress_callback: Optional[DownloadProgressProtocol] = None,
    ) -> str:
        '''Abstract method for downloading `BeletFile`
        to `output_filename`

        Args:
            file (BeletFile): `BeletFile` object
            output_filename (str): path where to download the file to
            download_progress_callback (DownloadProgressProtocol):
                download progress callback
        '''
        ...
