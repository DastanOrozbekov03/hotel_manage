from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone



class Hotel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за ночь
    tags = models.CharField(max_length=100)  # Тэги
    description = models.TextField()  # Описание
    photo = models.ImageField(upload_to='hotel_photos/')  # Фотография отеля
    stars = models.PositiveIntegerField(default=0)

    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за ночь

    def __str__(self):
        return f"{self.number} ({self.hotel.name})"


class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.hotel.name}"


class Booking(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)  # Ссылка на номер, а не на отель
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    

    def __str__(self):
        return f"{self.hotel.number} ({self.hotel.hotel.name}) - {self.user.username}"


class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')


class FavoriteHotel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'hotel')

    def __str__(self):
        return f"{self.hotel.name} - {self.user.username}"


class HotelLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hotel')