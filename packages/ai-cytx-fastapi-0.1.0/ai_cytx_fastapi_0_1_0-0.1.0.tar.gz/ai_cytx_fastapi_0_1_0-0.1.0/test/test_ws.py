# test_ws.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/ws')
def websocket_route():
    if not request.environ.get('wsgi.websocket'):
        return "WebSocket required", 400

    ws = request.environ['wsgi.websocket']
    print("新客户端已连接")

    try:
        while True:
            message = ws.receive()
            if message:
                ws.send(f"Echo: {message}")
    except Exception as e:
        print("发生错误:", e)
    finally:
        print("客户端已断开")
