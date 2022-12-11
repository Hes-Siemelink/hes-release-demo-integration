# temp stage
FROM python:3.10-alpine as builder
LABEL stage=builder
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/app

RUN apk update && apk upgrade && apk add gcc g++

COPY app $APP_HOME/

WORKDIR $APP_HOME

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install install -r $APP_HOME/requirements.txt


# final stage
FROM python:3.10-alpine

ENV APP_HOME=/app
ENV INPUT_LOCATION=/input
ENV OUTPUT_LOCATION=/output

RUN apk update && apk upgrade && apk add gcc g++

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder $APP_HOME $APP_HOME

WORKDIR $APP_HOME

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "dai_release_sdk.wrapper"]


