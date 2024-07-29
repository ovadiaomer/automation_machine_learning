from bs4 import BeautifulSoup


class FormClassifier:
    @staticmethod
    def classify_elements(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        classified_elements = {
            'text_fields': [],
            'password_fields': [],
            'buttons': [],
            'tables': [],
            'links': [],
            'selects': [],
            'textareas': [],
            'checkboxes': []

        }

        # Find all input elements regardless of their type
        for input_tag in soup.find_all('input'):
            input_type = input_tag.get('type', '').lower()
            if input_type in ['text', 'email', 'tel', 'url']:
                classified_elements['text_fields'].append({
                    'tag': input_tag.name,
                    'type': input_type,
                    'name': input_tag.get('name', ''),
                    'id': input_tag.get('id', ''),
                    'value': input_tag.get('value', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'text': input_tag.get_text(strip=True)
                })
            elif input_type == 'password':
                classified_elements['password_fields'].append({
                    'tag': input_tag.name,
                    'type': input_type,
                    'name': input_tag.get('name', ''),
                    'id': input_tag.get('id', ''),
                    'value': input_tag.get('value', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'text': input_tag.get_text(strip=True)
                })
            elif input_type == 'submit':
                classified_elements['buttons'].append({
                    'tag': input_tag.name,
                    'type': input_type,
                    'name': input_tag.get('name', ''),
                    'id': input_tag.get('id', ''),
                    'value': input_tag.get('value', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'text': input_tag.get_text(strip=True)
                })

            elif input_type == 'checkbox':
                classified_elements['checkboxes'].append({
                    'tag': input_tag.name,
                    'type': input_type,
                    'name': input_tag.get('name', ''),
                    'id': input_tag.get('id', ''),
                    'value': input_tag.get('value', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'text': input_tag.get_text(strip=True),
                    'checked': input_tag.get('checked', False),
                    'class': input_tag.get('class', '')
                })

        for button_tag in soup.find_all('button'):
            classified_elements['buttons'].append({
                'tag': button_tag.name,
                'type': button_tag.get('type', ''),
                'name': button_tag.get('name', ''),
                'id': button_tag.get('id', ''),
                'value': button_tag.get('value', ''),
                'placeholder': button_tag.get('placeholder', ''),
                'text': button_tag.get_text(strip=True),
                'aria-label': button_tag.get('aria-label', ''),
                'class': button_tag.get('class', '')
            })

        for textarea_tag in soup.find_all('textarea'):
            classified_elements['textareas'].append({
                'tag': textarea_tag.name,
                'type': '',
                'name': textarea_tag.get('name', ''),
                'id': textarea_tag.get('id', ''),
                'value': '',
                'placeholder': textarea_tag.get('placeholder', ''),
                'text': textarea_tag.get_text(strip=True)
            })

        for link_tag in soup.find_all('a'):
            classified_elements['links'].append({
                'tag': link_tag.name,
                'type': '',
                'name': link_tag.get('name', ''),
                'id': link_tag.get('id', ''),
                'value': '',
                'placeholder': '',
                'text': link_tag.get_text(strip=True),
                'href': link_tag.get('href', '')
            })

        for table in soup.find_all('table'):
            classified_elements['tables'].append({
                'tag': table.name,
                'type': '',
                'name': '',
                'id': '',
                'value': '',
                'placeholder': '',
                'text': table.get_text(strip=True)
            })

        for select_tag in soup.find_all('select'):
            options = [{'value': option.get('value', ''), 'text': option.get_text(strip=True)} for option in select_tag.find_all('option')]
            classified_elements['selects'].append({
                'tag': select_tag.name,
                'type': '',
                'name': select_tag.get('name', ''),
                'id': select_tag.get('id', ''),
                'value': '',
                'placeholder': '',
                'text': select_tag.get_text(strip=True),
                'options': options
            })

        return classified_elements