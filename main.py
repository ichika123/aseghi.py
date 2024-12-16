import requests
import time
import random
import uuid
import logging
import threading
from keep_alive import keep_alive

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TOKEN = "MTI2ODQ0OTg1MTEwNDgyMTMzMg.G2zodh.T7-6ni7teWcef5XLINWfXbprhhg9wrcpBXvEEc"
GUILD_ID = "1317351089019818055"
CHANNEL_ID = "1317351089322066002"

def create_headers(token):
    """Create headers for Discord API requests."""
    return {
        "Authorization": token,
        "Content-Type": "application/json",
    }

def generate_session_id():
    """Generate a random session ID."""
    return str(uuid.uuid4()).replace("-", "")

def send_bump_command(headers, payload):
    """Send a bump command to the Discord API."""
    url = "https://discord.com/api/v9/interactions"
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            logger.info("Bump command sent successfully.")
        else:
            logger.error(f"Failed to send bump command: {response.status_code} - {response.text}")
    except Exception as e:
        logger.exception("Error sending bump command.")

def simulate_typing():
    """Simulate human-like typing by adding random delays."""
    delay = random.uniform(2, 5)
    logger.info(f"Simulating typing for {delay:.2f} seconds.")
    time.sleep(delay)

def bump_every(interval_hours, application_id, command_id, command_name, payload_customizations=None):
    """
    Periodically send a bump command.
    
    Args:
        interval_hours (float): Base interval in hours between bumps.
        application_id (str): Application ID for the command.
        command_id (str): Command ID.
        command_name (str): Command name.
        payload_customizations (dict): Additional payload customizations.
    """
    headers = create_headers(TOKEN)

    # Send the command immediately
    payload = {
        "type": 2,
        "application_id": application_id,
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "session_id": generate_session_id(),
        "data": {
            "version": "1",
            "id": command_id,
            "name": command_name,
            "type": 1,
            "options": [],
        },
        "nonce": str(int(time.time() * 1000)),
    }

    if payload_customizations:
        payload.update(payload_customizations)

    # Ensure dynamic session_id and nonce
    payload["session_id"] = generate_session_id()
    payload["nonce"] = str(int(time.time() * 1000))

    simulate_typing()
    send_bump_command(headers, payload)

    # Wait and then periodically send the command
    while True:
        # Randomize delay slightly to mimic human-like behavior
        delay = random.uniform(interval_hours - 0.5, interval_hours + 0.5) * 60 * 60
        logger.info(f"Next bump for {command_name} in {delay / 3600:.2f} hours.")
        time.sleep(delay)

        payload["session_id"] = generate_session_id()
        payload["nonce"] = str(int(time.time() * 1000))

        simulate_typing()
        send_bump_command(headers, payload)

keep_alive()
if __name__ == "__main__":
    logger.info("Starting automated bumps...")

    # 5-hour bump with updated payload
    threading.Thread(
        target=bump_every,
        args=(
            5,
            "302050872383242240",
            "947088344167366698",
            "bump",
        ),
        kwargs={
            "payload_customizations": {
                "data": {
                    "version": "1051151064008769576",
                    "id": "947088344167366698",
                    "name": "bump",
                    "type": 1,
                    "options": [],
                    "application_command": {
                        "id": "947088344167366698",
                        "type": 1,
                        "application_id": "302050872383242240",
                        "version": "1051151064008769576",
                        "name": "bump",
                        "description": "Pushes your server to the top of all your server's tags and the front page",
                        "description_default": "Pushes your server to the top of all your server's tags and the front page",
                        "dm_permission": True,
                        "integration_types": [0],
                        "global_popularity_rank": 1,
                        "options": [],
                        "description_localized": "Bump this server.",
                        "name_localized": "bump",
                    },
                    "attachments": [],
                },
                "analytics_location": "slash_ui",
            }
        },
    ).start()

    # 24-hour bump (existing payload)
    threading.Thread(
        target=bump_every,
        args=(
            24,
            "1222548162741538938",
            "1225075208394768496",
            "bump",
        ),
        kwargs={
            "payload_customizations": {
                "data": {
                    "version": "1225075208394768497",
                    "id": "1225075208394768496",
                    "name": "bump",
                    "type": 1,
                    "options": [],
                    "application_command": {
                        "id": "1225075208394768496",
                        "type": 1,
                        "application_id": "1222548162741538938",
                        "version": "1225075208394768497",
                        "name": "bump",
                        "description": "Bump your Discadia listing!",
                        "dm_permission": True,
                        "integration_types": [0],
                        "global_popularity_rank": 1,
                        "options": [],
                        "description_localized": "Bump your Discadia listing!",
                        "name_localized": "bump",
                    },
                    "attachments": [],
                },
                "analytics_location": "slash_ui",
            }
        },
    ).start()