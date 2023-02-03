from django.contrib import admin
from .models import Countie,Parishe,Address
from django.contrib.auth import get_user_model
from base import models

from import_export import resources
from .models import Address
from import_export.admin import ImportExportModelAdmin
from django.dispatch import receiver
from import_export.signals import post_import, post_export

class AddressResource(resources.ModelResource):
    class Meta:
        model=Address
        skip_unchanged = True
        report_skipped = False
        import_id_fields = ('id',)
        fields = ('id','address',
'post_code',
'latitude',
'longitude',
'source',
'comm_poij',
'category',
'dev_area',
'parish',
'comm_sdc',
'settlement',
'name')

class addressAdmin(ImportExportModelAdmin):
    resource_classes = [AddressResource]

user=get_user_model()
# Register your models here.
admin.site.register(Countie)
admin.site.register(Parishe)
# admin.site.register(Address)
admin.site.register(user)
# admin.site.register(models.ResourceRouter)
admin.site.register(Address, addressAdmin)


