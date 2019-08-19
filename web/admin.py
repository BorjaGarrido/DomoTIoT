from django.contrib import admin

# Register your models here.

from .models import Modulo, UserProfile
from .models import dht, rfid, mq2, ldr, puerta, led
from .models import registroDHT, incidenciaDHT
from .models import registroMQ2, incidenciaMQ2, registroRFID

admin.site.register(Modulo)
admin.site.register(UserProfile)
admin.site.register(dht)
admin.site.register(rfid)
admin.site.register(mq2)
admin.site.register(ldr)
admin.site.register(puerta)
admin.site.register(led)
admin.site.register(registroDHT)
admin.site.register(incidenciaDHT)
admin.site.register(registroMQ2)
admin.site.register(incidenciaMQ2)
admin.site.register(registroRFID)
