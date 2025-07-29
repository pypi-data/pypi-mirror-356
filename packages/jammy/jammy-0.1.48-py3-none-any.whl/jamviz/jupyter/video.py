from __future__ import annotations

import base64
import mimetypes
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from IPython.display import HTML, display


def detect_media_type(file_path: Union[str, Path]) -> str:
    """
    Detect if a file is an image or video based on its MIME type.

    Args:
        file_path: Path to the media file

    Returns:
        'image' or 'video' or 'unknown'
    """
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type:
        if mime_type.startswith("image/"):
            return "image"
        elif mime_type.startswith("video/"):
            return "video"
    return "unknown"


def display_media(  # pylint: disable=too-many-arguments  # noqa: C901
    source: Union[str, Path, bytes, bytearray, BytesIO],
    media_type: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    autoplay: bool = False,
    loop: bool = False,
    muted: bool = False,
    controls: bool = True,
    alt_text: str = "Media content",
) -> None:
    """
    Display a media file (image or video) in a Jupyter Notebook using a data URL.

    Args:
        source: The media file to display. Can be a file path (str or Path)
               or media data (bytes, bytearray, or BytesIO).
        media_type: Force media type ('image' or 'video'). If None, will auto-detect from file extension.
        width: The width of the media player/image in pixels. Set to None for default size.
        height: The height of the media player/image in pixels. Set to None for default size.
        autoplay: Whether video should start playing automatically (ignored for images).
        loop: Whether video should loop when it reaches the end (ignored for images).
        muted: Whether video should be muted by default (ignored for images).
        controls: Whether to show video controls (ignored for images).
        alt_text: Alternative text for images (accessibility).

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the input type is not supported or media type cannot be determined.
        TypeError: If the input type is not supported.
    """
    # Handle different input types and get media data
    if isinstance(source, (str, Path)):
        file_path = Path(source)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Auto-detect media type if not provided
        if media_type is None:
            media_type = detect_media_type(file_path)
            if media_type == "unknown":
                # Try to guess from extension
                extension = file_path.suffix.lower()
                if extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"]:
                    media_type = "image"
                elif extension in [".mp4", ".webm", ".ogg", ".avi", ".mov"]:
                    media_type = "video"
                else:
                    raise ValueError(f"Cannot determine media type for file: {file_path}")

        with open(file_path, "rb") as f:
            media_data = f.read()

    elif isinstance(source, (bytes, bytearray)):
        media_data = bytes(source)
        if media_type is None:
            raise ValueError("media_type must be specified when providing raw bytes")

    elif isinstance(source, BytesIO):
        media_data = source.getvalue()
        if media_type is None:
            raise ValueError("media_type must be specified when providing BytesIO")
    else:
        raise TypeError(f"Unsupported input type: {type(source)}")

    # Validate media type
    if media_type not in ["image", "video"]:
        raise ValueError(f"media_type must be 'image' or 'video', got: {media_type}")

    # Create data URL
    if media_type == "image":
        # For images, try to detect format for proper MIME type
        if isinstance(source, (str, Path)):
            mime_type, _ = mimetypes.guess_type(str(source))
            if not mime_type or not mime_type.startswith("image/"):
                mime_type = "image/png"  # fallback
        else:
            mime_type = "image/png"  # fallback for raw data

        data_url = f"data:{mime_type};base64,{base64.b64encode(media_data).decode('utf-8')}"

        # Create image HTML
        style_attrs = []
        if width is not None:
            style_attrs.append(f"width: {width}px")
        if height is not None:
            style_attrs.append(f"height: {height}px")

        style = f' style="{"; ".join(style_attrs)}"' if style_attrs else ""

        html_content = f'<img src="{data_url}" alt="{alt_text}"{style}>'

    else:  # video
        # For videos, assume mp4 format (most common)
        data_url = f"data:video/mp4;base64,{base64.b64encode(media_data).decode('utf-8')}"

        # Prepare video attributes
        video_attrs = []
        if width is not None:
            video_attrs.append(f'width="{width}"')
        if height is not None:
            video_attrs.append(f'height="{height}"')
        if autoplay:
            video_attrs.append("autoplay")
        if loop:
            video_attrs.append("loop")
        if muted:
            video_attrs.append("muted")
        if controls:
            video_attrs.append("controls")

        # Create video HTML
        html_content = f"""
        <video {' '.join(video_attrs)}>
            <source src="{data_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        """

    display(HTML(html_content))


# Keep backward compatibility
def display_video(  # pylint: disable=too-many-arguments
    file: Union[str, Path, bytes, bytearray, BytesIO],
    width: Optional[int] = 640,
    height: Optional[int] = 480,
    autoplay: bool = False,
    loop: bool = False,
    muted: bool = False,
) -> None:
    """
    Legacy function for displaying videos. Use display_media() instead.

    This function is kept for backward compatibility.
    """
    display_media(
        source=file,
        media_type="video",
        width=width,
        height=height,
        autoplay=autoplay,
        loop=loop,
        muted=muted,
    )


# Convenience functions for specific media types
def show_image(
    source: Union[str, Path, bytes, bytearray, BytesIO],
    width: Optional[int] = None,
    height: Optional[int] = None,
    alt_text: str = "Image",
) -> None:
    """
    Convenience function to display an image.

    Args:
        source: The image file or data to display
        width: Width in pixels (optional)
        height: Height in pixels (optional)
        alt_text: Alternative text for accessibility
    """
    display_media(source=source, media_type="image", width=width, height=height, alt_text=alt_text)


def show_video(
    source: Union[str, Path, bytes, bytearray, BytesIO],
    width: Optional[int] = None,
    height: Optional[int] = None,
    autoplay: bool = False,
    loop: bool = False,
    muted: bool = False,
    controls: bool = True,
) -> None:
    """
    Convenience function to display a video.

    Args:
        source: The video file or data to display
        width: Width in pixels (optional)
        height: Height in pixels (optional)
        autoplay: Start playing automatically
        loop: Loop the video
        muted: Mute the video by default
        controls: Show video controls
    """
    display_media(
        source=source,
        media_type="video",
        width=width,
        height=height,
        autoplay=autoplay,
        loop=loop,
        muted=muted,
        controls=controls,
    )
