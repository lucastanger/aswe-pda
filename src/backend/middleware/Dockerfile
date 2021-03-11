FROM python:3.8.7-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5600

CMD ["python", "-u", "app.py"]
