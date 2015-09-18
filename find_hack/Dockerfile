FROM orchardup/python:2.7
RUN pip install Flask srvlookup
RUN pip install uwsgi
ADD . /code
WORKDIR /code
CMD uwsgi --http 0.0.0.0:8080 --wsgi-file find_hack.py --callable app --master --no-default-app -p 10 -R 5
