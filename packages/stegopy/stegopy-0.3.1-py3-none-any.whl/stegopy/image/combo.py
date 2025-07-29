from stegopy.image import _core
from typing import Optional

def encode(
        image_path: str, 
        output_path: str, 
        payload: str, 
        frame: Optional[int] = None, 
        region: Optional[str] = None, 
        channel: Optional[str] = None, 
        alpha: Optional[bool] = False
    ) -> None:
    """
    Encodes a payload into the least significant bits of an image.

    This function wraps the core encoding functionality to provide a simpler interface for encoding payloads into images. It supports encoding into specific regions and channels of the image, as well as using the alpha channel.

    Args:
        image_path (str): Path to the input image file.
        output_path (str): Path where the stego image will be saved.
        payload (str): Payload to embed.
        frame (Optional[int]): Target frame index for animated images (e.g. GIF).
        region (Optional[str]): Region of the image to embed into. Defaults to None.
        channel (Optional[str]): Specific RGB channel to use. Defaults to None.
        alpha (Optional[bool]): Whether to use the alpha channel. Defaults to False.

    Raises:
        FileNotFoundError: If input image does not exist.
        UnsupportedFormatError: If image cannot be read or is invalid.
        PayloadTooLargeError: If payload exceeds capacity.
    """
    _core.encode(image_path, output_path, payload, frame=frame, region=region, channel=channel, alpha=alpha)

def decode(
        image_path: str, 
        frame: Optional[int] = None, 
        region: Optional[str] = None, 
        channel: Optional[str] = None, 
        alpha: Optional[bool] = False
    ) -> str:
    """
    Decodes a payload from the least significant bits of an image.

    This function wraps the core decoding functionality to provide a simpler interface for extracting payloads from images. It supports decoding from specific regions and channels of the image, as well as from the alpha channel.

    Args:
        image_path (str): Image file containing stego data.
        frame (Optional[int]): Target frame index for animated images (e.g. GIF).
        region (Optional[str]): Region used during encoding. Defaults to None.
        channel (Optional[str]): Channel used during encoding. Defaults to None.
        alpha (Optional[bool]): If payload was encoded in alpha channel. Defaults to False.

    Returns:
        str: The decoded payload.

    Raises:
        FileNotFoundError: If file does not exist.
        UnsupportedFormatError: If image format is invalid.
        InvalidStegoDataError: If payload is corrupted or incomplete.
    """
    return _core.decode(image_path, frame=frame, region=region, channel=channel, alpha=alpha)
