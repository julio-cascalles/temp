import uvicorn
from modelos.util.mongo_table import MongoTable
from rotas.util.app import create_app


MongoTable.DATABASE_NAME = 'Vestuario'

uvicorn.run(
    create_app()
)