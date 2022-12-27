workers = 1  # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent"  # 采用gevent库，支持异步处理请求，提高吞吐量
max_requests = 5  # 每20次会重启一下服务
bind = "0.0.0.0:5000"  # 端口随便写，但是注意是否已经被占用。netstap -lntp
