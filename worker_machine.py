from gcc_powered_by_python import compiler
from flask import Flask, request
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
import json
import random
import threading
import time
from utils import current_datetime, gen_task_ID, getFiles
import requests

MQ_USER_NAME = 'guest' #MQ的用户名
MQ_USER_PASSWORD = 'guest' #MQ的密码
HOST_NAME = 'localhost' #MQ的网络地址
HOST_PORT = 5672 # MQ的端口

credentials = PlainCredentials(MQ_USER_NAME, MQ_USER_PASSWORD)  # MQ的用户名和密码,创建凭证

def send_msg_to_MQ(msg_data): # Build connection -> build channel -> send message
    #建立连接，然后发起通道，然后再发送信息
    connection = BlockingConnection(ConnectionParameters(host = HOST_NAME, port = HOST_PORT, virtual_host = '/',credentials = credentials))
    channel = connection.channel()
    result = channel.queue_declare(queue = 'judged') # 声明消息队列，消息将在这个队列传递，如不存在，则创建
    """
    data:
    msg_data;
    @key='TaskID' value->str # 任务ID
    @key='studentNumber' value->str # 学号
    @key='result' value->str # 代码评判和编译结果
    @key='time' value->str # 代码提交的时间
    """
    message = json.dumps({'TaskID':msg_data['TaskID'],'result':msg_data['result'],'time':msg_data['time'],'studentNumber':msg_data['studentNumber']}) # build msg
    channel.basic_publish(exchange = '',routing_key = 'judged',body = message)# 向队列插入数值 routing_key是队列名
    connection.close()

app = Flask(__name__)
#打工人，打工魂
@app.route('/', methods=['POST','GET'])
def worker():
    msg_params = request.form.get("msg")
    msg_params = json.loads(msg_params)
    returnCode, out = compiler(msg_params['code'], msg_params['TaskID'])
    # 开启子进程去编译（外部的子进程是G++编译器）
    time.sleep(3)
    if returnCode == 0:
        result = 'pass'
    else:
        result = 'Error+'+ out
    msg_return = {'TaskID':msg_params['TaskID'],'time':msg_params['time'],'studentNumber':msg_params['studentNumber'],'result':result}
    send_msg_to_MQ(msg_return) # 把评判结果存入消息队列
    return

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1235)