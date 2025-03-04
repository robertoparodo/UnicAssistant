"""
Before starting the bot, you need to configure your OpenAI API key, your Telegram token,
and your unique Telegram username.

Adding your Telegram username is crucial to ensure that only you can use the bot.
Once created, the bot will be publicly searchable under its name (e.g., "UnicAssistant").
To prevent unauthorized access, make sure to enter the correct username; otherwise, you will be denied access.

Follow these steps before launching the bot:
    1) Edit the config.env file
        Add your OpenAI API key: OPENAI_API_KEY=your_api_key_here
        Add your Telegram bot token: TOKEN_TELEGRAM=your_telegram_token_here
        Add your Telegram username: TELEGRAM_USERNAME=your_username_here

    (Make sure not to use quotes or double quotes around the values)

    2) How to generate your Telegram bot token:
        Open Telegram and search for BotFather
        Start the chat with BotFather
        Type /newbot and follow the instructions
        If successful, BotFather will generate an API token for your bot
        Copy and paste this token into the config.env file under TOKEN_TELEGRAM

    3) You're now ready to launch your chatbot!

Author:
Roberto Parodo, email: r.parodo2@studenti.unica.it
"""
from bot import Bot

if __name__ == '__main__':
    loop = Bot()