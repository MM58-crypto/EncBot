import discord
import requests
import json
import random
from replit import db
# connection to discord
client = discord.Client(intents=discord.Intents.all())

negative_words = [
  "sad", "miserable", "angry", "unhappy", "despair", "hopeless", "furious",
  "grief", "inconsolable"
]

starter_encourgaments = [
  "Cheer up", "You got this", "Hang in there", "You are great",
  "There is light at the end of the tunnel", "You can do this"
]
if "responding" not in db.keys():
  db["responding"] = True

# gets inspiration quotes from api
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)
#shows the user how to use the bot/commands list
def bot_manual():
  manual = '''To add a new msg to the bot/db -- $new,
  To delete an inspiring msg -- $del,
  To get a random inspiring quote -- $inspire'''
  return(manual)


def update_encourgaments(inspiring_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(inspiring_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [inspiring_msg]

def delete_encouragements(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
  
@client.event
# event occurs when bot is ready/ working
async def on_ready():
  print('We have logged in as {0.user}'.format(client))


# when a bot senses a msg
@client.event
async def on_message(message):
  # checks if author of msg is the bot itself
  if message.author == client.user:
    return
  msg = message.content

  if message.content.startswith('$hello'):
    # bot responds to a hello msg
    await message.channel.send('Hello!')
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
    
  if db["responding"]: 
    options = starter_encourgaments
    if "encouragements" in db.keys():
      options = options + list(db['encouragements'])
      # containing sad/negative words
      # selects a random encourgament from the starter list and responds to a msg
    if any(word in msg for word in negative_words):
      await message.channel.send(random.choice(options))  
  if msg.startswith('$manual'):
    manual = bot_manual()
    await message.channel.send(manual)
  # allows user to add inspiring words to db
  if msg.startswith("$new"):
    # removes $new from user message
    inspiring_msg = msg.split("$new ", 1)[1]
    update_encourgaments(inspiring_msg)
    await message.channel.send("New inspiring msg added to bot/db.")
  # user deletes encouraging/inspiring msg
  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  # if bot should respond to sad words or not
  if msg.startswith("$responding"):
    value = msg.split("$responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding activated")
    else :
      db["responding"] = False 
      await message.channel.send("Responding is deactivated")
# to run the bot
#token is in a seperate file
client.run(token)

