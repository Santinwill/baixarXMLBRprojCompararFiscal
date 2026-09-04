from playwright.sync_api import Page


def selecionar_todos(page: Page):

    checkbox_todos = page.locator("#TODOS")

    if checkbox_todos.count() == 0:
        raise Exception("Checkbox TODOS não foi encontrado na página.")

    checkbox_todos.check()

    if checkbox_todos.is_checked():
        print("Checkbox TODOS marcado com sucesso")
    else:
        raise Exception("O checkbox TODOS não permaneceu marcado.")