from paho.mqtt import client as mqtt_client
from env import MQTT_PORT, MQTT_HOST, MQTT_PASSWORD, MQTT_USERNAME, MQTT_CLIENT_ID


# Configuration functions of MQTT
def on_connect(client: mqtt_client, userdata, flags, rc: int):
    if rc == 0:
        print("Connected")
    else:
        print("Failed to connect, return code %d\n", rc)
    # client.loop_start()


def on_disconnect(client: mqtt_client, userdata, rc: int):
    if rc == 0:
        print("Disconnected")
    else:
        print("Disconnected, result code: " + str(rc))
    # client.loop_stop()


def on_message(client: mqtt_client, userdata, msg) -> str:
    payload = str(msg.payload.decode())
    print("[topic " + msg.topic + "; qos " + str(msg.qos) + "] payload -> " + payload)
    return payload


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(MQTT_HOST, int(MQTT_PORT))
    return client


# MQTT Publish function
def publish(client: mqtt_client, topic: str, msg: str, qos: int = 0):
    result = client.publish(topic, msg, qos=qos)
    result.wait_for_publish()
    status = result[0]
    if status == 0:
        print("[DEBUG] msg was sent ✅")
    else:
        print("[DEBUG] failed to send message ❌")


# MQTT Subscribe function
def subscribe(client: mqtt_client, topic: str):
    client.subscribe(topic)
    client.on_message = on_message


# MQTT Unsubscribe function
def unsubscribe(client: mqtt_client, topic: str):
    client.unsubscribe(topic)


# MQTT PUB SUB UNSUB functions
def mqtt_pub(topic: str, msg: str):
    client = connect_mqtt()
    # client.loop_start()
    publish(client=client, topic=topic, msg=msg)
    # client.loop_stop()


def mqtt_sub(topic: str):
    client = connect_mqtt()
    subscribe(client=client, topic=topic)
    # client.loop_forever()
    client.loop_start()


# ???
def mqtt_unsub(topic: str):
    client = connect_mqtt()
    unsubscribe(client=client, topic=topic)
    # client.loop_forever()
    client.loop_stop()


# if __name__ == '__main__':
#     mqtt_pub('/test', 'hello from paho client)')
