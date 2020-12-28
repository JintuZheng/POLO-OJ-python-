"""任务调度机器集群

这部分的进程和消费者进程是连体的，消费者进程属于任务调度机器进程的子进程
该部分机器用于接收消息队列的消息，并且发配任务新建新的消费者进程去完成任务

"""

from pika import PlainCredentials, BlockingConnection, ConnectionParameters
import json
import random
import threading
import requests

MQ_USER_NAME = 'guest' #MQ的用户名
MQ_USER_PASSWORD = 'guest' #MQ的密码
HOST_NAME = 'localhost' #MQ的网络地址
HOST_PORT = 5672 #MQ的端口
WORKERS_PORT = 1235 #评判服务器的端口

credentials = PlainCredentials(MQ_USER_NAME, MQ_USER_PASSWORD)  # MQ的用户名和密码,创建凭证

#监听事件：监听队列消息并处理
def callback(ch, method, properties, msg):
    ch.basic_ack(delivery_tag = method.delivery_tag)
    msg_params = msg.decode()
    call_worker(msg_params) # 调度向评判机器群发起一条新的评判申请

def get_msg_from_MQ(): # Build connection -> build channel -> get message
    #建立连接，然后发起通道，然后再接收信息
    connection = BlockingConnection(ConnectionParameters(host = HOST_NAME, port = HOST_PORT, virtual_host = '/',credentials = credentials))
    channel = connection.channel()
    result = channel.queue_declare(queue = 'un_judged') # 声明消息队列，消息将在这个队列传递，如不存在，则创建
    # 告诉rabbitmq，用callback来接收消息
    channel.basic_consume('un_judged',callback)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()


def call_worker(msg_params):
    try:
        request_url = "http://"+HOST_NAME+":"+str(WORKERS_PORT)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data={'msg':msg_params}, headers=headers)
    except Exception as e:
        print(e) #意外打印
        return None
    return None


class Broker(threading.Thread):
    def __init__(self):
        super(Broker, self).__init__()
        print('Broker thread running')

    def run(self):
        get_msg_from_MQ()

if __name__ == "__main__":
    broker = Broker()
    broker.start()
    broker.join()