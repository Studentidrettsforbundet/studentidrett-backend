FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt
RUN python manage.py collectstatic
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app.wsgi"]
EXPOSE 80