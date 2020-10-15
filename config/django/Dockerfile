FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD ./app /code/
RUN pip install -r requirements.txt

# init.sh converted to UNIX
RUN apt-get update && apt-get install -y dos2unix
COPY config/django/init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
RUN dos2unix /usr/local/bin/init.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/

EXPOSE 8000

CMD ["/usr/local/bin/init.sh"]