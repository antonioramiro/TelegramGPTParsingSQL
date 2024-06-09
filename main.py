import os
import mysql.connector as sql
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes
from openai import OpenAI

def main():
    print("Initializing Telegram GPT Parsing to SQL Database...")

    openaikey, telegrambotkey, dbsecrets = gather_secrets()

    global instructions
    instructions = '"""' + gather_instructions() + '"""'

    global connection
    connection = connect_to_database(dbsecrets)

    global GPT
    GPT = turn_gpt_on(openaikey)

    initiate_bot(telegrambotkey)

# Fetching the API keys and Database Secrets

def gather_secrets():
    openaikey = os.getenv('openaikey')
    telegrambotkey = os.getenv('telegramkey')
    dbsecrets = {
        'host': os.getenv('host'),
        'port': os.getenv('port'),
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'database': os.getenv('database')
    }

    print("Gathering secret keys and database secrets...")
    return openaikey, telegrambotkey, dbsecrets

def gather_instructions():
    with open("instructions.txt", "r") as file:
        instructions = file.read()

    print("Gathering instructions for GPT...")
    return instructions

# DATABASE and SQL

def connect_to_database(dbsecrets):
    print("Connecting to Database...")
    
    try:
        connection = sql.connect(
            host=dbsecrets['host'],
            port=dbsecrets['port'],
            user=dbsecrets['user'],
            password=dbsecrets['password'],
            database=dbsecrets['database']
        )       

        if connection.is_connected():
            print("Successfully connected to the database!")
    except sql.Error as e:
        print(f"Error: {e}")

    return connection

def save_to_database(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Successfully saved to the database!")
    except sql.Error as e:
        print(f"Error: {e}")

# OPEN AI GPT

def turn_gpt_on(openaikey):
    client = OpenAI(api_key=openaikey)

    print("GPT is ready to chat...")
    return client

# TELEGRAM BOT

def initiate_bot(telegrambotkey):
    print("Initializing Telegram Bot...")
    application = ApplicationBuilder().token(telegrambotkey).build()
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)

    application.add_handler(chat_handler)
    print("Bot is ready to chat, send the message to the bot to get a response...")
    application.run_polling()

# Chat Handler

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    completion = GPT.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": update.message.text}
        ]
    )

    resulting_message = completion.choices[0].message.content

    print("The following message was sent to the bot: \n" + update.message.text + "\n \n")
    print("Bot's SQL response: \n" + resulting_message + "\n")

    save_to_database(resulting_message)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resulting_message)

if __name__ == "__main__":
    main()
