from bs4 import BeautifulSoup

from src.form.form_classifier import FormClassifier


class FormVerifier:
    def __init__(self):
        self.form_classifier = FormClassifier()

    def verify_page_content(self, content, expected_data):
        soup = BeautifulSoup(content, 'html.parser')
        classified_content = self.form_classifier.classify_elements(content)
        verification_results = {}

        for field, expected_value in expected_data.items():
            if expected_value is None:
                continue

            input_element = soup.find('input', {'name': field})
            if input_element:
                actual_value = input_element.get('value', '')
                verification_results[field] = actual_value == expected_value
                print(f"Field: {field}, Expected: {expected_value}, Actual: {actual_value}")
            else:
                verification_results[field] = False
                print(f"Field: {field} not found in the page.")

            # Check for success message
            success_message = expected_data.get('message')
            if success_message:
                message_div = soup.find('div', id='formReplyMessage')
                message_found = False
                if message_div:
                    for div in message_div.find_all('div'):
                        if success_message in div.get_text(strip=True):
                            message_found = True
                            break
                verification_results['message'] = message_found
                print(f"Message: {success_message}, Found: {message_found}")

        return verification_results
