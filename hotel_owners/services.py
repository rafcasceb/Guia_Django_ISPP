from rest_framework.response import Response
from rest_framework import status
from .models import Hotel, HotelOwner
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class HotelOwnerService:

    @staticmethod
    def authorize_update_hotel_owner(request, pk):
        hotel_owner = HotelOwnerService.get_hotel_owner_by_id(pk)
        # permissions = [isAppAdmin, isHotelOwner]
        
        if not hotel_owner:
            raise NotFound("HotelOwner not found.")
        if not hotel_owner.is_active():
            raise PermissionDenied("HotelOwner is archived.")
        # In the future, also check that user making the request is active and is admin or the hotel owner being edited.
    
    
    @staticmethod
    def serialize_input_update_hotel_owner(request, pk):
        context = {"request": request}

        input_serializer = HotelOwnerSerializer(data=request.data, context=context)
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)
        
        return input_serializer

    
    @staticmethod
    def validate_semantically_update_hotel_owner(pk, input_serializer):
        # Add here semantic validations if needed using input_serializer.data I think
        valid = True
        errors = {}
        
        if not valid:
            raise ValidationError(errors)


    @staticmethod
    def update_hotel_owner(pk, input_serializer):
        hotel_owner = HotelOwnerService.get_hotel_owner_by_id(pk)
        for attr, value in input_serializer.validated_data.items():
            setattr(hotel_owner, attr, value)
        hotel_owner.save()
        return hotel_owner


    @staticmethod
    def serialize_output_hotel_owner(updated_hotel_owner):
        serializer = HotelOwnerSerializer(updated_hotel_owner)
        return serializer.data
    