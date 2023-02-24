import uvicorn
from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig
from env import MQTT_PORT, MQTT_HOST, MQTT_PASSWORD, MQTT_USERNAME

mqtt_config = MQTTConfig(host=MQTT_HOST,
                         port=MQTT_PORT,
                         username=MQTT_USERNAME,
                         password=MQTT_PASSWORD)
mqtt = FastMQTT(config=mqtt_config)

debug = '[DEBUG]'

app = FastAPI()
mqtt.init_app(app)


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt")  # subscribing mqtt topic
    print(debug + "Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print(debug + "Received message: ", topic, payload.decode(), qos, properties)
    return 0


@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print(debug + "Received message to specific topic: ", topic, payload.decode(), qos, properties)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print(debug + "Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print(debug + "subscribed", client, mid, qos, properties)


@app.get("/publish")
async def func(topic: str = '/test', message: str = "Hello from Fastapi"):
    mqtt.publish(topic, message)  # publishing for mqtt topic
    return {"result": True, "message": "Published"}


if __name__ == '__main__':
    uvicorn.run('mqtt_fastapi:app', port=3000, reload=True)
