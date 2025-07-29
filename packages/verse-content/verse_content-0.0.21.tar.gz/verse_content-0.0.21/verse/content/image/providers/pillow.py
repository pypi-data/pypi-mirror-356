"""
Image processed with Pillow.
"""

__all__ = ["Pillow"]


import base64
from io import BytesIO
from typing import Any

from PIL import Image as PILImage
from PIL.Image import Image

from verse.core import Context, Provider
from verse.core.exceptions import BadRequestError

from .._models import ImageInfo


class Pillow(Provider):
    _init: bool
    _image: Image
    _image_bytes: dict
    _image_base64: dict

    def __init__(self, **kwargs):
        """Intialize."""
        self._init = False
        self._image_bytes = dict()
        self._image_base64 = dict()

    def __setup__(self, context: Context | None = None) -> None:
        if self._init:
            return
        path = self.__component__.path
        url = None
        if path and (
            path.startswith("http://") or path.startswith("https://")
        ):
            url = path
        if self.__component__.url:
            url = self.__component__.url

        if self.__component__.pil_image is not None:
            self._image = self.__component__.pil_image
        elif path is not None and not url:
            self._image = PILImage.open(self.__component__.path)
        elif self.__component__.stream is not None:
            self._image = PILImage.open(self.__component__.stream)
        elif self.__component__.data is not None:
            self._image = PILImage.open(BytesIO(self.__component__.data))
        elif self.__component__.base64 is not None:
            self._image = PILImage.open(
                BytesIO(base64.b64decode(self.__component__.base64))
            )
        elif url is not None:
            import httpx

            with httpx.Client() as client:
                response = client.get(url)
                response.raise_for_status()
                self._image = PILImage.open(BytesIO(response.content))
        else:
            raise BadRequestError("Image not initialized.")
        self._init = True

    def get_info(self) -> ImageInfo:
        return ImageInfo(width=self._image.width, height=self._image.height)

    def convert(self, type: str, format: str | None = None) -> Any:
        if format is not None:
            format = format.upper()
        if type == "pil":
            return self._image
        elif type == "bytes":
            if format in self._image_bytes:
                return self._image_bytes[format]
            byte_io = BytesIO()
            self._image.save(
                byte_io, format=format or self._image.format or "PNG"
            )
            self._image_bytes[format] = byte_io.getvalue()
            return self._image_bytes[format]
        elif type == "base64":
            if format in self._image_base64:
                return self._image_base64[format]
            byte_io = BytesIO()
            self._image.save(
                byte_io, format=format or self._image.format or "PNG"
            )
            self._image_base64[format] = base64.b64encode(
                byte_io.getvalue()
            ).decode("utf-8")
            return self._image_base64[format]
        raise BadRequestError(f"Type {type} not supported")

    def save(self, path: str, format: str | None = None) -> Any:
        if format is not None:
            format = format.upper()
        self._image.save(path, format=format)

    def show(self):
        self._image.show()
