import logging
from rest_framework import generics, permissions, status, pagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .permissions import IsOwnerOrSuperuser, ReadOnly
from rest_framework.response import Response
from functools import wraps
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from hotel.tasks.task import send_email_task


logger = logging.getLogger(__name__)

def log_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f'{func.__name__} requested')
        return func(*args, **kwargs)
    return wrapper


class HotelListAPIView(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'stars']
    pagination_class = pagination.PageNumberPagination

    # @log_request
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class HotelCreateAPIView(generics.CreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsOwnerOrSuperuser]
    parser_classes = [MultiPartParser, FormParser] 

    @log_request
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hotel__name']
    pagination_class = pagination.PageNumberPagination

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class RoomCreateAPIView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class BookingListAPIView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    pagination_class = pagination.PageNumberPagination
    filterset_fields = ['hotel']

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            subject = 'Подтверждение бронирования'
            message = 'Ваше бронирование подтверждено.'
            recipient_list = [request.user.email]
            send_email_task.delay(subject, message, recipient_list)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrSuperuser]

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class ReviewLikeCreateAPIView(generics.CreateAPIView):
    queryset = ReviewLike.objects.all()
    serializer_class = ReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        review = self.get_review()
        if review.likes.filter(user=self.request.user).exists():
            return Response({'message': 'Вы уже поставили лайк на  этот отзыв.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id)

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class FavoriteHotelCreateAPIView(generics.CreateAPIView):
    queryset = FavoriteHotel.objects.all()
    serializer_class = FavoriteHotelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class FavoriteHotelDeleteAPIView(generics.DestroyAPIView):
    queryset = FavoriteHotel.objects.all()
    serializer_class = FavoriteHotelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        hotel_id = kwargs.get('pk')
        favorite_hotel = get_object_or_404(FavoriteHotel, user=user, hotel_id=hotel_id)
        self.perform_destroy(favorite_hotel)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class HotelLikeCreateAPIView(generics.CreateAPIView):
    serializer_class = HotelLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        hotel_id = self.kwargs.get('hotel_id')
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer.save(user=self.request.user, hotel=hotel)
        hotel.like_count += 1  
        hotel.save()

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class HotelLikeDeleteAPIView(generics.DestroyAPIView):
    serializer_class = HotelLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        hotel_id = kwargs.get('hotel_id')
        hotel_like = get_object_or_404(HotelLike, user=user, hotel_id=hotel_id)
        self.perform_destroy(hotel_like)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RecommendedHotelListAPIView(generics.ListAPIView):
    serializer_class = HotelSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return Hotel.objects.order_by('-like_count')
    
    @log_request
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class BookingHistoryListAPIView(generics.ListAPIView):
    queryset = BookingHistory.objects.all()
    serializer_class = BookingHistorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = pagination.PageNumberPagination