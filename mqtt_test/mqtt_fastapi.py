import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from env import MQTT_PORT, MQTT_HOST, MQTT_PASSWORD, MQTT_USERNAME

mqtt_config = MQTTConfig(host=MQTT_HOST,
                         port=MQTT_PORT,
                         username=MQTT_USERNAME,
                         password=MQTT_PASSWORD)
mqtt = FastMQTT(config=mqtt_config)
# print(MQTT_USERNAME, MQTT_PASSWORD)

app = FastAPI()
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received received_message: ", topic, payload.decode(), qos, properties)
    return 0


@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received received_message to specific topic: ", topic, payload.decode(), qos, properties)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/test")
async def func():
    mqtt.publish("/test", "Hello from Fastapi")  # publishing mqtt topic
    return {"result": True, "received_message": "Published"}


if __name__ == '__main__':
    uvicorn.run('mqtt_fastapi:app', port=3000, reload=True)
