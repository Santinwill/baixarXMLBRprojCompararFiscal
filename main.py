from playwright.sync_api import sync_playwright
from modules.config import (USUARIO,SENHA,validar_config)
from modules.login import fazer_login
from modules.filtros import configurar_filtros
from modules.pagination import (obter_total_paginas,ir_para_proxima_pagina)
from modules.download import (selecionar_todos,exportar_selecao)
from modules.extractor import processar_arquivo
from modules.logger import logger
from modules.statistics import Statistics
from modules.nfe_parser import processar_pasta_xmls
from modules.cte_parser import processar_pasta_ctes
from modules.nfse_parser import processar_pasta_nfses
from modules.fiscal_mapper import mapear_documentos
from modules.excel_exporter import gerar_excel
from datetime import datetime


def processar_consulta(page, stats):
    pagina_atual, total_paginas = obter_total_paginas(page)
    while pagina_atual <= total_paginas:
        mensagem = (f"Processando página {pagina_atual} de {total_paginas}")
        print(mensagem)
        selecionar_todos(page)
        arquivo_salvo = exportar_selecao(page,pagina_atual)
        resultado = processar_arquivo(arquivo_salvo)
        stats.xmls_novos += resultado["novos"]
        stats.xmls_duplicados += resultado["duplicados"]
        if pagina_atual < total_paginas:
            ir_para_proxima_pagina(page)
            pagina_atual, total_paginas = (obter_total_paginas(page))
        else:
            break

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
                browser = p.chromium.launch(headless=False)
                page = browser.new_page(accept_downloads=True)
                fazer_login(page,USUARIO,SENHA)
                logger.info("Login realizado com sucesso")
                print("Processando NFe e CTe")
                configurar_filtros(page,"documentos")
                processar_consulta(page,stats)
                configurar_filtros(page,"nfse")
                processar_consulta(page,stats)
                print("Todas as páginas foram processadas")
                logger.info("Todas as páginas foram processadas")
                print("Iniciando geração da planilha fiscal...")
                logger.info("Iniciando geração da planilha fiscal...")
                documentos = []
                documentos.extend(processar_pasta_xmls("xmls"))
                documentos.extend(processar_pasta_ctes("xmls"))
                documentos.extend(processar_pasta_nfses("xmls"))
                logger.info(f"NF e CTe processados: {len(documentos)}")
                print(f"NF-es encontradas: {len(processar_pasta_xmls('xmls'))}")
                print(f"CT-es encontrados: {len(processar_pasta_ctes('xmls'))}")
                print(f"NFse encontrados: {len(processar_pasta_nfses('xmls'))}")
                registros = mapear_documentos(documentos)
                print(f"Documentos totais: {len(documentos)}")
                print(f"Registros encontrados: {len(registros)}")
                logger.info(f"Registros fiscais gerados: {len(registros)}")
                if registros:
                    arquivo_excel = gerar_excel(registros)
                    mensagem_excel = (f"Excel gerado: {arquivo_excel}")
                    logger.info(mensagem_excel)
                else:
                    logger.warning("Nenhum registro fiscal encontrado.")
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
        logger.info("Processo BRProj encerrado\n\n")

if __name__ == "__main__":
    main()