from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


def test_main_page_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto("http://localhost:8080")

        assert response is not None
        assert response.status == 200
        expect(page).to_have_title("ООО «Униспектрум» — грузоперевозки по Беларуси и России")

        browser.close()

def test_secondary_minsk_moscow_page_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto("http://localhost:8080/minsk-moscow")

        assert response is not None
        assert response.status == 200
        expect(page).to_have_title("Грузоперевозки Минск – Москва — тентованные фуры 25 т | ООО «Униспектрум»")

        browser.close()

def test_secondary_minsk_spb_page_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto("http://localhost:8080/minsk-spb")

        assert response is not None
        assert response.status == 200
        expect(page).to_have_title("Грузоперевозки Минск – Санкт-Петербург — тентованные фуры 25 т | ООО «Униспектрум»")

        browser.close()

def test_secondary_minsk_tula_page_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto("http://localhost:8080/minsk-tula")

        assert response is not None
        assert response.status == 200
        expect(page).to_have_title("Грузоперевозки Минск – Тула — тентованные фуры 25 т | ООО «Униспектрум»")

        browser.close()