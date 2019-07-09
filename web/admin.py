from django.contrib import admin

# Register your models here.

from .models import Modulo, UserProfile, dht, rfid, mq2, ldr, puerta, led

admin.site.register(Modulo)
admin.site.register(UserProfile)
admin.site.register(dht)
admin.site.register(rfid)
admin.site.register(mq2)
admin.site.register(ldr)
admin.site.register(puerta)
admin.site.register(led)
