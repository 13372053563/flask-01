## 本地部署：
先创建虚拟环境，Python版本为3.8

然后下载requirements.txt
pip install -r requirement.txt

结晶检测的路径为：http://127.0.0.1:5000/detect_api/start_detect/http://inetujs.oss-cn-hangzhou.aliyuncs.com/11.21/1121_200422.png

## 服务器部署：
安装docker，建议镜像采用ubuntu22.04，然后使用命令一键安装docker

    sudo docker pull 1980794141/flask-crystal-detect
    sudo docker run -it -p 5000:5000 --name=detect 1980794141/flask-crystal-detect
http://139.159.253.152:8082/detect_api/start_detect/http://inetujs.oss-cn-hangzhou.aliyuncs.com/11.21/1121_200422.png

detect_api.py中的 # view_image(image_path=source, result=result) 可以将预测的结果展示在图片中

## 总结：
在完成过程中遇到了很多的问题：

①检测路径：起初并不是restful风格，原因是 detect_api中的get(self, img_path='not specified')方法必须要加上self，否则不能获取@ns.route('/start_detect/<path:img_path>')中的path

②检测时需要提供图片的本地路径，已开启采用先将图片下载的方式，这样可能会存在一些问题。现在改为提供网络地址，

        response = requests.get(img_path)
        image = Image.open(BytesIO(response.content))
        source = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
        source_shape = source.shape
这样直接将图片的cv2数据传给检测方法，也需要传输图片的shape。

③部署后存在内存泄露的问题：刚运行图片速度还可以，到大概第5张图片左右时，就会把服务器卡死，主要是内存在持续上升的原因。
对于这个问题，先把模型的加载提到了系统启动时，这样就不需要来一张图片就加载一次模型了。需要加入代码：

    sys.path.append(os.path.split(os.path.realpath(__file__))[0])
这个主要是为了解决pytorch加载模型的问题，因为在保存模型时，也会保存路径。

这样也没有解决泄露问题，只是将泄露的内存减少了。
最后，在部署部分，加入如下代码：

    workers = 1  # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
    max_requests = 5  # 每5次会重启一下服务
由于没有采用异步，所有worker只需要设置为1即可，如果太多了，也会导致模型被加载多次，会加重服务器的内存压力
max_requests主要用来解决内存泄露问题，每访问5次系统就会重启服务，这样就可以避免内存占用过多，服务器崩溃的情况了。

④dockerfile仍然存在些许问题，主要是需要的requirements.txt太多了，其中应该有一些包没有用到，但是不敢删除，怕报错。这也就导致最后生成的images大概有5G左右。
