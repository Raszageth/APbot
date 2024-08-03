# Discord Simulation Bot

The Discord Simulation Bot is designed to process simulation reports from Raidbots and Questionably Epic, upload them to WoW Audit, and respond with relevant messages in a Discord channel.

## Features

- Extracts character names from Raidbots and Questionably Epic reports.
- Posts simulation reports to WoW Audit.
- Sends automated responses to Discord channels based on report data.

## Prerequisites

- Python 3.8 or higher
- A Discord Bot Token
- WoW Audit Bearer Token
- `pip` to install Python packages

## Setup

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Raszageth/APbot.git
   cd APbot

2. **Create a Virtual Environment**

   Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install Dependencies**

   Install the required packages using pip:

   ```bash
   pip install -r requirements.txt

4. **Configure Environment Variables**

   Create a .env file in the project directory and add your tokens:

   ```bash
   DISCORD_BOT=your_discord_bot_token
   WOWAUDIT=your_wowaudit_bearer_token

## Usage

1. **Run the Bot**

   Activate the virtual environment and run the bot:

   ```bash
   source venv/bin/activate
   python3 apbot.py

2. **Interact with the Bot**
    
   Send a simulation report link from Raidbots or Questionably Epic in the specified Discord channel.
   The bot will respond with messages based on the report data.

## Contributing

1. Fork the repository.
2. Create your feature branch: git checkout -b feature/my-feature
3. Commit your changes: git commit -am 'Add new feature'
4. Push to the branch: git push origin feature/my-feature
5. Open a pull request.