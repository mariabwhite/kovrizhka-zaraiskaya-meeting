import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
HTML = BASE / "client-meeting-2026-09-22.html"
PDF = BASE / "Коврижка_рабочая_встреча_2026-09-22.pdf"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=[
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ])
        # viewport A4 landscape ratio, 1x scale — легче по памяти на большом количестве PNG
        ctx = await b.new_context(viewport={"width": 1200, "height": 850}, device_scale_factor=1)
        page = await ctx.new_page()
        page.set_default_timeout(120000)
        await page.goto(HTML.as_uri(), wait_until="load", timeout=120000)
        await page.evaluate("""
            () => Promise.all(
                Array.from(document.images)
                    .filter(img => !img.complete)
                    .map(img => new Promise(r => { img.onload = img.onerror = r; }))
            )
        """)
        await page.wait_for_timeout(3000)
        await page.emulate_media(media="screen")
        await page.pdf(
            path=str(PDF),
            format="A4",
            landscape=True,
            print_background=True,
            prefer_css_page_size=False,
            margin={"top": "8mm", "bottom": "8mm", "left": "8mm", "right": "8mm"},
            scale=1.0,
        )
        await b.close()
        print(f"OK -> {PDF}")

asyncio.run(main())
