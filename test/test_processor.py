from PIL import Image
from pixellab.processor import *
import pytest

def test_get_image_info(tmp_path):
    image_path = tmp_path / "test.png"

    image = Image.new("RGB", (600, 400))
    image.save(image_path)

    with Image.open(image_path) as opened_image:
        result = get_image_info(opened_image, image_path)

    assert result["width"] == 600
    assert result["height"] == 400
    assert result["mode"] == "RGB"
    assert result["format"] == "PNG"
    assert result["size_bytes"] == image_path.stat().st_size

    image_path = tmp_path / "test.png"

    image = Image.new("LA", (500, 500))
    image.save(image_path)

    with Image.open(image_path) as opened_image:
        result = get_image_info(opened_image, image_path)

    assert result["width"] == 500
    assert result["height"] == 500
    assert result["mode"] == "LA"
    assert result["format"] == "PNG"
    assert result["size_bytes"] == image_path.stat().st_size

def test_resize_image(tmp_path):
    image_path = tmp_path / "temp.png"

    image = Image.new("RGB", (400, 400))
    image.save(image_path)

    with Image.open(image_path) as opened_image:
        result = resize_image(opened_image, (100, 100))

    assert result.size == (100, 100)
    with Image.open(image_path) as original:
        assert original.size == (400, 400)

    with pytest.raises(ValueError):
        resize_image(image=image, size=(-100, 434))

    with pytest.raises(ValueError):
        resize_image(image=image, size=(100,))

    with pytest.raises(ValueError):
        resize_image(image=image, size=(0, 434))

    with pytest.raises(TypeError):
        resize_image(image=image, size=("", True))

    with pytest.raises(ValueError):
        resize_image(image=image, size=(9, 10, 10))

    with pytest.raises(TypeError):
        resize_image(image=image, size=[100, 200])

def test_rotate_image(tmp_path):
    image_path = tmp_path / "temp.png"

    image = Image.new(mode="RGB", size=(100, 200))
    image.save(image_path)

    with Image.open(image_path) as opened_image:
        result = rotate_image(image=opened_image, angle=90)

    assert result.size[0] == 200
    assert result.size[1] == 100

    with Image.open(image_path) as opened_image:
        result = rotate_image(image=opened_image, angle=-90)

    assert result.size[0] == 200
    assert result.size[1] == 100

    with pytest.raises(TypeError):
        rotate_image(image, "Unknown angle")

def test_grayscale_image(tmp_path):
    image_path = tmp_path / "temp.png"

    image = Image.new(mode="RGB", size=(100, 200))
    image.save(image_path)

    with Image.open(image_path) as opened_image:
        result = grayscale_image(image=opened_image)

    assert result.mode == "L"

    image = Image.new(mode="RGBA", size=(100, 200))
    image.save(image_path)

    with Image.open(image_path) as opened_image:
        result = grayscale_image(image=opened_image)

    assert result.mode == "LA"