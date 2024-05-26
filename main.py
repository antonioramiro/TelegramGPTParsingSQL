import json
import mysql.connector as sql
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

def main():
    print("Initializing Telegram GPT Parsing to SQL Database...")

    openaikey,telegrambotkey, dbsecrets = gatherSecrets()

    global instructions
    instructions = '"""' + gatherInstructions() + '"""'

    global connection
    connection = connectToDatase(dbsecrets)

    global GPT
    GPT = turnGPTOn(openaikey)

    initiateBot(telegrambotkey)


# Fetching the API keys and Database Secrets

def gatherSecrets():
    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    openaikey = secrets['openaikey']
    telegrambotkey = secrets['telegramkey']
    dbsecrets = secrets['dbsecrets']

    print("Gathering secret keys and database secrets...")
    return [openaikey, telegrambotkey, dbsecrets]

def gatherInstructions():
    with open("instructions.txt", "r") as file:
        instructions = file.read()

    print("Gathering instructions for GPT...")
    return instructions

# DATABASE and SQL

def connectToDatase(dbsecrets):
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


def saveToDatabase(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Successfully saved to the database!")
    except sql.Error as e:
        print(f"Error: {e}")

# OPEN AI GPT

def turnGPTOn(openaikey):
    client = OpenAI(
        api_key= openaikey
    )  

    print("GPT is ready to chat...")
    return client


# TELEGRAM BOT

def initiateBot(telegrambotkey):

    print("Initializing Telegram Bot...")
    application = ApplicationBuilder().token(telegrambotkey).build()
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)

    application.add_handler(chat_handler)
    print("Bot is ready to chat, send the message to the bot to get the response...")
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


    saveToDatabase(resulting_message)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resulting_message)

if __name__ == "__main__":
    main()