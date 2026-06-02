#!/usr/bin/env python3
"""
SEEK Auto-Apply Engine - HyperSuite Job Module
Applies to: Perigon Group, Budget Direct, Big Ass Fans, Randstad
Logs to: ~/Clipper/seek_apply.log
Screenshots to: ~/Clipper/seek_screenshots/
"""
import asyncio, os, shutil, logging, time, sys
from pathlib import Path

HOME = str(Path.home())
CLIPPER = os.path.join(HOME, 'Clipper')
SCREENSHOTS = os.path.join(CLIPPER, 'seek_screenshots')
os.makedirs(CLIPPER, exist_ok=True)
os.makedirs(SCREENSHOTS, exist_ok=True)

LOG = os.path.join(CLIPPER, 'seek_apply.log')
logging.basicConfig(
    filename=LOG, level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s', filemode='a'
)

def log(msg):
    print(msg, flush=True)
    logging.info(msg)

try:
    from playwright.async_api import async_playwright
except ImportError:
    log('Installing playwright...')
    os.system(f'{sys.executable} -m pip install playwright -q')
    os.system(f'{sys.executable} -m playwright install chromium')
    from playwright.async_api import async_playwright

CHROME_SRC = os.path.join(HOME, 'Library', 'Application Support', 'Google', 'Chrome')
PROFILE_COPY = os.path.join(CLIPPER, 'seek_chrome_session')

# ==================== COVER LETTERS ====================
# NOTE: No mention of references in any letter - avoids prompting recruiters to ask.

COVER_PERIGON = """Dear Hiring Manager,

I am writing to apply for the Data Entry Specialist position at Perigon Group. With hands-on experience in high-volume data entry and administration across logistics and customer service environments, I am confident I can contribute to your national project team with the accuracy and consistency this role demands.

In my role as a Relationship Consultant at FedEx, I managed logistics data across multiple high-priority accounts, consistently meeting a 4-hour email SLA while maintaining strict data accuracy KPIs. At Concentrix, I handled significant volumes of back-office processing, data entry, and records management across multiple campaigns simultaneously - building both speed and attention to detail in structured, process-driven settings.

I am proficient in Microsoft Office, comfortable navigating multiple systems, and well-practised in applying formatting and naming conventions to large datasets. I take genuine pride in delivering work that is complete and accurate the first time.

I am immediately available, Brisbane-based, and hold full Australian working rights. I am well-suited to the structured, high-volume nature of this 6-month project and look forward to contributing to your team.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_BUDGET = """Dear Hiring Manager,

I am pleased to apply for the Customer Service Consultant role at Budget Direct. Having spent several years in customer-facing roles across call centre, logistics, and e-commerce environments, I am drawn to Budget Direct's culture of recognition, clear progression pathways, and genuine investment in training from day one.

At Concentrix, I managed high volumes of inbound and outbound customer interactions across multiple campaigns including customer service, back-office processing, admin, data entry, and chat support. At FedEx, I managed ongoing relationships with high-priority accounts, ensuring smooth communication under fast-paced SLA requirements. At Omnisorb, I handled all customer queries end-to-end via phone and email, resolving delivery, warranty, and product issues with a calm, solution-focused approach.

I thrive in structured, team-based environments and am comfortable with rotating rosters and varied hours. I hold full unrestricted Australian working rights, am based in Brisbane, and am available to commence on the July 20 start date.

I am excited by the opportunity to bring my communication skills and customer-first mindset to Budget Direct and grow within the insurance sector through your 12-week training program.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_BIGASS = """Dear Hiring Manager,

I am applying for the Warehouse Junior role at Big Ass Fans. I am a physically capable, reliable, and detail-oriented worker with a strong track record in fast-paced operational environments, and I am eager to develop my warehouse career with a company that clearly invests in its team.

My background includes hands-on logistics and delivery work with DoorDash, where I maintained a 4.92/5 customer rating through consistent accuracy, time management, and a professional approach to every job. At Omnisorb, I was directly responsible for picking, packaging, and dispatching customer orders for e-commerce fulfilment, coordinating with couriers, conducting inventory checks, and maintaining accuracy throughout. I hold a current open Australian driver's licence and take workplace safety seriously.

I hold full unrestricted Australian working rights and am available to commence immediately.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_RANDSTAD = """Dear Hiring Manager,

