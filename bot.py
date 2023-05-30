import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
SUDO = os.environ.get("1964362058")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "**ι'м [𐏓︭͟𝐈𝛕ᷟ͢𝚣⃪ꙴ ❦∂єνι✨➳⃝🦋 𝆹𝅥˚˚](t.me/DeviXRoBot) **,\nι ωιℓℓ нєℓρ уσυ тσ мαкє fυи ωιтн уσυ.\nᴄℓιᴄк **/help** fσя мσяє ιиfσ👻.",


    link_preview=False,
    buttons=(
      [
        Button.url('ᴄнαт ɢяᴘ', 'https://t.me/budiesforever'),
        Button.url('σωиєя', 'https://t.me/my_dear_lightbright')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**нєℓρ мєиυ σf 𐏓︭͟𝐈𝛕ᷟ͢𝚣⃪ꙴ ❦∂єνι➳⃝🦋 𝆹𝅥˚˚**\n\nᴄσммαи∂: /mentionall\n__уσυ ᴄαи υѕє тнιѕ ᴄσммαи∂ ωιтн тєχт ωнαт уσυ ωαит тσ ѕαу тσ σтнєяѕ.__\n`єχαмρℓє`: /mentionall MSD on fire🔥!"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('ᴄнαт ɢяᴘ', 'https://t.me/houseofghost'),
        Button.url('σωиєя', 'https://t.me/my_dear_lightbright')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can mention all members!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to this group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    if usr.deleted or not usr.username:

   
       continue
    usrnum += 1
    usrtxt += f"@{usr.username}"
    
              
    if usrnum == 1:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
   
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Only admins can cancel!__")

  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

@client.on(events.NewMessage(pattern="^/leave$"))
async def leave(event):
         if event.sender_id == SUDO:
              pass
         else:
              return await event.respond('__Access Deniend__')
         input_chat = await event.input_chat
         await client(LeaveChannelRequest(input_channel))
         return
        

print(">> BOT STARTED <<")
client.run_until_disconnected()
