# 代码生成时间: 2025-09-02 13:15:45
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from alembic.command import upgrade, downgrade
from alembic.config import Config

# Database migration tool app
class MigrationToolApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/migrate/up", self.upgrade),
                Route("/migrate/down", self.downgrade),
            ]
        )

    async def upgrade(self, request):
        """
        Upgrades the database to the latest revision.
        """
        try:
            alembic_cfg = Config("alembic.ini")
            upgrade(alembic_cfg, "head")
            return JSONResponse({"message": "Database upgraded successfully"}, status_code=HTTP_200_OK)
        except SQLAlchemyError as e:
            return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    async def downgrade(self, request):
        """
        Downgrades the database to the previous revision.
        """
        try:
            alembic_cfg = Config("alembic.ini")
            downgrade(alembic_cfg, "-1")
            return JSONResponse({"message": "Database downgraded successfully"}, status_code=HTTP_200_OK)
        except SQLAlchemyError as e:
            return JSONResponse({"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# Entry point for the application
if __name__ == "__main__":
    os.makedirs("migrations/versions", exist_ok=True)
    MigrationToolApp().run(debug=True)