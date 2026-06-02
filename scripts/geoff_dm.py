import asyncio, os
from playwright.async_api import async_playwright

SESSION = '/Users/raymondpaterson/odysseus/odysseus/ig_session'
if not os.path.exists(SESSION):
    SESSION = os.path.expanduser('~/ig_session')

async def run():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            SESSION, headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        print('Opening Geoff profile...')
        await page.goto('https://www.instagram.com/geoffreeve/')
        await page.wait_for_timeout(6000)
        await page.screenshot(path='/tmp/geoff_step1.png')

        # Try all buttons and find Message one
        clicked = False
        btns = await page.query_selector_all('div[role="button"], button')
        for btn in btns:
            try:
                txt = await btn.inner_text()
                if 'essage' in txt:
                    print(f'Clicking button: {txt}')
                    await btn.click()
                    clicked = True
                    await page.wait_for_timeout(4000)
                    break
            except:
                pass

        if not clicked:
            print('No Message button found - check /tmp/geoff_step1.png')
            await ctx.close()
            return

        await page.screenshot(path='/tmp/geoff_step2.png')

        box = await page.query_selector('div[aria-label="Message"], div[contenteditable="true"], textarea')
        if box:
            print('Typing message...')
            await box.click()
            await page.wait_for_timeout(500)
            lines = [
                'こんにちは！🤖 สวัสดีครับ！你好！',
                '私はレイモンドのAIアシスタント、リトルバードです。',
                'ฉันชื่อ Littlebird — ผู้ช่วย AI ของ Raymond',
                '我是雷蒙德的人工智能助手。',
                'よろしくお願いします！🙏✨'
            ]
            for i, line in enumerate(lines):
                await box.type(line)
                if i < len(lines) - 1:
                    await page.keyboard.press('Shift+Enter')
            await page.wait_for_timeout(500)
            await page.keyboard.press('Enter')
            print('SENT TO GEOFF')
        else:
            print('No message box - check /tmp/geoff_step2.png')

        await page.wait_for_timeout(3000)
        await ctx.close()

asyncio.run(run())
