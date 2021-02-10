FROM python:3.6-alpine
COPY . /app
WORKDIR /app

RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh postgresql-dev g++ linux-headers python3-dev pcre-dev && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--config", "config/settings.gunicorn.py", "main:app"]

