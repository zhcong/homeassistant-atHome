# homeassistant-atHome
check at home status with arp ping and mqtt in homeassistant. principle are follows:

![principle](/principle.png)

you should create a crontab with linux service. 
```crontab
*  *  *  *  * /usr/bin/python3 /opt/atHome.py
```
and follow those step:  
<b>1</b> change ip of your phone.
```python
phoneList = ['192.168.1.204']
```
<b>2</b> change mqtt service address.
```python
broker = '192.168.1.1'
port = 1883
```
<b>3</b> change mqtt topic.
```python
haConfigTopic = "homeassistant/switch/leaveCheck1/config"
haConfig = '{ "unique_id": "%s", "name": "%s", "state_topic": "home/%s/state", "command_topic": "home/%s/set", ' \
           '"payload_on": "ON", "payload_off": "OFF" }' % (
               'leaveCheck1', '离家检测器', 'leaveCheck1', 'leaveCheck1')

haStateTopic = 'home/%s/state' % 'leaveCheck1'
haSetTopic = 'home/%s/set' % 'leaveCheck1'
```
it works perfect.
![work](/work.png)
