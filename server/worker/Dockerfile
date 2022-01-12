FROM python:3.9.9-alpine3.15

WORKDIR /worker
COPY . .

RUN apk add gcc musl-dev libc-dev
RUN pip install -r ./requirements.txt
RUN python ./setup.py build_ext --inplace

EXPOSE 8181

CMD [ "python", "./worker.py" ]