from .models import Hotel, HotelOwner
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class HotelService:
    
    @staticmethod
    def get_all_hotels():
        return Hotel.objects.all()
    

    @staticmethod
    def get_hotel_by_id(hotel_id):
        return Hotel.objects.filter(id=hotel_id).first()
    

    @staticmethod
    def get_hotel_by_name(hotel_name):
        return Hotel.objects.filter(name=hotel_name).first()


    @staticmethod
    def create_hotel(data):
        owner = HotelOwner.objects.get(id=data['owner_id'])
        return Hotel.objects.create(
            owner=owner,
            name=data['name'],
            location=data['location'],
            capacity=data['capacity']
        )
    
    
    @staticmethod
    def archive_or_delete_hotel(hotel_id):
        response = {}
        
        hotel = HotelService.get_hotel_by_id(hotel_id)
        if hotel == None:
            return {"error": "Hotel not found"}  
        
        if HotelService.check_has_recent_bookings(hotel_id) == True:
            Hotel.objects.filter(id=hotel_id).update(archived_at=timezone.now())
            response = {"status": "archived", "message": "Hotel archived due to recent bookings."}
        else:
            hotel.delete()
            response = {"status": "deleted"}
            
        return response
    

    @staticmethod
    def check_has_recent_bookings(hotel_id):
        """Returns True if the hotel has bookings from the last 3 years."""
            
        booking_age_limit = settings.BOOKING_AGE_LIMIT_DAYS   # settings.py tendría:  BOOKING_AGE_LIMIT_DAYS = 3 * 365
        three_years_ago = timezone.now() - timedelta(days=booking_age_limit)
        
        return Booking.objects.filter(
            hotel_id=hotel_id, 
            created_at__gt=three_years_ago  # created at greater than three_years_ago
        ).exists()
            
            
    @staticmethod
    def delete_old_archived():
        '''Admin can delete archivde hotels with more than 3 years'''
        
        booking_age_limit = settings.BOOKING_AGE_LIMIT_DAYS   # settings.py tendría:  BOOKING_AGE_LIMIT_DAYS = 3 * 365
        three_years_ago = timezone.now() - timedelta(days=booking_age_limit)

        # Buscar hoteles archivados que no tengan bookings en los últimos 3 años
        hotels_to_delete = Hotel.objects.filter(
            archived__isnull=False  # Solo archivados
        ).exclude(
            bookings__created_at__gt=three_years_ago  # Si tiene bookings recientes, no se borra
        )

        hotels_to_delete.delete()

        # Repetir para rooms, roomtypes, owners y customers

    
    # ...
        