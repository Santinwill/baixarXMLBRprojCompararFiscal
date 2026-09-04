from playwright.sync_api import Page
import re


def obter_total_paginas(page: Page):

    texto = page.locator("text=Página").first.text_content()
    numeros = re.findall(r"\d+", texto)

    pagina_atual = int(numeros[0])
    total_paginas = int(numeros[1])

    return pagina_atual, total_paginas


def ir_para_proxima_pagina(page):

    links = page.locator('a[href*="pagina="]')

    links.first.click()
    page.wait_for_load_state("networkidle")