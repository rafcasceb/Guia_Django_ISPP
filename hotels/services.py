from .models import Hotel, HotelOwner


class HotelService:
    @staticmethod
    def get_all_hotels():
        return Hotel.objects.all()
    
    @staticmethod
    def get_hotel_by_id(hotel_id):
        return Hotel.objects.filter(id=hotel_id).first()
    
    @staticmethod
    def get_hotel_by_id(hotel_name):
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
        
    # ...
        