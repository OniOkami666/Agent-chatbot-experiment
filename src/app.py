import asyncio
from lupa import LuaRuntime
from flask import Flask, render_template, Response, stream_with_context
from engine import chat_init

app = Flask(__name__)

lua = LuaRuntime(unpack_returned_tuples=True)
with open("log.lua", "r") as f:
    lua.execute(f.read())
lua_log = lua.globals().log

async def stream():
    chat = chat_init()

    try:
        async for message in chat.run_stream(task="Start a conversation about humans."):
            if hasattr(message, 'content'):
                lua_log(message.source, message.content)
                yield f"data: {message.source}: {message.content}\n\n"
    except exit:
        print("disconnected!  Stopping!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat_stream')
def chat_stream():
    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        gen = stream() 
        try:
            while True:
                
                yield loop.run_until_complete(gen.__anext__())
        except (StopAsyncIteration, exit):
            print("Chat ended or Kill Switch pressed.")
        finally:
            loop.close()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, port=3000)