from math import isfinite
from pathlib import Path

from PIL import Image


def get_image_info(
    image: Image.Image,
    image_path: str | Path
) -> dict:
    return {
        "width": image.size[0],
        "height": image.size[1],
        "format": image.format,
        "mode": image.mode,
        "size_bytes": Path(image_path).stat().st_size
    }

def resize_image(
    image: Image.Image,
    size: tuple[int, int]
) -> Image.Image:

    if type(size) != tuple:
        raise TypeError("Size object must be a Tuple")

    if len(size) != 2:
        raise ValueError("Size object must have two items.")
    
    if type(size[0]) != int or type(size[1]) != int:
        raise TypeError("Size object elements must be integer.")

    if size[0] <= 0 or size[1] <= 0:
        raise ValueError("Size elements must be positive")

    return image.resize(
        size=size,
        resample=Image.Resampling.LANCZOS
    )


def rotate_image(
    image: Image.Image,
    angle: float
) -> Image.Image:
    
    if type(angle) not in (int, float):
        raise TypeError("angle must be integer or float.")

    if not isfinite(angle):
        raise ValueError("angle must be finite.")

    return image.rotate(angle=angle, expand=True)


def grayscale_image(image: Image.Image) -> Image.Image:
    if image.mode not in ("L", "LA", "RGB", "RGBA"):
        raise ValueError("Invalid color mode.")

    target_mode = "L"

    if image.mode in ("RGBA", "LA"):
        target_mode = "LA"

    return image.convert(target_mode)