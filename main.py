from flask import Flask, request
from botbuilder.core import BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity
import asyncio
app = Flask(__name__)

loop = asyncio.get_event_loop()
bot_adapter = BotFrameworkAdapter("")

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return "Unsupported Media Type", 415
    
    activity = Activity().deserialize(body)
    auth_header = (
        request.headers["Authorization"] if "Authorization" in request.headers else ""
    )
    async def turn_call(turn_context: TurnContext):
        await turn_context.send_activity(f"You said: {turn_context.activity.text}")
    
    task = bot_adapter.process_activity(activity, auth_header,turn_call)
    loop.run_until_complete(task)
    return "",200


if __name__ == "__main__":
    app.run("localhost",4000)