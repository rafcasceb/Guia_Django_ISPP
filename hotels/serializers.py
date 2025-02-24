from rest_framework import serializers
from .models import Hotel, HotelOwner


class HotelSerializer(serializers.ModelSerializer):
    owner = HotelOwnerSerializer(read_only=True)  # To fully return the HotelOwner object in the attribute 'owner'.

    class Meta:
        model = Hotel
        fields = '__all__'



# ...
