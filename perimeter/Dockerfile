FROM orchardup/python:2.7
RUN pip install Flask cassandra-driver kafka-python srvlookup
ADD . /code
WORKDIR /code
CMD python perimeter.py
