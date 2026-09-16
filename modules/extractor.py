from pathlib import Path
from zipfile import ZipFile
import shutil

XML_DIR = Path("xmls")

XML_DIR.mkdir(parents=True,exist_ok=True)

def processar_arquivo(caminho_arquivo):
    caminho_arquivo = Path(caminho_arquivo)
    extensao = caminho_arquivo.suffix.lower()
    if extensao == ".zip":
        return extrair_zip(caminho_arquivo)
    if extensao == ".xml":
        return mover_xml(caminho_arquivo)
    print(f"Arquivo ignorado: {caminho_arquivo.name}")
    return {"novos": 0,"duplicados": 0}

def extrair_zip(caminho_zip):
    print(f"Extraindo ZIP: {caminho_zip.name}")
    novos = 0
    duplicados = 0
    with ZipFile(caminho_zip, "r") as zip_file:
        for nome_arquivo in zip_file.namelist():
            destino = XML_DIR / Path(nome_arquivo).name
            if destino.exists():
                print(f"XML já existe: {destino.name}")
                duplicados += 1
                continue
            zip_file.extract(nome_arquivo,XML_DIR)
            novos += 1
    print(f"{novos} novo(s) XML(s) extraído(s)")
    return {"novos": novos,"duplicados": duplicados}

def mover_xml(caminho_xml):
    nome_original = caminho_xml.stem
    partes = nome_original.split("_")
    chave = partes[-1]
    novo_nome = f"{chave}.xml"
    destino = XML_DIR / novo_nome
    if destino.exists():
        print(f"XML já existe: {novo_nome}")
        caminho_xml.unlink()
        return {"novos": 0,"duplicados": 1}
    shutil.move(str(caminho_xml),str(destino))
    print(f"XML movido: {novo_nome}")
    return {"novos": 1,"duplicados": 0}