FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
ADD app/ /code/
WORKDIR /code/

COPY ./config/ ./config
COPY config/django/sshd_config /etc/ssh/

RUN chmod +x ./config/django/start.sh

# external libraries for pillow
RUN apk --update add \
    build-base \
    jpeg-dev \
    zlib-dev

# Open SSH for azure database at port 2222 to run migrations
RUN apk add openssh && \
    echo "root:Docker!" | chpasswd

# Install dependencies for psycopg2
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

WORKDIR ./app

EXPOSE 2222 80
CMD /usr/sbin/sshd
CMD ["../config/django/start.sh"]