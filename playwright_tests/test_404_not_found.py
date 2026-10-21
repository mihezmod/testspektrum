from playwright.sync_api import expect


PAGE_URL="http://localhost:8080/invalid"
PAGE_TITLE="Страница не найдена — ООО «Униспектрум»"
RESPONSE_CODE=404
PAGE_TIMEOUT = 10_000


def test_404_not_found_page_opens(page):
    response = page.goto(
        PAGE_URL,
        timeout=PAGE_TIMEOUT,
        wait_until="domcontentloaded",
    )

    assert response is not None, (
        f"Не получен HTTP-ответ для страницы {PAGE_URL}"
    )

    assert response.status == RESPONSE_CODE, (
        f"Ожидался HTTP {RESPONSE_CODE}, получен HTTP {response.status}"
    )

    expect(page).to_have_title(
        PAGE_TITLE,
        timeout=PAGE_TIMEOUT,
    )