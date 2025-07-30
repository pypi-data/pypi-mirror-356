import threading
import requests
import msgpack
import logging
from websockets.sync.client import connect
from .events import EventDispatcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("FishClient: [%(asctime)s] [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class FishClient:
    def __init__(self, cookie=None):
        self.dispatcher = EventDispatcher()
        self.session = requests.Session()

        self.websocket = None
        self.socket_thread = None
        self.is_connected = False

        self.cookie = cookie
        self.access_token = None

        if cookie:
            self.session.cookies.set("sb-wcsaaupukpdmqdjcgaoo-auth-token", cookie, domain="api.fishtank.live")

        self.dispatcher.on("disconnect")(self.disconnect)
        self.dispatcher.on("connect_error")(self.disconnect)

    
    def update_auth_token(self):
        if not self.cookie:
            return
        
        auth_response = self.session.get("https://api.fishtank.live/v1/auth")

        if auth_response.status_code != 200:
            raise Exception("Failed to retrieve auth token. Check your cookie.")
        
        auth_data = auth_response.json()
        if "session" not in auth_data or not auth_data["session"]:
            raise Exception("No session found in auth response. Check your cookie.")
        
        self.access_token = auth_data["session"]["access_token"]
        


    def connect(self):
        self.update_auth_token()

        self.websocket = connect(
            "wss://ws.fishtank.live/socket.io/?EIO=4&transport=websocket",
            additional_headers={
                "Origin": "https://www.fishtank.live",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            },
        )

        self.websocket.recv() # wait for initial thing
        self.websocket.send(
            msgpack.packb(
                {
                    "type": 0,
                    "data": {
                        "token": self.access_token
                    },
                    "nsp": "/",
                },
                use_bin_type=True,
            )
        )

        self.is_connected = True
        self.socket_thread = threading.Thread(target=self.listen)
        self.socket_thread.start()
        

    def disconnect(self):
        self.is_connected = False

        if self.socket_thread is not None:
            self.socket_thread.join()

        if self.websocket is not None:
            self.websocket.close()

        self.websocket = None
        self.socket_thread = None

    def send_event(self, event_name, data, options=None):
        if not self.is_connected:
            raise Exception("WebSocket is not connected.")
        
        data = {
            "type": 2,
            "data": [event_name, data],
            "nsp": "/",
        }

        if options is not None:
            data.update(options)
            
        packed_data = msgpack.packb(
            data,
            use_bin_type=True,
        )

        try:
            self.websocket.send(packed_data)
            logger.debug(f"Sent event {event_name} with data: {data}")
        except Exception as e:
            logger.error(f"Error sending event {event_name}: {e}", exc_info=e)

    def listen(self):
        if self.websocket is None:
            raise Exception("WebSocket is not connected.")

        while self.is_connected:
            try:
                message = self.websocket.recv()
                self.handle_message(
                    message
                )

            except Exception as e:
                logger.error(f"Error receiving message: {e}", exc_info=e)
                logger.info("Reconnecting to fishtank...")
                self.connect()
                break

            

      
    

    def handle_event(self, unpacked):
        data = unpacked.get("data")

        packet_type = data[0]
        packet_data = data[1]
        
        logger.debug(f"Handling event of type {packet_type} with data: {packet_data}")
        self.dispatcher.emit(packet_type, packet_data)

    def handle_packed(self, message):
        unpacked = msgpack.unpackb(message, raw=False)
        type = unpacked.get("type")

        if type == 2:
            self.handle_event(unpacked)

    def handle_message(self, message):
        first_byte = message[0:1]
        
        if first_byte == "2": # ping packet
            self.websocket.send("3")
            logger.debug("Sent pong response to ping packet")

        if first_byte == b'\x83':
            self.handle_packed(message)

    def get_orders(self, stock_name):
        response = self.session.get(
            f"https://api.fishtank.live/v1/stocks/{stock_name}/orders"
        )

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve orders for {stock_name}. Status code: {response.status_code}")

        return response.json() 
    
    def get_stocks(self):
        response = self.session.get("https://api.fishtank.live/v1/stocks")

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve stocks. Status code: {response.status_code}")

        return response.json()
    
    def get_stock(self, stock_name):
        response = self.session.get(f"https://api.fishtank.live/v1/stocks/{stock_name}")

        if response.status_code != 200:
            raise Exception(f"Failed to retrieve stock {stock_name}. Status code: {response.status_code}")

        return response.json()