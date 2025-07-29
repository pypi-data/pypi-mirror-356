from pydantic import BaseModel
import time
import pydantic_socketio

# pydantic_socketio.monkey_patch()


class Data(BaseModel):
    value: int
    description: str


sio = pydantic_socketio.Client()


@sio.on("misc")
def misc(data: Data):
    print("==== misc ", data, type(data))


sio.connect("http://localhost:8000")
# sio.connect("http://localhost:8000", transports=["websocket"])
data = Data(value=123, description="test")
sio.emit("misc", data)
time.sleep(2)
