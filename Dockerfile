FROM python:3

WORKDIR /app

COPY . /app/

SHELL [ "/bin/bash", "-c" ]

ENV TOKEN "6692122746:AAGyex3zYUSayrD7OKLfSwcigkYisICxmZ8"
ENV MONGO_URI "mongodb+srv://blizzsoftword:eddyeddy@vendermejor.8r3dw9b.mongodb.net/?retryWrites=true&w=majority"

RUN python3 -m venv /app
RUN source /app/bin/activate
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["python3", "-m", "PromBOT"]