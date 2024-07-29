# Automation Machine Learning for UI Testing

## Overview
This project leverages Machine Learning (ML) to revolutionize UI automation testing. Traditionally, the Page Object Model (POM) design pattern has been used for UI automation, requiring the creation of a class for each page with endless lists of elements. This approach is time-consuming and requires constant maintenance. Our solution dynamically parses and classifies page elements using ML, significantly reducing the need for manual updates and making the automation process more robust and efficient.

## Features
- **Dynamic Parsing and Classification**: Automatically identifies and classifies UI elements on a page.
- **Automated Binding with Association Rule Learning**: Dynamically binds input data to the correct elements.
- **Seamless Form Filling**: Fills forms based on the classified elements and provided input data.
- **Intelligent Button Handling**: Identifies and clicks the appropriate buttons based on input criteria.
- **Supports Various Input Types**: Handles text fields, password fields, checkboxes, textareas, and select dropdowns.

## Project Structure
automation_ml

├── src
│ ├── browser_automation.py # Handles browser automation tasks using Playwright
│ ├── form_classifier.py # Classifies elements from parsed HTML content
│ ├── form_filler.py # Fills the form based on classified elements and input data
│ ├── form_verifier.py # Verifies the form submission results
│ ├── ml_classifier.py # ML classifier for dynamic element classification
│
├── tests/
│ ├── test_form_filler.py # Unit tests for form filler functionality
│
├── requirements.txt # Project dependencies
│
└── README.md # Project documentation


## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/ovadiaomer/automation_machine_learning.git
    cd automation_machine_learning
    ```

2. **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Install Playwright browsers:**
    ```sh
    playwright install
    ```

## Usage
1. **Run Tests:**
    ```sh
    pytest tests/test_form_filler.py
    ```

2. **Example Code:**
    Here's a brief example of how to use the form filler:

    ```python
    import asyncio
    from src.browser_automation import BrowserAutomation
    from src.form_filler import FormFiller

    form_data = {
        'name': 'Omer',
        'phone1Prefix': '+972',
        'phone1': '1234567890',
        'email': 'test_user@autoGennie.com',
        'category': 'Product',
        'note': 'xyz',
        'button': {
            'type': 'submit'
        }
    }

    expected_data = {
        'message': 'Thank you for your submission'
    }

    async def main():
        url = 'https://example.com/contact-us'
        browser_automation = BrowserAutomation()
        await browser_automation.launch_browser()
        await browser_automation.navigate(url)
        form_filler = FormFiller(form_data, expected_data, browser_automation)
        result = await form_filler.fill_form_and_verify()
        print(result)
        await browser_automation.close_browser()

    asyncio.run(main())
    ```

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License.

## Acknowledgments
Special thanks to all contributors and the open-source community for their invaluable support.

---

You can find the source code for this project on [GitHub](https://github.com/ovadiaomer/automation_machine_learning).
