from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from blog_service.models import Blog, Post, User

fake = Faker()

class Command(BaseCommand):
    help = 'Generate test data for the Post model'

    def handle(self, *args, **options):
        blogs = Blog.objects.all()

        for _ in range(1000):  # Generate 1000 records
            blog = fake.random_element(blogs)
            title = fake.sentence()
            text = fake.paragraph()
            created_at = fake.date_time_this_year()

            Post.objects.create(
                blog=blog,
                title=title,
                text=text,
            )

        for _ in range(500):  # Generate 500 users
            username = fake.user_name()
            email = fake.email()
            password = fake.password()

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated test data for Post model'))
