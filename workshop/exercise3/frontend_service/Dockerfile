FROM python:2.7
RUN pip install Flask srvlookup requests
ADD . /code
WORKDIR /code
EXPOSE 8080
CMD python front_end.py