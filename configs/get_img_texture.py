"""
Load and prepare image textures
Converted from getImgTexture.m
"""

from psychopy import visual
from PIL import Image
import numpy as np


def get_img_texture(image_path, window, x_pos, y_pos, image_width, image_height):
    """
    Load image and create PsychoPy visual stimulus
    
    Parameters:
    -----------
    image_path : str
        Path to image file
    window : psychopy.visual.Window
        PsychoPy window object
    x_pos, y_pos : float
        Position for image center (screen coordinates)
    image_width, image_height : float
        Desired image dimensions
        
    Returns:
    --------
    img_stim : psychopy.visual.ImageStim
        PsychoPy image stimulus
    dest_rect : list
        Destination rectangle [left, top, right, bottom]
    """
    # Load image
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"❌ Error loading image {image_path}: {e}")
        # Return a blank stimulus
        img_stim = visual.Rect(window, width=image_width*2, height=image_height*2)
        dest_rect = [x_pos - image_width, y_pos - image_height,
                    x_pos + image_width, y_pos + image_height]
        return img_stim, dest_rect

    # Convert position from screen coordinates to PsychoPy center-based coordinates
    x_psychopy = x_pos - window.size[0] / 2
    y_psychopy = -y_pos + window.size[1] / 2

    # OPTIMIZED: Better scaling - 1.8x for larger but not overflow
    scale_factor = 2.5  # Changed from 1.5 to make images bigger

    # Create image stimulus
    img_stim = visual.ImageStim(
        window,
        image=img,
        pos=[x_psychopy, y_psychopy],
        size=[image_width * scale_factor, image_height * scale_factor],
        units='pix'
    )

    # Calculate destination rectangle (in screen coordinates)
    half_width = image_width * scale_factor / 2
    half_height = image_height * scale_factor / 2

    dest_rect = [
        x_pos - half_width,
        y_pos - half_height,
        x_pos + half_width,
        y_pos + half_height
    ]

    return img_stim, dest_rect