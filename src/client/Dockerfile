From python:3.7 

WORKDIR /app
COPY client.py /app
COPY RequisicaoRobo_pb2.py /app
COPY config.json /app
COPY requirements.txt /app

RUN pip install -r requirements.txt
RUN pip install --upgrade protobuf

CMD python3 client.py
