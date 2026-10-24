
from playwright.sync_api import expect, Page


BASE_URL = "http://localhost:8080"
PAGE_TIMEOUT = 10_000
RESPONSE_CODE = 200

VIEWPORT_CASES = [
    (767, False),
    (768, True),
    (769, True),
]

FOOTER = "footer"
COMPANY_BLOCK = "footer > div.container-page.grid > div"
SECTIONS_BLOCK = 'footer nav[aria-label="Навигация в подвале"]'


def test_footer_responsive_layout(page: Page):
    for width, two_columns_expected in VIEWPORT_CASES:
        page.set_viewport_size({
            "width": width,
            "height": 900,
        })
        
        response = page.goto(
            BASE_URL,
            wait_until="domcontentloaded",
            timeout=PAGE_TIMEOUT,
        )

        assert response is not None
        assert response.status == RESPONSE_CODE

        footer = page.locator(FOOTER)
        company = page.locator(COMPANY_BLOCK)
        sections = page.locator(SECTIONS_BLOCK)

        expect(footer).to_be_visible()
        expect(company).to_be_visible()
        expect(sections).to_be_visible()

        company_box = company.bounding_box()
        sections_box = sections.bounding_box()

        assert company_box is not None
        assert sections_box is not None

        if two_columns_expected:
            assert company_box["x"] < sections_box["x"], (
                f"При ширине {width}px блок «Униспектрум» "
                "должен находиться левее блока «Разделы»"
            )
            assert abs(company_box["y"] - sections_box["y"]) < 5, (
                f"При ширине {width}px блоки должны находиться "
                "на одном уровне"
            )
        else:
            assert sections_box["y"] > company_box["y"], (
                f"При ширине {width}px блок «Разделы» "
                "должен находиться ниже блока «Униспектрум»"
            )
