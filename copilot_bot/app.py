import os
from aiohttp import web
from dotenv import load_dotenv
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from bot import CopilotBot

load_dotenv()

adapter_settings = BotFrameworkAdapterSettings(
    os.getenv("MICROSOFT_APP_ID"), 
    os.getenv("MICROSOFT_APP_PASSWORD")
)
adapter = BotFrameworkAdapter(adapter_settings)

async def on_error(context: TurnContext, error: Exception):
    print(f"Error: {error}")
    await context.send_activity("Oops! Something went wrong.")
adapter.on_turn_error = on_error

bot = CopilotBot()

async def messages(req: web.Request):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    await adapter.process_activity(activity, auth_header, bot.on_turn)
    return web.Response(status=200)

async def ping(req: web.Request) -> web.Response:
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_post("/api/messages", messages)
app.router.add_get("/", ping)

if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
