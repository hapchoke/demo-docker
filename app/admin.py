from django.contrib import admin
from .models import Item,OrderItem,Order,Address,Category


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered',
                    'being_delivered',
                    'received',
                    'address',
                    ]
    list_display_links = [
        'user',
        'address',
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',]
    search_fields = [
        'user__username',
        'ref_code'
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'prefecture',
        'street_address',
        'apartment_address',
        'zip',
        'default'
    ]
    list_filter = [ 'default']
    search_fields = ['user', 'prefecture', 'street_address', 'apartment_address', 'zip']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Category)