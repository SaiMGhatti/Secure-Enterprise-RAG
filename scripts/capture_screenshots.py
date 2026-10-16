"""Capture one screenshot per access-control scenario into docs/screenshots.

Requires the API to be running (uvicorn app.main:app --port 8000) with documents
indexed, plus:  pip install playwright   (uses the locally installed Edge browser).

    python scripts/capture_screenshots.py
"""
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://localhost:8000/"
OUTPUT_DIR = Path("docs/screenshots")

IT_QUESTION = "How are production incidents handled and who must be notified?"

SCENARIOS = [
    ("01-hr-manager-hr-question", "dev-hr-manager", "What is the remote work policy?"),
    ("02-hr-manager-denied-it", "dev-hr-manager", IT_QUESTION),
    (
        "03-hr-manager-denied-finance",
        "dev-hr-manager",
        "What are the vendor payment approval controls?",
    ),
    ("04-it-manager-it-question", "dev-it-manager", IT_QUESTION),
    (
        "05-finance-associate-denied-hr",
        "dev-finance-associate",
        "What is the remote work policy?",
    ),
]


def ask(page: Page, identity: str, question: str) -> None:
    page.select_option("#identity", identity)
    page.fill("#question", question)
    page.evaluate("document.getElementById('status').textContent = ''")
    page.click("#ask")
    page.wait_for_function(
        "document.getElementById('status').textContent.startsWith('Done')",
        timeout=280_000,
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")

        for name, identity, question in SCENARIOS:
            # Fresh page per scenario so "Recent questions" doesn't leak between shots
            page = browser.new_page(viewport={"width": 1000, "height": 640})
            page.goto(BASE_URL)
            ask(page, identity, question)
            # Hide timing so screenshots are stable between runs
            page.evaluate("document.getElementById('status').textContent = ''")
            page.evaluate("document.getElementById('historyCard').hidden = true")
            page.screenshot(path=str(OUTPUT_DIR / f"{name}.png"))
            page.close()
            print(f"Saved {name}.png")

        browser.close()


if __name__ == "__main__":
    main()
