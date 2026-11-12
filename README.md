# PixelLab 🖼️

**A lightweight command-line image processing tool built with Python and Pillow.**

PixelLab is a simple and extensible CLI application for inspecting and procesing images. It provides essential image operations through an easy-to-use command-line interface.

## ✨ Features

- **Image Information:** Display image dimensions, format, color mode, and file size.
- **Resize:** Change image dimensions using high-quality LANCZOS resampling.
- **Rotate:** Rotate images by a specified angle.
- **Grayscale:** Convert supported images to grayscale while preserving transparency.
- **Automatic Output Naming:** Avoid overwriting existing files by generating unique output filenames.
- **Error Handling:** Handle common file, image, and operating-system errors.

## 🛠️ Technologies

- Python 3.10+
- Pillow
- argparse
- pytest

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Tahapishnahad/PixelLab.git
cd PixelLab
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run PixelLab using:

```bash
python main.py <command> [arguments]
```

### 1. Image Information

Display information about an image:

```bash
python main.py info photo.png
```

Displayed information includes:

- Width
- Height
- Format
- Color mode
- File size in bytes

### 2. Resize

Resize an image by specifying its new width and height:

```bash
python main.py resize photo.png --width 800 --height 600
```

The output file will be saved alongside the original image with the `_resized` suffix.

### 3. Rotate

Rotate an image by a specified angle:

```bash
python main.py rotate photo.png --angle 90
```

The default rotation angle is `90` degrees.

The output file will be saved with the `_rotated` suffix.

### 4. Grayscale

Convert an image to grayscale:

```bash
python main.py grayscale photo.png
```

The output file will be saved with the `_grayscale` suffix.

## 📁 Output Files

PixelLab never intentionally overwrites the original image.

Generated files are saved in the same directory as the source image.

For example:

```text
photo.png
photo_resized.png
photo_rotated.png
photo_grayscale.png
```

If an output filename already exists, PixelLab automatically generates a unique name:

```text
photo_resized.png
photo_resized_1.png
photo_resized_2.png
```

## 🧪 Running Tests

PixelLab uses `pytest` for automated testing.

Run the complete test suite:

```bash
pytest -v
```

## 📂 Project Structure

```text
PixelLab/
├── pixellab/
│   ├── __init__.py
│   └── processor.py
├── test/
│   ├── test_processor.py
│   └── test_cli.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚠️ Limitations

- Supported input formats depend on the installed Pillow capabilities. PNG, JPEG, and WebP are among the intended formats.
- Grayscale processing supports `L`, `LA`, `RGB`, and `RGBA` color modes.
- Resize dimensions must be positive integers.
- Rotation angles must be finite numeric values.
- Simultaneous executions targeting the same output filename are not guaranteed to be race-safe.

## 📄 License

No license has been specified yet.

## 👨‍💻 Author

**Taha**

GitHub: [@Tahapishnahad](https://github.com/Tahapishnahad)

---

*PixelLab — Simple image processing from your terminal.*