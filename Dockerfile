FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk add mysql mysql-client
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD ["app.py" ]
# FROM mysql
# COPY ./db.sql /app/db.sql
# WORKDIR /app
# RUN source /app/db.sql