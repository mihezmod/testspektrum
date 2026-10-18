from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


def test_404_not_found_page_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto("http://localhost:8080/invalid")

        assert response is not None
        assert response.status == 404
        expect(page).to_have_title("Страница не найдена — ООО «Униспектрум»")

        browser.close()