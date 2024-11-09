class BeletFile:
    def __init__(
        self,
        filename: str,
        type: str,
        quality: str,

        # what is this doing here?
        download_url: str | None = None
    ) -> None:
        self.filename: str = filename
        self.type = type
        self.quality = int(quality.rstrip("p"))
