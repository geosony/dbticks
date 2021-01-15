FROM python:3.8-alpine
WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN mkdir -p ./uploads
RUN wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
RUN pip3 install  --no-cache-dir -r requirements.txt

RUN apk add --update --no-cache py3-numpy
ENV PYTHONPATH=/usr/lib/python3.8/site-packages

COPY . .
CMD ["python", "app.py"]