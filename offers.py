import requests
from bs4 import BeautifulSoup
from datetime import datetime
import discord
from discord.ext import commands
import asyncio
import time

# Discord bot setup
bot = commands.Bot(command_prefix='!')
TOKEN = '6765'  # Replace with your Discord bot token
CHANNEL_ID = '1395966273300467814'  # Replace with your Discord channel ID (enable Developer Mode in Discord to copy ID)

@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user} at {datetime.now()}')

async def send_message(message):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    else:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}")

async def main():
    k = 0
    old_text = None
    print('Scraping started at:', datetime.now())

    while True:
        try:
            # Check every 10 minutes (based on minute value divisible by 10)
            if int(datetime.now().strftime('%M')) % 10 == 0:
                html_doc = requests.get('https://www.desidime.com/new', timeout=10).text
                bs = BeautifulSoup(html_doc, 'html.parser')
                x = bs.findAll('div', class_="deal-url", limit=5)
                
                if x:  # Ensure we found some deals
                    i = x[0]
                    deal_text = i.text.lower()
                    if ('kettle' in deal_text or 'diaper' in deal_text or 'toothpaste' in deal_text) and i.text != old_text:
                        old_text = i.text
                        k += 1
                        link = i.find('a').get('href')
                        message = f"{i.text}\n{link}"
                        print(f'Scraping a deal for you! Found {k} deal(s)!')
                        await send_message(message)
                else:
                    print('No deals found in this scrape.')
            
            # Sleep for 60 seconds to avoid hammering the site and to check the minute
            await asyncio.sleep(60)
        
        except requests.RequestException as e:
            print(f"Error fetching webpage: {e}")
            await asyncio.sleep(60)  # Wait before retrying
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(60)  # Wait before retrying

# Run the bot and scraper
if __name__ == "__main__":
    asyncio.run(main())
