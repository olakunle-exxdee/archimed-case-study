from django.contrib import admin

from invoice.models import Bill, CapitalCall, Investment, Investor

admin.site.register(Investor)
admin.site.register(Investment)
admin.site.register(Bill)
admin.site.register(CapitalCall)
