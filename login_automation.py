import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from transformers import pipeline


class LoginAutomation:
    def __init__(self, url):
        self.url = url
        self.classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

    def extract_form_elements(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        form_elements = []

        for form in forms:
            elements = form.find_all(['input', 'button'])
            for element in elements:
                if element.get('type') in ['text', 'password', 'submit']:
                    form_elements.append({
                        'tag': element.name,
                        'type': element.get('type'),
                        'name': element.get('name'),
                        'id': element.get('id'),
                        'value': element.get('value'),
                        'placeholder': element.get('placeholder')
                    })
        return form_elements

    def classify_elements(self, form_elements):
        classified_elements = {'username': None, 'password': None, 'submit': None}

        for element in form_elements:
            element_text = f"{element['name']} {element['id']} {element['placeholder']}"
            prediction = self.classifier(element_text)

            if prediction[0]['label'] == 'LABEL_1':  # Assuming LABEL_1 indicates positive sentiment/relevance
                if 'username' in element_text.lower() or 'email' in element_text.lower():
                    classified_elements['username'] = element
                elif 'password' in element_text.lower():
                    classified_elements['password'] = element
                elif 'submit' in element_text.lower() or 'login' in element_text.lower():
                    classified_elements['submit'] = element

        return classified_elements

    async def scrape_login_page(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)
            html_content = await page.content()
            await browser.close()

            form_elements = self.extract_form_elements(html_content)
            classified_elements = self.classify_elements(form_elements)
            return classified_elements

    async def perform_login(self, username, password):
        elements = await self.scrape_login_page()

        if elements['username'] and elements['password'] and elements['submit']:
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                await page.goto(self.url)

                await page.fill(f'input[name="{elements["username"]["name"]}"]', username)
                await page.fill(f'input[name="{elements["password"]["name"]}"]', password)
                await page.click(f'input[type="{elements["submit"]["type"]}"]')

                await page.wait_for_timeout(3000)  # Adjust timeout as needed
                content = await page.content()

                if "Logout" in content or "Dashboard" in content:
                    print("Login successful")
                else:
                    print("Login failed")

                await browser.close()


# Usage
login_automation = LoginAutomation("http://testphp.vulnweb.com/login.php")


async def main():
    await login_automation.perform_login("testuser", "testpassword")


asyncio.run(main())
