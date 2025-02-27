from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import HotelSerializer
from .services import HotelService


class HotelViewSet(viewsets.ViewSet):
    
    # --------------
    # MÉTODOS RESERVADOS
    # --------------
    
    def list(self, request):  # GET /hotels/
        """Devuelve la lista de todos los hoteles"""
        hotels = HotelService.get_all_hotels()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):  # GET /hotels/{id}/
        """Devuelve un solo hotel por ID"""
        hotel = HotelService.get_hotel_by_id(pk)
        if hotel:
            serializer = HotelSerializer(hotel)
            return Response(serializer.data)
        return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)


    def create(self, request):  # POST /hotels/
        """Crea un nuevo hotel"""
        hotel = HotelService.create_hotel(request.data)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk=None):  # DELETE /hotels/{id}/
        """Elimina un hotel por ID"""
        hotel = HotelService.get_hotel_by_id(pk)
        if hotel:
            hotel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    # --------------
    # RUTAS PERSONALIZADAS SIMPLES
    # --------------
    
    # Si no ponemos detail, no espera un id (pk)
    @action(detail=False, methods=['get'], url_path="cities", url_name="get_all_cities")  # GET /hotels/cities
    def get_all_cities(self, request):
        """Find all cities"""
        cities = HotelService.get_all_cities()
        if cities:
            serializer = CitySerializer(cities, many=True)
            return Response(serializer.data)
        return Response({"error": "Cities not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    # Si ponemos detail, espera un id (pk) tras la ruta base
    @action(detail=True, methods=['get'], url_path="name", url_name="get_name_by_hotel_id")  # GET /hotels/{id}/name
    def get_name_by_hotel_id(self, request, pk=None):
        """Find name by hotel id"""
        name = HotelService.get_name_by_hotel_id(pk)
        if name:
            serializer = NameSerializer(name)  # Ahora mismo es solo un campo, así que no se consideraría mal no usar el serializador y poner directamente:  return Response({"name": name})
            return Response(serializer.data)
        return Response({"error": "Hotel not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    # --------------
    # PATH PARAMS (MÁS ALLÁ DEL ID)
    # --------------
    
    @action(detail=False, methods=['get'], url_path="city-summary/(?P<city>[\w\s-]+)", url_name="get_summary_by_city")  # GET /hotels/city-summary/{city}
    def get_summary_by_city(self, request, city=None):
        """Find city summary by city name"""
        city_summary = HotelService.get_city_summary_by_city(city)
        if city_summary:
            serializer = CitySummarySerializer(city_summary)
            return Response(serializer.data)
        return Response({"error": "City summary not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    # --------------
    # QUERY PARAMS
    # --------------
    
    @action(detail=False, methods=['get'], url_path="filter", url_name="filter")  # GET /hotels/filter?name={name}&city={city}
    def filter_hotels(self, request):
        """Filter hotels by allow fields"""
        
        allowed_fields = {"name", "city", "rating", "price_per_night"}  # Campos que permitimos filtrar
        # Podríamos hacer: 
        # from django.conf import settings
        # allowed_fields = getattr(settings, "FILTERABLE_HOTEL_FIELDS", set())
        # Y en settings.py tener:  FILTERABLE_HOTEL_FIELDS = {"name", "city", "rating", "price_per_night"}
        
        # A lo mejor no vale esta estrategia con foreign keys. 
        
        filters = {
            key: value for key, value in request.query_params.items() if key in allowed_fields and value
        }

        if not filters:
            return Response({"error": f"Invalid filters. Allowed: {', '.join(allowed_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        hotels = HotelService.filter_hotels(**filters)

        if hotels.exists():
            serializer = HotelSerializer(hotels, many=True)
            return Response(serializer.data)
        
        return Response({"error": "No hotels found with the given filters"}, status=status.HTTP_404_NOT_FOUND)
