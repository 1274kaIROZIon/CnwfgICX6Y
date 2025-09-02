# 代码生成时间: 2025-09-02 23:20:19
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import math

# 定义一个简单的搜索引擎
class SimpleSearchEngine:
    def __init__(self):
# TODO: 优化性能
        self.index = {}

    def add_document(self, doc_id, text):
        # 将文档的单词转化为词频
        words = text.lower().split()
        self.index[doc_id] = {}
        for word in words:
# 添加错误处理
            self.index[doc_id][word] = self.index[doc_id].get(word, 0) + 1

    def search(self, query):
        # 搜索查询词并返回匹配的文档ID列表
        query_words = query.lower().split()
# 扩展功能模块
        results = {}
        for doc_id, word_count in self.index.items():
            score = 0
# 扩展功能模块
            for word in query_words:
                if word in word_count:
                    score += math.log(word_count[word] + 1)
            if score > 0:
                results[doc_id] = score
        return sorted(results.items(), key=lambda x: x[1], reverse=True)

# 创建Starlette应用
app = Starlette(debug=True)

# 添加路由处理搜索请求
@app.route('/search', methods=['GET'])
async def search_request(request):
    query = request.query_params.get('q')
    if not query:
        return JSONResponse({'error': 'Missing query parameter'}, status_code=400)
    try:
        # 使用搜索引擎进行搜索
        results = app.state.search_engine.search(query)
        return JSONResponse({'results': [{'doc_id': doc_id, 'score': score} for doc_id, score in results]})
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)

# 应用状态中的搜索引擎实例
app.state.search_engine = SimpleSearchEngine()

# 添加路由处理添加文档请求
@app.route('/add', methods=['POST'])
async def add_document(request):
    try:
        data = await request.json()
        doc_id = data.get('doc_id')
        text = data.get('text')
        if not doc_id or not text:
            return JSONResponse({'error': 'Missing doc_id or text'}, status_code=400)
        app.state.search_engine.add_document(doc_id, text)
        return JSONResponse({'message': 'Document added successfully'})
    except Exception as e:
# NOTE: 重要实现细节
        return JSONResponse({'error': str(e)}, status_code=500)

# 程序入口点
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)