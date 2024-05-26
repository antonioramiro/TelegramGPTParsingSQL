# Telegram GPT Parsing to SQL Database

This project integrates the Telegram messaging platform with OpenAI's GPT (Generative Pre-trained Transformer) model to parse user messages and save the responses to a SQL database.

### Safety Notice

**Important**: This project involves the storage of user-generated content in a SQL database. Assure that IP whitelisting is implemented to restrict database access to trusted sources. Access to the telegram bot should be restricted to authorized users only. Future versions of this project will include additional security features (such as a password).

## Features

- **Message Parsing with GPT Model**: Automatically parse any message sent to Telegram using OpenAI's GPT model, enabling the interpretation of user queries and interactions in natural language.

- **Custom Natural Language Instructions**: Define custom natural language instructions tailored to your specific use case, allowing the GPT model to understand and respond contextually to user inquiries or commands.

- **Database Integration**: Save parsed messages to a SQL database for efficient storage and retrieval, facilitating the archiving and analysis of user interactions over time.

## Setup

### Prerequisites

- Python 3.12.3 installed on your system.
- A Telegram account and a Telegram Bot API key. Learn how to create a Telegram bot [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
- An OpenAI account and an OpenAI API key. Sign up for an OpenAI account [here](https://platform.openai.com/signup).
- A SQL database (e.g., MySQL, PostgreSQL) for storing the responses. Ensure you have the necessary credentials to connect to the database.

### Installation

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/antonioramiro/TelegramGPTParsingSQL
   ```

2. Install the required Python packages using pip:

   ```
   pip install -r requirements.txt
   ```

3. Obtain API keys for Telegram Bot and OpenAI and save them in a `secrets.json` file in the root directory of the project:

   ```json
   {
     "openaikey": "YOUR_OPENAI_API_KEY",
     "telegramkey": "YOUR_TELEGRAM_BOT_API_KEY",
     "dbsecrets": {
       "host": "DATABASE_HOST",
       "port": "DATABASE_PORT",
       "user": "DATABASE_USER",
       "password": "DATABASE_PASSWORD",
       "database": "DATABASE_NAME"
     }
   }
   ```

4. Create a `instructions.txt` file in the root directory with the instructions for the GPT model. Change the "X_placeholder" with your custom instructions.

   Some recommendations for the instructions are:

   - **State the desired output format**: Specify the format for dates, times, and other data fields. Common formats include ISO 8601 for dates (YYYY-MM-DD), ISO 3166-1 alpha-2 for country codes, etc. Examples include:

     - "Dates should be in the format YYYY-MM-DD."
     - "Country codes should follow the ISO 3166-1 alpha-2 standard."

   - **Provide examples of the expected input format**: Give clear examples of how the input should be structured. This helps ensure that the model generates responses in the correct format. Examples include:

     - "Please provide a two sentence description of the evnent."

   - **Instructions for handling missing data**: Clearly state what the model should do if certain data is not available. Options include using a default value, returning null, or providing an error message. Emphasize not to hallucinate or invent data. Examples include:

     - "If the deadline is not provided, use '0000-00-00' as a placeholder."
     - "If the country is not specified, use NULL as the value."

   - **Explanation for secondary keys**: If your data structure includes secondary keys or specific values, explain these to the model. Examples include:

     - "Use 0 for 'blue', 1 for 'yellow', and 2 for 'red'."

   - **Additional relevant information**: Include any other details that might help the model generate the correct response. This could include the desired level of detail, the structure of the response, or specific instructions on the content.

5. Initialize the Telegram bot by running the `main.py` script:

   ```
   python main.py
   ```

## Usage

1. Send the content to a conversation with the Telegram bot.
2. The bot will parse the message using the GPT model and respond with the generated text.
3. The responses will be saved to the configured SQL database.

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.
