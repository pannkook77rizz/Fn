import discord
from discord.ext import commands
import rebootpy
from rebootpy.ext import commands as fn_commands
import json
import asyncio
import aiohttp

# Load Config
with open('config.json') as f:
    config = json.load(f)

class MyFortniteBot(fn_commands.Bot):
    async def event_ready(self):
        print(f'Bot Online: {self.user.display_name}')
        # Setup the Renegade Raider look
        await self.party.me.set_outfit(
            asset=config['skin'],
            variants=self.party.me.create_variants(material=config['skin_style'])
        )
        await self.party.me.set_emote(asset=config['emote'])
        await self.party.me.set_battlepass_info(has_purchased=True, level=config['level'], tier=config['tier'])
        await self.party.me.set_banner(icon=config['banner_icon'], color=config['banner_color'])

    async def event_party_member_join(self, member):
        if member.id != self.user.id:
            await self.party.send("Welcome To bot Made By Riku")

    async def event_party_message(self, message):
        if message.author.display_name == config['owner_name']:
            content = message.content.lower()
            if content == ".ready":
                await self.party.me.set_ready(rebootpy.ReadyState.READY)
            elif content == ".unready":
                await self.party.me.set_ready(rebootpy.ReadyState.NOT_READY)

# Discord Setup
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)
fn_instance = None

@bot.command()
async def start(ctx):
    global fn_instance
    await ctx.send("🚀 Starting... check the console log for the link!")
    
    # Use AuthorizationCodeAuth for the easiest web-based login
    fn_instance = MyFortniteBot(
        command_prefix='!',
        auth=rebootpy.AuthorizationCodeAuth() 
    )
    asyncio.create_task(fn_instance.start())

@bot.command()
async def sendparty(ctx, *, msg):
    if ctx.author.name == config['owner_name'] and fn_instance:
        await fn_instance.party.send(msg)

bot.run(config['discord_token'])
