from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import requests

app = FastAPI()

# Permitir acceso desde el frontend (Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Podés poner solo Netlify si querés limitar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Noticia(BaseModel):
    noticia: str

# Tu clave de API de Google Fact Check
API_KEY = "AIzaSyBNbFL250S8h7fPqsqKrBW1ngEeWayekn8"
FACTCHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def consultar_factcheck_api(texto):
    params = {
        "query": texto,
        "key": API_KEY,
        "languageCode": "es"  # podés cambiar a "en" para inglés
    }

    try:
        response = requests.get(FACTCHECK_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if "claims" in data and data["claims"]:
                claim = data["claims"][0]
                texto_claim = claim["text"]
                veredicto = claim["claimReview"][0]["textualRating"]
                fuente = claim["claimReview"][0]["publisher"]["name"]

                # Interpretamos el veredicto
                if "true" in veredicto.lower():
                    estado = "🟢 Verificada"
                elif "false" in veredicto.lower():
                    estado = "🔴 Falsa"
                else:
                    estado = "🟠 Dudosa"

                mensaje = f"La noticia fue revisada por {fuente} y está marcada como: {veredicto}."
                resumen = f"Texto original verificado: {texto_claim}"
                return estado, mensaje, resumen
            else:
                return "🟠 Dudosa", "No se encontraron verificaciones sobre esta noticia.", "Sin información verificada disponible."
        else:
            return "🟠 Dudosa", f"Error al consultar la API: {response.status_code}", ""
    except Exception as e:
        return "🟠 Dudosa", f"Excepción al consultar la API: {str(e)}", ""

@app.post("/verificar")
def verificar_noticia(n: Noticia):
    estado, mensaje, resumen = consultar_factcheck_api(n.noticia)

    return {
        "estado": estado,
        "mensaje": mensaje,
        "resumen": resumen,
        "timestamp": datetime.utcnow().isoformat(),
        "noticia": n.noticia
    }


