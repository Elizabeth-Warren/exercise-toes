FROM python:3.7-alpine
COPY requirements.txt requirements-dev.txt /
RUN pip install -r /requirements-dev.txt
COPY . /app
WORKDIR /app
CMD python ./toes_app.py
