FROM python:3.10

WORKDIR /app

ENV MODEL_PATH "/app/data/iris.sav"
ENV COLUMNS "sepal.length,sepal.width,petal.length,petal.width"

RUN apt-get update && apt-get install -y build-essential python3-dev libc-dev libffi-dev

COPY . /app

RUN pip3 install -r requirements.txt

RUN chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]