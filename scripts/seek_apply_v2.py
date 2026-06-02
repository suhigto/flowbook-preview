#!/usr/bin/env python3
"""
SEEK Auto-Apply Engine v2 - HyperSuite
Jobs: TactiCall/QBCC, Re.Group, Volare, QLD Treasury, Hydraulink
Browser fallback: Chrome session -> Firefox session -> Manual login wait
No references. No children-related roles.
Log: ~/Clipper/seek_apply_v2.log
Screenshots: ~/Clipper/seek_screenshots_v2/
"""
import asyncio, os, shutil, logging, time, sys, glob
from pathlib import Path

HOME = str(Path.home())
CLIPPER = os.path.join(HOME, 'Clipper')
SCREENSHOTS = os.path.join(CLIPPER, 'seek_screenshots_v2')
os.makedirs(CLIPPER, exist_ok=True)
os.makedirs(SCREENSHOTS, exist_ok=True)

LOG = os.path.join(CLIPPER, 'seek_apply_v2.log')
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
    os.system(f'{sys.executable} -m playwright install chromium firefox')
    from playwright.async_api import async_playwright

# ===================== BROWSER PROFILE PATHS =====================

CHROME_SRC   = os.path.join(HOME, 'Library', 'Application Support', 'Google', 'Chrome')
CHROME_COPY  = os.path.join(CLIPPER, 'seek_chrome_v2')
FIREFOX_COPY = os.path.join(CLIPPER, 'seek_firefox_v2')
FRESH_DIR    = os.path.join(CLIPPER, 'seek_fresh_v2')

def prepare_chrome_profile():
    dest = os.path.join(CHROME_COPY, 'Default')
    os.makedirs(dest, exist_ok=True)
    src_default = os.path.join(CHROME_SRC, 'Default')
    for fname in ['Cookies', 'Web Data', 'Preferences', 'Secure Preferences']:
        src = os.path.join(src_default, fname)
        dst = os.path.join(dest, fname)
        try:
            if os.path.exists(src): shutil.copy2(src, dst)
        except Exception as e:
            log(f'Chrome copy warn {fname}: {e}')
    for dname in ['Local Storage', 'Session Storage']:
        src_d = os.path.join(src_default, dname)
        dst_d = os.path.join(dest, dname)
        try:
            if os.path.exists(src_d) and not os.path.exists(dst_d):
                shutil.copytree(src_d, dst_d)
        except Exception as e:
            log(f'Chrome copy dir warn {dname}: {e}')
    return CHROME_COPY

def find_firefox_profile():
    patterns = [
        os.path.join(HOME, 'Library', 'Application Support', 'Firefox', 'Profiles', '*.default-release'),
        os.path.join(HOME, 'Library', 'Application Support', 'Firefox', 'Profiles', '*.default'),
    ]
    for pat in patterns:
        found = glob.glob(pat)
        if found:
            log(f'Firefox profile found: {found[0]}')
            return found[0]
    log('No Firefox profile found')
    return None

def prepare_firefox_profile():
    src = find_firefox_profile()
    if not src:
        return None
    dest = FIREFOX_COPY
    if os.path.exists(dest):
        shutil.rmtree(dest, ignore_errors=True)
    try:
        shutil.copytree(src, dest)
        log(f'Firefox profile copied to: {dest}')
        return dest
    except Exception as e:
        log(f'Firefox profile copy failed: {e}')
        return None

# ===================== COVER LETTERS =====================
# No reference language anywhere.

COVER_TACTICALL = """Dear Hiring Manager,

I am writing to apply for the AO3 Customer Service Officer position at QBCC via TactiCall Recruitment. With a strong background in high-volume, multi-channel customer service across call centre, logistics, and e-commerce environments, I am well-placed to deliver the accurate, consistent, and empathetic service QBCC provides to Queensland's building and construction community.

At Concentrix, I managed a high volume of inbound and outbound customer interactions across multiple campaigns, consistently meeting KPIs for response times, resolution rates, and customer satisfaction. I was skilled at navigating multiple systems simultaneously, applying policies and procedures to resolve diverse customer queries, and documenting interactions with precision. At FedEx, I managed ongoing relationships with high-priority accounts, interpreting service terms and coordinating outcomes across multiple departments under tight SLA requirements.

I am comfortable handling complex or sensitive enquiries professionally and empathetically, including complaints, and I understand the importance of applying legislative and policy frameworks accurately to protect both consumers and the organisation. I am confident learning new systems and legislation rapidly, as demonstrated across varied campaigns in my time at Concentrix.

I hold full unrestricted Australian working rights, have completed a National Police Check (May 2026), and am available to commence on 3 August 2026. I am based in Brisbane and enthusiastic about contributing to QBCC's high-performing, community-focused team.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_REGROUP = """Dear Hiring Manager,

