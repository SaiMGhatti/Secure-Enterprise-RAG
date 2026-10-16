"""Record a short demo video of department-level access control.

Requires the API to be running (uvicorn app.main:app --port 8000) with documents
indexed, plus:  pip install playwright   (uses the locally installed Edge browser).

    python scripts/record_demo.py
"""
import shutil
import sys
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

BASE_URL = "http://localhost:8000/"
OUTPUT = Path("docs/demo.webm")

SCENARIOS = [
    (
        "dev-hr-manager",
        "HR Manager asks an HR question",
        "What is the remote work policy?",
        "Allowed: answered from HR documents",
    ),
    (
        "dev-hr-manager",
        "HR Manager asks about IT production incidents",
        "How are production incidents handled and who must be notified?",
        "Rejected: IT documents are not accessible to HR",
    ),
    (
        "dev-hr-manager",
        "HR Manager asks about Finance vendor payments",
        "What are the vendor payment approval controls?",
        "Rejected: Finance documents are not accessible to HR",
    ),
    (
        "dev-it-manager",
        "IT Manager asks the same question",
        "How are production incidents handled and who must be notified?",
        "Allowed: IT Manager can read IT documents",
    ),
]

CAPTION_JS = """
(text) => {
  let el = document.getElementById('demo-caption');
  if (!el) {
    el = document.createElement('div');
    el.id = 'demo-caption';
    el.style.cssText = 'position:fixed;bottom:0;left:0;right:0;padding:12px 20px;' +
      'background:#111827;color:#fff;font:600 17px system-ui;text-align:center;z-index:9999';
    document.body.appendChild(el);
  }
  el.textContent = text;
}
"""


def ask(page: Page, identity: str, question: str, timeout_ms: int = 280_000) -> None:
    page.select_option("#identity", identity)
    page.fill("#question", question)
    page.evaluate("document.getElementById('status').textContent = ''")
    page.click("#ask")
    page.wait_for_function(
        "document.getElementById('status').textContent.startsWith('Done')",
        timeout=timeout_ms,
    )


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    video_dir = OUTPUT.parent / "_video_tmp"
    shutil.rmtree(video_dir, ignore_errors=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")

        # Warm up models and the LLM off-camera so the recording stays short
        warm = browser.new_context().new_page()
        warm.goto(BASE_URL)
        ask(warm, "dev-hr-manager", "What is the remote work policy?")
        warm.close()

        context = browser.new_context(
            viewport={"width": 1000, "height": 760},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1000, "height": 760},
        )
        page = context.new_page()
        page.goto(BASE_URL)
        page.wait_for_timeout(1000)

        for identity, title, question, outcome in SCENARIOS:
            page.evaluate(CAPTION_JS, title)
            page.select_option("#identity", identity)
            page.fill("#question", "")
            page.type("#question", question, delay=15)
            page.wait_for_timeout(1200)
            ask(page, identity, question)
            page.evaluate(CAPTION_JS, outcome)
            page.wait_for_timeout(4500)

        video = page.video
        context.close()
        video.save_as(str(OUTPUT))
        browser.close()

    shutil.rmtree(video_dir, ignore_errors=True)
    print(f"Saved {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
