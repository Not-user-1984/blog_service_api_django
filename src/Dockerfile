FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ /app

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ]
