from websockify.websocketproxy import WebSocketProxy

LISTEN_HOST, LISTEN_PORT = "127.0.0.1", 6761
TARGET_HOST, TARGET_PORT = "127.0.0.1", 5761

def start_websocket_proxy():
    server = WebSocketProxy(
        listen_host=LISTEN_HOST,
        listen_port=LISTEN_PORT,
        target_host=TARGET_HOST,
        target_port=TARGET_PORT,
        daemon=True,
        verbose=True,
    )
    server.start_server()
