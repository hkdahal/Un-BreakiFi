from django.contrib import admin
from .models import Vendor, Transaction, Individual


admin.site.register(Vendor)
admin.site.register(Transaction)
admin.site.register(Individual)
