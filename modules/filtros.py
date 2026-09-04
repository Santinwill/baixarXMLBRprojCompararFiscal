from playwright.sync_api import Page
from datetime import datetime, timedelta


def configurar_filtros(page: Page):
    page.check('input[name="radiotipo"][value="recebidas"]')
    page.check("#chknfe")
    page.check("#chkcte")
    page.check('input[name="checktransf"]')
    page.fill("#destincnpj", "")
    page.click('input[name="semana"]')

    page.wait_for_load_state("networkidle")

    print("Filtros configurados")