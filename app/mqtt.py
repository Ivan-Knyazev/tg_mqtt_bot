from paho.mqtt import client as client_mqtt
from app.env import MQTT_PORT, MQTT_HOST, MQTT_PASSWORD, MQTT_USERNAME, MQTT_CLIENT_ID
import app.settings as sets


# Configuration functions of MQTT
def connect_mqtt() -> client_mqtt:
    client = client_mqtt.Client(client_id=MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host=MQTT_HOST, port=int(MQTT_PORT))
    return client


def on_connect(client: client_mqtt, userdata, flags, rc: int):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d\n", rc)
    # client.loop_start()


def on_disconnect(client: client_mqtt, userdata, rc: int):
    if rc == 0:
        print("Disconnected")
    else:
        print("Disconnected, result code: " + str(rc))
    # client.loop_stop()


def on_message(client: client_mqtt, userdata, msg):
    payload = str(msg.payload.decode())
    info = "[topic " + msg.topic + "; qos " + str(msg.qos) + "] payload -> " + payload
    print("[DEBUG] " + info)

    sets.received_message['topic'] = msg.topic
    sets.received_message['payload'] = payload
    sets.flag = True


# MQTT Publish function
def mqtt_publish(client: client_mqtt, topic: str, msg: str, qos: int = 0):
    result = client.publish(topic=topic, payload=msg, qos=qos)
    result.wait_for_publish()
    status = result[0]
    if status == 0:
        print("[DEBUG] msg was sent ✅")
    else:
        print("[DEBUG] failed to send message ❌")


# MQTT Subscribe function
def mqtt_subscribe(client: client_mqtt, topic: str, qos: int = 2):
    client.subscribe(topic=topic, qos=qos)
    client.on_message = on_message


# MQTT Unsubscribe function
def mqtt_unsubscribe(client: client_mqtt, topic: str):
    client.unsubscribe(topic=topic)
