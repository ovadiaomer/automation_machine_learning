import pytest

from src.automation.browser_automation import BrowserAutomation
from src.config.configuration import url
from src.form.form_filler import FormFiller


@pytest.mark.asyncio
async def test_form_filler():
    form_data = {
        'full-name': 'Omer',
        'role': 'Automation TL',
        'company': 'Auto Gennie',
        'phone-number': '1234567890',
        'email': 'test_user@auto.com',
        'button': {
            'type': 'submit'
        }
    }
    expected_data = {
        'message': 'תודה על הודעתך'  # Expected success message in Hebrew
    }
    browser_automation = BrowserAutomation()
    form_filler = FormFiller(form_data, expected_data, browser_automation)

    # Launch browser and navigate
    await browser_automation.launch_browser()
    await browser_automation.navigate(url)

    try:
        # Fill and verify the form
        verification_result = await form_filler.fill_form_and_verify()

        # Adjust assertions based on actual form fields and expected results
        form_filler.assert_verification(verification_result)
    finally:
        # Close the browser
        await browser_automation.close_browser()
