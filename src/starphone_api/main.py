from fastapi import FastAPI

from starphone_api.routes import main_router


app = FastAPI(title="Starphone PDV API")

app.include_router(main_router)
