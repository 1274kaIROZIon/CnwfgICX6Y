# 代码生成时间: 2025-08-06 20:23:49
 * It reads a text file, performs analysis and returns statistics.
 *
 * @author Your Name
 * @version 1.0
 * @since 2023-04-01
 */

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
import os
import string
import re


# Define the root path for static files (e.g., templates)
STATIC_FILES = os.path.join(os.path.dirname(__file__), 'static')

# Define the routes for the application
routes = [
    Route('/api/analyze', endpoint=analyze_text_file),
    Route('/', endpoint=lambda request: JSONResponse({'message': 'Text File Analyzer'}), methods=['GET']),
]

# Create the Starlette application with the defined routes
app = Starlette(debug=True, routes=routes, static_files={'/static': STATIC_FILES})

# Function to analyze text file content
async def analyze_text_file(request):
    # Get the file path from the request query parameters
    file_path = request.query_params.get('file')
    if not file_path:
        return JSONResponse({'error': 'File path parameter is required'}, status_code=400)

    # Check if the file exists
    if not os.path.isfile(file_path):
        return JSONResponse({'error': 'File not found'}, status_code=404)

    try:
        # Read the file content
        with open(file_path, 'r') as file:
            content = file.read()

        # Perform text analysis
        word_count = len(content.split())
        unique_words = len(set(word.lower() for word in content.split() if word.isalpha()))
        punctuation_count = sum(char in string.punctuation for char in content)
        lines_count = content.count('
') + 1

        # Create the analysis result dictionary
        result = {
            'word_count': word_count,
            'unique_words': unique_words,
            'punctuation_count': punctuation_count,
            'lines_count': lines_count
        }

        # Return the analysis result as JSON
        return JSONResponse(result)
    except Exception as e:
        # Return an error response if an exception occurs
        return JSONResponse({'error': str(e)}, status_code=500)
