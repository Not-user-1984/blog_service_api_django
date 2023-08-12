# testovoe_y_p

запуск через докер командой 

Делаем супер пользователя именно с этим названием
Нужно для генерации базы данных 

Миграции

Запус проекта 

Доступные ручки 
Можно подписываться на блоги и от отписываться

Можно помечать прочитанно

docker exec -it django python manage.py makemigrations
docker exec -it django python manage.py createsuperuser --username=admin1989 --email=test@test.com
docker exec -it django python manage.py generate_test_data

Так же лента новостей 

так насроена рассылка через Celary

<p>Приложение не держит нагрузку из ТЗ,
до 25, нужно примерно в два раза больше, возможно 
лучше было делать асинхронно на FastAPI, но была выбрана скорость разработки так с Fast API знаком не так много, еше лучше раздилить на микро сервисы, подписок и чтений статуса, например Go, а на Django оставить тупую базу создания постов, но нужно больше данных как и кто и сколько будут пользоваться, все ровно это игрушечный проект, думаю в проде все не так.
</p>
celery -A config.celery worker -l info

python manage.py createsuperuser --username=admin1989 --email=test@test.com

 locust -f locustfile.py

 python manage.py generate_test_data
