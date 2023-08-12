
# Запуск

```bash
    git clone git@github.com:Not-user-1984/testovoe_y_p.git
    cd infra_yp/dev
    docker compose up -d --build
    docker exec -it django python manage.py makemigrations
    docker exec -it django python manage.py migrate
    docker exec -it django python manage.py createsuperuser --username=admin1989 --email=test@test.com
    (Делаем супер пользователя именно с этим названием
    Нужно для генерации базы данных, делает на него подписки)
    docker exec -it django python manage.py generate_test_data
    docker exec -it django python manage.py pytest
```
## Доступные API endpoints

```bash
    http://localhost:8000/api/posts/  все посты
    http://localhost:8000/api/posts/1/  пост по id
    http://localhost:8000/api/posts/1/check_read_status/ проверка статуса прочитан ли пост
    http://localhost:8000/api/posts/1/mark_as_read/ ставит метку если прочитан
    http://localhost:8000/api/blogs/ все блоги и последние 5 постов блога
    http://localhost:8000/api/blogs/1  блога по id
    http://localhost:8000/api/blogs/1/subscribe/ подписка на блог
    http://localhost:8000/api/blogs/1/unsubscribe/ отписка на http://localhost:8000/api/personal_feed/ лента новостей
```

## Рассылка на email через Celery
```bash
    docker exec -it django celery -A config.celery worker -l info
```
Стресс-тест
```bash
   сd src
   locust -f locustfile.py
```
Приложение не выдерживает нагрузку согласно ТЗ. Возможно, для обработки большей нагрузки лучше использовать асинхронный подход с использованием FastAPI или разделить на микросервисы, например, с использованием Go(но заняло бы немного больше времени). Подробные требования и использование будут зависеть от количества пользователей и их действий. Это тестовый проект, и в реальном продакшене будут другие оптимизации и подходы.



 

