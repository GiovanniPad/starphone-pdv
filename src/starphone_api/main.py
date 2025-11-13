from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from starphone_api.routes import main_router


app = FastAPI(title="Starphone PDV API")

# Configurar CORS para permitir comunicação com Electron
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
