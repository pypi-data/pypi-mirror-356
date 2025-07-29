from verse.core import DataModel


class AudioParam(DataModel):
    path: str | None = None
    """Audio local path."""

    url: str | None = None
    """Audio url."""

    data: bytes | None = None
    """Audio bytes."""


class AudioInfo(DataModel):
    duration: float
    """Duration of the audio in seconds."""

    channels: int
    """Width of the video in pixels."""

    sample_rate: int
    """Sample rate of the audio."""

    bit_rate: int
    """Bit rate of the audio."""

    format: str | None = None
    """Format of the video."""

    codec: str | None = None
    """Name of the codec used for the audio stream."""
