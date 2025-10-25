import requests
import time
import os
import random
import uuid
import logging
import threading


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TOKEN = os.getenv("token")

# Define servers and their respective bump channels
SERVERS = [
    # {
    #     "guild_id": "1317351089019818055",
    #     "channels": {
    #         "5hr": "1317351089322066002",
    #         "24hr": "1317351089322066002",
    #     },
    # },
    {
        "guild_id": "1253604591791247370",
        "channels": {
            "5hr": "1298301267981897862",
            "24hr": "1298301267981897862",
        },
    },
    # {
    #     "guild_id": "1338762628113367071",
    #     "channels": {
    #         "5hr": "1338762628406841353",
    #         "24hr": "1338762628406841353",
    #     },
    # },
]

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

def bump_every(interval_hours, bump_type, guild_id, channel_id):
    """
    Periodically send a bump command for a specific bump type (disboard or discadia).
    """
    headers = create_headers(TOKEN)

    def build_payload():
        if bump_type == "disboard":
            return {
                "type": 2,
                "application_id": "302050872383242240",
                "guild_id": guild_id,
                "channel_id": channel_id,
                "session_id": generate_session_id(),
                "analytics_location": "slash_ui",
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
                        "description": "Pushes your server to the top of all your server's tags and the front page",
                        "description_default": "Pushes your server to the top of all your server's tags and the front page",
                        "description_localized": "Bump this server.",
                        "dm_permission": True,
                        "global_popularity_rank": 1,
                        "integration_types": [0],
                        "name": "bump",
                        "name_localized": "bump",
                        "options": [],
                        "version": "1051151064008769576"
                    }
                },
                "attachments": [],
                "nonce": str(int(time.time() * 1000))
            }

        elif bump_type == "discadia":
            return {
                "type": 2,
                "application_id": "1222548162741538938",
                "guild_id": guild_id,
                "channel_id": channel_id,
                "session_id": generate_session_id(),
                "analytics_location": "slash_ui",
                "data": {
                    "version": "1383872612815343718",
                    "id": "1225075208394768496",
                    "name": "bump",
                    "type": 1,
                    "options": [],
                    "application_command": {
                        "id": "1225075208394768496",
                        "type": 1,
                        "application_id": "1222548162741538938",
                        "description": "Bump your Discadia listing!",
                        "description_localized": "Bump your Discadia listing!",
                        "dm_permission": False,
                        "global_popularity_rank": 1,
                        "integration_types": [0],
                        "name": "bump",
                        "name_localized": "bump",
                        "options": [],
                        "version": "1383872612815343718"
                    }
                },
                "attachments": [],
                "nonce": str(int(time.time() * 1000))
            }

    while True:
        payload = build_payload()
        simulate_typing()
        send_bump_command(headers, payload)

        delay = random.uniform((interval_hours + 0.06) * 3600, (interval_hours + 0.4) * 3600)
        logger.info(f"Next bump ({bump_type}) in {delay / 3600:.2f} hours.")
        time.sleep(delay)



if __name__ == "__main__":
    logger.info("Starting automated bumps across multiple servers...")

    for server in SERVERS:
        guild_id = server["guild_id"]

        # Disboard bump (5-hour)
        time.sleep(random.uniform(5, 10))
        threading.Thread(
            target=bump_every,
            args=(2, "disboard", guild_id, server["channels"]["5hr"]),
        ).start()

        # Discadia bump (24-hour)
        time.sleep(random.uniform(5, 10))
        threading.Thread(
            target=bump_every,
            args=(25, "discadia", guild_id, server["channels"]["24hr"]),
        ).start()
