FROM alpine

RUN apk update \
    && apk add python3 git ffmpeg flac --no-cache \
    && git clone https://github.com/BennyThink/ExpressBot \
    && pip3 install -r /ExpressBot/requirements.txt

WORKDIR /ExpressBot


CMD python3 expressbot/main.py

# usage
# docker build -t expressbot:v1 .
# docker run -d --restart=always -e TOKEN="TOKEN" -e TURING="KEY"  expressbot:v1
