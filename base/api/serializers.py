from rest_framework.serializers import ModelSerializer
from base.models import Parishe,Countie,Address

class ParishSerializer(ModelSerializer):
    class Meta:
        model=Parishe
        fields='__all__'

class CountySerializer(ModelSerializer):
    class Meta:
        model=Countie
        fields='__all__'

class AddressSerializer(ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'