FROM python:3.6-alpine

COPY requirements /
RUN apk add build-base libffi-dev openssl-dev --no-cache \
 && python -m pip install -r requirements \
 && apk del --purge build-base libffi-dev openssl-dev

COPY publisher/* /publisher/

WORKDIR publisher
CMD /bin/sh start.sh
