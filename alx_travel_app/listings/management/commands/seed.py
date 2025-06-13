from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing, Booking, Review, Message, Payment

from faker import Faker
import random
from datetime import timedelta

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Seed the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Seeding database...")

        Message.objects.all().delete()
        Review.objects.all().delete()
        Payment.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("✅ Old data cleared")

        # Create users
        users = []
        for _ in range(10):
            role = random.choice(['guest', 'host'])
            user = User.objects.create_user(
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password="password123",
                phone_number=fake.phone_number(),
                role=role
            )
            users.append(user)

        self.stdout.write(f"✅ Created {len(users)} users")

        # Create admin
        User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass',
            first_name='Admin',
            last_name='User',
            role='admin'
        )

        # Create listings
        hosts = [u for u in users if u.role == 'host']
        listings = []
        for _ in range(10):
            host = random.choice(hosts)
            listing = Listing.objects.create(
                host_id=host,
                name=fake.company(),
                description=fake.text(),
                location=fake.city(),
                price_per_night=round(random.uniform(50, 300), 2)
            )
            listings.append(listing)

        self.stdout.write(f"✅ Created {len(listings)} listings")

        # Create bookings
        guests = [u for u in users if u.role == 'guest']
        bookings = []
        for _ in range(15):
            guest = random.choice(guests)
            listing = random.choice(listings)
            start_date = fake.date_between(start_date='-30d', end_date='+30d')
            end_date = start_date + timedelta(days=random.randint(1, 5))
            total_price = (end_date - start_date).days * \
                float(listing.price_per_night)
            booking = Booking.objects.create(
                listing_id=listing,
                user_id=guest,
                start_date=start_date,
                end_date=end_date,
                total_price=total_price,
                status=random.choice(['pending', 'confirmed', 'cancelled'])
            )
            bookings.append(booking)

        self.stdout.write(f"✅ Created {len(bookings)} bookings")

        # Create payments
        for booking in bookings:
            if booking.status == 'confirmed':
                Payment.objects.create(
                    booking_id=booking,
                    amount=booking.total_price,
                    payment_method=random.choice(
                        ['credit_card', 'paypal', 'stripe'])
                )

        self.stdout.write(f"✅ Created payments for confirmed bookings")

        # Create reviews
        for _ in range(10):
            listing = random.choice(listings)
            user = random.choice(guests)
            Review.objects.create(
                listing_id=listing,
                user_id=user,
                rating=random.randint(1, 5),
                comment=fake.sentence()
            )

        self.stdout.write("✅ Created 10 reviews")

        # Create messages
        for _ in range(20):
            sender = random.choice(users)
            recipient = random.choice([u for u in users if u != sender])
            Message.objects.create(
                sender_id=sender,
                recipient_id=recipient,
                message_body=fake.text()
            )

        self.stdout.write("✅ Created 20 messages")
        self.stdout.write(self.style.SUCCESS("🎉 Seeding complete!"))
