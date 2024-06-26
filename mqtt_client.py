import paho.mqtt.client as mqtt
import json

#FILE NOt USED

class MQTTClient:
    def __init__(self):
        self.connect()
        self.client.loop_start()
        '''
    def on_publish(self, client, userdata, mid, reason_codes, properties):
        print("Message published: {mid}")
        '''
    def on_publish(self, client, userdata, mid):
        print("Message published: {mid}")
        
    def publish(self, json_object):
        ret = self.client.publish(self.topic, json.dumps(json_object))
        print("Ret: " ret)

    def reconnect(self):
        self.client.disconnect()
        self.connect()

    def is_connection_active(self):
        return self.client.is_connected()
        
        '''
    def on_connect (self , client, userdata ,flags , reason_code,properties)
        return
        '''


    def connect(self):
        # Specify the path to your JSON file
        json_file_path = '/home/admin/Pi-Sensor-Hub-with-Facial-Recognition/SettingsPage/UserPrefs.json'

        # Open the JSON file for reading
        with open(json_file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)
        
        broker = data['mqttSettings']['broker']
        port = data['mqttSettings']['port']
        self.topic = "/1234/EnvironmentalSensor002/attrs"

        self.client = mqtt.Client()
        self.client.on_publish = self.on_publish
        #self.client.on_connect = self.on_connect
        self.client.connect(broker , port, 60)
