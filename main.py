from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import requests

app = FastAPI()

# Middleware CORS para frontend (Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Noticia(BaseModel):
    noticia: str

API_KEY = "AIzaSyBNbFL250S8h7fPqsqKrBW1ngEeWayekn8"
FACTCHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def consultar_factcheck_api(texto):
    params = {
        "query": texto,
        "key": API_KEY,
        "languageCode": "es"
    }

    try:
        response = requests.get(FACTCHECK_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if "claims" in data and data["claims"]:
                claim = data["claims"][0]
                texto_claim = claim.get("text", "")
                review = claim.get("claimReview", [])[0]
                veredicto = review.get("textualRating", "")
                fuente = review.get("publisher", {}).get("name", "fuente desconocida")

                if "true" in veredicto.lower():
                    estado = "🟢 Verificada"
                elif "false" in veredicto.lower():
                    estado = "🔴 Falsa"
                else:
                    estado = "🟠 Dudosa"

                mensaje = f"La noticia fue revisada por {fuente} y está marcada como: {veredicto}."
                resumen = f"Texto verificado: {texto_claim}"

                return estado, mensaje, resumen, True  # ← True = se encontró una verificación real
            else:
                return (
                    "🟠 Dudosa",
                    "No hay resultados verificados para esta noticia.",
                    "Ninguna fuente confiable ha verificado esta información.",
                    False
                )
        else:
            return (
                "🟠 Dudosa",
                f"Error consultando la API de Google: {response.status_code}",
                "",
                False
            )
    except Exception as e:
        return (
            "🟠 Dudosa",
            f"Error interno al contactar la API: {str(e)}",
            "",
            False
        )

@app.post("/verificar")
def verificar_noticia(n: Noticia):
    estado, mensaje, resumen, verificada = consultar_factcheck_api(n.noticia)

    return {
        "estado": estado,
        "mensaje": mensaje,
        "resumen": resumen,
        "verificada": verificada,  # ← ¡Importante para el frontend!
        "timestamp": datetime.utcnow().isoformat(),
        "noticia": n.noticia
    }
