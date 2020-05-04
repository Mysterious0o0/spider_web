# Linux安装Anaconda
## 安装
```
bash Anaconda3-2019.03-Linux-x86_64.sh
```
## 添加环境变量
```
vi ~/.bashrc
export PATH=$PATH:/home/maxwell/anaconda3/bin
```
## 环境变量生效
```
source ~/.bashrc
```

# 替换Anaconda国内镜像
## 在用户家目录下创建.condarc文件
```
touch ~/.condarc
```
## 添加如下内容到.condarc
```
channels:
  - defaults
show_channel_urls: true
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/pro
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```
## 清除索引缓存，保证用的是镜像站提供的索引
```
conda clean -i
```

# 安装python3.6
```
conda create --name python36 python=3.6.8
```

# gunicorn配置
## 在项目根目录创建gc.py
```
import gevent.monkey
gevent.monkey.patch_all()

debug = False  # 调试用，生产环境设为False

bind = "0.0.0.0:8888"  # 绑定地址:端口

pidfile = "log/gunicorn.pid"  # gunicorn进程ID日志

accesslog = "log/access.log"  # accesslog是访问日志，可以通过access_log_format设置访问日志格式

errorlog = "log/debug.log"

loglevel = "debug"  # loglevel用于控制errorlog的信息级别，可以设置为debug、info、warning、error、critical

daemon = False  # True意味着开启后台运行，默认为False

timeout = 100  # 请求超时时间

workers = 4  # 启动的进程数

worker_class = "gevent"  # 进程的模式类型，默认为sync模式

x_forwarded_for_header = 'X-FORWARDED-FOR'
```

# supervisor配置
## 1、导出配置模板到项目根目录
```
echo_supervisord_conf > supervisor.conf
```
## 2、编辑supervisor.conf
```
• 添加的部分
[program:programName]  ; programName是用户自定义的项目名称，任意
command=gunicorn -c gc.py manager:flask_app
startsecs=0
stopwaitsecs=0
autostart=true  ; start at supervisord start
autorestart=true  ; 程序崩溃时自动重启，重启次数是有限制的，默认为3次
stdout_logfile=/home/maxwell/Documents/Tools/log/stdout.log
stderr_logfile=/home/maxwell/Documents/Tools/log/stderr.log

• 修改的部分
[unix_http_server]
;file=/tmp/supervisor.sock   
file=/home/maxwell/Documents/Tools/supervisorConf/supervisor.sock ; 修改为项目下的子目录supervisorConf，避免被系统删除

[supervisord]
;logfile=/tmp/supervisord.log 
logfile=/home/maxwell/Documents/Tools/supervisorConf/supervisord.log ; 修改为项目下的子目录supervisorConf
;pidfile=/tmp/supervisord.pid 
pidfile=/home/maxwell/Documents/Tools/supervisorConf/supervisord.pid ; 修改为项目下的子目录supervisorConf

[supervisorctl]
;serverurl=unix:///tmp/supervisor.sock ; 必须和'unix_http_server'里面的设定匹配
serverurl=unix:///home/maxwell/Documents/Tools/supervisorConf/supervisor.sock ; 修改为项目下的子目录supervisorConf
```
## 3、启动服务
```
• 方式一(不推荐)：通过gunicorn运行服务(缺点是需要通过查找pid杀掉进程)
gunicorn -c gc.py main:flask_app

• 方式二(推荐)：通过supervisor运行服务
在项目根目录下运行：supervisord -c supervisorConf/supervisor.conf
```
## 4、[附录]supervisor相关命令
```
supervisorctl -c supervisor.conf stop 进程名：停止XXX进程
supervisorctl -c supervisor.conf stop all：停止所有进程
supervisorctl -c supervisor.conf start 进程名：启动XXX进程
supervisorctl -c supervisor.conf status：查看supervisor监管的进程状态
supervisorctl -c supervisor.conf reload：修改完配置文件后重新启动supervisor
supervisorctl -c supervisor.conf update：根据最新的配置文件，启动新配置
supervisorctl -u user -p 123 shutdown：关闭supervisord服务端
```
## 5、[附录]Centos7开放及查看端口
```
• 开放端口、关闭端口
firewall-cmd --zone=public --add-port=8888/tcp --permanent   # 开放8888端口
firewall-cmd --zone=public --remove-port=8888/tcp --permanent  #关闭8888端口
firewall-cmd --reload   # 配置立即生效

• 查看防火墙所有开放的端口
firewall-cmd --zone=public --list-ports

• 关闭防火墙(危险操作)
systemctl stop firewalld.service

• 查看防火墙状态
firewall-cmd --state

• 查看监听的端口
netstat -lnpt

• 检查端口被哪个进程占用
netstat -lnpt |grep 8888

• 查看进程的详细信息
ps 8888

• 杀死进程
kill -9 8888
```

# 参考资料
[Supervisor命令详解](https://www.cnblogs.com/kevingrace/p/7525200.html)
[gunicorn、nginx部署flask项目，并用supervisor来管理进程](https://www.cnblogs.com/xmxj0707/p/8452881.html)
