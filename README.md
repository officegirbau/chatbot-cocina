# Chatbot de Cocina 🍳

API de chat en Python (FastAPI) que responde preguntas sobre cocina: recetas, ingredientes, tiempos de cocción, sustituciones y consejos.

## Ejecutar

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/chat` | Enviar un mensaje y recibir la respuesta del bot |
| `GET`  | `/recetas` | Lista todas las recetas disponibles |
| `GET`  | `/recetas/{nombre}` | Detalle de una receta |
| `GET`  | `/health` | Comprobación de estado |
| `GET`  | `/docs` | Documentación interactiva (Swagger) |

## Ejemplo

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"mensaje": "receta de paella"}'
```

Respuesta:

```json
{
  "sesion_id": "a1b2c3d4e5f6",
  "respuesta": "Sobre paella valenciana: 70 min, dificultad media. Pídeme los ingredientes, los pasos o el tiempo.",
  "sugerencias": ["Receta de tortilla de patatas", "¿Con qué sustituyo la nata?", "¿Cuánto tarda la paella?", "Dame un consejo de cocina"]
}
```

## Qué entiende el bot

- **Recetas**: «receta de tortilla», «cómo hago carbonara»
- **Ingredientes**: «ingredientes del gazpacho»
- **Tiempos**: «cuánto tardan las lentejas»
- **Dificultad**: «¿es difícil la paella?»
- **Sustituciones**: «¿con qué sustituyo el huevo?»
- **Consejos**: «dame un truco de cocina»
- **Ideas**: «¿qué cocino hoy?»

## Añadir recetas

Edita el diccionario `RECETAS` en `bot.py`: cada receta tiene `ingredientes`, `pasos`, `tiempo_minutos` y `dificultad`. El bot la reconocerá automáticamente.
