""" 学生端机器程序

@Author: Jintu Zheng
@Date: 2020-12-28

该进程：最多能同时提交<Threads_limit> 份代码，每一份代码提交之后将
发送到消息队列里面，然后该线程等待一段时间之后从持久层的缓存服务器里面查询属于自己的评判结果
（用web访问持久层缓存服务器的一条缓存查询线程）
然后该提交线程才算结束。

提交一份代码之后我们并不阻止他继续提交多份代码，即便第一份代码没有评判完，在前端是没有感觉拥塞的
他依旧可以提交第二份，但是为了安全起见，我设置了<Threads_limit>来控制最多能提交的代码份数

只有当我们的提交线程从缓存服务器里面查询到自己的提交结果之后，提交线程才算真正结束
"""

from pika import PlainCredentials, BlockingConnection, ConnectionParameters
import json
import random
import threading
import time
from utils import current_datetime, gen_task_ID, getFiles
from queue import Queue
import requests
import json

MQ_USER_NAME = 'guest' #MQ的用户名
MQ_USER_PASSWORD = 'guest' #MQ的密码
HOST_NAME = 'localhost' #MQ的网络地址
HOST_PORT = 5672 # MQ的端口
CACHE_PORT = 1234 # 持久化缓存的端口 

Threads_limit = 4 # 该学生的机器单一进程能一次性最多提交4份代码
credentials = PlainCredentials(MQ_USER_NAME, MQ_USER_PASSWORD)  # MQ的用户名和密码,创建凭证

def send_msg_to_MQ(msg_data): # Build connection -> build channel -> send message
    #建立连接，然后发起通道，然后再发送信息
    connection = BlockingConnection(ConnectionParameters(host = HOST_NAME, port = HOST_PORT, virtual_host = '/',credentials = credentials))
    channel = connection.channel()
    result = channel.queue_declare(queue = 'un_judged') # 声明消息队列，消息将在这个队列传递，如不存在，则创建
    """
    data:
    msg_data;
    @key='TaskID' value->str # 自动生成唯一的任务ID (自动生成)
    @key='studentNumber' value->str # 学号
    @key='code' value->str # 需要评判的代码
    @key='time' value->str # 当前的时间 (自动生成)
    """
    TID = gen_task_ID(msg_data['studentNumber'])
    message = json.dumps({'TaskID':TID,'code':msg_data['code'],'time':current_datetime(),'studentNumber':msg_data['studentNumber']}) # build msg
    channel.basic_publish(exchange = '',routing_key = 'un_judged',body = message)        # 向队列插入数值 routing_key是队列名
    connection.close()
    return TID


def get_student_code()->str:
    # 发生IO过程
    fl = getFiles('student_codes')
    random_ID = random.randint(0,(len(fl)-1)) #随机选取一个代码文件进行读取
    with open(fl[random_ID], 'r', encoding='utf-8') as f:
        code_content = f.read() # 读取该代码文件
    return code_content


#用request post访问持久化缓存服务器
def call_check_from_cache(TID):
    try:
        request_url = "http://"+HOST_NAME+":"+str(CACHE_PORT)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data={'tid':TID}, headers=headers)
        if response:
            pack = response.content
            result = json.loads(pack)
            return result # 从缓存服务器里面找到的评判结果
    except Exception as e:
        print(e) #意外打印
        return None
    return None


# 提交代码的线程和接收评判结果的线程是配套的
# 用来提交代码的线程
class Summit(threading.Thread):
    def __init__(self):
        super(Summit, self).__init__()
    
    def run(self):
        studentNUmber = str(random.uniform(000000,999999)) #产生随机的学号
        code = get_student_code()
        msg = {}
        msg['studentNumber'] = studentNUmber
        msg['code'] = code
        print(msg)
        TID = send_msg_to_MQ(msg)
        # Student refresh 这里相当于学生在客户端刷新自己的评判结果
        # 这里从缓存服务器轮询直到收到结果（这里每一次轮询之前就手动线程暂停一段时间）
        while(True):
            result = call_check_from_cache(TID) # 从持久层缓存服务器里面查询结果，没有则进入线程等待
            print('学生线程任务：{}正在轮询缓存服务器并等待回应评判结果'.format(TID))
            if result!=None: # 假如我们得到结果了
                print(result)
                break
        

if __name__ == "__main__":
    #该学生机子产生代码并提交并异步查询代码的评判结果
    codes_summit_threads = []
    for i in range(Threads_limit):
        summit = Summit()
        summit.start()
        codes_summit_threads.append(summit)
    
    for t in codes_summit_threads:
        t.join()
        