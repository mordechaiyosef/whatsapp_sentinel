# WhatsApp Sentinel

## Overview

WhatsApp Sentinel is a Python-based application that interacts with WhatsApp to process messages and media, providing
responses based on predefined rules. The bot can handle text and image inputs, and it is designed to keep the chat
friendly and free of political or heated debates.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Example Usage](#example-usage)
7. [Troubleshooting](#troubleshooting)
8. [Contribution](#contribution)
9. [License](#license)

## Features

- **Text and Image Processing**: The bot can process both text and image inputs.
- **Automated Responses**: Generates responses based on the content of the messages.
- **Political Content Detection**: Identifies and responds to political content.
- **Media Handling**: Downloads and processes media files from WhatsApp messages.
- **Logging**: Logs important events and errors for debugging purposes.

## Requirements

- Python 3.x
- `pip` for managing Python packages

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/WPP_Whatsapp.git
    cd WPP_Whatsapp
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your environment variables with the necessary API keys:
    ```sh
    export OPENAI_API_KEY=your_openai_api_key
    ```

## Configuration

- **Logging**: The logging configuration is set up in `settings.py`.
- **Group Names**: Update the `GROUP_IDS` list in `settings.py` with the WhatsApp group IDs you want the bot to
  monitor.
- **Messages**: Customize the `IM_A_BOT_MESSAGE` and `DM_MESSAGE` in `settings.py` to change the bot's automated
  messages.

### Configure Group Names

1. Run the script to get the group names and IDs:
    ```sh
    python run.py --groups 1
    ```
2. Follow the instructions to scan the WhatsApp QR code in your browser.
3. Open the `groups.txt` file and manually add the desired group IDs to the `GROUP_IDS` list in `settings.py`.

## Usage

1. Start the bot:
    ```sh
    python run.py
    ```

2. Follow the instructions to scan the WhatsApp QR code in your browser.

3. The bot will start monitoring the specified groups and respond to messages based on the predefined rules.

## Example Usage

Here is an example of how the bot responds to a message:

- **User**: "Trump is great!"
- **Bot**: "Trump's rollback of environmental protections and withdrawal from the Paris Agreement showed a complete disregard for science and the future of our planet, prioritizing corporate profits over human survival."
- **Bot**: "Beep boop bop! 🤖 Just a bot here to keep things friendly. Let’s keep the chat fun and free of politics or
  heated debates. Peace and love, everyone! ✌️❤️"
- **Bot** (in DM to User): "Hey there! 😊 Just a quick note from me, your friendly chat bot. Let's try to keep the group chat positive and avoid topics that might stir up strong feelings, like politics. Thanks for understanding!"

## Another Example
Here is another example of how the bot responds the opposite of the previous example:

- **User**: "Trump is stupid!"
- **Bot**: "Calling Trump stupid ignores his strategic political maneuvers and the significant support he garnered, showcasing a deep misunderstanding of his impact on American politics."
- **Bot**: "Beep boop bop! 🤖 Just a bot here to keep things friendly. Let’s keep the chat fun and free of politics or
  heated debates. Peace and love, everyone! ✌️❤️"
- **Bot** (in DM to User): "Hey there! 😊 Just a quick note from me, your friendly chat bot. Let's try to keep the group chat positive and avoid topics that might stir up strong feelings, like politics. Thanks for understanding!"
 

**Notice that the bot will always disagree with the user's statement, regardless of what political side the user is on. 😈**

## Troubleshooting

- **Issue**: `GROUP_IDS is empty, see README.md`
- **Solution**: Ensure you have updated the `GROUP_IDS` list in `settings.py` with the correct group IDs from
  `groups.txt`.
- **Issue**: `OPENAI_API_KEY is empty, see README.md`
- **Solution**: Set the `OPENAI_API_KEY` environment variable with your OpenAI API key as documented in the
  [installation](#installation) section.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.