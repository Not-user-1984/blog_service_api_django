import logging
from celery import shared_task
from .models import Post, User


@shared_task
def send_daily_post_summary():
    """
    Отправляет ежедневное письмо со сводкой последних постов пользователям.
    """
    users = User.objects.all()
    for user in users:
        latest_posts = Post.objects.filter(
            blog__user=user).order_by('-created_at')[:5]
        email_message = 'Here are the latest posts:\n\n'
        for post in latest_posts:
            email_message += f'- {post.title}\n'
        log_file = 'src/blog_service/log_file_email.log'
        logging.basicConfig(filename=log_file, level=logging.INFO)
        try:
            logging.info(f"Email sent to {user.email}")
        except Exception as e:
            logging.error(f"Failed to send email to {user.email}: {e}")


send_daily_post_summary.apply_async()
