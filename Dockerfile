FROM python:3

WORKDIR /app

COPY . /app/

SHELL [ "/bin/bash", "-c" ]

ENV BOT_DIR "/app"

RUN python3 -m venv /app
RUN source /app/bin/activate
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["source", "start.sh"]