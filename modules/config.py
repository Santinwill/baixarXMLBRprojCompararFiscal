from dotenv import load_dotenv
import os

load_dotenv()

USUARIO = os.getenv("BRPROJ_USUARIO")
SENHA = os.getenv("BRPROJ_SENHA")
URL = os.getenv("BRPROJ_URL")

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
XML_DIR = os.getenv("XML_DIR", "xmls")
LOG_DIR = os.getenv("LOG_DIR", "logs")


def validar_config():
    campos_obrigatorios = {
        "BRPROJ_USUARIO": USUARIO,
        "BRPROJ_SENHA": SENHA,
        "BRPROJ_URL": URL,
    }

    faltando = [
        nome
        for nome, valor in campos_obrigatorios.items()
        if not valor
    ]

    if faltando:
        raise Exception(
            f"Variáveis não configuradas no .env: {', '.join(faltando)}"
        )