from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import HotelSerializer
from .services import HotelOwnerService, HotelService
from django.http import JsonResponse


class HotelOwnerViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):  # GET /hotels/{id}/
        hotel_owner = HotelOwnerService.get_hotel_owner_by_id(pk)
        
        if not hotel_owner:
            return Response({"error": "HotelOwner not found."}, status=status.HTTP_404_NOT_FOUND)
        if not hotel_owner.is_active():
            return Response({"error": "HotelOwner is archived."}, status=status.HTTP_404_NOT_FOUND) 
        # In the future, also check that user making the request admin or the hotel_owner being edited.
        
        serializer = HotelSerializer(hotel_owner)
        return Response(serializer.data, status=status.HTTP_200_OK)



   
    def update1(self, request, pk=None):
        context = {"request": request}
        hotel_owner = HotelOwnerService.get_hotel_owner_by_id(pk)
        
        # AUTORIZAR
        HotelOwnerService.check_if_hotel_owner_exits(hotel_owner)
        HotelOwnerService.check_if_hotel_owner_archived(hotel_owner)
        # In the future, also check that user making the request is active and is admin or the hotel owner being edited.
        
        # VALIDAR SINTÁCTICAMENTE Y ADAPTAR DATOS
        input_serializer = HotelOwnerSerializer(data=request.data, context=context)
        if not input_serializer.is_valid():
            raise ValidationError(input_serializer.errors)  # o return no sé
            
        # VALIDAR SEMÁNTICAMENTE
        # ... (si hacen falta, ver en cada caso)
        
        # REALIZAR ACCIÓN
        hotel_owner_updated = HotelOwnerService.update_hotel_owner(pk, input_serializer)
        
        # DEVOLVER RESPUESTA
        output_serializer_data = HotelOwnerSerializer(hotel_owner_updated).data
        return Response(output_serializer_data, status=status.HTTP_200_OK)


    def update2(self, request, pk=None):
        authorized, errors = HotelOwnerService.authorize_update_hotel_owner(request, pk)  # errors dictionary like above?
        if not authorized:
            return Response(errors, status=status.HTTP_403_FORBIDDEN)
        
        input_serializer, errors = HotelOwnerService.unbind_input_update_hotel_owner(request, pk)  # applies serializer and if it's valid, convert into object
        if not input_serializer:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        validated, errors = HotelOwnerService.validate_semantically_update_hotel_owner(pk, input_serializer)
        if not validated:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        hotel_owner_updated = HotelOwnerService.update_hotel_owner(pk, input_serializer)
        
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(hotel_owner_updated).data  # applies serializer to object to be returned.
        return Response(output_serializer_data, status=status.HTTP_200_OK)
  
  
    def update3(self, request, pk=None):
        HotelOwnerService.authorize_update_hotel_owner(request, pk)
        input_serializer = HotelOwnerService.serialize_input_hotel_owner(request, pk)
        HotelOwnerService.validate_semantically_update_hotel_owner(pk, input_serializer)
        hotel_owner_updated = HotelOwnerService.update_hotel_owner(pk, input_serializer)
        output_serializer_data = HotelOwnerService.serialize_output_hotel_owner(hotel_owner_updated)
        return Response(output_serializer_data, status=status.HTTP_200_OK)
  