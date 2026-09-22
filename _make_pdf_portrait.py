import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
HTML = BASE / "client-meeting-2026-09-22.html"
PDF = BASE / "Коврижка_рабочая_встреча_2026-09-22_вертикаль.pdf"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=[
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ])
        # viewport A4 portrait ratio ~0.707 (width < height)
        ctx = await b.new_context(viewport={"width": 900, "height": 1273}, device_scale_factor=1)
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
        # Inject vertical override — A4 portrait при печати
        await page.add_style_tag(content="""
            @page { size: A4 portrait; margin: 10mm; }
            @media print {
                .g5 { grid-template-columns: repeat(2, minmax(0,1fr)) !important; gap: 12px !important; }
                .g3 { grid-template-columns: repeat(2, minmax(0,1fr)) !important; }
                .g2 { grid-template-columns: minmax(0,1fr) !important; }
                h1 { font-size: 42px !important; }
                h2 { font-size: 26px !important; }
            }
        """)
        await page.pdf(
            path=str(PDF),
            format="A4",
            landscape=False,
            print_background=True,
            margin={"top": "10mm", "bottom": "10mm", "left": "10mm", "right": "10mm"},
            scale=1.0,
        )
        await b.close()
        print(f"OK -> {PDF}")

asyncio.run(main())
