from __future__ import annotations

from typing import IO, Any

from verse.core import Component, operation

from ._models import AudioInfo, AudioParam


class Audio(Component):
    path: str | None
    url: str | None
    stream: IO | None
    data: bytes | None

    def __init__(
        self,
        path: str | None = None,
        url: str | None = None,
        stream: IO | None = None,
        data: bytes | None = None,
        param: AudioParam | None = None,
        **kwargs,
    ):
        """Initialize.

        Args:
            path:
                Local path of the audio.
            url:
                URL of the audio.
            stream:
                IO stream containing audio.
            data:
                Raw bytes of the audio.
            param:
                Audio param.
        """
        self.path = path
        self.url = url
        self.stream = stream
        self.data = data
        if param is not None:
            self.path = param.path
            self.url = param.url
            self.data = param.data
        super().__init__(**kwargs)

    @operation()
    def get_info(self, **kwargs) -> AudioInfo:
        """Get audio info.

        Returns:
            Audio info.
        """

    @operation()
    def convert(
        self,
        type: str = "stream",
        format: str | None = None,
        codec: str | None = None,
        rate: int | None = None,
        channels: int | None = None,
        **kwargs,
    ) -> Any:
        """Convert to type.

        Args:
            type:
                Data type. One of "bytes", "stream".
            format:
                Audio format. One of "wav", "mp3", etc.
            codec:
                Audio codec. One of "mp3", "pcm_s16le", etc.
            rate:
                Target sample rate.
            channels:
                Number of channels.

        Returns:
            Converted audio.
        """

    @operation()
    def save(
        self,
        path: str,
        format: str | None = "mp3",
        codec: str | None = None,
        rate: int | None = None,
        channels: int | None = None,
        **kwargs,
    ) -> None:
        """Save audio.

        Args:
            path:
                Local path.
            format:
                Audio format. One of "wav", "mp3", etc.
            codec:
                Audio codec. One of "mp3", "pcm_s16le", etc.
            rate:
                Target sample rate.
            channels:
                Number of channels.
        """

    @operation()
    def close(self, **kwargs) -> None:
        """Close the audio stream."""

    @operation()
    async def aget_info(self, **kwargs) -> AudioInfo:
        """Get audio info.

        Returns:
            Audio info.
        """

    @operation()
    async def aconvert(
        self,
        type: str = "stream",
        format: str | None = None,
        codec: str | None = None,
        rate: int | None = None,
        channels: int | None = None,
        **kwargs,
    ) -> Any:
        """Convert to type.

        Args:
            type:
                Data type. One of "bytes", "stream".
            format:
                Audio format. One of "wav", "mp3", etc.
            codec:
                Audio codec. One of "mp3", "pcm_s16le", etc.
            rate:
                Target sample rate.
            channels:
                Number of channels.

        Returns:
            Converted audio.
        """

    @operation()
    async def asave(
        self,
        path: str,
        format: str | None = "mp3",
        codec: str | None = None,
        rate: int | None = None,
        channels: int | None = None,
        **kwargs,
    ) -> None:
        """Save audio.

        Args:
            path:
                Local path.
            format:
                Audio format. One of "wav", "mp3", etc.
            codec:
                Audio codec. One of "mp3", "pcm_s16le", etc.
            rate:
                Target sample rate.
            channels:
                Number of channels.
        """

    @operation()
    async def aclose(self, **kwargs) -> None:
        """Close the audio stream."""
