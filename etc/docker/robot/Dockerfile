From python:3.7 

WORKDIR /app
COPY /home/mateussobrinho/ProjetoIS/src/robot/robot.py /app
COPY /home/mateussobrinho/ProjetoIS/src/robot/RequisicaoRobo_pb2.py /app
COPY /home/mateussobrinho/ProjetoIS/src/robot/config.json /app
COPY requirements.txt /app

RUN pip install -r requirements.txt
RUN pip install --upgrade protobuf


