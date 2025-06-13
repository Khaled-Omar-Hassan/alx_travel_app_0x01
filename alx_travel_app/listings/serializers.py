from rest_framework import serializers
from .models import User, Listing, Booking, Payment, Review, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name',
                  'last_name', 'role', 'is_active', 'is_staff']
        read_only_fields = ['user_id']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model."""
    host_id = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ['listing_id', 'host_id', 'name', 'description',
                  'location', 'price_per_night', 'created_at', 'updated_at']
        read_only_fields = ['listing_id', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model."""
    user_id = UserSerializer(read_only=True)
    listing_id = ListingSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['booking_id', 'listing_id', 'user_id', 'created_at']
        read_only_fields = ['booking_id', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model."""
    user_id = UserSerializer(read_only=True)
    listing_id = ListingSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['payment_id', 'user_id', 'listing_id',
                  'amount', 'status', 'created_at']
        read_only_fields = ['payment_id', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user_id = UserSerializer(read_only=True)
    listing_id = ListingSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['review_id', 'user_id', 'listing_id',
                  'rating', 'comment', 'created_at']
        read_only_fields = ['review_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender_id = UserSerializer(read_only=True)
    receiver_id = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender_id',
                  'receiver_id', 'content', 'created_at']
        read_only_fields = ['message_id', 'created_at']
