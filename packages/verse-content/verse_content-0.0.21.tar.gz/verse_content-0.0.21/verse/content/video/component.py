from __future__ import annotations

from typing import IO

from verse.core import Component, operation

from ._models import VideoAudio, VideoFrame, VideoInfo, VideoParam


class Video(Component):
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
        param: VideoParam | None = None,
        **kwargs,
    ):
        """Initialize.

        Args:
            path: Local path of the video.
            url: URL of the video.
            stream: IO stream containing video.
            data: Raw bytes of the video.
            param: Video param.
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
    def get_info(self, **kwargs) -> VideoInfo:
        """Get video info.

        Returns:
            Video info.
        """

    @operation()
    def seek_frame(
        self,
        timestamp: float | None = None,
        frame_index: int | None = None,
        exact: bool = False,
        backward: bool = True,
        **kwargs,
    ) -> VideoFrame | None:
        """Seek frame.

        Args:
            timestamp:
                Timestamp in seconds to seek.
                If timestamp is provided, frame_index is ignored.
            frame_index:
                Frame index to seek.
            exact:
                If exact is false, the nearest key frame is returned.
                If exact is true, the exact frame is returned.
            backward:
                If a key frame is seeked, this value indicates
                whether to seek the key frame backwards from the
                given timestamp or frame index or forwards.

        Returns:
            Video frame.
        """

    @operation()
    def get_frame(
        self,
        **kwargs,
    ) -> VideoFrame | None:
        """Get the next frame in the video.

        Returns:
            Video frame.
        """

    @operation()
    def get_audio(
        self,
        start: float | None = None,
        end: float | None = None,
        format: str | None = None,
        codec: str | None = None,
        rate: int | None = None,
        channels: int | None = None,
        **kwargs,
    ) -> VideoAudio | None:
        """Get audio in video between two timestamps.

        Args:
            start:
                Start timestamp in seconds.
                If start timestamp is None, the start is the
                beginning of the video.
            end:
                End timestamp in seconds.
                If end timestamp is None, the end is the
                end of the video.
            format:
                Format of the audio segment.
                Possible values are "mp3", "wav", "ogg".
                Defaults to "mp3".
            codec:
                Codec of the audio segment.
                Possible values are "mp3", "pcm_s16le", etc.
                Defaults to "mp3".
            rate:
                Audio sample rate.
            channels:
                Number of channels. 1 is mono.

        Returns:
            Audio in video.
        """

    @operation()
    def close(self, **kwargs) -> None:
        """Close the video."""

    @operation()
    async def aget_info(self, **kwargs) -> VideoInfo:
        """Get video info.

        Returns:
            Video info.
        """

    @operation()
    async def aseek_frame(
        self,
        timestamp: float | None = None,
        frame_index: int | None = None,
        exact: bool = False,
        backward: bool = True,
        **kwargs,
    ) -> VideoFrame | None:
        """Seek frame.

        Args:
            timestamp:
                Timestamp in seconds to seek.
                If timestamp is provided, frame_index is ignored.
            frame_index:
                Frame index to seek.
            exact:
                If exact is false, the nearest key frame is returned.
                If exact is true, the exact frame is returned.
            backward:
                If a key frame is seeked, this value indicates
                whether to seek the key frame backwards from the
                given timestamp or frame index or forwards.

        Returns:
            Video frame.
        """

    @operation()
    async def aget_frame(
        self,
        **kwargs,
    ) -> VideoFrame | None:
        """Get the next frame in the video.

        Returns:
            Video frame.
        """

    @operation()
    async def aget_audio(
        self,
        start: float | None = None,
        end: float | None = None,
        format: str | None = None,
        codec: str | None = None,
        rate: int | None = None,
        channels: int | None = None,
        **kwargs,
    ) -> VideoAudio | None:
        """Get audio in video between two timestamps.

        Args:
            start:
                Start timestamp in seconds.
                If start timestamp is None, the start is the
                beginning of the video.
            end:
                End timestamp in seconds.
                If end timestamp is None, the end is the
                end of the video.
            format:
                Format of the audio segment.
                Possible values are "mp3", "wav", "ogg".
                Default to "mp3".
            codec:
                Codec of the audio segment.
                Possible values are "mp3", "pcm_s16le", etc.
                Default to "mp3".
            rate:
                Audio sample rate.
            channels:
                Number of channels. 1 is mono.

        Returns:
            Audio in video.
        """

    @operation()
    async def aclose(self, **kwargs) -> None:
        """Close the video."""
