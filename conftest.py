import pytest


@pytest.fixture(autouse=True)
def log_javascript_errors(page):
    def on_page_error(error):
        print(f"\n[JS EXCEPTION]: {error}")

    def on_console(message):
        if message.type == "error":
            print(f"\n[JS CONSOLE ERROR]: {message.text}")

    page.on("pageerror", on_page_error)
    page.on("console", on_console)

