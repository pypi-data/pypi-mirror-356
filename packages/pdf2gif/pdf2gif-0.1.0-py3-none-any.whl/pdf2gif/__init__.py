"""
PDF to GIF converter library.

This library provides functionality to convert PDF files to animated GIFs
with customizable frame delays and slide multipliers.
"""

import os
from pdf2image import convert_from_path
import numpy as np
import stackview


def convert_pdf_to_gif(pdf_filename, frame_delay=150, first_slide_multiplier=10):
    """
    Convert a PDF file to an animated GIF.
    
    Args:
        pdf_filename (str): Path to the input PDF file
        frame_delay (int): Frame delay in milliseconds (default: 150)
        first_slide_multiplier (int): Number of times to repeat the first slide (default: 10)
    
    Returns:
        str: Path to the generated GIF file
    """
    # Generate output filename
    gif_filename = os.path.splitext(pdf_filename)[0] + ".gif"
    
    # Convert PDF to images
    images = convert_from_path(pdf_filename, first_page=1)
    
    # Convert to numpy arrays and downsample
    numpy_images = [np.array(img)[::2, ::2] for img in images]
    
    # Repeat first slide according to multiplier
    numpy_images = [numpy_images[0]] * first_slide_multiplier + numpy_images
    
    # Create animated GIF
    stackview.animate(numpy_images, gif_filename, frame_delay_ms=frame_delay)
    
    return gif_filename


__version__ = "0.1.0"
