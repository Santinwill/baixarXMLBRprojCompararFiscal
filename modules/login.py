from playwright.sync_api import Page


def fazer_login(page: Page, usuario: str, senha: str):

    page.goto("https://gde2.brproj.com.br/default.asp")

    page.fill("#login", usuario)
    page.fill("#password", senha)

    page.click("#submit")

    page.wait_for_load_state("networkidle")

    print("Login realizado com sucesso")