FROM python:3.10.7-slim

WORKDIR /bot

RUN apt update && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pipenv

COPY Pipfile* .
RUN pipenv install --system --deploy --ignore-pipfile

ADD ./app /bot/app
#RUN mkdir /bot/data
ADD ./data /bot/data

CMD [ "python", "-m", "app" ]