from import_export import resources
from .models import Address

class AddressResource(resources.ModelResource):
    class Meta:
        model=Address