from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from paramiko_client import ParamikoClient
import gevent
import time
from multiprocessing import Pool

app = Flask(__name__)
bootstrap = Bootstrap(app)

task_num = 3

def process(section):
    client = ParamikoClient('config.ini', section)
    client.connect()
    client.run_cmd('echo $PATH')
    client.run_cmd('cat /proc/meminfo')


def gevent_func(section):
    client = ParamikoClient('config.ini', section)
    #读取文件阻塞　切换
    gevent.sleep(0)
    client.connect()
    #连接阻塞　切换
    gevent.sleep(0)
    #执行命令　阻塞　切换
    client.run_cmd('echo $PATH')
    gevent.sleep(0)
    #执行命令　阻塞　结束
    client.run_cmd('cat /proc/meminfo')



@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/test')
def test():
    begin = time.time()
    for i in range(task_num):
        section = 'ssh' + str(i)
        # process(section)
        process(section)
    time_lost = time.time() - begin
    print("程序顺序执行消耗时间 ", time_lost)
    return render_template("gevent.html", time_lost=time_lost)


@app.route('/gevent')
def gevent_test():
    begin = time.time()
    events = []
    for i in range(task_num):
        section = 'ssh' + str(i)
        event = gevent.spawn(gevent_func, section)
        events.append(event)
    gevent.joinall(events)
    time_lost = time.time() - begin
    print('协程并发执行消耗时间', time.time() - begin)
    return render_template("gevent.html", time_lost=time_lost)


@app.route('/mul')
def mul_proc():
    begin = time.time()
    pool = Pool(4)
    for i in range(task_num):
        section = 'ssh' + str(i)
        # process(section)
        pool.apply_async(process, args=(section,))
    pool.close()
    pool.join()
    time_lost = time.time() - begin
    print("多进程并发消耗时间 ", time_lost)
    return render_template("gevent.html", time_lost=time_lost)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
