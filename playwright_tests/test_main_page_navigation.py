
from playwright.sync_api import expect


BASE_URL = "http://localhost:8080"
PAGE_TIMEOUT = 10_000

SERVICES_SECTION = "#services"
CONTACTS_SECTION = "#contacts"


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
