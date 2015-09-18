FROM orchardup/python:2.7
RUN pip install Flask
ADD . /code
ADD ./templates /code/templates
WORKDIR /code
CMD python webservice.py
