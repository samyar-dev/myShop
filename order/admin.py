from django.contrib import admin
from .models import *
from django.http import HttpResponse
import openpyxl

# Register your models here.

def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreedsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=orders.xlsx'
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Orders'
    coulmn = ['ID', 'First Name', 'Last Name', 'Phone', 'Paid', 'Address', 'Created']
    ws.append(coulmn)

    for order in queryset:
        created = order.created.replace(tzinfo=None) if order.created else ''
        ws.append([
            order.id, order.first_name, order.last_name, order.phone,
            order.paid, str(order.order_address), created
        ])
    wb.save(response)
    return response


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 1
    raw_id_fields: list = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'created', 'paid', 'status']
    list_filter = ['paid', 'created', 'updated']
    list_editable = ['paid', 'status']
    inlines = [OrderItemInline]
    autocomplete_fields = ['address']
    actions = [export_to_excel]