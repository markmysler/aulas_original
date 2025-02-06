FROM python:3.6
WORKDIR /app
COPY requirements.txt /app/
COPY .env /app/
RUN pip install -r /app/requirements.txt
COPY . /app/
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]