FROM python:3

WORKDIR /app

COPY . /app/

SHELL [ "/bin/bash", "-c" ]

ENV TOKEN "6592524009:AAFp6S6PwNUXePWHRK_luYCZJObWrHZfPWc"

RUN python3 -m venv /app
RUN source /app/bin/activate
# RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["python3", "-m", "PromBOT"]