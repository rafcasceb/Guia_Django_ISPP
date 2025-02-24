from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import Hotel



class HotelViewSetTests:

    def setup_method(self):  # Recordad que el setup es para algunos objetos comunes que necesitemos para todos o la inmensa mayoría de los tests.
        self.client = APIClient()

        # Hotel de ejemplo para hacer pruebas
        self.hotel = Hotel.objects.create(
            name="Hotel Test",
            city="Test City",
            rating=5,
            price_per_night=100
        )
        
        self.url = reverse('hotel-list')  # La URL del listado es la URL base
        self.detail_url = reverse('hotel-detail', kwargs={'pk': self.hotel.pk})


    def test_list_hotels(self):
        """Test para obtener todos los hoteles"""
        
        response = self.client.get(self.url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0 


    def test_retrieve_hotel(self):
        """Test para obtener un hotel por ID"""
        response = self.client.get(self.detail_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == self.hotel.name


    def test_create_hotel(self):
        """Test para crear un nuevo hotel"""
        
        hotel_data = {
            'name': "Hotel New",
            'city': "New City",
            'rating': 4,
            'price_per_night': 80
        }
        response = self.client.post(self.url, hotel_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == hotel_data['name']
        assert Hotel.objects.count() == 2


    def test_delete_hotel(self):
        """Test para eliminar un hotel"""
        
        response = self.client.delete(self.detail_url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Hotel.objects.count() == 0


    def test_filter_hotels(self):
        """Test para filtrar hoteles por parámetros"""
        
        Hotel.objects.create(name="Hotel 1", city="Valencia", rating=5, price_per_night=150)
        Hotel.objects.create(name="Hotel 2", city="Sevilla", rating=3, price_per_night=80)

        # Filtro por nombre
        response = self.client.get(self.url + "?name=Hotel_1")  # No valen espacios en la URL
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1 

        # Filtro por ciudad
        response = self.client.get(self.url + "?city=Valencia")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

        # Filtro por precio
        response = self.client.get(self.url + "?price_per_night=150")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
