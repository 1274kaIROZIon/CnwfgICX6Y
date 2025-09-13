# 代码生成时间: 2025-09-13 19:14:48
import os
from PIL import Image
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from typing import List, Union
from glob import glob
from shutil import copy2
import tempfile

"""
Image Resizer Starlette Application
This application allows users to batch resize images.
"""

# Function to resize an image
def resize_image(image_path: str, output_path: str, size: tuple) -> bool:
    """
    Resize an image to a specified size and save it to the output path.
    :param image_path: Path to the original image
    :param output_path: Path to save the resized image
    :param size: Desired size of the image
    :return: True if successful, False otherwise
    """
    try:
        with Image.open(image_path) as img:
            img = img.resize(size)
            img.save(output_path)
            return True
    except IOError:
        return False


# Function to batch resize images in a directory
def batch_resize_images(directory: str, size: tuple, output_directory: str) -> List[dict]:
    """
    Resize all images in a directory and save them to an output directory.
    :param directory: Directory containing images to resize
    :param size: Desired size for all images
    :param output_directory: Directory to save resized images
    :return: List of dictionaries with original and resized image paths
    """
    resized_images = []
    for image_path in glob(os.path.join(directory, '*')):
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_directory, filename)
        if resize_image(image_path, output_path, size):
            resized_images.append({'original': image_path, 'resized': output_path})
        else:
            resized_images.append({'original': image_path, 'error': 'Failed to resize image'})
    return resized_images


# Starlette route for batch resizing images
async def batch_resize(request: Request) -> JSONResponse:
    "