I am pleased to apply for the Customer Service Officer role at Re.Group (Return-It). The opportunity to contribute to a company focused on positive community impact through recycling genuinely appeals to me, and my multi-channel customer service background aligns closely with the requirements of this role.

At Concentrix, I handled high volumes of customer enquiries via phone, email, and chat across multiple client campaigns, consistently maintaining accuracy and professionalism while meeting customer satisfaction targets. I am experienced in documenting customer interactions in CRM systems, processing refunds and orders, and resolving complaints with patience and empathy - all core functions of this role. At Omnisorb, I managed customer queries end-to-end via phone and email, resolving delivery, product, and account issues while maintaining detailed records of each interaction.

I am comfortable working on a rotating roster across Monday to Sunday and adapting to changing priorities and customer needs in a fast-paced environment. I hold full unrestricted Australian working rights and am immediately available to commence.

I am enthusiastic about joining Re.Group's supportive team and contributing to a genuinely meaningful mission.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_VOLARE = """Dear Hiring Manager,

I am writing to apply for the Administration Assistant position at your Kedron office via Volare Recruitment. I am drawn to this role because it offers genuine variety, a long-term team environment, and the opportunity to make a real contribution behind the scenes of a well-regarded business.

My background spans administration, data entry, records management, and customer coordination across several busy, fast-paced environments. At FedEx, I was responsible for managing account records, preparing client correspondence, and ensuring accurate documentation under strict SLA timelines. At Concentrix, I handled administrative processing across multiple client campaigns, including case logging, data entry, inbox management, and back-office coordination. I am proficient in Microsoft Office (Word, Excel, Outlook), comfortable working with databases and internal systems, and experienced in managing incoming mail and coordinating courier logistics.

I am a proactive, detail-oriented professional who takes pride in keeping operations running smoothly without needing to be micromanaged. I am reliable, friendly, and genuinely committed to becoming a valued long-term member of whichever team I join.

I hold full unrestricted Australian working rights and am available immediately. I would welcome the opportunity to contribute to your team at the Kedron office.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_TREASURY = """Dear Hiring Manager,

I am writing to apply for the AO3 Service Officer role with the Queensland Revenue Office, Land Tax division. This is an exciting opportunity to begin a career in the government sector and I am confident in my ability to deliver the accurate, client-centric service this role requires.

I have a strong foundation in multi-channel customer service and administrative processing. At Concentrix, I worked across campaigns that required interpreting policies and procedures to resolve customer queries accurately over phone, email, and chat - developing the ability to apply rules and processes clearly and consistently to diverse client situations. At FedEx, I managed account correspondence and documentation with a high degree of accuracy, reviewing service terms and applying them to resolve complex account issues under deadline pressure.

I am digitally proficient, comfortable navigating multiple systems, and capable of rapidly acquiring knowledge of new legislation and policy frameworks. I understand that accuracy, consistency, and a positive client experience are paramount in a revenue administration environment, and I take that responsibility seriously.

I hold full unrestricted Australian working rights, a completed National Police Check (May 2026), and am immediately available for interview. I am based in Brisbane and willing to commute to Ipswich. I am keen to grow within QRO and contribute to the team's delivery of fair and effective land tax administration.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

COVER_HYDRAULINK = """Dear Hiring Manager,

I am writing to apply for the Customer Service Officer role at Hydraulink Australia in Rocklea. I am drawn to Hydraulink's reputation as a thriving, market-leading company with a supportive team culture and genuine career development opportunities.

