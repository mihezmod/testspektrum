import re
import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.parametrize(
    "starting_page",
    [
        "https://unispektrum.by/",
        "https://unispektrum.by/minsk-moscow",
    ],
)
@pytest.mark.parametrize("button_location", ["header", "main"])
def test_contact_button(starting_page, button_location):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(starting_page)
            page.wait_for_timeout(2000)

            # Находим кнопку в нужной части страницы.
            button = page.locator(button_location).get_by_role(
                "link",
                 name=re.compile(r"Свяжитесь с нами|Связаться с нами"),
            )

            assert button.count() == 1, (
                f"Кнопка «Свяжитесь с нами» не найдена или найдена несколько раз. "
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