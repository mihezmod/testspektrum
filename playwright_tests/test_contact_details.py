import re
import pytest
from playwright.sync_api import sync_playwright


TEST_VALUES_BUTTON_PHONE = [
    ("http://localhost:8080", "header", r"body > div > header > div > div > a.hidden.text-sm.font-semibold.text-ink-foreground.sm\:block"),
    ("http://localhost:8080/minsk-moscow", "header", r"body > div > header > div > div > a.hidden.text-sm.font-semibold.text-ink-foreground.sm\:block"),
    ("http://localhost:8080", "#hero", r"#hero > div.container-page.py-16 > div > div > a.btn-base.btn-outline-light.hover\:bg-white\/10"),
    ("http://localhost:8080/minsk-spb", "contact details", r"body > div > main > section.section-y.pt-12 > div > div > a.btn-base.border.border-border.transition-colors.hover\:bg-secondary"),
]

TEST_VALUES_PHONE_DETAILS = [
    ("http://localhost:8080", "#contacts", r"#contacts > div > div.mt-10.grid.gap-6.lg\:grid-cols-\[0\.9fr_1\.1fr\] > div.card-surface.space-y-5.p-6 > p:nth-child(2) > span > span > a:nth-child(1)"),
    ("http://localhost:8080", "#contacts", r"#contacts > div > div.mt-10.grid.gap-6.lg\:grid-cols-\[0\.9fr_1\.1fr\] > div.card-surface.space-y-5.p-6 > p:nth-child(2) > span > span > a:nth-child(2)"),
    ("http://localhost:8080", "#contacts", r"#contacts > div > div.mt-10.grid.gap-6.lg\:grid-cols-\[0\.9fr_1\.1fr\] > div.card-surface.space-y-5.p-6 > p:nth-child(2) > span > span > a:nth-child(3)"),
    ("http://localhost:8080", "#contacts", r"#contacts > div > div.mt-10.grid.gap-6.lg\:grid-cols-\[0\.9fr_1\.1fr\] > div.card-surface.space-y-5.p-6 > p:nth-child(2) > span > span > a:nth-child(4)"),
    ("http://localhost:8080/minsk-moscow", "contact details", r"body > div > main > section:nth-child(4) > div > div.card-surface.p-6 > dl > div:nth-child(1) > a"),
    ("http://localhost:8080/minsk-spb", "contact details", r"body > div > main > section:nth-child(4) > div > div.card-surface.p-6 > dl > div:nth-child(2) > a"),
    ("http://localhost:8080/minsk-tula", "contact details", r"body > div > main > section:nth-child(4) > div > div.card-surface.p-6 > dl > div:nth-child(3) > a"),
    ("http://localhost:8080/minsk-moscow", "contact details", r"body > div > main > section:nth-child(4) > div > div.card-surface.p-6 > dl > div:nth-child(4) > a"),
]

TEST_VALUES_EMAIL_DETAILS = [
    ("http://localhost:8080", "#contacts", r"#contacts > div > div.mt-10.grid.gap-6.lg\:grid-cols-\[0\.9fr_1\.1fr\] > div.card-surface.space-y-5.p-6 > p:nth-child(3) > span > a"),
    ("http://localhost:8080/minsk-tula", "contact details", r"body > div > main > section:nth-child(4) > div > div.card-surface.p-6 > dl > div:nth-child(5) > a"),
]

EXPECTED_MAIN_PHONE_NUMBER = "375172750821"


# Функция оставляет только цифры в номере телефона
def normalize_phone(value):
    return re.sub(r"\D", "", value)

# Функция проверяет соответствие текста ссылки и адреса tel:
def check_phone_link(link):
    text = link.inner_text().strip()
    href = link.get_attribute("href")

    assert href is not None and href.lower().startswith("tel:"), (
        f"Ожидалась ссылка tel:, получено: {href}"
    )

    text_phone = normalize_phone(text)
    href_phone = normalize_phone(href[4:])

    assert text_phone, f"В ссылке отсутствует номер телефона: «{text}»"
    assert text_phone == href_phone, (
        f"Номер в тексте «{text}» не совпадает с номером в адресе «{href}»"
    )

# Проверяет соответствие текста ссылки и адреса mailto:
def check_email_link(link):
    text_email = link.inner_text().strip().lower()
    href = link.get_attribute("href")

    assert href is not None and href.lower().startswith("mailto:"), (
        f"Ожидалась ссылка mailto:, получено: {href}"
    )

    href_email = href[7:].split("?")[0].strip().lower()

    assert text_email, "Текст email-ссылки пуст"
    assert text_email == href_email, (
        f"Email в тексте «{text_email}» не совпадает с адресом «{href}»"
    )


@pytest.mark.parametrize("buttons", TEST_VALUES_BUTTON_PHONE)
def test_button_phone_links(buttons):
    page_url, location, button_selector = buttons
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(page_url)
            page.wait_for_timeout(2000)


            # Выбираем тестируемый элемент.
            button_phone_link = page.locator(button_selector)
            # Проверяем что нашелся конкретно он один
            assert button_phone_link.count() == 1, (
                f"Ожидалась ровно одна кнопка с телефоном в секции '{location}' на странице '{page_url}'"
            )
            # Проверяем соответствие ссылки и текста на кнопке
            check_phone_link(button_phone_link)
            
            button_phone_number = normalize_phone(
                button_phone_link.inner_text()
            )
            assert button_phone_number == EXPECTED_MAIN_PHONE_NUMBER, (
                f"Номер телефона в разделе {location} ({button_phone_number}) "
                f"не совпадает с основным номером телефона ({EXPECTED_MAIN_PHONE_NUMBER})"
            )
        finally:
            browser.close()


@pytest.mark.parametrize("phones", TEST_VALUES_PHONE_DETAILS)
def test_phone_details(phones):
    page_url, location, phone_selector = phones
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(page_url)
            page.wait_for_timeout(2000)
            
            # Выбираем тестируемый элемент.
            phone_link = page.locator(phone_selector)
            # Проверяем что нашелся конкретно он один
            assert phone_link.count() == 1, (
                f"Ожидался ровно один элемент по селектору '{phone_selector}' в секции '{location}' на странице '{page_url}'"
            )
            # Проверяем соответствие ссылки и текста на элементе
            check_phone_link(phone_link) 
        finally:
            browser.close()
            
            
@pytest.mark.parametrize("emails", TEST_VALUES_EMAIL_DETAILS)
def test_email_details(emails):
    page_url, location, email_selector = emails
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(page_url)
            page.wait_for_timeout(2000)
            
            # Выбираем тестируемый элемент.
            email_link = page.locator(email_selector)
            # Проверяем что нашелся конкретно он один
            assert email_link.count() == 1, (
                f"Ожидался ровно один элемент по селектору '{email_selector}' в секции '{location}' на странице '{page_url}'"
            )
            # Проверяем соответствие ссылки и текста на элементе
            check_email_link(email_link) 
        finally:
            browser.close()