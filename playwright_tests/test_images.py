
import pytest
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

TEST_URLS = [
    "http://localhost:8080",
    "http://localhost:8080/minsk-tula",
]

PAGE_TIMEOUT = 30_000
IMAGES_TIMEOUT = 15_000


@pytest.mark.parametrize("page_url", TEST_URLS)
def test_images_loaded(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch()

        try:
            page = browser.new_page()

            # Открываем страницу, не ожидая завершения всей сетевой активности
            page.goto(
                page_url,
                wait_until="domcontentloaded",
                timeout=PAGE_TIMEOUT,
            )

            # Просим браузер загрузить изображения с lazy loading и меняем на eager
            page.evaluate("""
                () => {
                    for (const img of document.images) {
                        img.loading = "eager";
                    }
                }
            """)

            # Ждём завершения загрузки всех изображений до истечения таймаута
            try:
                page.wait_for_function(
                    """
                    () => Array.from(document.images)
                        .every(img => img.complete)
                    """,
                    timeout=IMAGES_TIMEOUT,
                )
            except PlaywrightTimeoutError:
                # Незавершённые загрузки обнаружим в проверке ниже
                pass

            # Собираем изображения, которые не загрузились корректно
            broken_images = page.locator("img").evaluate_all("""
                images => images
                    .filter(img =>
                        !img.complete ||
                        img.naturalWidth === 0 ||
                        img.naturalHeight === 0
                    )
                    .map(img => ({
                        url: img.currentSrc || img.src,
                        complete: img.complete,
                        width: img.naturalWidth,
                        height: img.naturalHeight
                    }))
            """)

            assert not broken_images, (
                f"Проблемы с изображениями на странице {page_url}:\n"
                + "\n".join(
                    f"{img['url']} "
                    f"(complete={img['complete']}, "
                    f"size={img['width']}x{img['height']})"
                    for img in broken_images
                )
            )

        finally:
            browser.close()
