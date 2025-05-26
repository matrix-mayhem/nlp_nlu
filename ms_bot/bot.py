from botbuilder.core import ActivityHandler, TurnContext
from dotenv import load_dotenv
import os
import aiohttp

load_dotenv()

class EchoBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text
        await turn_context.send_activity(f"You said: {text}")

class CLUBot(ActivityHandler):
    def __init__(self):
        self.endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")  # e.g. https://<name>.cognitiveservices.azure.com
        self.api_key = os.getenv("AZURE_LANGUAGE_KEY")
        self.project_name = os.getenv("CLU_PROJECT_NAME")      # e.g., CLUWeatherBot
        self.deployment_name = os.getenv("CLU_DEPLOYMENT_NAME")  # usually 'production'

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text

        # Call CLU API
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }
        clu_url = f"{self.endpoint}/language/:analyze-conversations?api-version=2023-04-01"
        payload = {
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "id": "1",
                    "text": user_input,
                    "modality": "text",
                    "participantId": "user1"
                }
            },
            "parameters": {
                "projectName": self.project_name,
                "deploymentName": self.deployment_name,
                "stringIndexType": "TextElement_V8"
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(clu_url, headers=headers, json=payload) as resp:
                result = await resp.json()

        intent = result["result"]["prediction"]["topIntent"]

        # Respond based on intent
        if intent == "Greeting":
            await turn_context.send_activity("Hello! How can I help you today?")
        elif intent == "GetWeather":
            await turn_context.send_activity("Sure, I can help with the weather.")
        if intent == "BookFlight":
            await turn_context.send_activity("Yeah, When and where would you like to travel?")
        elif intent == "CancelFlight":
            await turn_context.send_activity("Sure, May I know the flight details")
        else:
            await turn_context.send_activity(f"Sorry, I didn't understand that (intent: {intent}).")