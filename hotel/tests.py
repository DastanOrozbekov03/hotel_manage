from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Hotel, Room, Review, Booking, ReviewLike, FavoriteHotel, HotelLike, BookingHistory
from django.utils import timezone
from datetime import timedelta



class YourTestCase(TestCase):
    def setUp(self):
        self.name = get_user_model().objects.create(email='testuser@example.com', password='12345')

class HotelModelTest(TestCase):
    def setUp(self):
        self.name = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)

    def test_hotel_creation(self):
        self.assertEqual(self.hotel.name, 'Test Hotel')
        self.assertEqual(self.hotel.owner, self.user)
        self.assertEqual(self.hotel.phone_number, '1234567890')
        self.assertEqual(self.hotel.price, 100.00)
        self.assertEqual(self.hotel.tags, 'test, hotel')
        self.assertEqual(self.hotel.description, 'Test hotel description')
        self.assertEqual(self.hotel.stars, 5)


class RoomModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.room = Room.objects.create(hotel=self.hotel, number='101', price=100.00)

    def test_room_creation(self):
        self.assertEqual(self.room.hotel, self.hotel)
        self.assertEqual(self.room.number, '101')
        self.assertEqual(self.room.price, 100.00)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.review = Review.objects.create(hotel=self.hotel, user=self.user, rating=5, comment='Great hotel!')

    def test_review_creation(self):
        self.assertEqual(self.review.hotel, self.hotel)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great hotel!')


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.booking = Booking.objects.create(hotel=self.hotel, user=self.user,
                                              check_in_date=timezone.now().date(),
                                              check_out_date=(timezone.now() + timedelta(days=2)).date())

    def test_booking_creation(self):
        self.assertEqual(self.booking.hotel, self.hotel)
        self.assertEqual(self.booking.user, self.user)


class ReviewLikeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.review = Review.objects.create(hotel=self.hotel, user=self.user, rating=5, comment='Great hotel!')
        self.like = ReviewLike.objects.create(review=self.review, user=self.user)

    def test_like_creation(self):
        self.assertEqual(self.like.review, self.review)
        self.assertEqual(self.like.user, self.user)


class FavoriteHotelModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.favorite_hotel = FavoriteHotel.objects.create(user=self.user, hotel=self.hotel)

    def test_favorite_hotel_creation(self):
        self.assertEqual(self.favorite_hotel.user, self.user)
        self.assertEqual(self.favorite_hotel.hotel, self.hotel)


class HotelLikeModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.hotel_like = HotelLike.objects.create(user=self.user, hotel=self.hotel)

    def test_hotel_like_creation(self):
        self.assertEqual(self.hotel_like.user, self.user)
        self.assertEqual(self.hotel_like.hotel, self.hotel)


class BookingHistoryModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser')
        self.hotel = Hotel.objects.create(owner=self.user, name='Test Hotel', phone_number='1234567890',
                                          price=100.00, tags='test, hotel', description='Test hotel description',
                                          stars=5)
        self.booking = Booking.objects.create(hotel=self.hotel, user=self.user,
                                              check_in_date=timezone.now().date(),
                                              check_out_date=(timezone.now() + timedelta(days=2)).date())
        self.booking_history = BookingHistory.objects.create(booking=self.booking, action='Created')

    def test_booking_history_creation(self):
        self.assertEqual(self.booking_history.booking, self.booking)
        self.assertEqual(self.booking_history.action, 'Created')
