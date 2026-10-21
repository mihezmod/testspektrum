import pytest


PAGES = [
    "http://localhost:8080",
    "http://localhost:8080/minsk-moscow",
]
EXPECTED_HREF = "/"
LOGO_LOCATOR = 'header a:has(img[alt="Логотип Униспектрум"])'
PAGE_TIMEOUT = 10_000


@pytest.mark.parametrize("page_url", PAGES)
def test_logo_navigation(page, page_url):

    page.goto(page_url, timeout=PAGE_TIMEOUT)
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

    # Ждём перехода на главную страницу.
    page.wait_for_url(
        lambda url: str(url).rstrip("/") == PAGES[0].rstrip("/"),
        timeout=PAGE_TIMEOUT,
    )
    page.wait_for_timeout(2000)

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
        f"Ошибка при навигации к главной странице, разделу с id='hero'. "
        f"Верх раздела в {top:.1f} px от верха окна, ожидалось менее 200 px. "
        f"Страница: {page_url}; меню: header"
    )