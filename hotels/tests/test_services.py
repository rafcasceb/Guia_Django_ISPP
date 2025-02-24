from ..services import HotelService
from ..models import Hotel



def test_hotel_creation():
    hotel = Hotel.objects.create(name="Hotel 1", city="Valencia", rating=5, price_per_night=150)
    assert hotel.name == "Hotel 1"
    assert hotel.city == "Valencia"
    
    

def test_get_hotel_by_name():
    """Prueba para obtener hotel por nombre"""
    hotel = Hotel.objects.create(name="Hotel Test", city="Test City", rating=5, price_per_night=100)
    result = HotelService.get_hotel_by_name("Hotel Test")
    assert result == hotel

def test_create_hotel():
    """Prueba para crear un hotel"""
    data = {'name': 'New Hotel', 'city': 'New City', 'rating': 4, 'price_per_night': 80}
    hotel = HotelService.create_hotel(data)
    assert hotel.name == 'New Hotel'
    assert hotel.city == 'New City'
