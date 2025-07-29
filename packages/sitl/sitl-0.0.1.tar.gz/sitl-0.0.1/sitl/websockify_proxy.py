from websockify.websocketproxy import WebSocketProxy
import time

LISTEN_HOST, LISTEN_PORT = "127.0.0.1", 6761
TARGET_HOST, TARGET_PORT = "127.0.0.1", 5761

def start_websocket_proxy():
    server = WebSocketProxy(
        listen_host=LISTEN_HOST,
        listen_port=LISTEN_PORT,
        target_host=TARGET_HOST,
        target_port=TARGET_PORT,
        daemon=False,
        verbose=True,
    )
    server.start_server()
def main():
    print(f"WebSocket proxy started on ws://{LISTEN_HOST}:{LISTEN_PORT} forwarding to {TARGET_HOST}:{TARGET_PORT}")
    start_websocket_proxy()
if __name__ == "__main__":
    main()

    

    

