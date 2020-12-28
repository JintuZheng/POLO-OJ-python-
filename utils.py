""" 工具箱

@Author: Jintu Zheng
@Date: 2020-12-28

"""

import time
import hashlib
import random
import os

def current_datetime()->str:
    """Generate datetime
    """
    return time.strftime("%d_%m_%Y_%H_%M_%S")
#print(current_datetime())

def gen_task_ID(studentNumber)->str:
    """Generate unique task ID
    """
    return hashlib.md5((current_datetime()+studentNumber+str(random.uniform(0,99999))).encode(encoding='UTF-8')).hexdigest()
#print(gen_task_ID('ss'))

def getFiles(dir)->list:
    flist=[]
    for root,dirs,files in os.walk(dir+'/'):
            for file in files:
                flist.append(os.path.join(root,file))
    return flist