from django.core.management.base import BaseCommand
from faker import Faker
from blog_service.models import Blog, Post, User
from tqdm import tqdm
fake = Faker()


class Command(BaseCommand):
    help = 'Generate test data for the Post model'

    def handle(self, *args, **options):
        blogs = Blog.objects.all()

        with tqdm(total=500, desc='Generating users') as pbar:
            for _ in range(500):
                username = fake.user_name()
                while User.objects.filter(username=username).exists():
                    username = fake.user_name()

                email = fake.email()
                password = fake.password()

                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                pbar.update(1)

        blogs = Blog.objects.all()

        with tqdm(total=1000, desc='Generating posts') as pbar:
            for _ in range(1000):  # Generate 1000 records
                blog = fake.random_element(blogs)
                title = fake.sentence()
                text = fake.text(max_nb_chars=130)

                Post.objects.create(
                    blog=blog,
                    title=title,
                    text=text,
                )
                pbar.update(1)

        try:
            superuser = User.objects.get(username='admin1989')
        except User.DoesNotExist:
            raise Exception(
                "Create a superuser with username 'admin1989' before running this command"
                )

        with tqdm(total=100, desc='Generating subscriptions') as pbar:
            for _ in range(100):  # Generate 100 subscriptions for superuser
                blog = fake.random_element(blogs)
                blog.subscription_set.create(subscriber=superuser)
                pbar.update(1)

        self.stdout.write(self.style.SUCCESS(
            'Successfully generated test data for Post model'))

