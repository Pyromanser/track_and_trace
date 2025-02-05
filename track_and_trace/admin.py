from django.contrib import admin

from track_and_trace.models import Address, Carrier, Shipment, Product, Article

admin.site.register(Address)
admin.site.register(Carrier)
admin.site.register(Shipment)
admin.site.register(Product)
admin.site.register(Article)
