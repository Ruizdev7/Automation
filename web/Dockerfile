# syntax=docker/dockerfile:1.0

FROM python:3.8-slim-buster

WORKDIR /

COPY . /

EXPOSE 5002

RUN pip3 install -r requirements.txt

ENV FLASK_APP=agriculture_app
ENV FLASK_DEBUG=True


CMD gunicorn -w 2 --bind 0.0.0.0:5002 wsgi:app


# CMD ["gunicorn" , "--bind", "0.0.0.0:8000", "agriculture_app:app"]
# CMD ["gunicorn" ,  "--chdir" , "app" , "main:app" , "-w 2" , "--threads 2" , "-b 0.0.0.0:5000"]
# CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "app:app"]
# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
