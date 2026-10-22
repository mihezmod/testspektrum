import pytest
from playwright.sync_api import expect


BASE_URL = "http://localhost:8080"
DIRECTION_NAME_AND_URN = [
    ("Минск → Москва", "/minsk-moscow"),
    ("Минск → Санкт-Петербург", "/minsk-spb"),
    ("Минск → Тула", "/minsk-tula"),
]
PAGE_TIMEOUT = 10_000

SERVICES_SECTION = "#services"
CONTACTS_SECTION = "#contacts"
GEOGRAPHY_SECTION = "#geography"


def test_service_contact_link_scrolls_to_contacts(page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    
    # Находим первую ссылку «Связаться» внутри раздела «Услуги».
    contact_link = page.locator(SERVICES_SECTION).get_by_role(
        "link", name="Связаться"
    ).first

    expect(contact_link).to_be_visible()
    contact_link.click()
    page.wait_for_timeout(2000)
    
    # Проверяем, что нужный раздел существует ровно в одном экземпляре и виден.
    contacts = page.locator(CONTACTS_SECTION)
    expect(contacts).to_be_visible()
    assert contacts.count() == 1, (
        f"Раздел «Контакты» с id='{CONTACTS_SECTION}' не найден или найден несколько раз. "
    )
    
    # Получаем расстояние от верхней границы раздела до верха окна.
    top = contacts.evaluate(
        "(element) => element.getBoundingClientRect().top"
    )
    # Убеждаемся что расстояние в допустимых пределах.
    assert abs(top) < 200, (
        f"Ошибка при навигации к разделу «Контакты» с id='{CONTACTS_SECTION}'. "
        f"Верх раздела в {top:.1f}px от верха окна, ожидалось менее 200 px. "
    )

@pytest.mark.parametrize("directions", DIRECTION_NAME_AND_URN)
def test_geography_button_opens_direction_page(page, directions):
    direction_name, expected_path = directions
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)

    geography = page.locator(GEOGRAPHY_SECTION)
    direction_button = geography.locator("a").filter(
        has=page.locator("span").filter(has_text=direction_name)
    )
    assert direction_button.count() == 1, (
        f"Кнопка направления '{direction_name}' не найдена или найдена несколько раз. "
    )
    expect(direction_button).to_be_visible()
    direction_button.click()

    expect(page).to_have_url(
        f"{BASE_URL}{expected_path}",
        timeout=PAGE_TIMEOUT,
    )
    page.wait_for_timeout(2000)