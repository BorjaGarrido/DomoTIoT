from django.contrib import admin

# Register your models here.

from .models import Modulo, dht, rfid, mq2, ldr, led, puerta

admin.site.register(dht)
admin.site.register(rfid)
admin.site.register(mq2)
admin.site.register(ldr)
admin.site.register(led)
admin.site.register(puerta)