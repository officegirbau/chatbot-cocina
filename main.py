from fastapi import FastAPI
from pydantic import BaseModel, Field

import bot

app = FastAPI(
    title="Chatbot de Cocina",
    description="API de chat que responde preguntas sobre cocina: recetas, ingredientes, sustituciones y consejos.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    mensaje: str = Field(min_length=1, max_length=1000, examples=["Receta de tortilla de patatas"])
    sesion_id: str | None = Field(default=None, examples=["abc123"])


class ChatResponse(BaseModel):
    sesion_id: str
    respuesta: str
    sugerencias: list[str]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(peticion: ChatRequest) -> ChatResponse:
    sesion = peticion.sesion_id or bot.nueva_sesion()
    return ChatResponse(
        sesion_id=sesion,
        respuesta=bot.responder(peticion.mensaje),
        sugerencias=bot.sugerencias(),
    )


@app.get("/recetas")
def listar_recetas() -> dict:
    return {
        nombre: {
            "tiempo_minutos": datos["tiempo_minutos"],
            "dificultad": datos["dificultad"],
            "ingredientes": datos["ingredientes"],
        }
        for nombre, datos in bot.RECETAS.items()
    }


@app.get("/recetas/{nombre}")
def obtener_receta(nombre: str) -> dict:
    clave = nombre.lower().strip()
    resuelta = clave if clave in bot.RECETAS else bot._buscar_receta(clave)
    if not resuelta:
        return {"error": f"Receta no encontrada. Disponibles: {', '.join(bot.RECETAS)}"}
    return bot.RECETAS[resuelta]
