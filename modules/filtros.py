from playwright.sync_api import Page
from datetime import datetime, timedelta

def obter_data_anterior():
    ontem = datetime.now() - timedelta(days=1)
    return ontem.strftime("%d/%m/%Y")

def configurar_filtros(page: Page, modo="documentos"):
    print("URL atual:")
    print(page.url)
    print("Título:")
    print(page.title())
    page.check('input[name="radiotipo"][value="recebidas"]')
    if modo == "documentos":
        page.check("#chknfe")
        page.check("#chkcte")
    elif modo == "nfse":
        page.wait_for_selector("#chknfsen",timeout=10000)
        page.check("#chknfsen")
    page.check('input[name="checktransf"]')
    data_consulta = obter_data_anterior()
    page.fill("#FormEmitDe", data_consulta)
    page.fill("#FormEmitAte", data_consulta)
    page.fill("#destincnpj", "")
    page.click('a[href="javascript:filtros.submit()"]')
    page.wait_for_load_state("networkidle")
    print(f"Filtros configurados: {modo}")    
    print(
    f"Modo selecionado: {modo}"
    )

    print(
        f"Página atual após pesquisa:"
    )

    texto = page.locator(
        "text=/\\d+\\s+de\\s+\\d+/"
    ).first.text_content()

    print(texto)