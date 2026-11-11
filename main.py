import argparse
from pixellab.processor import (
    get_image_info,
    resize_image,
    rotate_image,
    grayscale_image
)

from pathlib import Path
from PIL import Image

def handle_info(args):
    path = args.image
    with Image.open(path) as image:
        result = get_image_info(image=image, image_path=path)

    print(
        f"Image Info: {path}\n"
        f"Width: {result['width']}\n"
        f"Height: {result['height']}\n"
        f"Format: {result['format']}\n"
        f"Mode: {result['mode']}\n"
        f"Size (bytes): {result['size_bytes']}"
    )

def handle_resize(args):
    path = args.image
    with Image.open(path) as i:
        result = resize_image(image=i, size=(args.width, args.height))

    source = Path(path)
    save_path = source.with_name(
        f"{source.stem}_resized{source.suffix}"
    )
    result.save(save_path)
    result.close()
    print(f"Resized image saved at {save_path}.")


def handle_rotate(args):
    path = args.image
    with Image.open(path) as i:
        result = rotate_image(i, angle=args.angle)

    source = Path(path)
    save_path = source.with_name(
        f"{source.stem}_rotated{source.suffix}"
    )

    result.save(save_path)
    result.close()
    print(f"Rotated image saved at {save_path}")
    

def handle_grayscale(args):
    path = args.image
    with Image.open(path) as i:
        result = grayscale_image(i)

    source = Path(path)
    save_path = source.with_name(
        f"{source.stem}_grayscale{source.suffix}"
    )

    result.save(save_path)
    result.close()
    print(f"Changed image color mode to grayscale. Saved at {save_path}")

def create_parser():

    parser = argparse.ArgumentParser(
        description="PixelLab | Image Processing CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    info_parser = subparsers.add_parser(
        "info",
        help="Display image information"
    )

    info_parser.add_argument("image")

    info_parser.set_defaults(func=handle_info)

    resize_parser = subparsers.add_parser(
        "resize",
        help="Resize image dimensions",
    )

    resize_parser.add_argument("image")

    resize_parser.add_argument("--width", type=int, required=True)
    resize_parser.add_argument("--height", type=int, required=True)

    resize_parser.set_defaults(func=handle_resize)

    rotate_parser = subparsers.add_parser(
        "rotate",
        help="Rotate an image.",
    )

    rotate_parser.add_argument("image")
    rotate_parser.add_argument("--angle", type=float, default=90)

    rotate_parser.set_defaults(func=handle_rotate)

    grayscale_parser = subparsers.add_parser(
        "grayscale",
        help="Converts image colormode into grayscale."
    )

    grayscale_parser.add_argument("image")

    grayscale_parser.set_defaults(func=handle_grayscale)

    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()