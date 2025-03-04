"""
The "Bot" script file contains the necessary code for building and running a Telegram chatbot.
It includes all the instructions for creating a graphical user interface (GUI) that makes
the chatbot easily accessible and user-friendly.
The main class, "Bot," is responsible for starting the chatbot process and
managing user interactions.

Within the "Bot" class, another class called "LLM" (defined in a different script, "llm") is utilized.
This "LLM" class is crucial for the chatbot's functionality as it handles information retrieval and response generation.
Essentially, "LLM" fetches relevant information from available sources and generates
appropriate responses to user queries.

The combination of these two classes, "Bot" and "LLM," allows the chatbot to operate efficiently,
providing accurate and helpful answers based on user requests.
The implementation of the GUI ensures that users can interact with the chatbot intuitively and effortlessly.

In summary, the "Bot" file is the core of the chatbot system, orchestrating
both the user interface and the backend logic to ensure a smooth and informative user experience.

Author:
Roberto Parodo, email: r.parodo2@studenti.unica.it
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, \
    CallbackQueryHandler, ConversationHandler
from llm import Llm

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config.env")
TOKEN = os.getenv("TOKEN_TELEGRAM")
MY_USERNAME = os.getenv("TELEGRAM_USERNAME")
STEP_ZERO, STEP_ONE, STEP_TWO, STEP_THREE = range(4)

DIRECTORY_PDF = 'dataset'
DIRECTORY_FACULTY_NAME = os.listdir(DIRECTORY_PDF)


class Bot(object):
    def __init__(self):
        """
        Before starting the Bot, make sure to set up the API keys in tne config.env file.
        """
        print("Start Bot")
        self.llm_model = None
        self.type_course, self.faculty = "", ""
        self.course, self.query, self.answer = "", "", ""
        application = ApplicationBuilder().token(TOKEN).build()
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                STEP_ZERO: [
                    CallbackQueryHandler(self.button_step_zero),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_invalid_input),
                ],
                STEP_ONE: [
                    CallbackQueryHandler(self.button_step_one),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_invalid_input),
                ],
                STEP_TWO: [
                    CallbackQueryHandler(self.button_step_two),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_invalid_input)
                ],
                STEP_THREE: [
                    CommandHandler("change", self.redo_choice),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
                ]
            },
            fallbacks=[CommandHandler("help", self.help_command)],
            allow_reentry=True,
        )
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler("help", self.help_command))
        application.run_polling()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if update.effective_user.username == MY_USERNAME:
            text_message = (f"Ciao {update.effective_user.username}! Sono il tuo assistente di Unica. "
                            f"Sono qui per aiutarti a comprendere le regole del corso di laurea di tuo interesse.")
            await update.message.reply_text(text_message)
            return await self.show_faculty(update, context)
        else:
            await update.message.reply_text("Access Denied")

    async def show_faculty(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        keyboard = []
        aus_button = []
        for i, b in enumerate(DIRECTORY_FACULTY_NAME):
            aus_button.append(InlineKeyboardButton(b, callback_data=b))
            keyboard.append([aus_button[i]])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("In che facoltà si trova il corso sulla quale desideri avere informazioni?",
                                        reply_markup=reply_markup)
        return STEP_ZERO

    async def show_type_course(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        tip_course = os.listdir(DIRECTORY_PDF + "/" + self.faculty)
        tip_course = [i.replace("1", "") for i in tip_course]
        keyboard = []
        aus_button = []
        for i, b in enumerate(tip_course):
            aus_button.append(InlineKeyboardButton(b, callback_data=b))
            keyboard.append([aus_button[i]])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("Per cominciare seleziona che tipo di laurea cerchi",
                                                       reply_markup=reply_markup)
        return STEP_ONE

    async def show_course(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if self.type_course == "Laurea Triennale":
            self.type_course = "1Laurea Triennale"
        course = os.listdir(DIRECTORY_PDF + "/" + self.faculty + "/" + self.type_course)
        keyboard = []
        aus_button = []
        for i, b in enumerate(course):
            aus_button.append(InlineKeyboardButton(b.replace(".pdf", ""), callback_data=b.replace(".pdf", "")))
            keyboard.append([aus_button[i]])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("Ecco l'elenco dei corsi disponibili. "
                                                       "Di quale corso hai bisogno di informazioni?",
                                                       reply_markup=reply_markup)
        return STEP_TWO

    async def button_step_zero(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Hai selezionato: {query.data}")
        self.faculty = query.data
        return await self.show_type_course(update, context)

    async def button_step_one(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Hai selezionato: {query.data}")
        self.type_course = query.data
        return await self.show_course(update, context)

    async def button_step_two(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Hai selezionato: {query.data}")
        self.course = query.data
        pdf_path = f"dataset/{self.faculty}/{self.type_course}/{self.course}.pdf"
        self.llm_model = Llm(pdf_path)
        return STEP_THREE

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.query = update.message.text
        self.answer = self.llm_model.process_chat(self.query)["answer"]
        await update.message.reply_text(self.answer)
        #self.save_conversation()
        return STEP_THREE

    async def redo_choice(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        return await self.show_faculty(update, context)

    async def handle_invalid_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Prima di continuare fai la tua scelta")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Scrivi '/start' per riavviare il bot.")
        await update.message.reply_text("Scrivi '/change' per cambiare il corso.")

    def save_conversation(self) -> None:
        with open('conversation.txt', 'a') as file:
            file.write(self.query + ': ')
            file.write(self.answer + '\n')