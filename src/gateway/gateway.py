from __future__ import print_function
from is_wire.core import Channel, Message, Subscription, Logger, Status, StatusCode
from is_msgs.common_pb2 import Position
from is_wire.rpc import ServiceProvider, LogInterceptor
import time
from random import *
from RequisicaoRobo_pb2 import RequisicaoRobo
from is_msgs.robot_pb2 import RobotTaskRequest
from google.protobuf.empty_pb2 import Empty
import socket
import json 


config_file = 'config.json'
config = json.load(open(config_file,'r'))
channel_controll = Channel(config['broker_uri'])
channel_position = Channel(config['broker_uri'])
channel_rpc = Channel(config['broker_uri'])

log = Logger(name = "log")
log.info("Channel active")
provider = ServiceProvider(channel_rpc)
logging = LogInterceptor()
provider.add_interceptor(logging)

sub_controll = Subscription(channel_controll)
sub_position = Subscription(channel_position)


sub_controll.subscribe(topic ="Controle.Console")


def requisicao(requisicao_robo, ctx):

    robot_request = RobotTaskRequest()

    if requisicao_robo.function == "get_position":
        robot_request.id = requisicao_robo.id
        request = Message(content = robot_request, reply_to = sub_position)
        channel_position.publish(request, topic = "Get.Position")

        try:
            reply = channel_position.consume(timeout = 1.0)
            log.info(f'{reply.status.code}')
            robot_position = reply.unpack(Position)
            requisicao_robo.positions.x = robot_position.x
            requisicao_robo.positions.y = robot_position.y

            return requisicao_robo
   
        except socket.timeout:
            print("ERRO")
        
        
    else:
        if requisicao_robo.positions.x < 0 or requisicao_robo.positions.y < 0:
            return Status(StatusCode.OUT_OF_RANGE,"the number must be positive")

        else:
            robot_request.id = requisicao_robo.id
            robot_request.basic_move_task.positions.extend([Position(x = requisicao_robo.positions.x, y = requisicao_robo.positions.y,z = 0)])
            request = Message(content = robot_request , reply_to = sub_position)
            channel_position.publish(request, topic = "Set.Position")

            try:
                reply = channel_position.consume(timeout = 1.0)
                log.info(f'{reply.status.code}')
                return Status(reply.status.code)
            
            except socket.timeout:
                print("ERRO")
        

while True:
    
    received_message = channel_controll.consume()
    received_struct = received_message.body.decode('utf-8')
    rand = randint(0,1)
    if received_struct == "Ligar sistema":
        if rand == 1:
            message_text = "Ligado"
            message = Message()
            message.body = message_text.encode('utf-8')
            channel_controll.publish(message, topic = "Controle.Console")
            time.sleep(2)
            log.info("Sistema online")
            break
        else:
            message_text = "Não é possivel ligar o sistema"
            message = Message()
            message.body = message_text.encode('utf-8')
            channel_controll.publish(message, topic = "Controle.Console")
            time.sleep(2)
            log.info("Nao foi possivel ligar o sistema")


if message_text == "Ligado":
    provider.delegate(
        topic = "Requisicao.Robo",
        function = requisicao,
        request_type = RequisicaoRobo,
        reply_type = RequisicaoRobo)
    
    provider.run()




