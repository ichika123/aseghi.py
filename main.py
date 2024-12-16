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
TOKEN = "MTI1MjM0MDEwMzUxNTIxNDAwNw.GwE4Ul.06j2kIzhPr0BsY4xljSEsxQjCoqdS58eOEbNlA"

# Define servers and their respective bump channels
SERVERS = [
    {
        "guild_id": "1295703158999220234",
        "channels": {
            "5hr": "1307599070969204767",
            "24hr": "1307599070969204767",
        },
    },
    {
        "guild_id": "1317351089019818055",
        "channels": {
            "5hr": "1317351089322066002",
            "24hr": "1317351089322066002",
        },
    },
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

def bump_every(interval_hours, application_id, command_id, command_name, guild_id, channel_id, payload_customizations=None):
    """
    Periodically send a bump command for a specific server and channel.

    Args:
        interval_hours (float): Base interval in hours between bumps.
        application_id (str): Application ID for the command.
        command_id (str): Command ID.
        command_name (str): Command name.
        guild_id (str): Discord server (guild) ID.
        channel_id (str): Discord channel ID.
        payload_customizations (dict): Additional payload customizations.
    """
    headers = create_headers(TOKEN)

    payload = {
        "type": 2,
        "application_id": application_id,
        "guild_id": guild_id,
        "channel_id": channel_id,
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

    while True:
        payload["session_id"] = generate_session_id()
        payload["nonce"] = str(int(time.time() * 1000))

        simulate_typing()
        send_bump_command(headers, payload)

        delay = random.uniform(interval_hours - 0.5, interval_hours + 0.5) * 60 * 60
        logger.info(f"Next bump for {command_name} in {delay / 3600:.2f} hours.")
        time.sleep(delay)

keep_alive()
if __name__ == "__main__":
    logger.info("Starting automated bumps across multiple servers...")

    for server in SERVERS:
        guild_id = server["guild_id"]
        
        # Start a thread for the 5-hour bump
        threading.Thread(
            target=bump_every,
            args=(
                5,
                "302050872383242240",
                "947088344167366698",
                "bump",
                guild_id,
                server["channels"]["5hr"],
            ),
            kwargs={
                "payload_customizations": {
                    "data": {
                        "version": "1051151064008769576",
                        "id": "947088344167366698",
                        "name": "bump",
                        "type": 1,
                        "options": [],
                    },
                },
            },
        ).start()

        # Start a thread for the 24-hour bump
        threading.Thread(
            target=bump_every,
            args=(
                24,
                "1222548162741538938",
                "1225075208394768496",
                "bump",
                guild_id,
                server["channels"]["24hr"],
            ),
            kwargs={
                "payload_customizations": {
                    "data": {
                        "version": "1225075208394768497",
                        "id": "1225075208394768496",
                        "name": "bump",
                        "type": 1,
                        "options": [],
                    },
                },
            },
        ).start()
