# Image Size Reducer

A professional GUI application to optimize and compress images while maintaining or reducing quality based on user preference.

## Libraries Used

### Core Dependencies

- **tkinter** - Python's standard GUI toolkit for building the user interface
  - `tk` - Main Tkinter module for window and widget creation
  - `filedialog` - File and folder selection dialogs
  - `messagebox` - Alert and confirmation message boxes
  - `ttk` - Themed widgets for modern UI appearance

- **Pillow (PIL)** - Python Imaging Library for image processing
  - Image manipulation, conversion, and compression
  - Support for multiple image formats (JPG, PNG, WEBP, BMP, TIFF)
  - Color space conversion and optimization

- **threading** - Standard library module for concurrent execution
  - Enables background image processing without freezing the UI

- **pathlib** - Object-oriented filesystem path handling
  - Cross-platform path operations and file iteration

- **os** - Operating system interface
  - File and directory operations

## Purpose

The Image Size Reducer is designed to help users efficiently reduce image file sizes with two processing modes:

1. **No Quality Loss Mode** - Optimizes images through lossless compression techniques without reducing visual quality
2. **Quality Reduction Mode** - Reduces file size by adjusting JPEG quality levels with user-controlled quality slider (10-95%)

## Key Features

- **Batch Processing** - Process multiple images at once
- **Flexible Compression Options** - Choose between lossless optimization or quality-based compression
- **Quality Control** - Adjustable quality slider (10-95%) for fine-tuned compression
- **Real-time Progress** - Visual progress bar showing processing status
- **Format Support** - JPG, JPEG, PNG, WEBP, BMP, TIFF
- **Automatic Output Folder** - Creates "reduced_images" folder by default
- **File Size Reporting** - Displays original size, new size, and reduction percentage
- **Non-blocking UI** - Threading ensures UI remains responsive during processing

## What You Achieve

### Output Results

- **Reduced File Sizes** - Images are optimized to significantly smaller file sizes
- **Maintained Resolution** - Original image dimensions are preserved in both modes
- **Quality Preservation** - No Quality Loss mode maintains visual fidelity
- **Batch Efficiency** - Process hundreds of images automatically
- **Detailed Logging** - Console output shows before/after file sizes and reduction percentages

### Example Results

```
Processed: photo1.jpg
  Original: 2450.5 KB
  New: 892.3 KB
  Reduction: 63.6%

Processed: photo2.png
  Original: 1856.2 KB
  New: 1205.7 KB
  Reduction: 35.1%
```

## How to Use

### Installation

1. Ensure Python 3.7+ is installed
2. Install required dependencies:
   ```bash
   pip install Pillow
   ```
   (tkinter is included with Python)

### Running the Application

```bash
python main.py
```

### Usage Steps

1. Click "Browse" next to "Input Folder" and select folder containing images
2. (Optional) Click "Browse" next to "Output Folder" or use the auto-generated "reduced_images" folder
3. Choose compression mode:
   - **No Quality Loss** - For lossless optimization
   - **Reduce Size with Quality Adjustment** - For quality-based compression
4. If using quality adjustment, set desired quality level with the slider
5. Click "Start Processing" to begin
6. Monitor progress with the progress bar and status label
7. View results in the output folder and console log

## Project Structure

```
photo-size-reducer/
├── main.py           # Application entry point
├── app.py            # Main application logic (ImageSizeReducer)
├── ui.py             # User interface setup (UISetup)
├── processor.py      # Image processing logic (ImageProcessor)
├── utils.py          # File operations utility (FileOperations)
└── README.md         # This file
```

## Technical Highlights

- **Clean Architecture** - Separated concerns with modular classes
- **Error Handling** - Graceful error handling for corrupted or unsupported images
- **Background Processing** - Non-blocking threaded operations
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Optimized Output** - Uses progressive JPEG encoding and PNG optimization flags

## Supported Image Formats

- JPG/JPEG
- PNG
- WEBP
- BMP
- TIFF
