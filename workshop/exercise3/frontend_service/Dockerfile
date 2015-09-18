FROM python:2.7
RUN pip install flask srvlookup requests
ADD . /code
WORKDIR /code
EXPOSE 8080
CMD python front_end.py