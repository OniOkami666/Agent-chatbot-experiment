import asyncio
from threading import Event
from lupa import LuaRuntime
from flask import Flask, render_template, Response, stream_with_context
from engine import chat_init

# Just some initialization stuff for the kill switch and the flask app
app = Flask(__name__)
stop_event = Event()

# Because AI agents need time to think, we use async to pause snippets for other tasks to occur
async def stream(stop_event):
    yield "data: [SYSTEM] Agents starting...\n\n"  
    chat = chat_init()

    try:
        async for message in chat.run_stream(task="Start a conversation about anything."):
            if stop_event.is_set():
                break
            if hasattr(message, 'content'):
                yield f"data: {message.source}: {message.content}\n\n"
    finally:
        yield "data: [SYSTEM] Stream stopped.\n\n"
        print("Stream stopped.")
# Point to the html file
@app.route('/')
def index():
    return render_template('index.html')
# This is a streaming response that bridges the AI with Flask as Flask is older while the AI is "modern"
@app.route('/chat_stream')
def chat_stream():
    stop_event.clear()  

    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        gen = stream(stop_event)  

        try:
            while not stop_event.is_set():
                # Display the next message
                yield loop.run_until_complete(gen.__anext__())
        except StopAsyncIteration:
            print("Chat ended naturally.")
        except GeneratorExit:
            print("Client disconnected.")
            stop_event.set()
        finally:
            loop.close()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/kill', methods=['POST'])
def kill():
    stop_event.set()
    return "Killed", 200

if __name__ == '__main__':
    app.run(debug=False, port=5000)
