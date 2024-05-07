import json
import time
import paho.mqtt.client as mqtt
from temp_sensor_class import SensorReader
from sense_hat import SenseHat

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def main():
    # Initialize SensorReader
    sensor_reader = SensorReader()
    sensehat = SenseHat()

    
    # Initialize MQTT client
    print("init MQTT")
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    #mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.connect("35.240.151.148", 1883)
    mqtt_client.loop_start()
    print("Starting Main Loop")
    
    
    while True:
        # Read temperature and humidity
        temp = None
        humidity = None
        
        if sensor_reader.ser is None:
            sensor_reader.retry_serial_connection()
        else:
            temp = sensor_reader.get_temp()
            humidity = sensor_reader.get_humidity()
        
        
        if temp is None or humidity is None: #Change source to sensehat if needed
            temp = sensehat.get_temperature_from_humidity()
            humidity = sensehat.get_humidity()
        
        
        # Construct JSON payload
        payload = {
            "temperature": temp,
            "humidity": humidity
        }
        

        
        # Publish payload to MQTT topic
        ret = mqtt_client.publish("/1234/EnvironmentalSensor002/attrs", json.dumps(payload))
        print(payload)
        print("Ret: " , ret)
        # Wait for some time before reading again
        time.sleep(5)  # Adjust the interval as needed
        
        #Test sensehat
        temp = sensehat.get_temperature_from_humidity()
        humidity = sensehat.get_humidity()
        print("")
        print("From sensehat - Temp: ", temp , "   Humdidity: ", humidity)

# Run the main function
if __name__ == "__main__":
    main()
