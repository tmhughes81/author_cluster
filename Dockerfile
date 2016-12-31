FROM python:2.7
ENV PYTHONUNBUFFERED 1
ENV HOSTNAME localhost
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
CMD /usr/bin/python /code/acp/manage.py runserver 0.0.0.0:8000
