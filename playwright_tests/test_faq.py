
from playwright.sync_api import expect


PAGE_URL = "http://localhost:8080/"
PAGE_TIMEOUT = 10_000
FAQ_SELECTOR = "#faq details"


def test_faq_answers_open_and_close(page):
    page.goto(
        PAGE_URL,
        timeout=PAGE_TIMEOUT,
        wait_until="domcontentloaded",
    )

    faq_items = page.locator(FAQ_SELECTOR)
    expect(faq_items).to_have_count(6, timeout=PAGE_TIMEOUT)

    # Все ответы изначально закрыты.
    for i in range(faq_items.count()):
        expect(faq_items.nth(i)).not_to_have_attribute("open", "")

    # Проверяем открытие и закрытие первого ответа.
    item = faq_items.nth(0)
    question = item.locator("summary")
    answer = item.locator("p")

    expect(answer).to_be_hidden()

    # Открываем нажатием на вопрос.
    question.click()
    expect(item).to_have_attribute("open", "")
    expect(answer).to_be_visible()

    # Закрываем повторным нажатием.
    question.click()
    expect(item).not_to_have_attribute("open", "")
    expect(answer).to_be_hidden()

    # Проверяем нажатие на другую область строки вопроса.
    question.click(position={"x": 20, "y": 20})
    expect(item).to_have_attribute("open", "")
    expect(answer).to_be_visible()

    question.click(position={"x": 10, "y": 10})
    expect(item).not_to_have_attribute("open", "")
    expect(answer).to_be_hidden()
