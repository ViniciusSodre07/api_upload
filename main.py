from fastapi import FastAPI, UploadFile, File, Form
import os
from datetime import datetime

app = FastAPI()

BASE_DIR = "dados_recebidos"
os.makedirs(BASE_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "API rodando"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    cliente: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...)
):
    pasta = f"{estado}_{cidade}_{cliente}".replace(" ", "_")
    caminho_pasta = os.path.join(BASE_DIR, pasta)
    os.makedirs(caminho_pasta, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{timestamp}_{file.filename}"
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)

    with open(caminho_arquivo, "wb") as f:
        f.write(await file.read())

    return {"status": "ok", "arquivo": nome_arquivo}