import os
from aiohttp import web
from dotenv import load_dotenv
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
    TurnContext,
    ConversationState,
    MemoryStorage,
)
from botbuilder.schema import Activity
from bot import EchoBot, CLUBot

load_dotenv()

# Settings
APP_ID = os.getenv("MICROSOFT_APP_ID")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")
SETTINGS = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Catch-all error handler
async def on_error(context: TurnContext, error: Exception):
    print(f"Error: {error}")
    await context.send_activity("Sorry, something went wrong.")
ADAPTER.on_turn_error = on_error

LUIS_APP_ID = os.getenv("LUIS_APP_ID")
LUIS_API_KEY = os.getenv("LUIS_API_KEY")
LUIS_API_HOST_NAME = os.getenv("LUIS_API_HOST_NAME")

# Create the bot
#BOT = EchoBot()
BOT = CLUBot()

# Listen for incoming requests on /api/messages
async def messages(req: web.Request) -> web.Response:
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    return web.Response(status=200)

async def ping(req: web.Request) -> web.Response:
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_post("/api/messages", messages)
app.router.add_get("/", ping)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
