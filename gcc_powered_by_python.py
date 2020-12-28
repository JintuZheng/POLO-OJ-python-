import os
import subprocess
import random


def runCmd(cmd) :
    res = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    sout ,serr = res.communicate() #该方法和子进程交互，返回一个包含 输出和错误的元组，如果对应参数没有设置的，则无法返回
    return res.returncode, sout, serr, res.pid #可获得返回码、输出、错误、进程号

def compiler_from_file(code_file:str, out_file:str):
    returnCode,out,_,_ = runCmd('g++ '+code_file+' -o '+out_file)
    out = str(out,encoding = "utf-8")
    return returnCode, out


def compiler(code_content:str, tag:str):
    code_name = 'tmps/'+str(tag)+'.cpp'
    exe_name = 'tmps/'+str(tag)+'.exe'
    with open(code_name, 'w', encoding='utf8') as f:
        f.write(code_content)
    returnCode, out = compiler_from_file(code_name, exe_name)
    return returnCode, out
