from django.urls import path
from .views import *

urlpatterns = [
    # URL для списка отелей (только чтение)
    path('hotels/', HotelListAPIView.as_view(), name='hotel-list'),
    # Добавляем URL для поиска отелей по названию
    path('hotels/search/', HotelListAPIView.as_view(), name='hotel-search'),
    # URL для создания нового отеля
    path('hotels/create/', HotelCreateAPIView.as_view(), name='hotel-create'),
    
    # URL для списка комнат (только чтение)
    path('rooms/', RoomListAPIView.as_view(), name='room-list'),
    # URL для создания новой комнаты
    path('rooms/create/', RoomCreateAPIView.as_view(), name='room-create'),
    
    # URL для списка бронирований (только чтение)
    path('bookings/', BookingListAPIView.as_view(), name='booking-list'),
    # URL для создания нового бронирования
    path('bookings/create/', BookingCreateAPIView.as_view(), name='booking-create'),

    # URL для списка отзывов (создание и просмотр)
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list'),
    # URL для просмотра, обновления и удаления отдельного отзыва
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-detail'),
    # URL для создания лайка к отзыву
    path('review-likes/<int:review_id>/', ReviewLikeCreateAPIView.as_view(), name='review-like'),

    # URL для добавления отеля в избранное
    path('favorite-hotels/', FavoriteHotelCreateAPIView.as_view(), name='favorite-hotel-create'),
    # URL для удаления отеля из избранного
    path('favorite-hotels/<int:pk>/', FavoriteHotelDeleteAPIView.as_view(), name='favorite-hotel-delete'),

    path('hotels/<int:hotel_id>/like/', HotelLikeCreateAPIView.as_view(), name='hotel-like'),
    path('hotels/<int:hotel_id>/unlike/', HotelLikeDeleteAPIView.as_view(), name='hotel-unlike'),
    path('recommended-hotels/', RecommendedHotelListAPIView.as_view(), name='recommended-hotels'),
]