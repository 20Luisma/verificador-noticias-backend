from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
import random

app = FastAPI()

# ✅ Habilitar CORS para que Netlify pueda hablar con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Si querés limitarlo, poné ["https://fabulous-daifuku-c7c1bb.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Noticia(BaseModel):
    noticia: str

@app.post("/verificar")
async def verificar_noticia(n: Noticia):
    noticia = n.noticia.lower()

    # Ejemplo básico para simular verificación
    estado = random.choice(["🟢 Verificada", "🟠 Dudosa", "🔴 Falsa"])
    mensaje = {
        "🟢 Verificada": "La noticia es confiable y ha sido verificada por fuentes contrastadas.",
        "🟠 Dudosa": "La noticia contiene información no confirmada. Requiere verificación adicional.",
        "🔴 Falsa": "La noticia ha sido desmentida por múltiples verificadores confiables."
    }[estado]

    resumen = "Resumen automático: Esta noticia trata sobre un evento reciente relevante y ha sido confirmada por varias fuentes." if estado == "🟢 Verificada" else "Resumen automático: Esta noticia podría no ser confiable, revisá fuentes adicionales."

    return {
        "estado": estado,
        "mensaje": mensaje,
        "resumen": resumen,
        "timestamp": datetime.utcnow().isoformat(),
        "noticia": noticia
    }

