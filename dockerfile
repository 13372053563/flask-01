# docker build -t testdetect .
# docker run -it -p 5000:5000 --name=detect testdetect
# docker tag testdetect 1980794141/flask-crystal-detect
# docker push 1980794141/flask-crystal-detect
# 设置python环境镜像
FROM python:3.8

# 代码添加到Chenge文件夹，code不需要新建（docker执行时自建）
ADD .  /code
# 通过WORKDIR设置工作目录后，Dockerfile中其后的命令RUN、CMD、ENTRYPOINT、ADD、COPY等命令都会在该目录下执行
WORKDIR /code

# 安装相应的python库
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


RUN /usr/local/bin/python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]

# ImportError: libGL.so.1: cannot open shared object file: No such file or directory