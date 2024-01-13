from paho.mqtt import client as mqtt_client
import random
import os
import pickle
import time

phoneList = ['192.168.199.204']

broker = '192.168.1.1'
port = 1883
haConfigTopic = "homeassistant/switch/leaveCheck1/config"
haConfig = '{ "unique_id": "%s", "name": "%s", "state_topic": "home/%s/state", "command_topic": "home/%s/set", ' \
           '"payload_on": "ON", "payload_off": "OFF" }' % (
               'leaveCheck1', '离家检测器', 'leaveCheck1', 'leaveCheck1')

haStateTopic = 'home/%s/state' % 'leaveCheck1'
haSetTopic = 'home/%s/set' % 'leaveCheck1'

client_id = 'python-mqtt-{' + str(random.randint(0, 1000)) + '}'


def exec(cmd: str):
    return os.popen(cmd)


def save(status):
    with open('/tmp/leaveCheck1.status', 'wb') as fp:
        pickle.dump(status, fp)


def read() -> bool:
    with open('/tmp/leaveCheck1.status', 'rb') as fp:
        return pickle.load(fp)


def connectMqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def homeAssistantReg(client):
    client.publish(haConfigTopic, haConfig)


def checkPhoneExist(phone: str):
    resp = exec("arping -c 5 -f %s" % phone)
    lines = resp.readlines()
    # return lines[-1].find('已接受到 1 个响应') >= 0
    return lines[-1].find('Received 1 response') >= 0


def checkPhoneExists():
    for phone in phoneList:
        if checkPhoneExist(phone):
            save(True)
            return True
    save(False)
    return False


def run():
    client = connectMqtt()
    homeAssistantReg(client)
    if not os.path.exists('/tmp/leaveCheck1.status'):
        print('init.')
        exec('touch /tmp/leaveCheck1.status')
        time.sleep(0.5)
        save(True)
        time.sleep(0.1)
    lastStatus = read()
    if not checkPhoneExists() and not lastStatus:
        print('ON')
        client.publish(haStateTopic, 'ON')
    else:
        print('OFF')
        client.publish(haStateTopic, 'OFF')


if __name__ == '__main__':
    run()
