
from playwright.sync_api import expect


BASE_URL = "http://localhost:8080"
MAIN_PAGE = f"{BASE_URL}/"
SECONDARY_PAGE = f"{BASE_URL}/minsk-moscow"

PAGE_TIMEOUT = 10_000
BUTTONS_BLOCK = "div.fixed.right-4.bottom-4"
THEME_BUTTON = 'button[aria-label="Тёмная тема"], button[aria-label="Светлая тема"]'

# Выбранная тема сохраняется при переходе между страницами сайта.
def test_theme_persists_between_pages(page):
    page.goto(MAIN_PAGE, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    
    html = page.locator("html")
    theme_button = page.locator(BUTTONS_BLOCK).locator(THEME_BUTTON)

    # Проверяем начальную светлую тему.
    expect(html).not_to_have_class("dark")
    expect(theme_button.locator("svg.lucide-moon")).to_be_visible()

    # Переключаем тему на тёмную.
    theme_button.click()

    expect(html).to_have_class("dark")
    expect(theme_button.locator("svg.lucide-sun")).to_be_visible()
    assert page.evaluate("localStorage.getItem('theme')") == "dark"

    # Переходим на второстепенную страницу.
    page.goto(SECONDARY_PAGE, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    
    html = page.locator("html")
    theme_button = page.locator(BUTTONS_BLOCK).locator(THEME_BUTTON)

    # Тёмная тема должна сохраниться после перехода.
    expect(html).to_have_class("dark")
    expect(theme_button.locator("svg.lucide-sun")).to_be_visible()
    assert page.evaluate("localStorage.getItem('theme')") == "dark"

    # Возвращаемся на главную.
    page.goto(MAIN_PAGE, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    
    html = page.locator("html")
    theme_button = page.locator(BUTTONS_BLOCK).locator(THEME_BUTTON)

    # Тёмная тема должна сохраниться и после обратного перехода.
    expect(html).to_have_class("dark")
    expect(theme_button.locator("svg.lucide-sun")).to_be_visible()
    assert page.evaluate("localStorage.getItem('theme')") == "dark"