I bring several years of experience in customer-facing and client administration roles across logistics, call centre, and e-commerce environments. At FedEx, I managed ongoing relationships with high-priority accounts, coordinating sales administration, correspondence, and query resolution with a professional and solutions-focused approach. At Concentrix, I handled high volumes of customer interactions across multiple channels, maintaining accuracy, speed, and a positive customer experience under KPI targets. At Omnisorb, I was the primary point of contact for all customer enquiries, managing phone and email correspondence, processing orders, and coordinating with logistics teams to resolve delivery and product issues efficiently.

I am proficient in Microsoft Office and CRM systems, a fast and accurate data entry operator, and experienced in supporting sales teams with administrative coordination. I take pride in building positive relationships with customers and colleagues alike.

I hold full unrestricted Australian working rights, hold a current open Australian driver's licence, and am available to commence immediately.

Kind regards,
Raymond Paterson
0432 130 983 | paterson250304@gmail.com"""

# ===================== JOB LIST =====================

JOBS = [
    {'id': '92461526', 'company': 'TactiCall / QBCC',      'title': 'AO3 Customer Service Officer',  'cover': COVER_TACTICALL},
    {'id': '92448886', 'company': 'Re.Group',              'title': 'Customer Service Officer',       'cover': COVER_REGROUP},
    {'id': '92451124', 'company': 'Volare Recruitment',    'title': 'Administration Assistant',       'cover': COVER_VOLARE},
    {'id': '92434086', 'company': 'QLD Treasury',          'title': 'AO3 Service Officer',            'cover': COVER_TREASURY},
    {'id': '92448769', 'company': 'Hydraulink Australia',  'title': 'Customer Service Officer',       'cover': COVER_HYDRAULINK},
]

# ===================== HELPERS =====================

async def ss(page, name):
    try:
        p = os.path.join(SCREENSHOTS, f'{name}.png')
        await page.screenshot(path=p)
        log(f'Screenshot saved: {name}')
    except Exception as e:
        log(f'Screenshot failed: {e}')

async def is_logged_in(page):
    """Check if currently logged into SEEK."""
    await page.goto('https://au.seek.com', timeout=30000)
    await page.wait_for_timeout(3000)
    content = await page.content()
    title = (await page.title()).lower()
    # If we see sign in links prominently and no profile elements, not logged in
    logged_in = ('sign out' in content.lower() or
                 'my account' in content.lower() or
                 'raymond' in content.lower() or
                 '/profile' in content.lower())
    log(f'Login check - logged_in={logged_in}, title={title[:60]}')
    return logged_in

async def wait_for_login(page, timeout_secs=120):
    """Wait for user to manually log in."""
    log(f'Waiting up to {timeout_secs}s for manual SEEK login...')
    await ss(page, 'login_wait')
    for _ in range(timeout_secs // 5):
        await asyncio.sleep(5)
        content = await page.content()
        url = page.url
        if ('sign out' in content.lower() or
                'my account' in content.lower() or
                'raymond' in content.lower() or
                'dashboard' in url or
                '/job/' in url):
            log('Manual login detected - proceeding')
            return True
    log('Login timeout - continuing anyway')
    return False

async def skip_references(page):
    content = await page.content()
    cl = content.lower()
    is_refs = ('reference' in cl and
               any(k in cl for k in [
                   'add a reference', 'add reference', 'referee',
                   'reference name', 'reference details', 'your references',
                   'provide a reference'
               ]))
    if not is_refs:
        return False
    log('References step detected - skipping...')
    await ss(page, f'refs_{int(time.time())}')
    skip_sels = [
        'button:has-text("Skip")', 'a:has-text("Skip")',
        '[data-automation="skip"]', 'button:has-text("I\'ll do this later")',
        'button:has-text("Not now")', 'a:has-text("Skip this step")',
        'button:has-text("Skip this step")',
    ]
    for sel in skip_sels:
        try:
            el = await page.query_selector(sel)
            if el and await el.is_visible():
                await el.click()
                log(f'References skipped via: {sel}')
                await page.wait_for_timeout(2500)
                return True
        except:
            pass
    # No skip button - click next with empty fields
    next_sels = [
        'button:has-text("Next")', 'button:has-text("Continue")',
        'button:has-text("Submit application")', 'button:has-text("Submit")',
        '[data-automation="next"]', 'button[type="submit"]',
    ]
    for sel in next_sels:
        try:
            el = await page.query_selector(sel)
            if el and await el.is_visible() and await el.is_enabled():
                txt = (await el.text_content() or '').strip()
                await el.click()
                log(f'References: clicked "{txt}" with empty fields')
                await page.wait_for_timeout(2500)
                return True
        except:
            pass
    return True

async def fill_cover(page, text):
    sels = [
        'textarea[name="coverLetter"]',
        '[data-automation="coverLetterTextArea"] textarea',
        '[data-automation*="cover"] textarea',
        'textarea[aria-label*="cover" i]',
        'textarea[placeholder*="cover" i]',
        'textarea[id*="cover" i]',
        'textarea',
    ]
    for sel in sels:
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
                    log(f'Clicked "{txt}"')
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
            if any(k in txt for k in ['right to work', 'work in australia', 'australian working rights']):
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: right to work = Yes')
            elif any(k in txt for k in ['located in', 'reside in', 'based in australia', 'live in']):
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: location = Yes')
            elif any(k in txt for k in ['immediately available', 'available to start', 'available to commence']):
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: available = Yes')
            elif 'customer service' in txt and 'experience' in txt:
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: customer service experience = Yes')
            elif 'driver' in txt and 'licence' in txt and 'forklift' not in txt:
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: driver licence = Yes')
            elif 'forklift' in txt:
                no = await g.query_selector('label:has-text("No")')
                if no: await no.click(); log('Q: forklift = No')
            elif 'blue card' in txt:
                no = await g.query_selector('label:has-text("No")')
                if no: await no.click(); log('Q: blue card = No')
            elif any(k in txt for k in ['do you have a reference', 'can you provide a reference', 'do you have referees']):
                no = await g.query_selector('label:has-text("No")')
                if no: await no.click(); log('Q: references = No')
            elif 'rotating roster' in txt or 'work on a rotating roster' in txt:
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: rotating roster = Yes')
            elif 'medical check' in txt or 'pre-employment medical' in txt:
                yes = await g.query_selector('label:has-text("Yes")')
                if yes: await yes.click(); log('Q: medical check = Yes')
        # Handle salary text inputs
        salary_inputs = await page.query_selector_all('input[placeholder*="salary" i], input[aria-label*="salary" i], input[name*="salary" i]')
        for inp in salary_inputs:
            if await inp.is_visible():
                await inp.fill('65000')
                log('Salary field filled: 65000')
    except Exception as e:
        log(f'Questions error: {e}')

# ===================== APPLY LOGIC =====================

async def apply_job(ctx, job):
    log(f'\n{"="*55}')
    log(f'APPLYING: {job["company"]} | {job["title"]}')
    log(f'URL: https://au.seek.com/job/{job["id"]}/apply')
    log(f'{"="*55}')
    page = await ctx.new_page()
    try:
        url = f'https://au.seek.com/job/{job["id"]}/apply'
        await page.goto(url, timeout=45000)
        await page.wait_for_timeout(4000)
        await ss(page, f'{job["id"]}_start')

        content = await page.content()
        if ('already applied' in content.lower() or
                'application has been sent' in content.lower()):
            log(f'SKIP: Already applied to {job["company"]}')
            await page.close()
            return 'ALREADY_APPLIED'

        cover_done = False
        for step in range(1, 18):
            url_now = page.url
            log(f'Step {step} | {url_now[:80]}')
            content = await page.content()

            # Success
            if ('success' in url_now or
                    'application sent' in content.lower() or
                    'good luck' in content.lower()):
                log(f'>>> SUCCESS: {job["company"]} SENT <<<')
                await ss(page, f'{job["id"]}_SUCCESS')
                await page.close()
                return 'SENT'

            # References skip first
            ref_handled = await skip_references(page)
            if ref_handled:
                continue

            # Screening questions
            await handle_questions(page)

            # Cover letter
            if not cover_done:
                filled = await fill_cover(page, job['cover'])
                if filled:
                    cover_done = True
                    await page.wait_for_timeout(800)

            # Next button
            btn = await click_next(page)
            if not btn:
                log(f'No button at step {step}')
                await ss(page, f'{job["id"]}_stuck_s{step}')
                break

            await page.wait_for_timeout(2500)

        final = await page.content()
        if 'application sent' in final.lower() or 'good luck' in final.lower() or 'success' in page.url:
            log(f'>>> SUCCESS: {job["company"]} <<<')
            await page.close()
            return 'SENT'

        await ss(page, f'{job["id"]}_uncertain')
        log(f'UNCERTAIN: {job["company"]} - check screenshots')
        await page.close()
        return 'UNCERTAIN'

    except Exception as e:
        log(f'ERROR {job["company"]}: {e}')
        try:
            await ss(page, f'{job["id"]}_error')
            await page.close()
        except:
            pass
        return 'ERROR'

# ===================== BROWSER LAUNCH WITH FALLBACK =====================

async def launch_with_session(pw):
    """
    Try browsers in order:
    1. Chromium with copied Chrome session
    2. Firefox with copied Firefox session
    3. Fresh Chromium (manual login)
    Returns (context, browser_type_name)
    """

    # --- Attempt 1: Chrome session ---
    log('Attempt 1: Launching Chromium with Chrome session...')
    try:
        profile = prepare_chrome_profile()
        ctx = await pw.chromium.launch_persistent_context(
            user_data_dir=profile,
            headless=False,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled'],
            ignore_https_errors=True
        )
        page = ctx.pages[0] if ctx.pages else await ctx.new_page()
        if await is_logged_in(page):
            log('Chrome session: LOGGED IN')
            return ctx, 'chromium'
        log('Chrome session: not logged in')
        await ctx.close()
    except Exception as e:
        log(f'Chrome session failed: {e}')

    # --- Attempt 2: Firefox session ---
    log('Attempt 2: Launching Firefox with saved session...')
    try:
        ff_profile = prepare_firefox_profile()
        if ff_profile:
            ctx = await pw.firefox.launch_persistent_context(
                user_data_dir=ff_profile,
                headless=False,
            )
            page = ctx.pages[0] if ctx.pages else await ctx.new_page()
            if await is_logged_in(page):
                log('Firefox session: LOGGED IN')
                return ctx, 'firefox'
            log('Firefox session: not logged in')
            await ctx.close()
        else:
            log('No Firefox profile available')
    except Exception as e:
        log(f'Firefox session failed: {e}')

    # --- Attempt 3: Fresh browser - wait for manual login ---
    log('Attempt 3: Fresh browser - please log into SEEK manually...')
    ctx = await pw.chromium.launch_persistent_context(
        user_data_dir=FRESH_DIR,
        headless=False,
        args=['--no-sandbox'],
    )
    page = ctx.pages[0] if ctx.pages else await ctx.new_page()
    await page.goto('https://au.seek.com/oauth/login', timeout=30000)
    await wait_for_login(page, timeout_secs=180)
    log('Continuing with fresh browser after manual login')
    return ctx, 'fresh'

# ===================== MAIN =====================

async def main():
    log('=' * 60)
    log('SEEK AUTO-APPLY ENGINE v2 - HyperSuite')
    log(f'Time: {time.strftime("%Y-%m-%d %H:%M:%S")}')
    log(f'Jobs queued: {len(JOBS)}')
    log('=' * 60)

    async with async_playwright() as pw:
        ctx, browser_type = await launch_with_session(pw)
        log(f'Running with: {browser_type}')

        results = {}
        for job in JOBS:
            status = await apply_job(ctx, job)
            results[job['company']] = status
            await asyncio.sleep(4)

        log('\n' + '=' * 60)
        log('FINAL RESULTS')
        log('=' * 60)
        for co, st in results.items():
            log(f'  {co:35s}: {st}')
        log('=' * 60)
        log(f'Browser used: {browser_type}')
        log('Screenshots: ~/Clipper/seek_screenshots_v2/')
        log('Log: ~/Clipper/seek_apply_v2.log')

        await asyncio.sleep(6)
        await ctx.close()
        log('Engine complete.')

if __name__ == '__main__':
    asyncio.run(main())
