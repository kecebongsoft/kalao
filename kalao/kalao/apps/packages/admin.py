from django.contrib import admin
from core.admin import BaseAdmin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from .models import Package, PackageBatch, Remark, PackageHotel

class PackageBatchInline(admin.TabularInline):
    model = PackageBatch
    extra = 1
    exclude = ('created_by', 'modified_by')

class RemarkInline(admin.TabularInline):
    model = Remark
    extra = 1
    exclude = ('created_by', 'modified_by')

class PackageHotelInline(admin.TabularInline):
    model = PackageHotel
    extra = 1
    exclude = ('created_by', 'modified_by')

class PackageAdmin(BaseAdmin, admin.ModelAdmin):
    list_filter = ('package_hotels__hotel',  'created_by', 'modified_by')
    search_fields = ('name',)
    list_display = ('name',  'markup_amount', 'date_modified', 'created_by', 'modified_by')
    exclude = ('created_by', 'modified_by')

    inlines = (PackageBatchInline, PackageHotelInline, RemarkInline)

    def bulk_table(self, request, queryset):
        pks = [str(q.pk) for q in queryset]
        url = "%s?%s" % (reverse("packages:table", args=[0]), "pks=%s" % ','.join(pks))
        return redirect(url)

    bulk_table.short_description = "View selected packages calculation"

    actions = [bulk_table, ]

admin.site.register(Package, PackageAdmin)
