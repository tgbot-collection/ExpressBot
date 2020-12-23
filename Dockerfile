FROM python:alpine

RUN apk update \
    && apk add git ffmpeg flac --no-cache \
    && git clone https://github.com/tgbot-collection/ExpressBot \
    && pip3 install --no-cache-dir -r /ExpressBot/requirements.txt 

WORKDIR /ExpressBot


CMD ["python3", "expressbot/main.py"]

# usage
# docker build -t expressbot:v1 .
# docker run -d --restart=always -e TOKEN="TOKEN" -e TURING="KEY"  expressbot:v1
