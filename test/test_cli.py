from PIL import Image
from main import main, get_available_path
from errno import ENOSPC
from pathlib import Path
import pytest


def test_get_available_path(tmp_path):
    path = tmp_path / "photo.png"
    assert get_available_path(path) == path

def test_get_available_path_with_existing_file(tmp_path):
    path = tmp_path / "photo.png"
    path.write_text("")
    assert get_available_path(path).name == "photo_1.png"

def test_get_available_path_with_many_existing_files(tmp_path):
    path = tmp_path / "photo.png"
    path.write_text("")
    (tmp_path / "photo_1.png").write_text("")
    (tmp_path / "photo_2.png").write_text("")
    assert get_available_path(path).name == "photo_3.png"

def test_info_command(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test_info.png"

    image = Image.new("RGB", (600, 400))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "info", str(image_path)]
    )

    main()

    captured = capsys.readouterr()

    assert "Image Info:" in captured.out
    assert "Width: 600" in captured.out
    assert "Height: 400" in captured.out
    assert "Format: PNG" in captured.out
    assert "Mode: RGB" in captured.out
    assert captured.err == ""

def test_resize_command(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(300, 400))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "resize", str(image_path), "--width", "150", "--height", "200"]
    )

    main()

    captured = capsys.readouterr()

    resized_image_path = tmp_path / "test_resized.png"
    with Image.open(resized_image_path) as resized:
        assert resized.size == (150, 200)

    assert "Resized" in captured.out
    assert str(resized_image_path) in captured.out
    with Image.open(image_path) as original:
        assert original.size == (300, 400)
    assert captured.err == ""

def test_resize_command_with_existing_file(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(300, 400))
    image.save(image_path)
    image.close()
    existing_path = tmp_path / "test_resized.png"
    existing_path.write_text("existing")

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "resize", str(image_path), "--width", "75", "--height", "100"]
    )
    
    main()

    captured = capsys.readouterr()

    resized_image_path = tmp_path / "test_resized_1.png"
    with Image.open(resized_image_path) as resized:
        assert resized.size == (75, 100)
    
    assert "Resized" in captured.out
    assert str(resized_image_path) in captured.out
    with Image.open(image_path) as original:
        assert original.size == (300, 400)
    assert existing_path.read_text() == "existing"
    assert captured.err == ""


def test_rotate_command(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", (200, 400))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "rotate", str(image_path), "--angle", "90"]
    )

    main()

    captured = capsys.readouterr()
    image_rotated_path = tmp_path / "test_rotated.png"
    with Image.open(image_rotated_path) as image:
        assert image.size == (400, 200)

    assert str(image_rotated_path) in captured.out
    assert "Rotated" in captured.out
    with Image.open(image_path) as image:
        assert image.size == (200, 400)

    assert captured.err == ""

def test_rotate_command_with_existing_file(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(200, 400))
    image.save(image_path)
    image.close()
    existing_path = tmp_path / "test_rotated.png"
    existing_path.write_text("existing")

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "rotate", str(image_path), "--angle", "90"]
    )
    
    main()

    captured = capsys.readouterr()

    image_rotated_path = tmp_path / "test_rotated_1.png"
    with Image.open(image_rotated_path) as resized:
        assert resized.size == (400, 200)
    
    assert "Rotated" in captured.out
    assert str(image_rotated_path) in captured.out
    with Image.open(image_path) as original:
        assert original.size == (200, 400)
    assert existing_path.read_text() == "existing"
    assert captured.err == ""

def test_grayscale_command_rgb(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", (100, 100))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "grayscale", str(image_path)]
    )

    main()

    captured = capsys.readouterr()
    image_grayscale_path = tmp_path / "test_grayscale.png"
    with Image.open(image_grayscale_path) as image:
        assert image.mode == "L"
        assert image.size == (100, 100) # Check just changes mode

    assert str(image_grayscale_path) in captured.out
    assert "Changed image color mode to grayscale" in captured.out
    with Image.open(image_path) as image:
        assert image.mode == "RGB"
    assert captured.err == ""

