from playwright.sync_api import sync_playwright


def test_site_opens():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        response = page.goto("http://localhost:8080")

        assert response is not None
        assert response.status == 200

        # Проверяем, что у страницы есть заголовок
        assert page.title() != ""

        browser.close()


def test_contacts_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("http://localhost:8080")

        page.get_by_text("Контакты", exact=True).first.click()

        page.wait_for_timeout(1000)

        assert page.evaluate("window.scrollY") > 0

        browser.close()


def test_contact_links():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("http://localhost:8080")

        phone_link = page.locator('a[href^="tel:"]')
        email_link = page.locator('a[href^="mailto:"]')

        assert phone_link.count() > 0, "На странице нет ссылки на телефон"
        assert email_link.count() > 0, "На странице нет ссылки на email"

        browser.close()
