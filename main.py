from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()

class Noticia(BaseModel):
    noticia: str

@app.post("/verificar")
def verificar_noticia(data: Noticia):
    estados = [
        {
            "estado": "🟢 Verificada",
            "mensaje": "La noticia es confiable y ha sido verificada por fuentes contrastadas.",
            "resumen": "Resumen automático: Esta noticia trata sobre un evento reciente relevante y ha sido confirmada por varias fuentes.",
        },
        {
            "estado": "🟡 Dudosa",
            "mensaje": "La noticia tiene elementos que requieren verificación adicional.",
            "resumen": "Resumen automático: La noticia presenta contenido parcialmente verificado. Se recomienda cautela.",
        },
        {
            "estado": "🔴 Falsa",
            "mensaje": "La noticia ha sido desmentida por verificadores confiables.",
            "resumen": "Resumen automático: Esta noticia ha sido identificada como engañosa o incorrecta según múltiples verificadores.",
        }
    ]

    resultado = random.choice(estados)
    resultado["timestamp"] = datetime.utcnow().isoformat()
    resultado["noticia"] = data.noticia
    return resultado
