FROM orchardup/python:2.7
RUN pip install Flask cassandra-driver srvlookup pyspark
ADD . /code
WORKDIR /code
CMD python perimeter.py
