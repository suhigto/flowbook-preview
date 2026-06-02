#!/usr/bin/env python3
"""
external_apply.py - Apply to company websites (Eagers Automotive + Randstad)
Targets:
  - Eagers Automotive: Fleet Inventory Coordinator (Hendra)
  - Eagers Automotive: Administration Officer (Moorooka/EVDealer)
  - Eagers Automotive: New Vehicle Sales Consultant (Aspley)
  - Randstad: AO3 Administration Officer (Brisbane CBD)
"""

import asyncio
import logging
import os
from datetime import datetime
from playwright.async_api import async_playwright

LOG_FILE = os.path.expanduser("~/Clipper/external_apply.log")
SCREENSHOT_DIR = os.path.expanduser("~/Clipper/external_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ── Applicant details ──────────────────────────────────────────────────
APPLICANT = {
    "first_name": "Raymond",
    "last_name": "Paterson",
    "email": "paterson250304@gmail.com",
    "phone": "0432130983",
    "suburb": "Nundah",
    "state": "QLD",
    "postcode": "4012",
    "cv_path": "",  # resolved at runtime
}

# ── Eagers Automotive roles ────────────────────────────────────────────
EAGERS_JOBS = [
    {
        "title": "Fleet Inventory Coordinator",
        "apply_url": "https://careers.eagersautomotive.com.au/talentcommunity/apply/1358504466/?locale=en_GB",
        "location": "Hendra QLD",
        "cover_letter": (
            "Dear Hiring Manager,\n\n"
            "I am writing to apply for the Fleet Inventory Coordinator role at Eagers Automotive. "
            "With a background in high-volume logistics and data management at FedEx, I am confident "
            "I can contribute meaningfully to your national partner network.\n\n"
            "As a Relationship Consultant at FedEx, I managed complex inventory data across multiple "
            "high-priority accounts, tracked movements with precision, and ensured pricing accuracy "
            "under strict SLA requirements. This built in me a sharp analytical mindset, genuine "
            "attention to pricing performance, speed-to-sale metrics, and data integrity - exactly "
            "what this role demands.\n\n"
            "I am proficient in Microsoft Excel and comfortable working across multiple data systems. "
            "I understand how to balance commercial judgement with live market data and take pride in "
            "maintaining accuracy in fast-moving environments.\n\n"
            "I am Brisbane-based, immediately available, and hold full working rights in Australia. "
            "I am excited by the opportunity to work at the intersection of data and automotive retail.\n\n"
            "Kind regards,\nRaymond Paterson\n0432 130 983\npaterson250304@gmail.com"
        ),
    },
    {
        "title": "Administration Officer",
        "apply_url": "https://careers.eagersautomotive.com.au/talentcommunity/apply/1362075966/?locale=en_GB",
        "location": "Moorooka QLD (EVDealer)",
        "cover_letter": (
            "Dear Hiring Manager,\n\n"
            "I am pleased to apply for the Administration Officer role at EVDealer Group. My background "
            "in corporate administration, data entry, and customer service across FedEx and Concentrix "
            "makes me well-suited to supporting deal processing, invoice entry, and internal coordination.\n\n"
            "At FedEx, I managed end-to-end documentation for corporate freight accounts, processed "
            "financial records, and maintained high-accuracy data under tight time pressure. At Concentrix, "
            "I handled multi-campaign back-office processing including data entry, records management, "
            "and compliance reporting.\n\n"
            "I am proficient in Microsoft Office Suite and thrive in structured environments that demand "
            "organisation and attention to detail. I am a collaborative team player who is also comfortable "
            "working autonomously on deadline-driven tasks.\n\n"
            "I am available to start immediately, Brisbane-based, and hold full Australian working rights. "
            "I would love to contribute to EVDealer's mission of advancing sustainable transport.\n\n"
            "Kind regards,\nRaymond Paterson\n0432 130 983\npaterson250304@gmail.com"
        ),
    },
    {
        "title": "New Vehicle Sales Consultant",
        "apply_url": "https://careers.eagersautomotive.com.au/talentcommunity/apply/1359410166/?locale=en_GB",
        "location": "Aspley QLD",
        "cover_letter": (
            "Dear Hiring Manager,\n\n"
            "I am excited to apply for the New Vehicle Sales Consultant role at Automall Aspley. "
            "With a background in relationship management and customer service, I am well-positioned "
            "to deliver exceptional experiences and contribute to your sales targets.\n\n"
            "As a Relationship Consultant at FedEx, I managed ongoing accounts for high-value clients, "
            "handled consultative conversations, and developed strong people skills through daily "
            "customer interaction. I maintained a 4.92/5 customer rating as a DoorDash delivery driver "
            "and consistently demonstrated professionalism under pressure.\n\n"
            "I am self-motivated, target-driven, and genuinely passionate about cars. I hold a current "
            "open Australian driver's licence and am comfortable working in fast-paced, customer-facing "
            "environments across multiple brands.\n\n"
            "I am Brisbane-based, available to start immediately, and hold full Australian working rights. "
            "I would relish the opportunity to build a long-term automotive career with Eagers.\n\n"
            "Kind regards,\nRaymond Paterson\n0432 130 983\npaterson250304@gmail.com"
        ),
    },
]

# ── Randstad job ───────────────────────────────────────────────────────
RANDSTAD_JOB = {
    "title": "AO3 Administration Officer",
    "apply_url": "https://www.randstad.com.au/jobs/ao3-administration-officer_brisbane_46951972/",
    "cover_letter": (
        "Dear Randstad Team,\n\n"
        "I am writing to apply for the AO3 Administration Officer role at the State Government "
        "Department in Brisbane CBD. With a background in corporate administration, records management, "
        "and high-volume data processing, I am well-equipped to hit the ground running in this "
        "government support environment.\n\n"
        "At FedEx, I provided high-level administrative support across multiple corporate accounts, "
        "managing correspondence, coordinating logistics, and maintaining accurate financial and "
        "operational records with a consistent 4-hour SLA. I have strong proficiency in Microsoft "
        "Office and experience navigating SAP-adjacent finance systems in fast-paced environments.\n\n"
        "At Concentrix, I handled sensitive customer information across multiple government and "
        "corporate campaigns under strict confidentiality protocols - directly applicable to the "
        "discretion required in public sector administration.\n\n"
        "I am Brisbane-based, available to commence from 15 June 2026, and hold full working rights "
        "in Australia. I would welcome the opportunity to discuss my suitability for this role.\n\n"
        "Kind regards,\nRaymond Paterson\n0432 130 983\npaterson250304@gmail.com"
    ),
}


def find_cv():
    """Find the CV file in common locations."""
    candidates = [
        os.path.expanduser("~/Downloads/CV_Raymond_Paterson_2026.pdf"),
        os.path.expanduser("~/Desktop/CV_Raymond_Paterson_2026.pdf"),
        os.path.expanduser("~/Documents/CV_Raymond_Paterson_2026.pdf"),
        os.path.expanduser("~/Clipper/CV_Raymond_Paterson_2026.pdf"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


async def screenshot(page, name):
    path = os.path.join(SCREENSHOT_DIR, f"{name}_{datetime.now().strftime('%H%M%S')}.png")
    try:
        await page.screenshot(path=path, full_page=True)
        log.info(f"Screenshot saved: {path}")
    except Exception as e:
        log.warning(f"Screenshot failed: {e}")


async def fill_field(page, selectors, value, label=""):
    """Try multiple selectors to fill a form field."""
    for selector in selectors:
        try:
            elem = await page.query_selector(selector)
            if elem and await elem.is_visible():
                await elem.triple_click()
                await elem.fill(value)
                log.info(f"Filled {label or selector[:40]}: {value[:30]}")
                return True
        except:
            pass
    return False


async def click_button(page, selectors, label=""):
    """Try multiple selectors to click a button."""
    for selector in selectors:
        try:
            elem = await page.query_selector(selector)
            if elem and await elem.is_visible():
                log.info(f"Clicking {label or selector[:50]}")
                await elem.click()
                await page.wait_for_load_state("networkidle", timeout=15000)
                await asyncio.sleep(2)
                return True
        except:
            pass
    return False


async def upload_cv(page, cv_path):
    """Try to upload the CV to any file input."""
    if not cv_path or not os.path.exists(cv_path):
        log.warning("CV file not found, skipping upload")
        return False
    try:
        # Try direct file input
        file_inputs = await page.query_selector_all('input[type="file"]')
        for fi in file_inputs:
            try:
                await fi.set_input_files(cv_path)
                log.info(f"CV uploaded via file input: {cv_path}")
                await asyncio.sleep(2)
                return True
            except:
                pass
        # Try drag-drop zone click (opens file dialog) - can't automate without OS dialog
        log.warning("No file input found for CV upload")
        return False
    except Exception as e:
        log.error(f"CV upload error: {e}")
        return False


async def apply_eagers(page, job, cv_path):
    """Apply to an Eagers Automotive role via SAP SuccessFactors."""
    log.info(f"\n{'='*60}")
    log.info(f"Eagers: {job['title']} ({job['location']})")
    log.info(f"{'='*60}")

    try:
        await page.goto(job["apply_url"], wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)
        await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_01_start")

        # SAP SF: Check if login wall appears
        page_text = (await page.content()).lower()

        # Look for the actual application form fields
        # SAP SF Talent Community apply form fields
        personal_info_selectors = [
            'input[id*="firstName"]', 'input[name*="firstName"]',
            'input[placeholder*="First Name"]', 'input[placeholder*="first"]'
        ]

        # Try to find any input on the page
        all_inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"]')
        if not all_inputs:
            log.warning(f"No input fields found on page for {job['title']}")
            # Try clicking 'Apply now' if visible
            clicked = await click_button(page,
                ['button:has-text("Apply now")', 'a:has-text("Apply now")',
                 'button:has-text("Apply")', '[class*="apply"]'],
                "Apply now"
            )
            if clicked:
                await asyncio.sleep(3)
                await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_02_after_apply")
                all_inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"]')

        if not all_inputs:
            log.warning(f"Still no input fields - may need manual login for {job['title']}")
            # Wait up to 90s for manual login
            log.info("Waiting up to 90s for manual login/form fill...")
            for i in range(18):
                await asyncio.sleep(5)
                all_inputs = await page.query_selector_all('input[type="text"], input[type="email"], input[type="tel"]')
                if all_inputs:
                    break

        # Fill first name
        await fill_field(page,
            ['input[id*="firstName"]', 'input[name*="firstName"]',
             'input[placeholder*="First"]', 'input[data-field*="first"]'],
            APPLICANT["first_name"], "First Name"
        )
        # Fill last name
        await fill_field(page,
            ['input[id*="lastName"]', 'input[name*="lastName"]',
             'input[placeholder*="Last"]', 'input[data-field*="last"]'],
            APPLICANT["last_name"], "Last Name"
        )
        # Fill email
        await fill_field(page,
            ['input[type="email"]', 'input[id*="email"]', 'input[name*="email"]',
             'input[placeholder*="Email"]'],
            APPLICANT["email"], "Email"
        )
        # Fill phone
        await fill_field(page,
            ['input[type="tel"]', 'input[id*="phone"]', 'input[name*="phone"]',
             'input[placeholder*="Phone"]', 'input[placeholder*="Mobile"]'],
            APPLICANT["phone"], "Phone"
        )

        await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_03_filled")

        # Upload CV
        await upload_cv(page, cv_path)

        # Fill cover letter textarea
        cl_filled = False
        for selector in ['textarea', 'div[contenteditable="true"]',
                         '[name*="cover"]', '[placeholder*="cover"]',
                         '[name*="message"]']:
            try:
                elem = await page.query_selector(selector)
                if elem and await elem.is_visible():
                    await elem.fill(job["cover_letter"])
                    log.info("Cover letter filled")
                    cl_filled = True
                    break
            except:
                pass

        await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_04_cover")

        # Handle checkboxes/consent
        for selector in ['input[type="checkbox"]']:
            try:
                checkboxes = await page.query_selector_all(selector)
                for cb in checkboxes:
                    is_checked = await cb.is_checked()
                    if not is_checked:
                        label_elem = await cb.evaluate('el => el.closest("label") || document.querySelector(`label[for="${el.id}"]`)')
                        if label_elem:
                            label_text = await page.evaluate('el => el.textContent', label_elem)
                            if any(w in label_text.lower() for w in ["consent", "agree", "privacy", "terms"]):
                                await cb.check()
                                log.info(f"Checked consent: {label_text[:50]}")
            except:
                pass

        # Click Next / Submit
        for btn_text in ["Next", "Continue", "Submit Application", "Submit", "Apply"]:
            clicked = await click_button(page,
                [f'button:has-text("{btn_text}")', f'input[value="{btn_text}"]'],
                btn_text
            )
            if clicked:
                await asyncio.sleep(3)
                await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_05_submitted")
                break

        # Check success
        page_text = (await page.content()).lower()
        if any(w in page_text for w in ["thank you", "application received", "successfully", "submitted", "applied"]):
            log.info(f"SUCCESS - Eagers: {job['title']}")
            return True
        else:
            log.warning(f"Application status unclear - Eagers: {job['title']}")
            await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_UNCLEAR")
            return False

    except Exception as e:
        log.error(f"Error on Eagers {job['title']}: {e}")
        await screenshot(page, f"eagers_{job['title'][:15].replace(' ','_')}_ERROR")
        return False


async def apply_randstad(page, cv_path):
    """Apply to Randstad AO3 Administration Officer via randstad.com.au."""
    log.info(f"\n{'='*60}")
    log.info("Randstad: AO3 Administration Officer (Brisbane CBD)")
    log.info(f"{'='*60}")

    try:
        await page.goto(RANDSTAD_JOB["apply_url"], wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(4)
        await screenshot(page, "randstad_01_start")

        # Click Apply / Apply now button
        clicked = await click_button(page,
            ['a:has-text("apply now")', 'button:has-text("apply now")',
             'a:has-text("Apply now")', 'a[class*="apply"]',
             'button[class*="apply"]', '.apply-button', '#apply-button'],
            "Apply now"
        )

        if not clicked:
            # Try scrolling to find it
            await page.evaluate("window.scrollTo(0, 500)")
            await asyncio.sleep(1)
            clicked = await click_button(page,
                ['a:has-text("Apply")', 'button:has-text("Apply")'],
                "Apply"
            )

        await asyncio.sleep(3)
        await screenshot(page, "randstad_02_form")

        # Fill personal info
        await fill_field(page,
            ['input[name="firstName"]', 'input[id*="firstName"]', 'input[placeholder*="First name"]', 'input[placeholder*="First Name"]'],
            APPLICANT["first_name"], "First Name"
        )
        await fill_field(page,
            ['input[name="lastName"]', 'input[id*="lastName"]', 'input[placeholder*="Last name"]', 'input[placeholder*="Last Name"]'],
            APPLICANT["last_name"], "Last Name"
        )
        await fill_field(page,
            ['input[type="email"]', 'input[name="email"]', 'input[placeholder*="Email"]'],
            APPLICANT["email"], "Email"
        )
        await fill_field(page,
            ['input[type="tel"]', 'input[name="phone"]', 'input[name="mobile"]',
             'input[placeholder*="Phone"]', 'input[placeholder*="Mobile"]'],
            APPLICANT["phone"], "Phone"
        )

        # Right to work - try to select Yes
        for selector in ['input[value="yes"]', 'input[value="Yes"]',
                         'label:has-text("Yes")', 'option[value*="yes"]']:
            try:
                elem = await page.query_selector(selector)
                if elem and await elem.is_visible():
                    await elem.click()
                    log.info("Right to work: Yes selected")
                    break
            except:
                pass

        # Upload CV
        await upload_cv(page, cv_path)

        # Cover letter / message textarea
        for selector in ['textarea[name*="cover"]', 'textarea[name*="message"]',
                         'textarea[name*="letter"]', 'textarea',
                         'div[contenteditable="true"]']:
            try:
                elem = await page.query_selector(selector)
                if elem and await elem.is_visible():
                    await elem.fill(RANDSTAD_JOB["cover_letter"])
                    log.info("Cover letter filled on Randstad")
                    break
            except:
                pass

        await screenshot(page, "randstad_03_filled")

        # Consent checkboxes
        try:
            checkboxes = await page.query_selector_all('input[type="checkbox"]')
            for cb in checkboxes:
                if not await cb.is_checked():
                    await cb.check()
                    log.info("Checkbox checked")
        except:
            pass

        # Submit
        submitted = await click_button(page,
            ['button[type="submit"]', 'button:has-text("Submit")',
             'button:has-text("Send application")',
             'button:has-text("Send my application")',
             'input[type="submit"]'],
            "Submit"
        )

        await asyncio.sleep(4)
        await screenshot(page, "randstad_04_submitted")

        page_text = (await page.content()).lower()
        if any(w in page_text for w in ["thank you", "application received", "successfully", "applied", "submitted"]):
            log.info("SUCCESS - Randstad: AO3 Administration Officer")
            return True
        else:
            log.warning("Randstad application status unclear")
            return False

    except Exception as e:
        log.error(f"Error on Randstad: {e}")
        await screenshot(page, "randstad_ERROR")
        return False


async def main():
    log.info("=" * 60)
    log.info("EXTERNAL APPLY - Starting")
    log.info(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S AEST')}")
    log.info("Targets:")
    for job in EAGERS_JOBS:
        log.info(f"  Eagers: {job['title']} ({job['location']})")
    log.info(f"  Randstad: {RANDSTAD_JOB['title']}")
    log.info("=" * 60)

    cv_path = find_cv()
    if cv_path:
        log.info(f"CV found: {cv_path}")
    else:
        log.warning("CV not found - applications will proceed without upload")

    results = []

    # Browser launch order: Chrome persistent session > fresh Chromium > Firefox
    chrome_session_dir = os.path.expanduser("~/Clipper/external_chrome_session")
    os.makedirs(chrome_session_dir, exist_ok=True)

    async with async_playwright() as p:
        browser = None
        context = None

        # Try Chrome with existing session
        try:
            context = await p.chromium.launch_persistent_context(
                chrome_session_dir,
                headless=False,
                args=["--no-first-run", "--disable-blink-features=AutomationControlled",
                      "--start-maximized"],
                viewport={"width": 1280, "height": 900},
                ignore_https_errors=True,
            )
            log.info("Browser: Chrome persistent context")
        except Exception as e:
            log.warning(f"Chrome failed: {e}. Trying Chromium fresh...")
            try:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context(viewport={"width": 1280, "height": 900})
                log.info("Browser: fresh Chromium")
            except Exception as e2:
                log.warning(f"Chromium failed: {e2}. Trying Firefox...")
                browser = await p.firefox.launch(headless=False)
                context = await browser.new_context(viewport={"width": 1280, "height": 900})
                log.info("Browser: Firefox")

        page = await context.new_page()

        # 1. Apply to Randstad first
        r = await apply_randstad(page, cv_path)
        results.append(("Randstad - AO3 Administration Officer", r))
        await asyncio.sleep(3)

        # 2. Apply to 3 Eagers roles
        for job in EAGERS_JOBS:
            r = await apply_eagers(page, job, cv_path)
            results.append((f"Eagers - {job['title']}", r))
            await asyncio.sleep(5)

        await context.close()
        if browser:
            await browser.close()

    # Final summary
    log.info("\n" + "=" * 60)
    log.info("EXTERNAL APPLY COMPLETE")
    log.info("Results:")
    success_count = 0
    for name, ok in results:
        status = "SUCCESS" if ok else "NEEDS REVIEW"
        if ok:
            success_count += 1
        log.info(f"  [{status}] {name}")
    log.info(f"\nTotal: {success_count}/{len(results)} confirmed applied")
    log.info(f"Screenshots: {SCREENSHOT_DIR}")
    log.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
