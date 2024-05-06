import serial
import time
import json
import paho.mqtt.client as paho
from paho import mqtt

# MQTT settings
mqtt_host = "XXXXXXXXXXXXXXXXXXXXXXXX.XX.XX.hivemq.cloud"  # replace with your HiveMQ
mqtt_port = 8883  # 8884 websocket
topic = "generic/location/sensor"  # replace with your topic
userMQ = "Testing"   # Go to access-management and create new user/device in HiveMQ
passMQ = "Testing123"

# Adjust the port and parameters as needed
ser = serial.Serial('COM11', 9600, timeout=1)

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
 
    
# paho V2 reqirement need declare API version, while HiveMQ using MQTT V5    
client = paho.Client(paho.CallbackAPIVersion.VERSION2,client_id="", userdata=None, protocol=paho.MQTTv5) 
client.on_connect = on_connect
# Enable TLS for secure connection, HiveMQ requirement
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# Set username and password 
client.username_pw_set(userMQ, passMQ) 
# Connect to the broker
client.connect(mqtt_host, mqtt_port)
# Start the loop
client.loop_start()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        line_arry= line.split(";") # We spilt using ;
        # Example data come in COM
        # Hello;123;35.255;60.27;Test  
        # Create a dictionary with the data (example JSON with 5 data)
        data = {
            "Location_ID": line_arry[0],#Hello
            "Location_Name": line_arry[1], #123
            "Dispenser_Code": line_arry[2], #35.255
            "Dispenser_Name": line_arry[3], #60.27
            "Log_Temperature": line_arry[4] #Test
        }
        
        # Convert the dictionary to a JSON string
        payload = json.dumps(data)
        
        try:
            print(f"Writing Payload = {payload} to host: {mqtt_host}")
            msg_info = client.publish(topic, payload, qos=1 )
            if msg_info.is_published() == False:
                print('Message is not yet published.')

            msg_info.wait_for_publish()
            print("Success sending data!")
            print(f"Send `{payload}` to topic `{topic}`")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("An error occurred: ", str(e))
        time.sleep(5)  # Pause for 5 second (asume limit rate)
