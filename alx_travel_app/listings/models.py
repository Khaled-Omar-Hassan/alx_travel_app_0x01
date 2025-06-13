import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Listing(models.Model):
    """Represents a travel listing (hotel, apartment, etc)."""
    listing_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    host_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='listings')
    name = models.CharField(max_length=255)
    description = models.TextField(null=False)
    location = models.CharField(max_length=255, null=False)
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    """Represents a user's booking for a listing."""
    booking_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='bookings')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False)
    status = models.CharField(
        max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id.first_name} booking {self.listing_id.name}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
    ]

    payment_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    booking_id = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, null=False)

    def __str__(self):
        return f"Payment of {self.amount} via {self.payment_method}"


class Review(models.Model):
    """User review for a listing."""
    review_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], default=5, null=False)
    comment = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}/5 by {self.user_id.email} for {self.listing_id.name}"


class Message(models.Model):
    """Represents a message between users."""
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender_id.email} to {self.recipient_id.email}"
