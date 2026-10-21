
from playwright.sync_api import expect
import pytest


BASE_URL = "http://localhost:8080"
PAGES = [
    f"{BASE_URL}/",
    f"{BASE_URL}/minsk-moscow",
]

MAIN_PHONE = "tel:+375172750821"
PAGE_TIMEOUT = 10_000
SCROLL_THRESHOLD = 600

BUTTONS_BLOCK = "div.fixed.right-4.bottom-4"
SCROLL_TOP_BUTTON = 'button[aria-label="Наверх"]'
CALL_BUTTON = 'a[aria-label="Позвонить"]'
THEME_BUTTON = 'button[aria-label="Тёмная тема"], button[aria-label="Светлая тема"]'


# Блок кнопок виден на обеих страницах, порядок кнопок правильный.
@pytest.mark.parametrize("url", PAGES)
def test_floating_buttons_visibility_and_order(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    page.evaluate(
                "window.scrollTo(0, document.body.scrollHeight)"
            )
    block = page.locator(BUTTONS_BLOCK)
    expect(block).to_be_visible()

    # Проверяем порядок элементов сверху вниз.
    buttons = block.locator(":scope > button, :scope > a")
    expect(buttons).to_have_count(3)

    expect(block.locator(SCROLL_TOP_BUTTON)).to_have_count(1)
    expect(block.locator(CALL_BUTTON)).to_have_count(1)
    expect(block.locator(THEME_BUTTON)).to_have_count(1)

    scroll_box = block.locator(SCROLL_TOP_BUTTON).bounding_box()
    call_box = block.locator(CALL_BUTTON).bounding_box()
    theme_box = block.locator(THEME_BUTTON).bounding_box()

    assert scroll_box["y"] < call_box["y"], "Кнопка «Наверх» должна быть выше кнопки звонка"
    assert call_box["y"] < theme_box["y"], "Кнопка звонка должна быть выше кнопки темы"


# Кнопка «Наверх» появляется после прокрутки и скрывается у начала страницы.
@pytest.mark.parametrize("url", PAGES)
def test_scroll_to_top_button_visibility(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    scroll_button = page.locator(BUTTONS_BLOCK).locator(SCROLL_TOP_BUTTON)
    # В начале страницы кнопка должна быть скрыта.
    page.evaluate("window.scrollTo(0, 0)")
    expect(scroll_button).to_be_hidden()
    # Прокручиваем страницу ниже предполагаемого порога.
    page.evaluate("(threshold) => window.scrollTo(0, threshold + 1)", SCROLL_THRESHOLD)
    expect(scroll_button).to_be_visible()
    # Нажимаем кнопку и проверяем возврат к началу.
    scroll_button.click()
    page.wait_for_function(
        "() => window.scrollY === 0",
        timeout=PAGE_TIMEOUT,
    )
    expect(scroll_button).to_be_hidden()


# Кнопка звонка видна и содержит правильный номер телефона.
@pytest.mark.parametrize("url", PAGES)
def test_call_button_link(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)

    call_button = page.locator(BUTTONS_BLOCK).locator(CALL_BUTTON)

    expect(call_button).to_be_visible()
    expect(call_button).to_have_attribute("href", MAIN_PHONE)


# Иконка соответствует теме, переключение меняет тему и сохраняет выбор.
@pytest.mark.parametrize("url", PAGES)
def test_theme_button_icon_and_toggle(page, url):
    # Устанавливаем светлую тему перед загрузкой страницы.
    page.add_init_script("""
        localStorage.setItem("theme", "light");
    """)

    page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
    page.wait_for_timeout(2000)
    
    html = page.locator("html")
    theme_button = page.locator(BUTTONS_BLOCK).locator(THEME_BUTTON)

    # Светлая тема: у html нет класса dark, кнопка показывает луну.
    expect(html).not_to_have_class("dark")
    expect(theme_button).to_be_visible()
    expect(theme_button).to_have_attribute("aria-label", "Тёмная тема")
    expect(theme_button.locator("svg.lucide-moon")).to_be_visible()

    # Переключаемся на тёмную тему.
    theme_button.click()

    expect(html).to_have_class("dark")
    expect(theme_button).to_have_attribute("aria-label", "Светлая тема")
    expect(theme_button.locator("svg.lucide-sun")).to_be_visible()
    assert page.evaluate("localStorage.getItem('theme')") == "dark"

    # Возвращаемся к светлой теме.
    theme_button.click()

    expect(html).not_to_have_class("dark")
    expect(theme_button).to_have_attribute("aria-label", "Тёмная тема")
    expect(theme_button.locator("svg.lucide-moon")).to_be_visible()
    assert page.evaluate("localStorage.getItem('theme')") == "light"
