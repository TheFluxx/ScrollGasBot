# ScrollGasBot
GasTracker - your reliable companion on the Scroll Network! Get timely gas price notifications, customize language and price thresholds. Stay informed on GitHub!

Welcome to GasTracker, your personal assistant on the Scroll Network! This Telegram bot is designed to keep you informed about the latest gas prices, ensuring you never miss out on crucial updates. With GasTracker, you have the power to customize your experience by selecting your preferred language and setting price thresholds for personalized notifications. Stay ahead of the curve in the fast-paced world of gas price fluctuations with GasTracker by your side. Join us on GitHub and revolutionize the way you monitor gas prices on the Scroll Network!

# GasTracker Setup Guide

Follow these steps to set up GasTracker on the Scroll Network.

1. **Clone Repository**: 
   ```bash
   git clone https://github.com/TheFluxx/ScrollGasBot

2. **Navigate to Directory**:
   ```bash
   cd scroll_gas_bot

3. **Install Requirements**: 
   ```bash
   pip install -r requirements.txt
   
4. **Set Environment Variables**:
   Create a .env file and add the following variables:<br>
    BOT_TOKEN=your_bot_token_here'<br>
    DB_DRIVER='postgresql+asyncpg'<br>
    DB_USERNAME='your_db_username'<br>
    DB_PASSWORD='your_db_password'<br>
    DB_HOST='localhost'<br>
    DB_NAME='scroll_gas_bot'<br>
    CHAT_ID='@ScrollGas'<br>
   Replace your_bot_token_here, your_db_username, and your_db_password with your actual values.

5. **Run the Bot**:
   ```bash
   python main.py
