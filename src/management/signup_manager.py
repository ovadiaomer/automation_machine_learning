import asyncio
from src.form.form_filler import FormFiller

class SignupManager:
    def __init__(self, url, user_data):
        self.url = url
        self.user_data = user_data

    async def perform_signup(self):
        form_filler = FormFiller(self.url, self.user_data)
        result_content = await form_filler.fill_and_submit_form()
        return result_content

if __name__ == "__main__":
    user_data = {
        "username": "newuser",
        "password": "newpassword",
        "email": "newuser@example.com"
    }
    signup_manager = SignupManager("http://testphp.vulnweb.com/signup.php", user_data)
    asyncio.run(signup_manager.perform_signup())
