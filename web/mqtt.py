from .models import Modulo, UserProfile, dht, rfid, mq2, ldr, puerta, led
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import paho.mqtt.client as mqtt

def on_message_dht(mosq, obj, msg, sensor_id):
    # This callback will only be called for messages with topics that match
    # $SYS/broker/bytes/#

    member = request.user.userprofile

    sensor = member.dht.get(pk=sensor_id)

    men = str(msg.payload)
    men = men.replace("'", "")
    men = men.replace("b", "")
    men = men.replace("Hum", "")
    men = men.replace("Temp", "")
    men = men.split(" ")

    sensor.temperatura = float(men[1])
    sensor.humedad = float(men[3])

    sensores.save()
    member.dht.add(sensor)

    return render(request, 'web/dht_mqtt.html')

mqttc = mqtt.Client()

# Add message callbacks that will only trigger on a specific subscription match.
mqttc.message_callback_add("casa/temperatura", on_message_dht)

mqttc.connect("192.168.1.143", 1883, 60)
mqttc.subscribe("casa/#", 0)
