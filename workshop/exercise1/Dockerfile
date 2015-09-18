FROM orchardup/python:2.7
RUN pip install Flask
ADD . /code
WORKDIR /code
EXPOSE 8080
CMD ./simple_webservice.py
