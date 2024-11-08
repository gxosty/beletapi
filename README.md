# beletapi
Belet REST API client

# Installation
Install from github

```bash
pip install https://github.com/gxosty/beletapi
```

or install from sources

```bash
git clone https://github.com/gxosty/beletapi
cd beletapi
pip install -e .
```

# Example Usage:
Login and download a movie
```py
from beletapi import BeletClient
from beletapi.exceptions import UnauthorizedError


def download_progress(downloaded_size, current_segment, max_segment):
    # `downloaded_size` isn't complete, so it will be always 0
    print(f"Downloaded: {current_segment+1}/{max_segment}", end="\r")


def main():
    client = BeletClient()

    try:
        # Refresh token if expired
        client.refresh_if_expired()
    except UnauthorizedError:
        # Login if token is not available
        client.login("+99365123456")

    # You can pass only movie id too (e.g. 343315)
    movie = client.get_movie("https://film.belet.tm/player/1/343315")

    # Get files and download movie
    # Files just describe movie quality files, e.g. 480p, 1080p, etc.
    client.download(
        movie.get_files()[0],  # quality file
        movie.name + ".mp4",  # output filename
        download_progress,  # download progress callback
    )


if __name__ == '__main__':
    main()
```