I am writing to apply for the AO3 Administration Officer contract role with Randstad, supporting your State Government client in Brisbane. I am available to commence from 15 June 2026.

Throughout my career across FedEx, Concentrix, and Omnisorb, I have developed strong administrative foundations: managing high-volume email correspondence, maintaining accurate data and records, processing orders and coordinating logistics, and supporting multiple stakeholders simultaneously under tight deadlines. I am proficient in Microsoft Office - particularly Word, Excel, and Outlook - and I am a confident learner when it comes to new platforms including financial and records management systems.

I understand the importance of confidentiality, accurate documentation, and professional conduct in a government-facing environment. I hold full unrestricted Australian working rights, a completed National Police Check (May 2026), and am immediately available for interview at short notice.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

# ==================== JOB LIST ====================

JOBS = [
    {'id': '92326132', 'company': 'Perigon Group',  'title': 'Data Entry Specialist',       'cover': COVER_PERIGON},
    {'id': '92437271', 'company': 'Budget Direct',   'title': 'Customer Service Consultant', 'cover': COVER_BUDGET},
    {'id': '92135907', 'company': 'Big Ass Fans',    'title': 'Warehouse Junior',            'cover': COVER_BIGASS},
    {'id': '92461106', 'company': 'Randstad',        'title': 'AO3 Admin Officer',           'cover': COVER_RANDSTAD},
]

# ==================== HELPERS ====================

async def ss(page, name):
    try:
        p = os.path.join(SCREENSHOTS, f'{name}.png')
        await page.screenshot(path=p)
        log(f'Screenshot: {p}')
    except Exception as e:
        log(f'Screenshot failed: {e}')

def prepare_profile():
    dest_default = os.path.join(PROFILE_COPY, 'Default')
    os.makedirs(dest_default, exist_ok=True)
    src_default = os.path.join(CHROME_SRC, 'Default')
    for fname in ['Cookies', 'Web Data', 'Preferences', 'Secure Preferences']:
        src = os.path.join(src_default, fname)
        dst = os.path.join(dest_default, fname)
        try:
            if os.path.exists(src):
                shutil.copy2(src, dst)
                log(f'Copied profile file: {fname}')
        except Exception as e:
            log(f'Could not copy {fname}: {e}')
    for dname in ['Local Storage', 'Session Storage']:
        src_d = os.path.join(src_default, dname)
        dst_d = os.path.join(dest_default, dname)
        try:
            if os.path.exists(src_d) and not os.path.exists(dst_d):
                shutil.copytree(src_d, dst_d)
                log(f'Copied profile dir: {dname}')
        except Exception as e:
            log(f'Could not copy dir {dname}: {e}')
    return PROFILE_COPY

async def wait_for_login(page):
    content = await page.content()
    title = (await page.title()).lower()
    if 'sign in' in content.lower() and 'seek' in title:
        log('SEEK login page detected - waiting up to 90s...')
        for _ in range(18):
            await asyncio.sleep(5)
            content = await page.content()
            if 'sign in' not in content.lower() or 'dashboard' in page.url:
                log('Login detected - continuing')
                return True
        log('Timed out waiting for login')
        return False
    return True

