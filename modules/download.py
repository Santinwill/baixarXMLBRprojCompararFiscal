from pathlib import Path
from playwright.sync_api import Page

DOWNLOADS_DIR = Path("downloads")

DOWNLOADS_DIR.mkdir(parents=True,exist_ok=True)

def selecionar_todos(page: Page):
    print("Selecionando checkbox TODOS...")
    checkbox_todos = page.locator("#TODOS")
    if checkbox_todos.count() == 0:
        raise Exception("Checkbox TODOS não foi encontrado na página.")
    checkbox_todos.check()
    if not checkbox_todos.is_checked():
        raise Exception("O checkbox TODOS não permaneceu marcado.")
    print("Checkbox TODOS marcado com sucesso")

def exportar_selecao(page: Page, pagina_atual: int):
    print("Iniciando exportação...")
    botao_exportar = page.locator('input[value="Exporta Seleção"]')
    if botao_exportar.count() == 0:
        raise Exception("Botão Exporta Seleção não encontrado.")
    with page.expect_download() as download_info:
        botao_exportar.click()
    download = download_info.value
    nome_original = download.suggested_filename
    destino = DOWNLOADS_DIR / (f"pagina_{pagina_atual}_{nome_original}")
    download.save_as(destino)
    print(f"Arquivo salvo em: {destino}")

    return destino