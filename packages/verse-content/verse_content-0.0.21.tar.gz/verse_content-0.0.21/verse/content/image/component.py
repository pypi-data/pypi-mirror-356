from __future__ import annotations

from typing import IO, Any

from verse.core import Component, operation

from ._models import ImageInfo, ImageParam


class Image(Component):
    path: str | None
    url: str | None
    stream: IO | None
    data: bytes | None
    base64: str | None
    pil_image: Any | None

    def __init__(
        self,
        path: str | None = None,
        url: str | None = None,
        stream: IO | None = None,
        data: bytes | None = None,
        base64: str | None = None,
        pil_image: Any | None = None,
        param: ImageParam | None = None,
        **kwargs,
    ):
        """Initialize.

        Args:
            path: Local path of the image.
            url: URL of the image.
            stream: IO stream containing image.
            data: Raw bytes of the image.
            base64: Base64 representation of the image.
            param: Image param.
        """
        self.path = path
        self.url = url
        self.stream = stream
        self.data = data
        self.base64 = base64
        self.pil_image = pil_image
        if param is not None:
            self.path = param.path
            self.url = param.url
            self.data = param.data
            self.base64 = param.base64
        super().__init__(**kwargs)

    @operation()
    def get_info(self) -> ImageInfo:
        """Get image info.

        Returns:
            Image info.
        """

    @operation()
    def convert(
        self,
        type: str,
        format: str | None = None,
        **kwargs,
    ) -> Any:
        """Convert to type.

        Args:
            type: One of "bytes", "base64", "pil", "opencv".
            format: One of "JPEG", "PNG", "BMP".

        Returns:
            Converted image.
        """

    @operation()
    def save(
        self,
        path: str,
        format: str | None = None,
        **kwargs,
    ) -> Any:
        """Save image.

        Args:
            path: Local path.
            format: One of "JPEG", "PNG", "BMP".
        """

    @operation()
    def show(
        self,
        **kwargs,
    ) -> None:
        """Show the image."""

    @operation()
    async def aget_info(self) -> ImageInfo:
        """Get image info.

        Returns:
            Image info.
        """

    @operation()
    async def aconvert(
        self,
        type: str,
        format: str | None = None,
        **kwargs,
    ) -> Any:
        """Convert to type.

        Args:
            type: One of "bytes", "base64", "pil", "opencv".
            format: One of "JPEG", "PNG", "BMP".

        Returns:
            Converted image.
        """

    @operation()
    async def asave(
        self,
        path: str,
        format: str | None = None,
        **kwargs,
    ) -> None:
        """Save image.

        Args:
            path: Local path.
            format: One of "JPEG", "PNG", "BMP".
        """

    @operation()
    async def ashow(
        self,
        **kwargs,
    ) -> None:
        """Show the image."""

    @staticmethod
    def load(image: str | bytes | Image | ImageParam | dict | None) -> Image:
        if isinstance(image, str):
            return Image(path=image)
        elif isinstance(image, bytes):
            return Image(data=image)
        elif isinstance(image, dict):
            return Image(param=ImageParam.from_dict(image))
        elif isinstance(image, ImageParam):
            return Image(param=image)
        return image
