from verse.content.audio import Audio
from verse.content.image import Image
from verse.core import DataModel


class VideoParam(DataModel):
    path: str | None = None
    """Video local path."""

    url: str | None = None
    """Video url."""

    data: bytes | None = None
    """Video bytes."""


class VideoFrame(DataModel):
    timestamp: float
    """Timestamp of the frame in seconds."""

    frame_index: int | None = None
    """Index of the frame."""

    key_frame: bool
    """A value indicating whether the frame is a key frame."""

    width: int
    """Width of the video frame in pixels."""

    height: int
    """Height of the video frame in pixels."""

    image: Image
    """Image."""


class VideoAudio(DataModel):
    start: float | None = None
    """Start timestamp of the audio."""

    end: float | None = None
    """End timestamp of the audio."""

    format: str | None = None
    """Format of the audio."""

    codec: str | None = None
    """Codec of the audio"""

    audio: Audio
    """Audio."""


class VideoInfo(DataModel):
    duration: float
    """Duration of the video in seconds."""

    width: int
    """Width of the video in pixels."""

    height: int
    """Height of the video in pixels."""

    total_frames: int
    """Total number of frames in the video stream."""

    frame_rate: float
    """Frame rate of the video."""

    bit_rate: int
    """ Bit rate of the video in bits per second."""

    format: str | None = None
    """Format of the video."""

    codec: str | None = None
    """Name of the codec used for the video stream."""

    pixel_format: str | None = None
    """Pixel format of the video stream."""

    start_time: float | None = None
    """Start time of the video in seconds."""
