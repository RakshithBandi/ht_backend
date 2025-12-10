from django.contrib import admin
from .models import Expenditure


@admin.register(Expenditure)
class ExpenditureAdmin(admin.ModelAdmin):
    list_display = ('year', 'purpose_short', 'amountSpent', 'createdAt')
    list_filter = ('year', 'createdAt')
    search_fields = ('year', 'purpose')
    ordering = ('-createdAt',)
    readonly_fields = ('createdAt', 'updatedAt')

    def purpose_short(self, obj):
        return obj.purpose[:50] + '...' if len(obj.purpose) > 50 else obj.purpose
    purpose_short.short_description = 'Purpose'
