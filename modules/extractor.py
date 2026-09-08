from pathlib import Path
from zipfile import ZipFile
import shutil


XML_DIR = Path("xmls")

XML_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def processar_arquivo(caminho_arquivo):
    caminho_arquivo = Path(caminho_arquivo)
    extensao = caminho_arquivo.suffix.lower()
    if extensao == ".zip":
        return extrair_zip(caminho_arquivo)
    if extensao == ".xml":
        return mover_xml(caminho_arquivo)
    print(f"Arquivo ignorado: {caminho_arquivo.name}")
    return []

def extrair_zip(caminho_zip):
    print(f"Extraindo ZIP: {caminho_zip.name}")
    with ZipFile(caminho_zip, "r") as zip_file:
        arquivos = zip_file.namelist()
        zip_file.extractall(XML_DIR)
    print(f"{len(arquivos)} arquivo(s) extraído(s)")
    return arquivos

def mover_xml(caminho_xml):
    nome_original = caminho_xml.stem
    partes = nome_original.split("_")
    chave = partes[-1]
    novo_nome = f"{chave}.xml"
    destino = XML_DIR / novo_nome
    shutil.move(
        str(caminho_xml),
        str(destino)
    )
    print(f"XML movido: {novo_nome}")
    return [novo_nome]