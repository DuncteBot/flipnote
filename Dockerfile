FROM python:3.9-alpine

WORKDIR /flipnote

RUN apk --no-cache add --virtual build-deps gcc python3-dev musl-dev && \
    apk --no-cache add jpeg-dev zlib-dev libjpeg freetype-dev libpng

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apk del build-deps

ENTRYPOINT ["hypercorn", "main:app", "--bind", "0.0.0.0:5000"]