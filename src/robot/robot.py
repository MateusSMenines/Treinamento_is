from is_wire.rpc import ServiceProvider, LogInterceptor
from is_wire.core import Channel, Subscription, Message, Status, StatusCode, Logger
from RequisicaoRobo_pb2 import RequisicaoRobo
from is_msgs import common_pb2
from is_msgs.robot_pb2 import RobotTaskRequest
from google.protobuf.empty_pb2 import Empty
from is_msgs.common_pb2 import Position
import time
import json 


class Robot():
    def __init__(self, id, x, y):
        self.id = id
        self.pos_x = x
        self.pos_y = y

    def get_id(self):
        return self.id

    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def get_position(self):
        return self.pos_x, self.pos_y


def get_position(robo_id, ctx):

    position = Position()
    for robo in robot_list:
        if robo.id == robo_id.id:
            position.x,position.y = robo.get_position()
 
    return position


def set_position(position, ctx):

    for robo in robot_list:
        if robo.id == position.id:
            x = position.basic_move_task.positions[0].x
            y = position.basic_move_task.positions[0].y
            robo.set_position(x = x, y = y)
            return Status(StatusCode.OK)
            

robot_list = [Robot(id = 1,x = 1,y = 1), Robot(id = 2,x = 3,y = 5)]


config_file = 'config.json'
config = json.load(open(config_file,'r'))
channel = Channel(config['broker_uri'])


provider = ServiceProvider(channel)
logging = LogInterceptor() 
provider.add_interceptor(logging)


provider.delegate(
    topic="Get.Position",
    function=get_position,
    request_type=RobotTaskRequest,
    reply_type=Position) 

provider.delegate(
    topic="Set.Position",
    function=set_position,
    request_type=RobotTaskRequest,
    reply_type=Empty)

provider.run()
