from bs4 import BeautifulSoup
from transformers import pipeline


class MLClassifier:
    def __init__(self):
        self.classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

    def extract_form_elements(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        form_elements = []

        for form in forms:
            elements = form.find_all(['input', 'button', 'textarea', 'select', 'table'])
            for element in elements:
                form_elements.append({
                    'tag': element.name,
                    'type': element.get('type', ''),
                    'name': element.get('name', ''),
                    'id': element.get('id', ''),
                    'value': element.get('value', ''),
                    'placeholder': element.get('placeholder', ''),
                    'text': element.text.strip()
                })
        return form_elements

    def classify_elements(self, form_elements):
        classified_elements = {'text_fields': [], 'password_fields': [], 'buttons': [], 'tables': []}

        for element in form_elements:
            element_text = f"{element['name']} {element['id']} {element['placeholder']} {element['text']}"
            prediction = self.classifier(element_text)

            if prediction[0]['label'] == 'LABEL_1':  # Assuming LABEL_1 indicates positive sentiment/relevance
                if 'username' in element_text.lower() or 'email' in element_text.lower() or 'text' in element['type'].lower():
                    classified_elements['text_fields'].append(element)
                elif 'password' in element_text.lower():
                    classified_elements['password_fields'].append(element)
                elif 'submit' in element_text.lower() or 'button' in element['type'].lower():
                    classified_elements['buttons'].append(element)
                elif 'table' in element['tag'].lower():
                    classified_elements['tables'].append(element)
                # Here you can add other classifier types

        return classified_elements

    @staticmethod
    def extract_message_text(soup):
        message_div = soup.find('div', id='formReplyMessage')
        if message_div:
            return ' '.join(div.get_text(strip=True) for div in message_div.find_all('div'))
        return ''

    def verify_page_content(self, content, expected_data):
        soup = BeautifulSoup(content, 'html.parser')
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

        # Check for success message using ML
        success_message = expected_data.get('message')
        if success_message:
            message_text = self.extract_message_text(soup)
            if message_text:
                prediction = self.classifier(message_text)
                message_found = any(pred['label'] == 'LABEL_1' for pred in prediction)  # Assuming LABEL_1 indicates relevance
                verification_results['message'] = message_found
                print(f"Message: {success_message}, Found: {message_found}, Prediction: {prediction}")
            else:
                verification_results['message'] = False
                print(f"Message: {success_message} not found in the formReplyMessage div.")

        return verification_results
