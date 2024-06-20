FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY app.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
STOPSIGNAL SIGNIT

ENTRYPOINT ["python", "app.py"]