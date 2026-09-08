from fastapi import FastAPI
from src.interfaces.api.routes import router

app = FastAPI(
    title="Banco Digital - Microsserviço de Conta de Pagamentos",
    description="Implementação do padrão tático do DDD para avaliação de Enterprise Architecture",
    version="1.0.0"
)

app.include_router(router)

