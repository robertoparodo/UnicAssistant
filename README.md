# README #

### ABSTRACT ###

Development of a Q&A chatbot designed to answer questions about the academic 
regulations of the University of Cagliari. 
The system, after receiving a user query, performs a semantic search in 
the database to identify relevant information. 
It then generates a response using a language model (LLM), 
incorporating the query and the retrieved document as context.

### CONTENTS ###

The system is composed of six Python scripts, each with a specific function:

- **`chunk.py`** → Splits PDFs into chunks and stores them in the Vector Database.
- **`create_db.py`** → Creates and manages the Vector Database.
- **`load_db.py`** → Loads the Database when needed.
- **`llm.py`** → Manages interactions with the language model.
- **`bot.py`** → Connects the chatbot to Telegram.
- **`main.py`** → Starts the chatbot application.

### What is this repository for? ###

* This repository is dedicated to the development of a Q&A chatbot 
designed to respond to inquiries about the academic regulations 
of the University of Cagliari. 
However, the system can be adapted and expanded to 
incorporate various types of informational content, 
making it highly flexible.

### How do I get set up? ###

##### Summary of set up #####
* To start the bot, make sure to follow all these steps listed below.

### 1️⃣ Prerequisites
Before running the chatbot, ensure you have:
- **Python** (>=3.8) installed on your system.
- **Telegram** installed on your mobile device or computer.
- **Required Python libraries** (installable with the command below).

### 2️⃣ Installation Steps
1. Clone the repository and navigate into the project folder:
   ```bash
   git clone <repository_url>
   cd <project_folder>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Obtain a **Telegram Bot Token**:
   - Open Telegram and search for **BotFather**.
   - Start a chat and type:
     ```
     /newbot
     ```
   - Follow the instructions to create your bot.
   - Copy and securely store the **API Token** provided.


4. Configure environment variables:
   - Update `config.env`, make sure to add the OpenAI API keys, Telegram-Token, Telegram-Username:
     ```ini
     OPENAI_API_KEY=your_openai_api_key
     TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     TELEGRAM_USERNAME=your_username
     ```

##### How to run #####
To create the database, first, run the chunk script to generate the chunks for each PDF document. 
After that, run the create_db.py script to build the vector database.

Since the database has already been created previously, to start the bot, simply run the main.py script. 
Then, search for the bot (either UnicAssistant or the name you've assigned to it) on Telegram. 
Now, you're ready to start chatting!

### Who do I talk to? ###

* Roberto Parodo - r.parodo2@studenti.unica.it