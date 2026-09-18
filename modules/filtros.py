from playwright.sync_api import Page
from datetime import datetime, timedelta

def obter_data_anterior():
    ontem = datetime.now() - timedelta(days=1)
    return ontem.strftime("%d/%m/%Y")

def configurar_filtros(page: Page, modo="documentos"):
    page.check('input[name="radiotipo"][value="recebidas"]')
    if modo == "documentos":
        page.check("#chknfe")
        page.check("#chkcte")
    elif modo == "nfse":
        page.check("#chknfsen")
    page.check('input[name="checktransf"]')
    data_consulta = obter_data_anterior()
    page.fill("#FormEmitDe", data_consulta)
    page.fill("#FormEmitAte", data_consulta)
    page.fill("#destincnpj", "")
    page.click('a[href="javascript:filtros.submit()"]')
    page.wait_for_load_state("networkidle")
    print(f"Filtros configurados: {modo}")    