async def skip_references(page):
    """
    Detect if the current step is a references page and skip it.
    Tries: Skip button, skip link, remove any pre-filled reference fields.
    Returns True if references step was detected and handled.
    """
    content = await page.content()
    content_lower = content.lower()
    is_references_page = (
        'reference' in content_lower and
        any(k in content_lower for k in [
            'add a reference', 'add reference', 'referee', 'reference name',
            'reference details', 'your references', 'provide a reference'
        ])
    )
    if not is_references_page:
        return False

    log('References step detected - attempting to skip...')
    await ss(page, f'refs_step_{int(time.time())}')

    # Try clicking Skip buttons/links first
    skip_selectors = [
        'button:has-text("Skip")',
        'a:has-text("Skip")',
        'button:has-text("skip")',
        '[data-automation="skip"]',
        '[data-automation*="skip" i]',
        'button:has-text("I\'ll do this later")',
        'button:has-text("Not now")',
        'a:has-text("Skip this step")',
        'button:has-text("Skip this step")',
    ]
    for sel in skip_selectors:
        try:
            el = await page.query_selector(sel)
            if el and await el.is_visible():
                await el.click()
                log(f'References skipped via: {sel}')
                await page.wait_for_timeout(2500)
                return True
        except:
            pass

    # No skip button - leave all reference fields empty and click Next/Continue
    log('No skip button found on references step - leaving fields empty and proceeding...')
    next_selectors = [
        'button:has-text("Next")',
        'button:has-text("Continue")',
        'button:has-text("Submit application")',
        'button:has-text("Submit")',
        '[data-automation="next"]',
        'button[type="submit"]',
    ]
    for sel in next_selectors:
        try:
            el = await page.query_selector(sel)
            if el and await el.is_visible() and await el.is_enabled():
                txt = (await el.text_content() or '').strip()
                await el.click()
                log(f'References step: clicked "{txt}" with empty fields')
                await page.wait_for_timeout(2500)
                return True
        except:
            pass

    log('Could not bypass references step automatically')
    return True  # Still flag as detected so main loop knows

async def fill_cover(page, text):
    selectors = [
        'textarea[name="coverLetter"]',
        '[data-automation="coverLetterTextArea"] textarea',
        '[data-automation*="cover"] textarea',
        'textarea[aria-label*="cover" i]',
        'textarea[placeholder*="cover" i]',
        'textarea[id*="cover" i]',
        'textarea',
    ]
    for sel in selectors:
        try:
            els = await page.query_selector_all(sel)
            for el in els:
                if await el.is_visible():
                    await el.click()
                    await el.fill(text)
                    log(f'Cover letter filled via: {sel}')
                    return True
        except:
            pass
    log('WARNING: Cover letter field not found on this step')
    return False

async def click_next(page):
    priority = [
        'button:has-text("Submit application")',
        'button:has-text("Submit")',
        'button:has-text("Next")',
        'button:has-text("Continue")',
        '[data-automation="submit-application"]',
        '[data-automation="next"]',
        'button[type="submit"]',
    ]
    for sel in priority:
        try:
            btns = await page.query_selector_all(sel)
            for btn in btns:
                if await btn.is_visible() and await btn.is_enabled():
                    txt = (await btn.text_content() or '').strip()
                    await btn.click()
                    log(f'Clicked: "{txt}" via {sel}')
                    await page.wait_for_timeout(3000)
                    return txt
        except:
            pass
    return None

async def handle_questions(page):
    try:
        groups = await page.query_selector_all('fieldset')
        for g in groups:
            txt = (await g.text_content() or '').lower()
            if any(k in txt for k in ['right to work', 'work in australia', 'australian working rights', 'australian citizen']):
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: right to work = Yes')
            elif any(k in txt for k in ['located in', 'reside in', 'based in australia', 'live in']):
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: located in = Yes')
            elif any(k in txt for k in ['immediately available', 'available to start', 'available to commence']):
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: immediately available = Yes')
            elif 'driver' in txt and 'licence' in txt and 'forklift' not in txt:
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: driver licence = Yes')
            elif 'forklift' in txt:
                no = await g.query_selector('label:has-text("No")')
                if no: await no.click(); log('Q: forklift = No')
            # References-related questions - skip/answer No
            elif any(k in txt for k in ['do you have a reference', 'can you provide a reference', 'do you have referees']):
                no = await g.query_selector('label:has-text("No")')
                if no: await no.click(); log('Q: references = No')
    except Exception as e:
        log(f'Questions handler error: {e}')

# ==================== APPLY LOGIC ====================

