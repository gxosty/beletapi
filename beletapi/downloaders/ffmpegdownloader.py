import os
import re
from subprocess import Popen, PIPE
from typing import Optional

import m3u8

from .downloaderbase import DownloaderBase, DownloadProgressProtocol
from beletapi.models.file import BeletFile


class FFmpegDownloader(DownloaderBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_proc(
        self,
        proc: Popen,
        m: m3u8.M3U8,
        download_progress_callback: Optional[DownloadProgressProtocol] = None,
    ) -> None:
        segment_pattern = re.compile(
            "\\[https @ [0-9a-f]+\\] Opening '[\\w\\d\\-\\._/:]+?video"
            "[\\w\\d\\-\\._/:]+?([\\d]{1,4}).ts' for reading"
        )

        # downloaded_pattern = re.compile("size=\\s+([\\d]+kB)")

        downloaded_size = 0
        downloaded_segment = 0
        max_segments = len(m.segments)

        while True:
            output = proc.stderr.readline()
            if output == b"" and proc.poll() is not None:
                break
            if output:
                output = output.decode("utf-8")

                if found := segment_pattern.search(output):
                    downloaded_segment = int(found[1])
                # elif found := downloaded_pattern.search(output):
                #     downloaded_size = int(found[1][:-2]) * 1024

                if download_progress_callback:
                    download_progress_callback(
                        downloaded_size, downloaded_segment, max_segments
                    )

    def _fetch_video_metadata(self, file: BeletFile) -> m3u8.M3U8:
        response = self._session.get(file.filename)
        response.raise_for_status()

        m = m3u8.M3U8(response.text)

        if not m.is_endlist:
            url = file.filename[: file.filename.rfind("/")]
            url = url + "/" + m.playlists[0].uri
            response = self._session.get(url)
            response.raise_for_status()

            m = m3u8.M3U8(response.text)

        return m

    # override
    def download(
        self,
        file: BeletFile,
        output_filename: Optional[str],
        download_progress_callback: Optional[DownloadProgressProtocol] = None,
    ) -> str:
        if output_filename is None:
            output_filename = os.path.splitext(
                file.filename.rsplit("/", 1)[1]
            )[0] + ".mp4"

        m = self._fetch_video_metadata(file)

        proc = Popen(
            " ".join(
                [
                    "ffmpeg -y",
                    f'-headers "Authorization: {self._session.token}"',
                    f'-i "{file.filename}" -bsf:a aac_adtstoasc',
                    f'-vcodec copy -c copy -crf 23 "{output_filename}"',
                ]
            ),
            stdout=PIPE,
            stderr=PIPE,
            shell=True,
        )

        self._read_proc(proc, m, download_progress_callback)

        return output_filename
