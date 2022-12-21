FROM python:3.8
WORKDIR /home/lizhenghao/PycharmProjects/flask-01
COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y libgl1-mesa-dev \
    && pip install virtualenv -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && virtualenv ./venv \
    && ./venv/bin/pip install --no-cache-dir -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD ["./venv/bin/gunicorn", "app:app", "-c", "./gunicorn.conf.py"]
