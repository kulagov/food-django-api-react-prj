FROM python:3.8.5
RUN mkdir /code
WORKDIR /code
COPY ./backend/foodgram/requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY ./backend/foodgram .
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000 
