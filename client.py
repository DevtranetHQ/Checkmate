import json
import os
import platform
import random
import sys

import discord
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord.ext.commands import Context

import asyncio

from validate_email import validate_email

from helpers.checks import reaction_check, is_author
from helpers.embed import custom_embed
from helpers.requests import email_in_endpoint

from mailing.api import send_code


if not os.path.isfile("credentials.json"):
    sys.exit("'credentials.json' not found! Please add it and try again.")
else:
    with open("credentials.json") as file:
        credentials = json.load(file)

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True

client = Bot(command_prefix=config["prefix"], intents=intents)
# Removes the default help command of discord.py to be able to create our custom help command.
client.remove_command("help")


@client.event
async def on_ready() -> None:
    """
    The code in this even is executed when the client is ready
    """
    print(f"Logged in as {client.user.name}")
    print(f"Discord API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    status_task.start()

    # Assign unchecked role to the members who joined while the bot was offline
    for guild in client.guilds:
        uncheckedRole = discord.utils.get(guild.roles, name=config["uncheckedRoleName"])
        checkedRole = discord.utils.get(guild.roles, name=config["checkedRoleName"])

        if not uncheckedRole or not checkedRole:
            continue

        for member in guild.members:
            if uncheckedRole not in member.roles and checkedRole not in member.roles and member != client.user:
                await member.add_roles(uncheckedRole)


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the client
    """

    statuses = ["YOU SHALL NOT PASS!"]
    await client.change_presence(activity=discord.Game(random.choice(statuses)))


async def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await client.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@client.event
async def on_message(message: discord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """
    if message.author == client.user or message.author.bot:
        return

    await client.process_commands(message)


@client.event
async def on_command_error(ctx: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param ctx: The normal command that failed executing.
    :param error: The error that has been faced.
    """

    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B,
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission(s) `"
            + ", ".join(error.missing_permissions)
            + "` to execute this command!",
            color=0xE02B2B,
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code.
            color=0xE02B2B,
        )
        await ctx.send(embed=embed)
    raise error


@client.event
async def on_guild_join(guild) -> None:
    client.dispatch("setup", guild)


@client.event
async def on_member_join(member) -> None:
    uncheckedRole = discord.utils.get(member.guild.roles, name=config["uncheckedRoleName"])

    if not uncheckedRole:
        return

    await member.add_roles(uncheckedRole)


@client.event
async def on_change_state(state) -> None:
    """
    The code in this event is executed every time the on_change_state event is called
    """
    with open("state.json", "w") as file:
        if state.lower() == "disable":
            json.dump({"isEnabled": False}, file)
        elif state.lower() == "enable":
            json.dump({"isEnabled": True}, file)


@client.event
async def on_setup(guild) -> bool:
    """
    The code in this event is executed every time the on_setup event is called
    """
    uncheckedRole = discord.utils.get(guild.roles, name=config["uncheckedRoleName"])
    checkedRole = discord.utils.get(guild.roles, name=config["checkedRoleName"])
    participantRole = discord.utils.get(guild.roles, name=config["participantRoleName"])

    checkChannel = discord.utils.get(guild.channels, name=config["checkChannelName"])

    if not uncheckedRole:
        uncheckedRole = await guild.create_role(name=config["uncheckedRoleName"])
    if not checkedRole:
        checkedRole = await guild.create_role(name=config["checkedRoleName"])
    if not participantRole:
        participantRole = await guild.create_role(name=config["participantRoleName"])

    for role in guild.roles:
        # Remove all perms for default role
        if role.name == "@everyone":
            perms = discord.Permissions()
            perms.update(
                view_channel=False,
            )
            await role.edit(reason=None, permissions=perms)
        # Give all perms to checked role
        if role.id == checkedRole.id:
            perms = discord.Permissions()
            perms.update(
                read_messages=True,
                read_message_history=True,
                connect=True,
                speak=True,
                send_messages=True,
                change_nickname=False,
                view_channel=True,
            )
            await role.edit(reason=None, permissions=perms)
        # Only allow access to check channel for unchecked role
        elif role.id == uncheckedRole.id:
            perms = discord.Permissions()
            perms.update(
                read_messages=True,
                read_message_history=True,
                connect=False,
                speak=False,
                send_messages=False,
                change_nickname=False,
                view_channel=False,
            )
            await role.edit(reason=None, permissions=perms)

    if checkChannel:
        await checkChannel.delete()


@client.event
async def on_raw_reaction_add(payload):
    """
    The code in this event is executed every time the on_raw_reaction_add event is called
    """

    if payload.member == client.user:
        return

    channel_payload = client.get_channel(payload.channel_id)
    channel_check = discord.utils.get(channel_payload.guild.channels, name=config["checkChannelName"])

    if channel_payload.id == channel_check.id and str(payload.emoji) == "✅":
        message = await channel_payload.fetch_message(payload.message_id)

        await message.remove_reaction("✅", payload.member)

        client.dispatch("check_started", payload)


@client.event
async def on_check_started(payload):
    """
    The code in this event is executed every time the on_check_started event is called
    """
    member = payload.member
    guild = client.get_guild(payload.guild_id)

    # Ask for user's email
    embed = discord.Embed(
        title="checkmate | Check Process 1/2",
        description=config["checkProcessAskEmailMessage"],
        color=0xF6E6CC,
    )
    await member.send(embed=embed)

    try:
        email = await client.wait_for("message", check=is_author(member), timeout=60 * 10)
    except asyncio.TimeoutError:
        await custom_embed(
            config["checkProcessTimeOutErrorMessage"],
            member,
            False,
        )

    # Check if the email is valid
    try:
        isValid = validate_email(email.content)
    except:
        isValid = False

    if isValid:
        # Check if the user has an account on the website
        userRoles = email_in_endpoint(config["userInDbEndpoint"], email.content)

        if userRoles:
            pass
        else:
            await custom_embed(
                config["checkProcessAccountErrorMessage"],
                member,
                False,
            )
            return

        # Ask the user the verification code they received
        embed = discord.Embed(
            title=f"checkmate | Check Process 2/2",
            description=config["checkProcessAskCodeMessage"],
            color=0xF6E6CC,
        )
        await member.send(embed=embed)

        # Send a verification code to the user
        realCode = send_code(email.content, guild.name, member.name, config["SENDGRID_KEY"])

        try:
            userCode = await client.wait_for("message", check=is_author(member), timeout=60 * 10)
        except asyncio.TimeoutError:
            await custom_embed(
                config["checkProcessTimeOutErrorMessage"],
                member,
                False,
            )

        # Check if the generated code and the code entered by theuser are the same
        if realCode == userCode.content:
            client.dispatch("check_completed", guild, member, email, userRoles)
        # Throw an error if the code is not valid
        else:
            await custom_embed(
                config["checkProcessCodeErrorMessage"],
                member,
                False,
            )

    # Throw an error if the email is not valid
    else:
        await custom_embed(
            config["checkProcessEmailErrorMessage"],
            member,
            False,
        )


@client.event
async def on_check_completed(guild, member, email, userRoles) -> None:
    """
    The code in this event is executed every time the on_check_completed event is called
    """
    uncheckedRole = discord.utils.get(guild.roles, name=config["uncheckedRoleName"])
    checkedRole = discord.utils.get(guild.roles, name=config["checkedRoleName"])

    # Give checked role to the user
    if checkedRole:
        await member.add_roles(checkedRole)
    else:
        await custom_embed(
            config["basicErrorMessage"],
            member,
            False,
        )
        return

    # Remove unchecked role from the user
    if uncheckedRole:
        await member.remove_roles(uncheckedRole)
    else:
        await custom_embed(
            config["basicErrorMessage"],
            member,
            False,
        )
        return

    for roleName in userRoles:
        role = discord.utils.get(guild.roles, name=roleName)

        if not role:
            role = await guild.create_role(name=roleName)

        await member.add_roles(role)

    await custom_embed(
        config["checkProcessCompletedMessage"],
        member,
        True,
    )

    embed = discord.Embed(
        title="",
        description=config["checkProcessAskAttendanceMessage"],
        color=0xF6E6CC,
    )

    msg = await member.send(embed=embed)

    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    confirmation = await client.wait_for("reaction_add", check=reaction_check(client, msg.id))

    if confirmation[0].emoji == "✅":
        participantRole = discord.utils.get(member.guild.roles, name=config["participantRoleName"])

        if not participantRole:
            return

        await member.add_roles(participantRole)

        await custom_embed(
            "You were added the " + config["participantRoleName"] + " role!",
            member,
            True,
        )
    else:
        await custom_embed(
            config["checkProcessNotAttendingMessage"],
            member,
            False,
        )

    await msg.delete()


async def main() -> None:
    async with client:
        await load_commands("normal")
        await client.start(credentials["token"])


if __name__ == "__main__":
    """
    This will automatically load slash commands and normal commands located in their respective folder.
    If you want to remove slash commands, which is not recommended due to the Message Intent being a privileged intent, you can remove the loading of slash command.
    """
    asyncio.run(main())
