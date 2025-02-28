# Restart Module for Pyrogram Bot


This module allows an authorized user to restart the Pyrogram-based Telegram bot through a command. The restart command is restricted to users whose IDs are specified in the `ADMIN_IDS` list.

## Features

- **Authorization Check**: Only users with IDs in the `ADMIN_IDS` list can use the restart command.
- **Response Messages**: Sends appropriate response messages for unauthorized access and during the restart process.
- **Inline Keyboard**: Provides useful links with inline buttons in the response messages.
- **Bot Restart**: Restarts the bot process by re-executing the Python script.

## Setup Instructions

### Prerequisites

- A Pyrogram-based Telegram bot.
- Python 3.8 to 3.11.
- Pyrogram library installed (`pip install pyrogram`).

### Step-by-Step Guide

1. **Clone the Repository or Download the Script**

   If you haven't already, clone the repository or download the `restart.py` script and place it in your bot's directory.

2. **Install Required Libraries**

   Ensure that you have the `pyrogram` library installed. You can install it using pip:

   ```sh
   pip install pyrogram
   ```

3. **Update `config.py`**

   Make sure your `config.py` file contains the `ADMIN_IDS` list with the Telegram user IDs of the authorized administrators. For example:

   ```python
   # config.py
   ADMIN_IDS = [123456789, 987654321]  # Replace with actual admin user IDs
   ```

4. **Integrate `restart.py` in Your Main Script**

   Import the `setup_restart_handler` function from the `restart.py` script and call it with your Pyrogram `Client` instance. For example:

   ```python
   # main.py
   from pyrogram import Client
   from restart import setup_restart_handler

   api_id = 'YOUR_API_ID'
   api_hash = 'YOUR_API_HASH'
   bot_token = 'YOUR_BOT_TOKEN'

   app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

   # Set up the restart handler
   setup_restart_handler(app)

   app.run()
   ```

5. **Running the Bot**

   Run your bot as usual:

   ```sh
   python main.py
   ```

6. **Using the Restart Command**

   Send `/restart` or `.restart` command in a private chat with the bot. Only authorized users (specified in `ADMIN_IDS`) can execute this command.

### Example Response Messages

- **Unauthorized Access**

  If an unauthorized user tries to use the restart command, the bot will respond with:

  ```
  ❌ You are not authorized to use this command.
  ```

  Along with inline buttons linking to the developer, other bots, source code, and update channel.

- **Restarting the Bot**

  When an authorized user uses the restart command, the bot will respond with:

  ```
  🔄 Restarting the bot...
  ```

  After a brief delay, the bot will restart and send the message:

  ```
  Bot Successfully Started! 💥
  ```

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests.

## License

This project is licensed under the [MIT License](./LICENSE).