async def apply_job(ctx, job):
    log(f'\n{"="*55}')
    log(f'APPLYING: {job["company"]} | {job["title"]}')
    log(f'{"="*55}')
    page = await ctx.new_page()
    try:
        url = f'https://au.seek.com/job/{job["id"]}/apply'
        await page.goto(url, timeout=45000)
        await page.wait_for_timeout(4000)
        await ss(page, f'{job["id"]}_start')

        start_content = await page.content()
        if 'already applied' in start_content.lower() or 'application has been sent' in start_content.lower():
            log(f'SKIP: Already applied to {job["company"]}')
            await page.close()
            return 'ALREADY_APPLIED'

        await wait_for_login(page)

        cover_done = False
        for step in range(1, 15):
            url_now = page.url
            log(f'Step {step} | {url_now[:90]}')

            content = await page.content()

            # Success detection
            if ('success' in url_now or
                    'Application sent' in content or
                    'application has been sent' in content.lower() or
                    'good luck' in content.lower()):
                log(f'>>> SUCCESS: {job["company"]} application SENT! <<<')
                await ss(page, f'{job["id"]}_SUCCESS')
                await page.close()
                return 'SENT'

            # ALWAYS check for references step first and skip it
            ref_handled = await skip_references(page)
            if ref_handled:
                continue  # Re-evaluate the page after skipping

            # Handle screening questions
            await handle_questions(page)

            # Fill cover letter (once)
            if not cover_done:
                filled = await fill_cover(page, job['cover'])
                if filled:
                    cover_done = True
                    await page.wait_for_timeout(800)

            # Click next/submit
            btn = await click_next(page)
            if not btn:
                log(f'No button found at step {step} - stopping')
                await ss(page, f'{job["id"]}_stuck_s{step}')
                break

            await page.wait_for_timeout(2500)

        final_content = await page.content()
        if 'Application sent' in final_content or 'success' in page.url or 'good luck' in final_content.lower():
            log(f'>>> SUCCESS: {job["company"]} <<<')
            await page.close()
            return 'SENT'

        await ss(page, f'{job["id"]}_uncertain')
        log(f'UNCERTAIN: {job["company"]} - check screenshots')
        await page.close()
        return 'UNCERTAIN'

    except Exception as e:
        log(f'ERROR for {job["company"]}: {e}')
        try:
            await ss(page, f'{job["id"]}_error')
            await page.close()
        except:
            pass
        return 'ERROR'

# ==================== MAIN ====================

async def main():
    log('=' * 60)
    log('SEEK AUTO-APPLY ENGINE - HyperSuite')
    log(f'Time: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    log(f'Jobs: {len(JOBS)}')
    log('=' * 60)

    profile = prepare_profile()
    log(f'Profile dir: {profile}')

    async with async_playwright() as pw:
        try:
            ctx = await pw.chromium.launch_persistent_context(
                user_data_dir=profile,
                headless=False,
                args=[
                    '--no-sandbox',
                    '--disable-blink-features=AutomationControlled',
                ],
                ignore_https_errors=True
            )
            log('Browser launched with Chrome session profile')
        except Exception as e:
            log(f'Profile launch failed: {e}')
            log('Falling back to fresh browser...')
            ctx = await pw.chromium.launch_persistent_context(
                user_data_dir=os.path.join(CLIPPER, 'seek_fresh'),
                headless=False
            )

        page = ctx.pages[0] if ctx.pages else await ctx.new_page()

        log('Checking SEEK session...')
        await page.goto('https://au.seek.com', timeout=30000)
        await page.wait_for_timeout(3000)
        await ss(page, '00_seek_home')
        log(f'SEEK title: {await page.title()}')

        results = {}
        for job in JOBS:
            status = await apply_job(ctx, job)
            results[job['company']] = status
            await asyncio.sleep(4)

        log('\n' + '=' * 60)
        log('FINAL RESULTS')
        log('=' * 60)
        for co, st in results.items():
            log(f'  {co:30s}: {st}')
        log('=' * 60)
        log('Screenshots: ~/Clipper/seek_screenshots/')
        log('Log: ~/Clipper/seek_apply.log')

        await asyncio.sleep(6)
        await ctx.close()
        log('Engine complete.')

if __name__ == '__main__':
    asyncio.run(main())
