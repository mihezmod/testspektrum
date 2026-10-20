import pytest
from playwright.sync_api import sync_playwright


PAGES = [
    "http://localhost:8080",
    "http://localhost:8080/minsk-moscow",
]
SECTIONS = [
    ("Услуги", "/#services", "services"),
    ("Направления", "/#geography", "geography"),
    ("Преимущества", "/#advantages", "advantages"),
    ("Как мы работаем", "/#process", "process"),
    ("Контакты", "/#contacts", "contacts"),
    ("О нас", "/#about", "about"),
]
MENUES = [
    ("header", "body > div > header > div > nav > a"),
    ("footer", r"body > div > footer > div.container-page.grid.gap-8.md\:grid-cols-2 > nav > ul > li > a"),
]


# Декоратор pytest. Позволяет запустить функцию несколько раз с разными значениями аргументов.
@pytest.mark.parametrize("page_url", PAGES)
@pytest.mark.parametrize("menu", MENUES)
@pytest.mark.parametrize("section", SECTIONS)
def test_section_navigation(section, menu, page_url):
    link_title, expected_href, section_id = section
    menu_name, menu_selector = menu

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(page_url)
            page.wait_for_timeout(2000)
            
            # Прокручиваем страницу вниз перед проверкой навигации, чтобы была видна навигация в footer
            # page.evaluate() нужен для выполнения JavaScript-кода внутри страницы
            if menu_name == "footer":
                page.evaluate(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
                page.wait_for_timeout(500)
                
            # Выбираем ссылки в Header или Footer по CSS-селектору.
            menu_links = page.locator(menu_selector)
            # Ищем среди выбранных ссылок ту, у которой нужный текст.
            link = menu_links.get_by_text(link_title, exact=True)
            # Убеждаемся, что такая ссылка там одна
            assert link.count() == 1, (
                f"Ссылка с текстом «{link_title}» не найдена или найдена несколько раз. "
                f"Страница: {page_url}; меню: {menu_name}"
            )
            
            # Проверяем, что ссылка ведёт в ожидаемый раздел.
            actual_href = link.get_attribute("href")
            assert actual_href == expected_href, (
                f"У ссылки «{link_title}» неверный href. "
                f"Ожидался: {expected_href}; получен: {actual_href}. "
                f"Страница: {page_url}; меню: {menu_name}"
            )
            
            link.click()
            page.wait_for_timeout(3000)

            # Проверяем, что нужный раздел существует ровно в одном экземпляре.
            section_element = page.locator(f"#{section_id}")
            assert section_element.count() == 1, (
                f"Раздел «{link_title}» с id='{section_id}' не найден или найден несколько раз. "
                f"Страница: {page_url}; меню: {menu_name}"
            )

            # Получаем расстояние от верхней границы раздела до верха окна.
            top = section_element.evaluate(
                "(element) => element.getBoundingClientRect().top"
            )
            # Убеждаемся что расстояние в допустимых пределах.
            assert abs(top) < 200, (
                f"Навигация к разделу «{link_title}» с id='{section_id}' не сработала корректно. "
                f"Верх раздела находится на расстоянии {top:.1f} px от верха окна, ожидалось менее 200 px. "
                f"Страница: {page_url}; меню: {menu_name}"
            )

        finally:
            browser.close()
