from playwright.sync_api import sync_playwright
from modules.config import (USUARIO,SENHA,validar_config)
from modules.login import fazer_login
from modules.filtros import configurar_filtros
from modules.pagination import (obter_total_paginas,ir_para_proxima_pagina)
from modules.download import (selecionar_todos,exportar_selecao)
from modules.extractor import processar_arquivo

def main():
    validar_config()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )
        page = browser.new_page()
        fazer_login(page,USUARIO,SENHA)
        configurar_filtros(page)
        pagina_atual, total_paginas = obter_total_paginas(page)
        while pagina_atual <= total_paginas:
            print(
                f"Processando página {pagina_atual} de {total_paginas}"
            )
            selecionar_todos(page)
            arquivo_salvo = exportar_selecao(page,pagina_atual)
            arquivos_processados = processar_arquivo(arquivo_salvo)
            print(f"{len(arquivos_processados)} arquivo(s) processado(s)")
            if pagina_atual < total_paginas:
                ir_para_proxima_pagina(page)
                pagina_atual, total_paginas = (
                    obter_total_paginas(page)
                )
            else:
                break
        print("Todas as páginas foram processadas")
        browser.close()

if __name__ == "__main__":
    main()    