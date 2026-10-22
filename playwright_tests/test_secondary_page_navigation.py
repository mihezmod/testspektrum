
import pytest
from playwright.sync_api import expect, Page


BASE_URL = "http://localhost:8080"
PAGE_TIMEOUT = 10_000

SECONDARY_PAGE = "/minsk-moscow"

BREADCRUMB_LINKS = [
    ("Главная", "/", "hero", BASE_URL),
    ("Направления", "/#geography", "geography", BASE_URL),
]

ALL_SERVICES_SELECTOR = (
    "body > div > main > section:nth-child(4) "
    "> div > div.card-surface.p-6 > a"
)


@pytest.mark.parametrize("link_title, href, section_id, expected_url", BREADCRUMB_LINKS)
def test_breadcrumb_navigation_to_main_page(
    page: Page, link_title, href, section_id, expected_url
):
    page.goto(
        f"{BASE_URL}{SECONDARY_PAGE}",
        wait_until="domcontentloaded",
        timeout=PAGE_TIMEOUT,
    )

    breadcrumbs = page.get_by_role("navigation", name="Хлебные крошки")
    link = breadcrumbs.get_by_role("link", name=link_title, exact=True)

    expect(link).to_be_visible()
    expect(link).to_have_attribute("href", href)

    link.click()
    page.wait_for_timeout(2000)

    # Проверяем, что нужный раздел существует ровно в одном экземпляре.
    section_element = page.locator(f"#{section_id}")
    assert section_element.count() == 1, (
        f"Раздел «{link_title}» с id='{section_id}' не найден или найден несколько раз. "
        f"Страница: {page.url};"
    )

    # Получаем расстояние от верхней границы раздела до верха окна.
    top = section_element.evaluate(
        "(element) => element.getBoundingClientRect().top"
    )
    # Убеждаемся что расстояние в допустимых пределах.
    assert abs(top) < 200, (
        f"Ошибка при навигации к разделу «{link_title}» с id='{section_id}'. "
        f"Верх раздела в {top:.1f}px от верха окна, ожидалось менее 200 px. "
        f"Страница: {page.url}; "
    )


def test_all_services_link_opens_services_section(page):
    page.goto(
        f"{BASE_URL}{SECONDARY_PAGE}",
        wait_until="domcontentloaded",
        timeout=PAGE_TIMEOUT,
    )

    all_services_link = page.locator(ALL_SERVICES_SELECTOR)

    expect(all_services_link).to_be_visible()
    expect(all_services_link).to_have_text("← Все услуги компании")
    
    all_services_link.click()
    page.wait_for_timeout(2000)
    
    section_element = page.locator(f"#services")
    assert section_element.count() == 1, (
        f"Раздел «Услуги» с id='#services' не найден или найден несколько раз. "
        f"Страница: {page.url};"
    )
    
    # Получаем расстояние от верхней границы раздела до верха окна.
    top = section_element.evaluate(
        "(element) => element.getBoundingClientRect().top"
    )
    # Убеждаемся что расстояние в допустимых пределах.
    assert abs(top) < 200, (
        f"Ошибка при навигации к разделу «Услуги» с id='#services'. "
        f"Верх раздела в {top:.1f}px от верха окна, ожидалось менее 200 px. "
        f"Страница: {page.url}; "
    )
