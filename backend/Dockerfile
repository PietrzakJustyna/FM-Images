FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt
COPY . /app/