def test_grayscale_command_with_existing_file(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(100, 100))
    image.save(image_path)
    image.close()
    existing_path = tmp_path / "test_grayscale.png"
    existing_path.write_text("existing")

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "grayscale", str(image_path)]
    )
    
    main()

    captured = capsys.readouterr()

    image_grayscale_path = tmp_path / "test_grayscale_1.png"
    with Image.open(image_grayscale_path) as resized:
        assert resized.size == (100, 100)
        assert resized.mode == "L"
    
    assert "grayscale" in captured.out
    assert str(image_grayscale_path) in captured.out
    with Image.open(image_path) as original:
        assert original.size == (100, 100)
        assert original.mode == "RGB"
    assert existing_path.read_text() == "existing"
    assert captured.err == ""

def test_grayscale_command_rgba(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGBA", (100, 100))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "grayscale", str(image_path)]
    )

    main()

    captured = capsys.readouterr()
    image_grayscale_path = tmp_path / "test_grayscale.png"
    with Image.open(image_grayscale_path) as image:
        assert image.mode == "LA"
        assert image.size == (100, 100) # Check just changes mode

    assert str(image_grayscale_path) in captured.out
    assert "Changed image color mode to grayscale" in captured.out
    with Image.open(image_path) as image:
        assert image.mode == "RGBA"
    assert captured.err == ""

def test_grayscale_command_rgba_with_existing_file(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGBA", size=(100, 100))
    image.save(image_path)
    image.close()
    existing_path = tmp_path / "test_grayscale.png"
    existing_path.write_text("existing")

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "grayscale", str(image_path)]
    )
    
    main()

    captured = capsys.readouterr()

    image_grayscale_path = tmp_path / "test_grayscale_1.png"
    with Image.open(image_grayscale_path) as resized:
        assert resized.size == (100, 100)
        assert resized.mode == "LA"
    
    assert "grayscale" in captured.out
    assert str(image_grayscale_path) in captured.out
    with Image.open(image_path) as original:
        assert original.size == (100, 100)
        assert original.mode == "RGBA"
    assert existing_path.read_text() == "existing"
    assert captured.err == ""

def test_resize_missing_width(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(300, 400))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "resize", str(image_path), "--height", "200"]
    )

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()

    assert exc.value.code == 2
    assert "--width" in captured.err
    assert captured.out == ""

def test_resize_invalid_width_type(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(300, 400))
    image.save(image_path)
    image.close()

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "resize", str(image_path), "--width", "abc", "--height", "200"]
    )

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()

    assert exc.value.code == 2
    assert "--width" in captured.err
    assert "abc" in captured.err
    assert "invalid int value" in captured.err
    assert captured.out == ""


def test_missing_file_handled(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "info", "missing.png"]
    )

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()

    assert exc.value.code == 1
    assert captured.out == ""
    assert "Error: Image 'missing.png' not found" in captured.err
    assert "FileNotFoundError" not in captured.err
    assert "Traceback" not in captured.err

def test_unidentified_image(tmp_path, monkeypatch, capsys):
    image_path = tmp_path / "corrupted.png"
    image_path.write_text("...")

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "info", str(image_path)]
    )

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()

    assert exc.value.code == 1
    assert captured.out == ""
    assert f"Error: {str(image_path)!r} is not a valid or supported image" in captured.err
    assert "UnidentifiedImageError" not in captured.err
    assert "Traceback" not in captured.err

def test_info_permission_error_handled(monkeypatch, capsys):

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "info", "test.png"]
    )
    monkeypatch.setattr("main.Image.open", mock_image_open)

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()


    assert exc.value.code == 1
    assert captured.out == ""
    assert f"Error: Permission denied when opening 'test.png'" in captured.err
    assert "Traceback" not in captured.err

def test_no_space_left(tmp_path, monkeypatch, capsys):

    image_path = tmp_path / "test.png"
    image = Image.new("RGB", size=(300, 400))
    image.save(image_path)
    image.close()

    output = image_path.with_name(
        f"{image_path.stem}_resized{image_path.suffix}"
    )

    monkeypatch.setattr(
        "sys.argv",
        ["main.py", "resize", str(image_path), "--width", "150", "--height", "200"]
    )
    monkeypatch.setattr("main.Image.Image.save", mock_image_save)

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()

    assert not output.exists()
    assert exc.value.code == 1
    assert captured.out == ""
    assert "Error: No space left on device" in captured.err
    assert "Traceback" not in captured.err

def mock_image_open(path):
    raise PermissionError("Access denied")

def mock_image_save(self, path, *args, **kwargs):
    Path(path).write_text("incomplete image")
    raise OSError(ENOSPC, "No space left on device")