# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

CMD ["--placement-manager"]