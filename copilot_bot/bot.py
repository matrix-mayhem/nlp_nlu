from botbuilder.core import ActivityHandler, TurnContext
from graph_client import GraphClient

class CopilotBot(ActivityHandler):
    def __init__(self):
        self.graph = GraphClient()

    async def on_message_activity(self, turn_context: TurnContext):
        user_input = turn_context.activity.text.lower()

        if "schedule" in user_input:
            # Simple hardcoded meeting details (you can parse input later)
            response = self.graph.create_event(
                subject="Strategy Meeting",
                start_time="2025-05-26T14:00:00",
                end_time="2025-05-26T15:00:00",
                attendee_email="john@example.com"
            )
            if "id" in response:
                await turn_context.send_activity("✅ Meeting scheduled with John at 2 PM!")
            else:
                await turn_context.send_activity("❌ Failed to create meeting.")
        else:
            await turn_context.send_activity("Say: 'Schedule a meeting with John at 2 PM tomorrow'")
