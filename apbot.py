import re
import os
import json
import discord
import requests
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv('DISCORD_BOT')
WOWAUDIT_API_URL = 'https://wowaudit.com/v1/wishlists'
BEARER_TOKEN = os.getenv('WOWAUDIT')
CHANNEL_NAME = "raidbot"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


def extract_report_id(url):
    raidbots_match = re.search(r'https://www\.raidbots\.com/simbot/report/([\w\d]+)', url)
    qe_match = re.search(r'https://questionablyepic\.com/live/upgradereport/([\w\d]+)', url)

    if raidbots_match:
        return 'raidbots', raidbots_match.group(1)
    if qe_match:
        return 'qe', qe_match.group(1)
    return None, None


def get_character_name_from_raidbots(report_id):
    try:
        url = f'https://www.raidbots.com/simbot/report/{report_id}/data.json'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            character_name = data.get('sim', {}).get('players', [{}])[0].get('name')
            return character_name
        return None
    except requests.RequestException as e:
        print(f"Error fetching Raidbots report data: {e}")
        return None

def get_character_name_from_qe(report_id):
    try:
        url = f'https://questionablyepic.com/api/getUpgradeReport.php?reportID={report_id}'
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = json.loads(response.text) # wtf QE
            data_dict = json.loads(data)
            character_name = data_dict.get('playername')
            return character_name
        return None
    except requests.RequestException as e:
        print(f"Error fetching QE report data: {e}")
        return None

def post_to_wowaudit(report_id, character_name):
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'report_id': report_id,
        'character_name': character_name,
        'configuration_name': 'Single Target',
        'replace_manual_edits': True,
        'clear_conduits': True
    }
    response = requests.post(WOWAUDIT_API_URL, json=data, headers=headers, timeout=5)
    return response


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    for guild in client.guilds:
        channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)
        if channel:
            try:
                await channel.send("APbot is now online and ready to receive simulation links!")
                break
            except discord.errors.Forbidden:
                print(f"Cannot send messages to {channel.name}")
        else:
            print(f"Channel named '{CHANNEL_NAME}' not found in guild '{guild.name}'.")

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.name != CHANNEL_NAME:
        return

    message_author_name = message.author.display_name
    platform, report_id = extract_report_id(message.content)
    if report_id:
        character_name = None
        if platform == 'raidbots':
            character_name = get_character_name_from_raidbots(report_id)
        elif platform == 'qe':
            character_name = get_character_name_from_qe(report_id)

        if character_name is not None:
            response = post_to_wowaudit(report_id, character_name)
            response_data = response.json()
            if response.status_code == 200:
                if 'error:' in response_data:
                    await message.channel.send(
                        f"Error adding sim to WoWAudit wishlist, {response_data['error:']}"
                    )
                else:
                    if character_name == "Seby":
                        await message.channel.send(
                        "Why you need loot? its not transmo run..."
                    )
                    if character_name == "Omnikrom":
                        await message.channel.send(
                        "Why are you simming? Aren't you on vacation?"
                    )
                    await message.channel.send(
                        f'Successfully added {message_author_name} sim '
                        f'to WoW Audit {character_name} wishlist!'
                    )
            else:
                await message.channel.send(
                    f"Failed to add {message_author_name} sim to WoW Audit:"
                    f"{response.status_code}: {response_data['message']}"
                )
    # else:
    #     await message.channel.send(
    #             f'Failed to analyze {message_author_name} sim, check your raidbots link'
    #         )

client.run(TOKEN)
