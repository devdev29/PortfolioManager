FROM python:3.9
 
WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./ /code

RUN apt-get update

EXPOSE 8080

USER 1000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]