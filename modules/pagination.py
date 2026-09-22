from playwright.sync_api import Page
import re

def obter_total_paginas(page: Page):
    texto_paginacao = page.locator("text=/\\d+\\s+de\\s+\\d+/").first.text_content()
    if not texto_paginacao:
        raise Exception("Não foi possível localizar o texto de paginação.")
    numeros = re.findall(r"\d+",texto_paginacao)
    if len(numeros) < 2:
        raise Exception(
            f"Não foi possível interpretar a paginação: "
            f"{texto_paginacao}"
        )
    pagina_atual = int(numeros[0])
    total_paginas = int(numeros[1])
    print(f"Página atual: {pagina_atual} | Total de páginas: {total_paginas}")
    return pagina_atual, total_paginas

def ir_para_pagina(page: Page, numero_pagina: int):
    url = (
        "https://gde2.brproj.com.br/"
        f"home.asp?pagina={numero_pagina}"
    )
    page.goto(url,wait_until="networkidle")
