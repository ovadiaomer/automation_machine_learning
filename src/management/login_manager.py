import asyncio
from src.form.form_filler import FormFiller

class LoginManager:
    def __init__(self, username, password):
        self.url = "http://testphp.vulnweb.com/login.php"
        self.user_data = {
            "username": username,
            "password": password
        }

    async def perform_login(self):
        form_filler = FormFiller(self.url, self.user_data)
        result_content = await form_filler.fill_and_submit_form()
        return result_content

if __name__ == "__main__":
    login_manager = LoginManager("testuser", "testpassword")
    asyncio.run(login_manager.perform_login())
