from src.form.form_classifier import FormClassifier
from src.form.form_verifier import FormVerifier


class FormFiller:
    def __init__(self, form_data, expected_data, browser_automation):
        self.form_data = form_data
        self.expected_data = expected_data
        self.browser_automation = browser_automation
        self.form_classifier = FormClassifier()
        self.form_verifier = FormVerifier()

    async def fill_form(self):
        html_content = await self.browser_automation.fetch_page_content()
        classified_elements = self.form_classifier.classify_elements(html_content)
        for field in classified_elements['text_fields']:
            extracted_name = self.browser_automation.extract_field_name(field['name'])
            if extracted_name in self.form_data:
                await self.browser_automation.page.fill(f'input[name="{field["name"]}"]',
                                                        self.form_data[extracted_name])

        for field in classified_elements['password_fields']:
            extracted_name = self.browser_automation.extract_field_name(field['name'])
            if extracted_name in self.form_data:
                await self.browser_automation.page.fill(f'input[name="{field["name"]}"]',
                                                        self.form_data[extracted_name])

        # Check if a specific button is provided in form_data
        button_spec = self.form_data.get('button')

        if button_spec:
            button_type = button_spec.get('type', 'submit').lower()
            button_text = button_spec.get('button_text')

            if button_text:
                for button in classified_elements['buttons']:
                    if button['type'].lower() == button_type and button_text in button['text']:
                        await self.browser_automation.page.click(
                            f'button[type="{button_type}"]:has-text("{button_text}")')
                        break
            else:
                for button in classified_elements['buttons']:
                    if button['type'].lower() == button_type:
                        await self.browser_automation.page.click(f'button[type="{button_type}"]')
                        break
        else:
            # Click the first submit button found if no specific button is specified
            for button in classified_elements['buttons']:
                if button['type'].lower() == 'submit':
                    await self.browser_automation.page.click(f'button[type="submit"]')
                    break

        await self.browser_automation.page.wait_for_load_state('networkidle')
        result_content = await self.browser_automation.page.content()
        return result_content

    def verify(self, content):
        return self.form_verifier.verify_page_content(content, self.expected_data)

    async def fill_form_and_verify(self):
        result_content = await self.fill_form()
        verification_result = self.verify(result_content)
        return verification_result

    def assert_verification(self, verification_result):
        for key, expected_value in self.expected_data.items():
            assert verification_result[
                key], f"Expected {key} to be {expected_value}, but it was not found or was incorrect."
