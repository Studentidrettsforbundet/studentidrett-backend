FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD ./app /code/
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y dos2unix

COPY config/django/init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

RUN dos2unix /usr/local/bin/init.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get update \
	&& apt-get install -y --no-install-recommends openssh-server \
	&& echo "$SSH_PASSWD" | chpasswd

COPY config/django/sshd_config /etc/ssh/

# CMD ["gunicorn", "--bind", "0.0.0.0:80", "app.wsgi"]
EXPOSE 2222 80

CMD ["../usr/local/bin/init.sh"]