import os
import subprocess

def runCmd(cmd) :
    res = subprocess.Popen(cmd, shell=True,  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    sout ,serr = res.communicate() #该方法和子进程交互，返回一个包含 输出和错误的元组，如果对应参数没有设置的，则无法返回
    return res.returncode, sout, serr, res.pid #可获得返回码、输出、错误、进程号


returnCode,out,_,_ = runCmd('g++ main.cpp -o out.exe')
print(returnCode) # 0 is right, 1 is error
out = str(out,encoding = "utf-8")
print(out)
