import asyncio
from threading import Event
from lupa import LuaRuntime
from flask import Flask, render_template, Response, stream_with_context
from engine import chat_init

app = Flask(__name__)
stop_event = Event()

async def stream(stop_event):
    yield "data: [SYSTEM] Agents starting...\n\n"  # immediate first yield
    chat = chat_init()

    try:
        async for message in chat.run_stream(task="Start a conversation about humans."):
            if stop_event.is_set():
                break
            if hasattr(message, 'content'):
                yield f"data: {message.source}: {message.content}\n\n"
    finally:
        yield "data: [SYSTEM] Stream stopped.\n\n"
        print("Stream stopped.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_stream')
def chat_stream():
    stop_event.clear()  # reset at start of new stream

    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        gen = stream(stop_event)  # pass stop_event to your async generator

        try:
            while not stop_event.is_set():
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