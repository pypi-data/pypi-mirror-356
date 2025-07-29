# Phovision

A pure Python computer vision library implementing various image processing algorithms from scratch. This library provides implementations of common image processing operations with flexible image I/O support.

## Features

Image Processing:
- Gaussian Blur
- Median Filter (Noise Removal)
- Mean Filter (Averaging)
- Bilateral Filter (Edge-preserving smoothing)

Image I/O:
- Read images from files, URLs, base64 strings, or bytes
- Save images in various formats (PNG, JPEG, etc.)
- Convert images to base64 strings
- Supports both PIL/Pillow and OpenCV as backends

## Installation

Basic installation with NumPy only:
```bash
pip install phovision
```

With PIL/Pillow support (recommended):
```bash
pip install phovision[PIL]
```

With OpenCV support:
```bash
pip install phovision[cv2]
```

With both PIL and OpenCV support:
```bash
pip install phovision[all]
```

## Usage

### Basic Image Processing

```python
from phovision import (
    read_image, save_image,
    gaussian_blur, median_filter, 
    mean_filter, bilateral_filter
)

# Read an image (supports various formats)
image = read_image('input.jpg')

# Apply filters
blurred = gaussian_blur(image, kernel_size=5, sigma=1.0)
denoised = median_filter(image, kernel_size=3)
averaged = mean_filter(image, kernel_size=3)
smoothed = bilateral_filter(image, kernel_size=5, sigma_spatial=1.0, sigma_intensity=50.0)

# Save results
save_image(blurred, 'blurred.png')
save_image(denoised, 'denoised.png')
```

### Flexible Image I/O

```python
from phovision import read_image, save_image, to_base64

# Read from local file
img1 = read_image('local_image.jpg')

# Read from URL
img2 = read_image('https://example.com/image.jpg')

# Read from base64 string
img3 = read_image('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgA...')

# Convert to base64 (useful for web applications)
base64_str = to_base64(img1, format='PNG')

# Save in different formats
save_image(img1, 'output.png')  # PNG
save_image(img1, 'output.jpg')  # JPEG
```

### Working with NumPy Arrays

```python
import numpy as np
from phovision import read_image, gaussian_blur

# Create a synthetic image
width, height = 200, 200
x, y = np.meshgrid(np.linspace(0, 1, width), np.linspace(0, 1, height))
synthetic = np.sin(10 * x) * np.cos(10 * y) * 127 + 128
synthetic = synthetic.astype(np.uint8)

# Process the synthetic image
processed = gaussian_blur(synthetic, kernel_size=5, sigma=1.0)

# The library also accepts existing numpy arrays
if isinstance(processed, np.ndarray):
    print("Output is a numpy array!")
```

## Requirements

Core dependencies:
- Python >= 3.7
- NumPy >= 1.21.0

Optional dependencies:
- PIL/Pillow >= 9.0.0 (for enhanced image I/O)
- OpenCV >= 4.5.0 (alternative backend for image I/O)

## License

MIT License 