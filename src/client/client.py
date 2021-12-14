
from __future__ import print_function
from is_wire.core import Channel, Subscription, Message, Logger, Status, StatusCode
import time
from is_msgs.common_pb2 import Position
from RequisicaoRobo_pb2 import RequisicaoRobo
from random import randint
from google.protobuf.empty_pb2 import Empty
import socket
import json 


empty = Empty()
requisicao_robo = RequisicaoRobo()
requisicao_robo.id = 1

config_file = 'config.json'
config = json.load(open(config_file,'r'))

channel = Channel(config['broker_uri'])
channel_rpc  = Channel(config['broker_uri'])

sub = Subscription(channel)
sub_rpc = Subscription(channel_rpc)
sub.subscribe(topic = "Controle.Console")

log = Logger(name = "CLIENT")
log.info("Criando canal...")

message = Message()
message.body = "Ligar sistema".encode("utf-8")

log.info("Ligando sistema")
log.info("Esperando resposta...")


while True:

    channel.publish(message, topic= "Controle.Console")
    message = channel.consume()
    if message.body.decode('utf-8') == "Ligado":
        log.info(message.body.decode('utf-8'))
        break


while message.body.decode('utf-8') == "Ligado":

    ramdom_position_x = randint(-2,10)
    ramdom_position_y = randint(-2,10)
 
    time.sleep(2)
    log_set = Logger(name = 'Set_position')
    requisicao_robo.function = "set_position"

    requisicao_robo.positions.x = ramdom_position_x
    requisicao_robo.positions.y = ramdom_position_y
    requisicao_robo.id = 1
    message_set = Message(content = requisicao_robo, reply_to = sub_rpc)
    channel_rpc.publish(message_set, topic = "Requisicao.Robo")

    try:
        reply = channel_rpc.consume(timeout = 1)
        log_set.info(f'{reply.status.code}')

    except socket.timeout:
        print("error_set")

    
    log_get = Logger(name = 'get_position')
    requisicao_robo.function = "get_position"
    requisicao_robo.id = 1
    message_get = Message(content = requisicao_robo, reply_to = sub_rpc)
    channel_rpc.publish(message_get, topic = "Requisicao.Robo")
    time.sleep(1.5)

    try:
        reply = channel_rpc.consume(timeout = 1)
        position = reply.unpack(RequisicaoRobo)
        log_get.info(f'x = {position.positions.x}, y = {position.positions.y}')

    except socket.timeout:
        print('Error_get')

