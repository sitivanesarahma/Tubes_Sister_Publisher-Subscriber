import paho.mqtt.client as mqtt
import time

data = []

def on_message(client, userdata, message):
    payload_str = message.payload.decode('utf-8')
    payload_numeric = float(payload_str)
    data.append({
        'topic': message.topic,
        'value':payload_numeric
    })

    print(message.topic + " = " + payload_str)

broker_address = "mqtt.eclipseprojects.io"
client = mqtt.Client("subscriber")

# Hubungkan client ke broker
client.connect(broker_address, port=1883)

# Kaitkan fungsi callback
client.on_message = on_message

# Mulai loop client
client.loop_start()

# Subscriber akan menerima data dan menghitung rata-rata setiap 10 detik
try:
    while True:
        # Subscribe to topics
        client.subscribe("info_sensor1")
        client.subscribe("info_sensor2")
        client.subscribe("info_sensor3")
        time.sleep(5)
        if data:
            total_suhu = sum(data['value'] for data in data)
            hasil = total_suhu / len(data)
            print("Rata-rata Suhu Bandung saat ini:", hasil, "Celcius")
            print(" ")
            data.clear()

except KeyboardInterrupt:
    # Hentikan loop MQTT
    client.loop_stop()
