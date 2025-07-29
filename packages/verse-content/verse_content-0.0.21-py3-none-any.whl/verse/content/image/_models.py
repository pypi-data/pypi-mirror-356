from verse.core import DataModel


class ImageParam(DataModel):
    path: str | None = None
    """Image local path."""

    url: str | None = None
    """Image url."""

    data: bytes | None = None
    """Image bytes."""

    base64: str | None = None
    """Image base64 representation."""


class ImageInfo(DataModel):
    width: int
    """Width of the image in pixels."""

    height: int
    """Height of the image in pixels."""
