from playwright.sync_api import Page
import re

def obter_total_paginas(page: Page):
    texto_paginacao = page.locator("text=/\\d+\\s+de\\s+\\d+/").first.text_content()
    if not texto_paginacao:
        raise Exception("Não foi possível localizar o texto de paginação.")
    numeros = re.findall(r"\d+", texto_paginacao)
    if len(numeros) < 2:
        raise Exception(f"Não foi possível interpretar a paginação: {texto_paginacao}")
    pagina_atual = int(numeros[0])
    total_paginas = int(numeros[1])
    print(f"Página atual: {pagina_atual} | "
          f"Total de páginas: {total_paginas}")
    return pagina_atual, total_paginas

def ir_para_proxima_pagina(page: Page):
    links = page.locator('a[href*="pagina="]')
    if links.count() == 0:
        raise Excepti*n("Botão de próxima página não enc*ntrado.")
    links.first.click()
    page.wait_for_load_state("networkidle")
    print("Próxima pági*a carregada")