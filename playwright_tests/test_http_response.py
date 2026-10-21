import pytest
from playwright.sync_api import sync_playwright, expect


RESPONSE_CODE = 200
TEST_VALUES = [
    ("http://localhost:8080", "ООО «Униспектрум» — грузоперевозки по Беларуси и России"),
    ("http://localhost:8080/minsk-moscow", "Грузоперевозки Минск – Москва — тентованные фуры 25 т | ООО «Униспектрум»"),
    ("http://localhost:8080/minsk-spb", "Грузоперевозки Минск – Санкт-Петербург — тентованные фуры 25 т | ООО «Униспектрум»"),
    ("http://localhost:8080/minsk-tula", "Грузоперевозки Минск – Тула — тентованные фуры 25 т | ООО «Униспектрум»"),
]
PAGE_TIMEOUT = 10_000


@pytest.mark.parametrize("test_values", TEST_VALUES)
def test_page_opens(page, test_values):
    page_url, page_title = test_values
    
    response = page.goto(page_url, timeout=PAGE_TIMEOUT, wait_until="domcontentloaded")

    assert response is not None, (
        f"Не получен HTTP-ответ для {page_url}"
    )
    assert response.status == RESPONSE_CODE, (
        f"Ожидался HTTP {RESPONSE_CODE}, "
        f"получен HTTP {response.status}: {page_url}"
    )

    expect(page).to_have_title(page_title, timeout=PAGE_TIMEOUT)