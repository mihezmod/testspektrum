
import pytest
from playwright.sync_api import expect


BASE_URL = "http://localhost:8080"
PAGE_TIMEOUT = 10_000
RESPONSE_CODE = 200

HEADER = "header"
NAVIGATION = 'nav[aria-label="Основная навигация"]'
PHONE = 'a[href="tel:+375172750821"]'
CONTACT_BUTTON = 'a.btn-cta[href="/#contacts"]'
MENU_BUTTON = 'button[aria-label="Меню"]'

VIEWPORT_CASES = [
    (1280, True, True, False),
    (1279, True, True, False),
    (1024, True, True, False),
    (1023, False, True, True),
    (640, False, True, True),
    (639, False, False, True),
]


@pytest.mark.parametrize(
    "width, navigation_visible, phone_visible, menu_visible",
    VIEWPORT_CASES,
)
def test_header_elements_visibility(
    page,
    width,
    navigation_visible,
    phone_visible,
    menu_visible,
):
    page.set_viewport_size({"width": width, "height": 900})

    response = page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=PAGE_TIMEOUT,
    )

    assert response is not None
    assert response.status == RESPONSE_CODE

    header = page.locator(HEADER)
    navigation = header.locator(NAVIGATION)
    phone = header.locator(PHONE)
    contact_button = header.locator(CONTACT_BUTTON)
    menu_button = header.locator(MENU_BUTTON)

    expect(header).to_be_visible()

    if navigation_visible:
        expect(navigation).to_be_visible()
    else:
        expect(navigation).to_be_hidden()

    if phone_visible:
        expect(phone).to_be_visible()
    else:
        expect(phone).to_be_hidden()

    if menu_visible:
        expect(menu_button).to_be_visible()
    else:
        expect(menu_button).to_be_hidden()

    expect(contact_button).to_be_visible()
