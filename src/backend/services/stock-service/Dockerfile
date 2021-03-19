FROM python:3.8.7-alpine3.13

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5585

CMD ["python", "server.py"]
