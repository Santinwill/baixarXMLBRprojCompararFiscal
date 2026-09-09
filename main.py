from playwright.sync_api import sync_playwright
from modules.config import (USUARIO,SENHA,validar_config)
from modules.login import fazer_login
from modules.filtros import configurar_filtros
from modules.pagination import (obter_total_paginas,ir_para_proxima_pagina)
from modules.download import (selecionar_todos,exportar_selecao)
from modules.extractor import processar_arquivo
from modules.logger import logger
from modules.statistics import Statistics
from datetime import datetime

def main():
    stats = Statistics()
    inicio_execucao = datetime.now()
    logger.info("Iniciando processo BRProj")
    try:
        validar_config()
        logger.info("Configurações do ambiente validadas")
        with sync_playwright() as p:
            browser = None
            try:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(accept_downloads=True)
                fazer_login(page,USUARIO,SENHA)
                logger.info("Login realizado com sucesso")
                configurar_filtros(page)
                logger.info("Filtros configurados com sucesso")
                pagina_atual, total_paginas = (obter_total_paginas(page))
                while pagina_atual <= total_paginas:
                    mensagem_pagina = (f"Processando página "f"{pagina_atual} de "f"{total_paginas}")
                    print(mensagem_pagina)
                    logger.info(mensagem_pagina)
                    stats.paginas_processadas += 1
                    selecionar_todos(page)
                    arquivo_salvo = exportar_selecao(page,pagina_atual)
                    stats.downloads_realizados += 1
                    logger.info(f"Arquivo salvo: "f"{arquivo_salvo}")
                    resultado = processar_arquivo(arquivo_salvo)
                    stats.xmls_novos += (resultado["novos"])
                    stats.xmls_duplicados += (resultado["duplicados"])
                    mensagem_novos = (f"XMLs novos na página "f"{pagina_atual}: "f"{resultado['novos']}")
                    mensagem_duplicados = (f"XMLs duplicados na página "f"{pagina_atual}: "f"{resultado['duplicados']}")
                    print(mensagem_novos)
                    print(mensagem_duplicados)
                    logger.info(mensagem_novos)
                    logger.info(mensagem_duplicados)
                    if pagina_atual < total_paginas:
                        ir_para_proxima_pagina(page)
                        pagina_atual, total_paginas = (obter_total_paginas(page))
                    else:
                        break
                print("Todas as páginas foram processadas")
                logger.info("Todas as páginas foram processadas")
            finally:
                if browser is not None:
                    try:
                        browser.close()
                        logger.info("Navegador encerrado")
                    except Exception as erro_fechamento:
                        stats.erros += 1
                        logger.exception("Erro ao encerrar navegador: "f"{erro_fechamento}")
    except Exception as erro:
        stats.erros += 1
        print(f"Erro durante a execução: {erro}")
        logger.exception(f"Erro durante a execução: {erro}")
        raise
    finally:
        fim_execucao = datetime.now()
        tempo_total = (fim_execucao - inicio_execucao)
        stats.tempo_execucao = (str(tempo_total).split(".")[0])
        resumo = stats.resumo()
        print(resumo)
        logger.info(resumo)
        logger.info("Processo BRProj encerrado")

if __name__ == "__main__":
    main()