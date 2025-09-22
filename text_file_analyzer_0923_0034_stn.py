# 代码生成时间: 2025-09-23 00:34:39
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.requests
# FIXME: 处理边界情况
from starlette.status import HTTP_404_NOT_FOUND
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
# FIXME: 处理边界情况
from collections import Counter
import os
import io

# Ensure the required NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Constants
TEXT_FILE_PATH = "./text_files/"  # Directory where text files are stored
ALLOWED_EXTENSIONS = {'.txt'}
# FIXME: 处理边界情况

# Function to analyze text file
def analyze_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            sentences = sent_tokenize(content)
            words = [word_tokenize(sentence) for sentence in sentences]
            words = [word for sublist in words for word in sublist]
            filtered_words = [word.lower() for word in words if word.isalpha()]
            stop_words = set(stopwords.words('english'))
            cleaned_words = [word for word in filtered_words if word not in stop_words]
            word_counts = Counter(cleaned_words)
            return word_counts
    except FileNotFoundError:
        raise FileNotFoundError(f"No file found at {file_path}")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
# NOTE: 重要实现细节

# Starlette application
class TextFileAnalyzer(starlette.applications-Starlette):
    def __init__(self):
        routes = [
            starlette.routing.Route("/analyze", endpoint=AnalyzeEndpoint, methods=["POST"]),
        ]
        super().__init__(routes=routes)
# 增强安全性

# Endpoint to handle analyze requests
# 扩展功能模块
class AnalyzeEndpoint:
    async def post(self, request: starlette.requests.Request):
        # Get the text file from the request form
        file = await request.form()
        if 'file' not in file.files:
            return starlette.responses.JSONResponse(
                {"error": "No file provided"}, status_code=400
            )

        file_obj = file.files['file']
        if not file_obj.filename.endswith(tuple(ALLOWED_EXTENSIONS)):
            return starlette.responses.JSONResponse(
# 添加错误处理
                {"error": "Unsupported file extension"}, status_code=400
            )

        # Save the file to a temporary location
        temp_file_path = os.path.join(TEXT_FILE_PATH, file_obj.filename)
# NOTE: 重要实现细节
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(await file_obj.read())
# 扩展功能模块

        # Analyze the text file
        try:
            word_counts = analyze_text(temp_file_path)
            return starlette.responses.JSONResponse(word_counts)
        except Exception as e:
            return starlette.responses.JSONResponse(
                {"error": str(e)}, status_code=500
            )
        finally:
            # Remove the temporary file
            os.remove(temp_file_path)

# If running directly, start the server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(TextFileAnalyzer(), host='0.0.0.0', port=8000)
