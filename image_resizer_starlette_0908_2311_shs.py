# 代码生成时间: 2025-09-08 23:11:06
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image Resizer Service using Starlette framework.
"""
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
# 改进用户体验
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
# TODO: 优化性能
from PIL import Image

"""
Configuration for image processing.
"""
OUTPUT_DIR = 'resized_images'

"""
Error messages.
"""
# 改进用户体验
ERROR_MSG_INVALID_INPUT = "Invalid input. Please provide a valid image path and dimensions."
ERROR_MSG_IMAGE_NOT_FOUND = "Image not found."
ERROR_MSG_PROCESSING_ERROR = "Error occurred during image processing."

"""
Image Resizing Function.
"""
def resize_image(image_path, output_path, width=None, height=None):
# TODO: 优化性能
    try:
        with Image.open(image_path) as img:
            if width and height:
                resized_img = img.resize((width, height))
# TODO: 优化性能
            elif width:
                resized_img = img.resize((width, int(width * img.height / img.width)))
            elif height:
                resized_img = img.resize((int(height * img.width / img.height), height))
            else:
                raise ValueError('Either width or height must be specified.')
            resized_img.save(output_path)
            return True
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")
        return False

"""
Image Resizer API Endpoint.
# 扩展功能模块
"""
async def resize_image_endpoint(request):
    # Parse the request
    data = await request.json()
    image_path = data.get('image_path')
    width = data.get('width')
    height = data.get('height')

    # Validate input
    if not image_path or not (width or height):
        return JSONResponse({'detail': ERROR_MSG_INVALID_INPUT}, status_code=HTTP_400_BAD_REQUEST)

    # Check if the file exists
# NOTE: 重要实现细节
    if not os.path.exists(image_path):
        return JSONResponse({'detail': ERROR_MSG_IMAGE_NOT_FOUND}, status_code=HTTP_404_NOT_FOUND)

    # Define the output path
    file_name = os.path.basename(image_path)
# 增强安全性
    output_path = os.path.join(OUTPUT_DIR, file_name)

    # Resize the image
    if resize_image(image_path, output_path, width, height):
# 改进用户体验
        # Return the path to the resized image
# TODO: 优化性能
        return JSONResponse({'file_path': output_path}, status_code=HTTP_200_OK)
    else:
        # Error during processing
# 增强安全性
        return JSONResponse({'detail': ERROR_MSG_PROCESSING_ERROR}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

"""
Starlette Application.
"""
app = Starlette(debug=True)
app.add_route('/api/resize', resize_image_endpoint, methods=['POST'])
# 改进用户体验

"""
Run the application.
"""
if __name__ == '__main__':
# TODO: 优化性能
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)