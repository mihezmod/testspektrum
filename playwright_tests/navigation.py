
import pytest
from playwright.sync_api import sync_playwright

# Декоратор pytest. Позволяет запустить функцию несколько раз с разными значениями аргументов.
@pytest.mark.parametrize("starting_page", [
    "http://localhost:8080",
    "http://localhost:8080/minsk-moscow"
])
@pytest.mark.parametrize("menu_selector", ["header", "footer"])
@pytest.mark.parametrize("section", [
    ("Услуги", "/#services", "services"),
    ("Направления", "/#geography", "geography"),
    ("Преимущества", "/#advantages", "advantages"),
    ("Как мы работаем", "/#process", "process"),
    ("Контакты", "/#contacts", "contacts"),
    ("О нас", "/#about", "about"),
])
def test_section_navigation(menu_selector, section, starting_page):
    name, href, section_id = section

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(starting_page)
            page.wait_for_timeout(2000)

            # В шапке выбираем именно ссылку "Контакты", а не кнопку "Свяжитесь с нами", у которой тот же самый href
            if menu_selector == "header":
                link = page.get_by_role(
                    "navigation", name="Основная навигация"
                ).locator(f'a[href="{href}"]') # Буква f перед строкой позволяет подставлять значения переменных внутрь текста
            else:
                # Прокручиваем страницу вниз перед проверкой навигации, чтобы была видна навигация в footer
                # page.evaluate() нужен для выполнения JavaScript-кода внутри страницы
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                link = page.locator(f'footer a[href="{href}"]') 

            assert link.count() == 1, (
                f"Ссылка «{name}» c href='{href}' не найдена или найдена несколько раз. "
                f"Тестовые данные: {starting_page} {menu_selector} "
            )

            link.click()
            page.wait_for_timeout(3000)

            # Проверяем, что нужный раздел существует ровно в одном экземпляре.
            section_element = page.locator(f"#{section_id}")
            assert section_element.count() == 1, (
                f"Раздел «{name}» с id='{section_id}' не найден или найден несколько раз. "
                f"Тестовые данные: {starting_page} {menu_selector} "
            )

            # Получаем расстояние от верхней границы раздела до верха окна.
            top = section_element.evaluate(
                "(element) => element.getBoundingClientRect().top"
            )
            # Убеждаемся что расстояние в допустимых пределах.
            assert abs(top) < 200, (
                f"Навигация к разделу «{name}» с id='{section_id}' не сработала корректно. "
                f"Верх раздела находится на расстоянии {top:.1f} px от верха окна, ожидалось менее 200 px. "
                f"Тестовые данные: {starting_page} {menu_selector} "
            )

        finally:
            browser.close()
