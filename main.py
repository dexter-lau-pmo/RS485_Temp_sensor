import json
import time
import paho.mqtt.client as mqtt
from temp_sensor_class import SensorReader

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def main():
    # Initialize SensorReader
    sensor_reader = SensorReader()
    
    # Initialize MQTT client
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    mqtt_client.on_connect = on_connect
    mqtt_client.connect("35.240.151.148", 1883)
    mqtt_client.loop_start()
    
    while True:
        # Read temperature and humidity
        temp = sensor_reader.get_temp()
        humidity = sensor_reader.get_humidity()
        print("Temperature:", temp)
        print("Humidity:", humidity)
        
        # Construct JSON payload
        payload = {
            "temperature": temp,
            "humidity": humidity
        }
        
        # Publish payload to MQTT topic
        mqtt_client.publish("/1234/EnvironmentalSensor002/attrs", json.dumps(payload))
        
        # Wait for some time before reading again
        time.sleep(5)  # Adjust the interval as needed

# Run the main function
if __name__ == "__main__":
    main()
