import pytest
from playwright.sync_api import sync_playwright


PAGES = [
    "http://localhost:8080",
    "http://localhost:8080/minsk-moscow",
]
EXPECTED_HREF = "/"
LOGO_LOCATOR = 'header a:has(img[alt="Логотип Униспектрум"])'


@pytest.mark.parametrize("page_url", PAGES)
def test_logo_navigation(page_url):

    with sync_playwright() as p:
        browser = p.chromium.launch()

        try:
            page = browser.new_page()
            page.goto(page_url)
            page.wait_for_timeout(2000)

            # Находим ссылку с логотипом в Header.
            link = page.locator(LOGO_LOCATOR)
            assert link.count() == 1, (
                f"Ссылка с логотипом не найдена или найдена несколько раз. Страница: {page_url}"
            )

            # Проверяем, что ссылка ведёт на главную страницу.
            actual_href = link.get_attribute("href")
            assert actual_href == EXPECTED_HREF, (
                f"У ссылки с логотипом неверный href. "
                f"Ожидался: {EXPECTED_HREF}; получен: {actual_href}. "
                f"Страница: {page_url}"
            )

            # Нажимаем на логотип.
            link.click()
            page.wait_for_timeout(3000)

            # Проверяем, что открылась главная страница.
            assert page.url.rstrip("/") == PAGES[0].rstrip("/"), (
                f"После нажатия на логотип ожидалась главная страница. "
                f"Текущий URL: {page.url}"
            )

            # Проверяем, что главный раздел существует.
            section_element = page.locator("#hero")
            assert section_element.count() == 1, (
                "Главный раздел с id='hero' не найден или найден несколько раз."
            )
             # Проверяем, что верх раздела находится близко к верху окна.
            top = section_element.evaluate(
                "(element) => element.getBoundingClientRect().top"
            )
            assert abs(top) < 200, (
                f"Навигация к главному разделу «Униспектрум» с id='hero' не сработала корректно. "
                f"Верх раздела находится на расстоянии {top:.1f} px от верха окна, ожидалось менее 200 px. "
                f"Страница: {page_url}; меню: header"
            )
            
        finally:
            browser.close()
