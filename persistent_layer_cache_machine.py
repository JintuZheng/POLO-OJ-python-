""" 持久化缓存服务器进程

@Author: Jintu Zheng
@Date: 2020-12-28

该进程用于获取消息队列里面评判结果并存访到进程通信队列当中，
其他的进程可以通过web访问这个服务器访问到自己的代码是否已经评判出结果了

# 此处如果出现数据量巨大的时候，我们考虑建立数据缓存查找索引，这样就能减轻对于数据库访问的压力
我们将制定一些预备策略：我们先检索处理了的结果消息缓存队列，假如缓存队列里面不具备的话，我们将对
数据库进行查询，都没有的话则返回等待信号

# 为了防止一些出错或者冲突，比如说我们在Worker服务器/MQ服务器里面弄丢了这个数据结果的话，我们将减少每一次
客户端对于缓存服务器查找的概率，防止客户无休止进行轮询，因此使用二进制指数退避算法可以完成。
时间仓促，明天答辩，因此此处不做。仅在答辩的时候提及即可。

# 一旦客户轮询的次数过多，我们将拒绝客户服务。

"""
# Check from database in cache backend, if not found it join
from flask import Flask, request
import json
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
import json
import random
import threading
import requests
from multiprocessing import Queue

MQ_USER_NAME = 'guest' #MQ的用户名
MQ_USER_PASSWORD = 'guest' #MQ的密码
HOST_NAME = 'localhost' #MQ的网络地址
HOST_PORT = 5672 #MQ的端口
WORKERS_PORT = 1235 #评判服务器的端口

credentials = PlainCredentials(MQ_USER_NAME, MQ_USER_PASSWORD)  # MQ的用户名和密码,创建凭证

#监听事件：监听队列消息并处理
def callback(ch, method, properties, msg):
    global Cache_Queue
    global Cache_List
    ch.basic_ack(delivery_tag = method.delivery_tag)
    msg_params = msg.decode()
    # 缓存数据（消息队列当中的评判结果）
    #Cache_Queue.put(msg_params)
    Cache_List.append(msg_params)
    
    
def get_msg_from_MQ(): # Build connection -> build channel -> get message
    #建立连接，然后发起通道，然后再接收信息
    print('Running cache server')
    connection = BlockingConnection(ConnectionParameters(host = HOST_NAME, port = HOST_PORT, virtual_host = '/',credentials = credentials))
    channel = connection.channel()
    result = channel.queue_declare(queue = 'judged') # 声明消息队列，消息将在这个队列传递，如不存在，则创建
    # 告诉rabbitmq，用callback来接收消息
    channel.basic_consume('judged',callback)
    # 开始接收信息，并进入阻塞状态，队列里有信息才会调用callback进行处理
    channel.start_consuming()

app = Flask(__name__)

Cache_Queue = Queue() #Process Queue system channel
Cache_List = []

# 执行该函数将把数据写入到数据库里面
def write_in_database(result):
    return

def call_check(tid):
    global Cache_List
    for item in Cache_List:
        item = json.loads(item)
        if item['TaskID'] == tid:
            return item
    return None
    

@app.route('/', methods=['POST','GET'])
def response_from_student():
    tid = request.form.get("tid") 
    tid_check_result = call_check(tid)
    if tid_check_result == None:
        return None
    else:
        result = {'tid':tid, 'result':tid_check_result}
        return result

if __name__ == '__main__':
    cache_getter = threading.Thread(target=get_msg_from_MQ)
    cache_getter.start()
    app.run(host='0.0.0.0',port=1234)
