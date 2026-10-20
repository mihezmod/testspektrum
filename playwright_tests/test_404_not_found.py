from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


PAGE_URL="http://localhost:8080/invalid"
PAGE_TITLE="Страница не найдена — ООО «Униспектрум»"
RESPONSE_CODE=404

def test_404_not_found_page_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto(PAGE_URL)

        assert response is not None
        assert response.status == RESPONSE_CODE
        expect(page).to_have_title(PAGE_TITLE)

        browser.close()