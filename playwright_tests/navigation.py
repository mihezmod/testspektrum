
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
        browser = p.chromium.launch()

        try:
            page = browser.new_page()
            page.goto(starting_page)

            # Прокручиваем страницу вниз перед проверкой навигации, чтобы была видна навигация в footer
            # page.evaluate() нужен для выполнения JavaScript-кода внутри страницы
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            # В шапке выбираем именно ссылку "Контакты", а не кнопку "Свяжитесь с нами", у которой тот же самый href
            if menu_selector == "header":
                link = page.get_by_role(
                    "navigation", name="Основная навигация"
                ).locator(f'a[href="{href}"]') # Буква f перед строкой позволяет подставлять значения переменных внутрь текста
            else:
                link = page.locator(f'footer a[href="{href}"]') 

            assert link.count() == 1, (
                f"Ссылка «{name}» не найдена или найдена несколько раз"
            )

            link.click()

             # Ждём начала прокрутки, а затем её завершения.
            scroll_result = page.evaluate("""
                () => new Promise(resolve => {
                    let lastY = window.scrollY;
                    let started = false;
                    let stableFrames = 0;
                    const startTime = performance.now();

                    function checkScroll() {
                        const currentY = window.scrollY;
                        const elapsed = performance.now() - startTime;
                        const moved = Math.abs(currentY - lastY) >= 1;

                        if (moved) {
                            started = true;
                            stableFrames = 0;
                        } else if (started) {
                            stableFrames++;
                        }

                        lastY = currentY;

                        if (started && stableFrames >= 10) {
                            resolve({
                                status: "completed",
                                scrollY: currentY
                            });
                        } else if (!started && elapsed >= 3000) {
                            resolve({
                                status: "not_started",
                                scrollY: currentY
                            });
                        } else if (elapsed >= 10000) {
                            resolve({
                                status: "timeout",
                                scrollY: currentY
                            });
                        } else {
                            requestAnimationFrame(checkScroll);
                        }
                    }

                    requestAnimationFrame(checkScroll);
                })
            """)
            assert scroll_result["status"] == "completed", (
                f"Прокрутка не завершилась корректно. "
                f"Статус: {scroll_result['status']}; "
                f"текущий scrollY: {scroll_result['scrollY']} px"
            )

            # Проверяем, что нужный раздел существует ровно в одном экземпляре.
            section_element = page.locator(f"#{section_id}")
            assert section_element.count() == 1, (
                f"Раздел «{name}» с id='{section_id}' "
                f"не найден или найден несколько раз"
            )

            # Получаем расстояние от верхней границы раздела до верха окна.
            # Убеждаемся что оно в допустимых пределах.
            top = section_element.evaluate(
                "(element) => element.getBoundingClientRect().top"
            )
            assert abs(top) < 200, (
                f"Навигация к разделу «{name}» не сработала корректно. "
                f"Верх раздела находится на расстоянии {top:.1f} px "
                f"от верха окна, ожидалось менее 200 px."
            )

        finally:
            # Выполнится даже при падении теста.
            browser.close()
