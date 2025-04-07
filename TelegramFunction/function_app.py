import azure.functions as func
import datetime
import json
import logging
import os
import telebot
import requests

# Read bot token from environment variable
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")

app = func.FunctionApp()

@app.function_name(name="iot-hub-trigger")
@app.event_hub_message_trigger(arg_name="event", event_hub_name="package-theft-hub", connection="IOT_HUB_CONNECTION_STRING", consumer_group="$Default")
def main(event: func.EventHubEvent):
    bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
    logging.info(f"TELEGRAM_BOT_TOKEN is set: {bool(TELEGRAM_BOT_TOKEN)}")
    response = requests.get("https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe")
    logging.info(response.text)
    bot.send_message(915971839, "Test message from Azure")

    
    # Extract and parse event data
    try:
        event_data = json.loads(event.get_body().decode("utf-8"))
        telegram_user_id = event_data.get("telegram_user_id")
        video_url = event_data.get("video_url")

        if telegram_user_id and video_url:
            bot.send_message(telegram_user_id, f"Button triggered! Video available at:\n{video_url}")
            logging.info(f"Sent message to user {telegram_user_id} with video URL: {video_url}")
        else:
            logging.warning("Invalid event data: Missing telegram_user_id or video_url")
        logging.info('Python EventHub trigger processed an event: %s', event.get_body().decode('utf-8'))

    except Exception as e:
        logging.error(f"Error processing event: {str(e)}")