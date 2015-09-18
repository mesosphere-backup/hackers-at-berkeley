FROM python:2.7
RUN pip install flask
ADD . /code
WORKDIR /code
EXPOSE 8080
CMD python back_end.py