import serial
import time
import serial.tools.list_ports

class SensorReader:
    def __init__(self):
        
        ports = serial.tools.list_ports.comports()
        device_name = "/dev/ttyUSB0"
        for port in ports:
            try:
                self.ser = serial.Serial(port.device, baudrate=9600, timeout=1.0)
                print("Serial port found:", port.device)
                device_name = port.device
                break
            except serial.SerialException:
                continue
        else:
            print("No serial port available. Please check your connections.")

        self.ser = serial.Serial(port=device_name, baudrate=9600, timeout=1.0) # Remember, you might need to replace '/dev/ttyUSB0' with the port name where your USB to RS485 converter is connected
        self.temp_ref_frame = [0x01, 0x04, 0x00, 0x01, 0x00, 0x01, 0x60, 0x0a] # Request frame for temp sensor
        self.humid_ref_frame = [0x01, 0x04, 0x00, 0x02, 0x00, 0x01, 0x90, 0x0a] # Request frame for humidity sensor


    def get_temp(self):
        if self.ser is None:
            print("Serial port is not initialized. Call find_serial_port() first.")
            return None

        print("Fetching temperature...")
        self.ser.write(bytes(self.temp_ref_frame))
        time.sleep(1)
        buf = self.ser.read(7)
        print("Received data:", buf)
        if buf:
            temp_value = (buf[3] << 8) | buf[4]
            temperature = temp_value / 10.0
            return temperature
        else:
            return None

    def get_humidity(self):
        if self.ser is None:
            print("Serial port is not initialized. Call find_serial_port() first.")
            return None

        print("Fetching humidity...")
        self.ser.write(bytes(self.humid_ref_frame))
        time.sleep(1)
        buf = self.ser.read(7)
        print("Received data:", buf)
        if buf:
            humid_value = (buf[3] << 8) | buf[4]
            humidity = humid_value / 10.0
            return humidity
        else:
            return None

# Example usage:
'''
sensor_reader = SensorReader()
temp = sensor_reader.get_temp()
humidity = sensor_reader.get_humidity()
print("Temperature:", temp)
print("Humidity:", humidity)
'''
