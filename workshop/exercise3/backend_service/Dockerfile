FROM orchardup/python:2.7
RUN pip install Flask
RUN pip install uwsgi
ADD . /code
WORKDIR /code
CMD uwsgi --http 0.0.0.0:8080 --wsgi-file back_end.py --callable app --master --no-default-app -p 10
