FROM python:3.9-alpine3.13
LABEL maintainer="chaudharytushar014@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY . /Redirects
WORKDIR /Redirects
EXPOSE 7000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

ENV PATH="/py/bin:$PATH"

CMD ["python3", "reroute.py"]
