from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    owner = models.ForeignKey(HotelOwner, on_delete=models.CASCADE, related_name="hotels")
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    is_archived = models.BooleanField()

    def __str__(self):
        return self.name

# A lo mejor tenemos que añadir una para habitación por ejemplo. Depende de su uso, podemos definirla aquí o deberíamos separarla en un paquete nuevo.