# 代码生成时间: 2025-09-14 20:29:47
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST
import sqlite3
from sqlite3 import Error

# Database configuration
DATABASE_FILE = "example.db"

# Function to create a database connection
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

# Function to prevent SQL injection by using parameterized queries
def secure_query(conn, query, params):
    """ Execute a parameterized query to prevent SQL injection
    """
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    except Error as e:
        print(e)
        return None

# Route to handle GET requests to /data
async def get_data(request):
    """ Handle GET requests to retrieve data from the database safely
    """
    search_term = request.query_params.get("search", "")
    if not search_term:
        return JSONResponse(
            content={"error": "Search term is required"}, status_code=HTTP_400_BAD_REQUEST
        )

    conn = create_connection(DATABASE_FILE)
    if conn is not None:
        results = secure_query(
            conn, "SELECT * FROM users WHERE name LIKE ?", ("%" + search_term + "%",)
        )
        conn.close()
        if results:
            return JSONResponse(content=results)
        else:
            return JSONResponse(content={"error": "No data found"})
    else:
        return JSONResponse(content={"error": "Database connection failed"})

# Define routes
routes = [
    Route("/data", endpoint=get_data, methods=["GET"])
]

# Create a Starlette application
app = Starlette(debug=True, routes=routes)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)