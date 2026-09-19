#!/usr/bin/env python3
"""
Skill: webapp-testing
Script: playwright_runner.py
Scopo: test di base nel browser con Playwright
Uso: python playwright_runner.py <url> [--screenshot] [--a11y]
Output: JSON con informazioni sulla pagina, stato di salute ed eventuale percorso dello screenshot
Nota: richiede playwright (pip install playwright && playwright install chromium)
Screenshot: salvati nella cartella temporanea di sistema (ripulita dal sistema operativo)
"""
import sys
import json
import os
import tempfile
from datetime import datetime

# Codifica della console di Windows per l'output Unicode
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass  # Python < 3.7

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

INSTALL_HINT = "pip install playwright && playwright install chromium"

# Pulsanti e link senza testo accessibile (niente testo visibile, aria-label o title)
UNNAMED_JS = """
(selector) => [...document.querySelectorAll(selector)].filter(el =>
    !((el.innerText || '').trim() || el.getAttribute('aria-label') ||
      el.getAttribute('aria-labelledby') || el.getAttribute('title'))
).length
"""


def run_basic_test(url: str, take_screenshot: bool = False) -> dict:
    """Esegue un test di base nel browser sull'URL."""
    if not PLAYWRIGHT_AVAILABLE:
        return {
            "error": "Playwright non installato",
            "fix": INSTALL_HINT
        }

    result = {
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "status": "pending"
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            page = context.new_page()

            # Errori in console: il listener va registrato prima della navigazione
            console_errors = []
            page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

            # Navigazione
            response = page.goto(url, wait_until="networkidle", timeout=30000)

            # Informazioni di base
            result["page"] = {
                "title": page.title(),
                "url": page.url,
                "status_code": response.status if response else None
            }

            # Controlli di salute
            result["health"] = {
                "loaded": response.ok if response else False,
                "has_title": bool(page.title()),
                "has_h1": page.locator("h1").count() > 0,
                "has_links": page.locator("a").count() > 0,
                "has_images": page.locator("img").count() > 0
            }

            # Metriche di prestazione
            result["performance"] = {
                "dom_content_loaded": page.evaluate("window.performance.timing.domContentLoadedEventEnd - window.performance.timing.navigationStart"),
                "load_complete": page.evaluate("window.performance.timing.loadEventEnd - window.performance.timing.navigationStart")
            }

            # Screenshot nella cartella temporanea di sistema (multipiattaforma, ripulita dal sistema)
            if take_screenshot:
                # Windows=%TEMP%, Linux/macOS=/tmp
                screenshot_dir = os.path.join(tempfile.gettempdir(), "maestro_screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                page.screenshot(path=screenshot_path, full_page=True)
                result["screenshot"] = screenshot_path
                result["screenshot_note"] = "Salvato nella cartella temporanea (ripulita dal sistema operativo)"

            # Conteggio degli elementi
            result["elements"] = {
                "links": page.locator("a").count(),
                "buttons": page.locator("button").count(),
                "inputs": page.locator("input").count(),
                "images": page.locator("img").count(),
                "forms": page.locator("form").count()
            }

            result["console_errors"] = console_errors[:20]

            browser.close()

            result["status"] = "success" if result["health"]["loaded"] else "failed"
            result["summary"] = "[OK] Pagina caricata correttamente" if result["status"] == "success" else "[X] La pagina non si è caricata"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
        result["summary"] = f"[X] Errore: {str(e)[:100]}"

    return result


def run_accessibility_check(url: str) -> dict:
    """Esegue un controllo di accessibilità di base."""
    if not PLAYWRIGHT_AVAILABLE:
        return {"error": "Playwright non installato", "fix": INSTALL_HINT}

    result = {"url": url, "accessibility": {}}

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Controlli di accessibilità di base
            result["accessibility"] = {
                "images_with_alt": page.locator("img[alt]").count(),
                "images_without_alt": page.locator("img:not([alt])").count(),
                "buttons_without_label": page.evaluate(UNNAMED_JS, "button"),
                "links_without_text": page.evaluate(UNNAMED_JS, "a[href]"),
                "form_labels": page.locator("label").count(),
                "has_lang": bool(page.get_attribute("html", "lang")),
                "headings": {
                    "h1": page.locator("h1").count(),
                    "h2": page.locator("h2").count(),
                    "h3": page.locator("h3").count()
                }
            }

            browser.close()
            result["status"] = "success"

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Uso: python playwright_runner.py <url> [--screenshot] [--a11y]",
            "examples": [
                "python playwright_runner.py https://example.com",
                "python playwright_runner.py https://example.com --screenshot",
                "python playwright_runner.py https://example.com --a11y"
            ]
        }, indent=2, ensure_ascii=False))
        sys.exit(1)

    url = sys.argv[1]
    take_screenshot = "--screenshot" in sys.argv
    check_a11y = "--a11y" in sys.argv

    if check_a11y:
        result = run_accessibility_check(url)
    else:
        result = run_basic_test(url, take_screenshot)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    # Uscita diversa da 0 se il controllo non va a buon fine, così checklist.py e
    # verify_all.py non lo contano come superato (anche con Playwright mancante).
    sys.exit(0 if result.get("status") == "success" else 1)
