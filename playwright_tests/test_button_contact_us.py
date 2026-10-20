import re
import pytest
from playwright.sync_api import sync_playwright


TEST_VALUES=[
    ("http://localhost:8080", r"body > div > header > div > div > a.btn-base.btn-cta.hover\:btn-cta-hover.\!px-4.\!py-2.\!text-xs.text-center"),
    ("http://localhost:8080/minsk-moscow", r"body > div > header > div > div > a.btn-base.btn-cta.hover\:btn-cta-hover.\!px-4.\!py-2.\!text-xs.text-center"),
    ("http://localhost:8080", r"#hero > div.container-page.py-16 > div > div > a.btn-base.btn-cta.hover\:btn-cta-hover"),
    ("http://localhost:8080/minsk-spb", r"body > div > main > section.section-y.pt-12 > div > div > a.btn-base.btn-cta.hover\:btn-cta-hover"),
]


@pytest.mark.parametrize("test_values", TEST_VALUES)
def test_contact_button(test_values):
    starting_page, button_location = test_values
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(starting_page)
            page.wait_for_timeout(2000)

            # Находим кнопку в нужной части страницы.
            button = page.locator(button_location)
            assert button.count() == 1, (
                f"Кнопка не найдена или найдена несколько раз. "
                f"Тестовые данные: {starting_page} {button_location}; "
            )

            button.click()
            page.wait_for_timeout(3000)

           # Проверяем, что нужный раздел существует ровно в одном экземпляре.
            section_element = page.locator("#contacts")
            assert section_element.count() == 1, (
                f"Раздел «Контакты» не найден или найден несколько раз. "
                f"Тестовые данные: {starting_page} {button_location}; "
            )

            # Получаем расстояние от верхней границы раздела до верха окна.
            top = section_element.evaluate(
                "(element) => element.getBoundingClientRect().top"
            )
            # Убеждаемся что расстояние в допустимых пределах.
            assert abs(top) < 200, (
                f"Навигация к разделу «Контакты» не сработала корректно. "
                f"Верх раздела находится на расстоянии {top:.1f} px от верха окна, ожидалось менее 200 px. "
                f"Тестовые данные: {starting_page} {button_location}; "
            )

        finally:
            browser.close()