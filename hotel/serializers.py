from rest_framework import serializers
from .models import *



class HotelSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)
    photo = serializers.ImageField(required=False)  

    class Meta:
        model = Hotel
        fields = ['id', 'owner', 'name', 'phone_number', 'price', 'tags', 'description', 'photo', 'stars', 'like_count']

    def create(self, validated_data):
        photo = validated_data.pop('photo', None)  
        instance = super().create(validated_data)
        if photo:
            instance.photo = photo  
            instance.save()
        return instance

    def update(self, instance, validated_data):
        photo = validated_data.pop('photo', None) 
        instance = super().update(instance, validated_data)
        if photo:
            instance.photo = photo  
            instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'hotel', 'number', 'price']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'hotel', 'user', 'rating', 'comment', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'hotel', 'user', 'check_in_date', 'check_out_date']

class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = ['id', 'review', 'user', 'created_at']

class FavoriteHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteHotel
        fields = ['id', 'user', 'hotel']

class HotelLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLike
        fields = ['id', 'user', 'hotel', 'created_at']

class BookingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingHistory
        fields = ['id', 'booking', 'action', 'timestamp']