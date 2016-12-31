FROM python:2.7
ENV PYTHONUNBUFFERED 1
ENV HOSTNAME localhost
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
EXPOSE 8000
