from playwright.sync_api import expect


BASE_URL = "http://localhost:8080"
PAGE_TIMEOUT = 10_000
MOBILE_WIDTH = 1023

MENU_BUTTON = 'header button[aria-label="Меню"]'
MOBILE_MENU_LINKS = "body > div > header > nav > div > a"
MOBILE_MENU_LINKS_COUNT = 6
MOBILE_NAVIGATION = 'body > div > header > nav[aria-label="Мобильная навигация"]'


def test_mobile_menu_toggle(page):
    page.set_viewport_size({
        "width": MOBILE_WIDTH,
        "height": 900,
    })

    page.goto(
        BASE_URL,
        wait_until="domcontentloaded",
        timeout=PAGE_TIMEOUT,
    )
    page.wait_for_timeout(3000)

    menu_button = page.locator(MENU_BUTTON)
    mobile_navigation = page.locator(MOBILE_NAVIGATION)

    # Изначально меню закрыто
    expect(menu_button).to_be_visible()
    expect(menu_button).to_have_attribute("aria-expanded", "false")
    expect(mobile_navigation).to_be_hidden()

    # Открываем меню
    menu_button.click()
    expect(menu_button).to_have_attribute(
        "aria-expanded",
        "true",
        timeout=PAGE_TIMEOUT,
    )
    expect(mobile_navigation).to_be_visible(timeout=PAGE_TIMEOUT)

    # Проверяем количество и видимость ссылок в открытом меню
    menu_links = mobile_navigation.locator("div > a")
    expect(menu_links).to_have_count(MOBILE_MENU_LINKS_COUNT)
    for link in menu_links.all():
        expect(link).to_be_visible()

    # Закрываем меню повторным нажатием
    menu_button.click()
    expect(menu_button).to_have_attribute(
        "aria-expanded",
        "false",
        timeout=PAGE_TIMEOUT,
    )
    
    expect(mobile_navigation).to_be_hidden(timeout=PAGE_TIMEOUT)
    # Проверяем количество и видимость ссылок в открытом меню
    for link in menu_links.all():
        expect(link).to_be_hidden()
    
